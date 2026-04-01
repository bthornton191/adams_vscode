"""Adams CMD Lint MCP Server.

Exposes Adams CMD linting and schema lookup as MCP tools consumable by any
MCP-compatible agent harness (e.g. GitHub Copilot in agent mode).

Pure stdlib implementation — no external MCP/pydantic dependencies required.

Transport: stdio (JSON-RPC 2.0 over newline-delimited JSON).
Protocol: MCP 2024-11-05

Tools provided:
  adams_lint_cmd_text  — Lint raw CMD text, return JSON diagnostics.
  adams_lint_cmd_file  — Lint a CMD file by path, return JSON diagnostics.
  adams_lookup_command — Look up a command's arguments and schema.

The Schema and MacroRegistry are loaded once at startup in main() and stored
as module-level globals shared across all tool calls.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

from .diagnostics import Severity
from .linter import lint_text
from .macros import MacroRegistry, scan_macro_files, DEFAULT_MACRO_PATTERNS
from .schema import Schema

# Module-level singletons initialised by main() before the server loop starts.
_schema: Schema | None = None
_macro_registry: MacroRegistry | None = None
_show_macro_hint: bool = True


# ---------------------------------------------------------------------------
# Shared serialisation helpers
# ---------------------------------------------------------------------------

def _serialise_diagnostics(diagnostics, file_path=None):
    """Convert a list of Diagnostic objects to a JSON-serialisable dict."""
    errors = sum(1 for d in diagnostics if d.severity == Severity.ERROR)
    warnings = sum(1 for d in diagnostics if d.severity == Severity.WARNING)
    info = sum(1 for d in diagnostics if d.severity == Severity.INFO)
    result = {
        "diagnostics": [
            {
                "line": d.line + 1,
                "column": d.column + 1,
                "end_line": d.end_line + 1,
                "end_column": d.end_column + 1,
                "code": d.code,
                "message": d.message,
                "severity": d.severity.value,
            }
            for d in diagnostics
        ],
        "summary": {"errors": errors, "warnings": warnings, "info": info},
    }
    if file_path is not None:
        result["file"] = file_path
    return result


# ---------------------------------------------------------------------------
# Tool handlers  (async so callers can `await` them)
# ---------------------------------------------------------------------------

async def adams_lint_cmd_text(text: str, min_severity: str = "info") -> str:
    """Lint a string of Adams CMD source text and return diagnostics as JSON.

    Use this to validate CMD content before writing it to a file, or to
    check a snippet the agent has just produced.

    Args:
        text (str): Raw Adams CMD content to lint. May be a single command
            or multi-line script. Continuation lines (trailing '&') are
            handled automatically.
        min_severity (str): Minimum severity level to include in results.
            One of "error", "warning", "info" (default: "info").
            Use "error" to suppress warnings and info diagnostics.

    Returns:
        str: JSON object with the following schema:
            {
                "diagnostics": [
                    {
                        "line": int,        // 1-based line number
                        "column": int,      // 1-based column number
                        "end_line": int,
                        "end_column": int,
                        "code": str,        // e.g. "E001", "W005", "I202"
                        "message": str,
                        "severity": str     // "error", "warning", or "info"
                    }
                ],
                "summary": {
                    "errors": int,
                    "warnings": int,
                    "info": int
                }
            }
            An empty "diagnostics" list means the input is clean.

    Examples:
        - Use when: validating CMD text you just wrote before sending to Adams
        - Use when: checking a multi-command script for errors
        - Don't use when: you have a file path (use adams_lint_cmd_file instead)
    """
    if _schema is None:
        return json.dumps({"error": "MCP server not fully initialised — schema missing"})

    valid_severities = {"error", "warning", "info"}
    if min_severity not in valid_severities:
        return json.dumps({"error": f"Invalid min_severity '{min_severity}'. Must be one of: {sorted(valid_severities)}"})

    diagnostics = lint_text(
        text,
        schema=_schema,
        min_severity=min_severity,
        macro_registry=_macro_registry,
        show_macro_hint=_show_macro_hint,
    )
    return json.dumps(_serialise_diagnostics(diagnostics), indent=2)


async def adams_lint_cmd_file(file_path: str, min_severity: str = "info") -> str:
    """Lint an Adams CMD file by path and return diagnostics as JSON.

    Reads the file from disk and runs the Adams CMD linter on its contents.
    Results include the resolved file path for traceability.

    Args:
        file_path (str): Absolute path to a .cmd file to lint.
            Example: "/home/user/project/model.cmd" or
            "C:\\\\Adams\\\\project\\\\model.cmd"
        min_severity (str): Minimum severity level to include in results.
            One of "error", "warning", "info" (default: "info").

    Returns:
        str: JSON object with the following schema:
            {
                "file": str,            // Resolved absolute path
                "diagnostics": [...],   // Same structure as adams_lint_cmd_text
                "summary": {"errors": int, "warnings": int, "info": int}
            }

    Examples:
        - Use when: you have a .cmd file on disk you want to validate
        - Use when: checking a file the user just saved
        - Don't use when: content is in memory (use adams_lint_cmd_text instead)

    Error Handling:
        Returns JSON with an "error" key if the file cannot be read.
    """
    if _schema is None:
        return json.dumps({"error": "MCP server not fully initialised — schema missing"})

    valid_severities = {"error", "warning", "info"}
    if min_severity not in valid_severities:
        return json.dumps({"error": f"Invalid min_severity '{min_severity}'. Must be one of: {sorted(valid_severities)}"})

    resolved = os.path.realpath(file_path)
    if not os.path.isfile(resolved):
        return json.dumps({"error": f"File not found: {file_path}"})

    try:
        text = Path(resolved).read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return json.dumps({"error": f"Could not read file: {exc}"})

    diagnostics = lint_text(
        text,
        schema=_schema,
        min_severity=min_severity,
        macro_registry=_macro_registry,
        show_macro_hint=_show_macro_hint,
    )
    return json.dumps(_serialise_diagnostics(diagnostics, file_path=resolved), indent=2)


async def adams_lookup_command(command: str) -> str:
    """Look up the schema definition of an Adams CMD command.

    Resolves abbreviated command names (Adams shortest-unique-prefix rules)
    and returns the full argument list, required flags, types, and mutual
    exclusion groups.

    Args:
        command (str): Command name to look up. May be abbreviated per Adams
            prefix rules. Examples: "marker create", "mar cre", "model mod".

    Returns:
        str: JSON object with the following schema on success:
            {
                "command": str,             // Canonical command key
                "arguments": {
                    "<arg_name>": {
                        "required": bool,
                        "type": str,        // e.g. "new_object", "real", "boolean"
                        "min_prefix": int,  // Minimum abbreviation length
                        "default": str | null,
                        "object_type": str | null
                    }
                },
                "exclusive_groups": [
                    {"group": int, "members": [str, ...]}
                ]
            }
            On failure:
            {
                "error": str,
                "suggestion": str | null    // Closest prefix match if available
            }

    Examples:
        - Use when: you need to know the required arguments for a command
        - Use when: writing CMD code and need to check argument names/types
        - Use when: debugging an E002 (invalid argument) or E005 (missing required arg)
    """
    if _schema is None:
        return json.dumps({"error": "MCP server not fully initialised — schema missing"})

    tokens = command.strip().lower().split()
    if not tokens:
        return json.dumps({"error": "Empty command string"})

    canonical_key, error_idx = _schema.resolve_command_key(tokens)

    if canonical_key is None:
        # Provide a hint by trying progressively shorter token lists
        suggestion = None
        for length in range(len(tokens) - 1, 0, -1):
            partial_key, partial_err = _schema.resolve_command_key(tokens[:length])
            if partial_key is not None:
                suggestion = f"Did you mean a command starting with '{partial_key}'?"
                break
        return json.dumps({
            "error": f"Unknown command: '{command}'. Token at position {error_idx} could not be resolved.",
            "suggestion": suggestion,
        })

    cmd_def = _schema.get_command(canonical_key)
    args = cmd_def.get("args", {}) if cmd_def else {}
    exclusive_groups = _schema.get_exclusive_groups(canonical_key)

    return json.dumps({
        "command": canonical_key,
        "arguments": {
            name: {
                "required": arg_def.get("required", False),
                "type": arg_def.get("type"),
                "min_prefix": arg_def.get("min_prefix", 1),
                "default": arg_def.get("default"),
                "object_type": arg_def.get("object_type"),
            }
            for name, arg_def in args.items()
        },
        "exclusive_groups": exclusive_groups,
    }, indent=2)


# ---------------------------------------------------------------------------
# Tool registry
# ---------------------------------------------------------------------------

_TOOL_HANDLERS = {
    "adams_lint_cmd_text": adams_lint_cmd_text,
    "adams_lint_cmd_file": adams_lint_cmd_file,
    "adams_lookup_command": adams_lookup_command,
}

_TOOLS_LIST = [
    {
        "name": "adams_lint_cmd_text",
        "description": (
            "Lint a string of Adams CMD source text and return diagnostics as JSON. "
            "Use to validate CMD content before writing it to a file, or to check "
            "a snippet the agent has just produced."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Raw Adams CMD content to lint.",
                },
                "min_severity": {
                    "type": "string",
                    "description": (
                        'Minimum severity level to include: "error", "warning", '
                        'or "info" (default).'
                    ),
                },
            },
            "required": ["text"],
        },
        "annotations": {
            "title": "Lint Adams CMD text",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    },
    {
        "name": "adams_lint_cmd_file",
        "description": (
            "Lint an Adams CMD file by absolute path and return diagnostics as JSON. "
            "Reads the file from disk. Results include the resolved file path."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Absolute path to a .cmd file to lint.",
                },
                "min_severity": {
                    "type": "string",
                    "description": (
                        'Minimum severity level to include: "error", "warning", '
                        'or "info" (default).'
                    ),
                },
            },
            "required": ["file_path"],
        },
        "annotations": {
            "title": "Lint an Adams CMD file",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    },
    {
        "name": "adams_lookup_command",
        "description": (
            "Look up the schema definition of an Adams CMD command. Resolves "
            "abbreviated command names and returns arguments, required flags, "
            "types, and mutual exclusion groups."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": (
                        "Command name to look up. May be abbreviated per Adams "
                        "prefix rules. Example: \"marker create\" or \"mar cre\"."
                    ),
                },
            },
            "required": ["command"],
        },
        "annotations": {
            "title": "Look up an Adams CMD command",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    },
]


# ---------------------------------------------------------------------------
# JSON-RPC 2.0 / MCP protocol helpers
# ---------------------------------------------------------------------------

_PROTOCOL_VERSION = "2024-11-05"
_SERVER_INFO = {"name": "adams_cmd_lint_mcp", "version": "0.1.0"}


def _write_message(obj: dict) -> None:
    """Serialise and write one JSON-RPC message to stdout."""
    try:
        sys.stdout.write(json.dumps(obj) + "\n")
        sys.stdout.flush()
    except (BrokenPipeError, OSError):
        sys.exit(0)


def _ok(req_id, result: dict) -> dict:
    return {"jsonrpc": "2.0", "id": req_id, "result": result}


def _err(req_id, code: int, message: str) -> dict:
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}


async def _handle_message(msg: dict) -> None:
    """Dispatch a single JSON-RPC message and send a response when required."""
    method = msg.get("method", "")
    req_id = msg.get("id")  # None for notifications
    params = msg.get("params") or {}

    if method == "initialize":
        _write_message(_ok(req_id, {
            "protocolVersion": _PROTOCOL_VERSION,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": _SERVER_INFO,
        }))

    elif method == "ping":
        _write_message(_ok(req_id, {}))

    elif method in ("notifications/initialized", "notifications/cancelled"):
        pass  # notifications — no response required

    elif method == "tools/list":
        _write_message(_ok(req_id, {"tools": _TOOLS_LIST}))

    elif method == "tools/call":
        name = params.get("name", "")
        arguments = params.get("arguments") or {}
        handler = _TOOL_HANDLERS.get(name)
        if handler is None:
            _write_message(_err(req_id, -32601, f"Unknown tool: {name!r}"))
            return
        try:
            text = await handler(**arguments)
        except TypeError as exc:
            _write_message(_err(req_id, -32602, f"Invalid params: {exc}"))
            return
        except Exception as exc:  # noqa: BLE001
            _write_message(_err(req_id, -32603, f"Internal error: {exc}"))
            return
        _write_message(_ok(req_id, {"content": [{"type": "text", "text": text}]}))

    elif req_id is not None:
        # Unknown method with an id — respond with Method Not Found
        _write_message(_err(req_id, -32601, f"Method not found: {method!r}"))

    # Unknown notifications (no id) are silently ignored per JSON-RPC 2.0


async def _stdio_loop_async() -> None:
    """Async stdin loop that processes each message within a single event loop."""
    for raw_line in sys.stdin:
        line = raw_line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            print(f"[adams-cmd-mcp] ignoring malformed JSON: {line!r}", file=sys.stderr)
            continue
        await _handle_message(msg)


def _run_stdio_loop() -> None:
    """Start the single-event-loop stdio server."""
    asyncio.run(_stdio_loop_async())


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    """Start the Adams CMD Lint MCP server via stdio."""
    global _schema, _macro_registry, _show_macro_hint  # noqa: PLW0603

    parser = argparse.ArgumentParser(
        prog="adams-cmd-mcp",
        description="Adams CMD Lint MCP Server",
    )
    parser.add_argument(
        "--schema",
        metavar="PATH",
        help="Path to command_schema.json (default: bundled)",
    )
    parser.add_argument(
        "--macro-paths",
        nargs="+",
        metavar="GLOB",
        default=[],
        help=(
            "Glob patterns for macro file discovery, resolved relative to "
            "--macro-base-dir. Example: '**/*.mac'"
        ),
    )
    parser.add_argument(
        "--macro-base-dir",
        metavar="DIR",
        default=None,
        help="Base directory for resolving --macro-paths globs (default: cwd).",
    )
    parser.add_argument(
        "--macro-ignore-paths",
        nargs="+",
        metavar="GLOB",
        default=[],
        help="Glob patterns to exclude from macro scanning.",
    )
    parser.add_argument(
        "--scan-workspace-macros",
        action="store_true",
        default=False,
        help="Scan --macro-base-dir for macro files at startup.",
    )
    parser.add_argument(
        "--no-show-macro-hint",
        action="store_true",
        default=False,
        help="Suppress the E001 hint about scanWorkspaceMacros.",
    )
    args = parser.parse_args()

    # Reconfigure stdin/stdout to UTF-8 so that multi-byte characters in CMD
    # text are handled correctly on all platforms (especially Windows).
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    # Load schema (once, shared for all tool calls)
    _schema = Schema.load(args.schema) if args.schema else Schema.load()
    _show_macro_hint = not args.no_show_macro_hint

    # Build macro registry at startup so the first lint call has no cold-start
    # latency and config errors surface immediately rather than mid-session.
    _macro_registry = MacroRegistry()

    if args.scan_workspace_macros:
        base_dir = args.macro_base_dir or os.getcwd()
        patterns = args.macro_paths if args.macro_paths else DEFAULT_MACRO_PATTERNS
        ignore_patterns = args.macro_ignore_paths or None
        scan_macro_files(
            roots=[base_dir],
            patterns=patterns,
            ignore_patterns=ignore_patterns,
            registry=_macro_registry,
        )

    _run_stdio_loop()

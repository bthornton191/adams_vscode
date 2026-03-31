"""Adams CMD Lint MCP Server.

Exposes Adams CMD linting and schema lookup as MCP tools consumable by any
MCP-compatible agent harness (e.g. GitHub Copilot in agent mode).

Transport: stdio (default).

Tools provided:
  adams_lint_cmd_text  — Lint raw CMD text, return JSON diagnostics.
  adams_lint_cmd_file  — Lint a CMD file by path, return JSON diagnostics.
  adams_lookup_command — Look up a command's arguments and schema.

The Schema and MacroRegistry are loaded once at startup in main() and stored
as module-level globals shared across all tool calls.
"""

import argparse
import json
import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .diagnostics import Severity
from .linter import lint_text
from .macros import MacroRegistry, scan_macro_files, DEFAULT_MACRO_PATTERNS
from .schema import Schema

mcp = FastMCP("adams_cmd_lint_mcp")

# Module-level singletons initialised by main() before mcp.run().
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
# Tools
# ---------------------------------------------------------------------------

@mcp.tool(
    name="adams_lint_cmd_text",
    annotations={
        "title": "Lint Adams CMD text",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
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


@mcp.tool(
    name="adams_lint_cmd_file",
    annotations={
        "title": "Lint an Adams CMD file",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
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


@mcp.tool(
    name="adams_lookup_command",
    annotations={
        "title": "Look up an Adams CMD command",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
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

    mcp.run(transport="stdio")

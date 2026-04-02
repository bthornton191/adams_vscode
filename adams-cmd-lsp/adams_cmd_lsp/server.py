"""LSP server for Adams CMD language.

Uses pygls 2.x (from pygls.lsp.server import LanguageServer).
Start via:
    python -m adams_cmd_lsp          # stdio (default, for editors)
    adams-cmd-lsp                    # same, via entry point
    adams-cmd-lsp --tcp --port 2087  # TCP, for debugging
"""

import argparse
import fnmatch
import os
from pathlib import Path
from urllib.parse import urlparse, unquote, quote

from pygls.lsp.server import LanguageServer
from lsprotocol import types

from .linter import lint_text
from .parser import parse as _parse_cmd
from .schema import Schema
from .diagnostics import Severity
from .macros import (
    scan_macro_files, parse_macro_file, MacroRegistry, DEFAULT_MACRO_PATTERNS,
    DEFAULT_IGNORE_DIRS, extract_macros_from_statements,
    _USER_ENTERED_COMMAND_RE,
)
from .references import MacroIndex, index_file_text


server = LanguageServer("adams-cmd-lsp", "v0.1.0")

# Semantic token legend — used for macro command/argument highlighting
_SEMANTIC_TOKEN_TYPES = ["keyword", "parameter"]
_SEMANTIC_TOKEN_MODIFIERS: list = []
_SEMANTIC_LEGEND = types.SemanticTokensLegend(
    token_types=_SEMANTIC_TOKEN_TYPES,
    token_modifiers=_SEMANTIC_TOKEN_MODIFIERS,
)
_TOKEN_TYPE_KEYWORD = _SEMANTIC_TOKEN_TYPES.index("keyword")
_TOKEN_TYPE_PARAMETER = _SEMANTIC_TOKEN_TYPES.index("parameter")

# Schema and macro registry are loaded once in main() and stored here
_schema = None
_macro_registry = None
_macro_index = MacroIndex()          # persistent cross-file invocation index
_macro_patterns = DEFAULT_MACRO_PATTERNS
_macro_ignore_patterns: list = []
_scan_workspace_macros = False
_macro_show_hint: bool = True
_workspace_roots: list = []
_index_cmd_extensions = {".cmd", ".mac"}

_SEVERITY_MAP = {
    Severity.ERROR: types.DiagnosticSeverity.Error,
    Severity.WARNING: types.DiagnosticSeverity.Warning,
    Severity.INFO: types.DiagnosticSeverity.Information,
}


def _to_lsp_diagnostic(d):
    """Convert a Diagnostic dataclass to an LSP Diagnostic protocol object."""
    return types.Diagnostic(
        range=types.Range(
            start=types.Position(line=d.line, character=d.column),
            end=types.Position(line=d.end_line, character=d.end_column),
        ),
        message=d.message,
        source="adams-cmd-lint",
        code=d.code,
        severity=_SEVERITY_MAP.get(d.severity, types.DiagnosticSeverity.Information),
    )


def _validate_document(uri, text):
    """Lint the document text and publish diagnostics to the client."""
    try:
        diagnostics = lint_text(
            text,
            schema=_schema,
            macro_registry=_macro_registry if _scan_workspace_macros else None,
            show_macro_hint=_macro_show_hint,
        )
    except Exception as exc:  # noqa: BLE001
        # Never let a lint crash kill the server
        server.window_log_message(
            types.LogMessageParams(
                type=types.MessageType.Error,
                message=f"adams-cmd-lint error: {exc}",
            )
        )
        diagnostics = []
    lsp_diags = [_to_lsp_diagnostic(d) for d in diagnostics]
    server.text_document_publish_diagnostics(
        types.PublishDiagnosticsParams(uri=uri, diagnostics=lsp_diags)
    )


@server.feature(types.TEXT_DOCUMENT_DID_OPEN)
def did_open(params: types.DidOpenTextDocumentParams):
    doc = params.text_document
    _validate_document(doc.uri, doc.text)
    _index_document(doc.uri, doc.text)


@server.feature(types.TEXT_DOCUMENT_DID_CHANGE)
def did_change(params: types.DidChangeTextDocumentParams):
    doc = server.workspace.get_text_document(params.text_document.uri)
    _validate_document(params.text_document.uri, doc.source)
    _index_document(params.text_document.uri, doc.source)


@server.feature(types.TEXT_DOCUMENT_DID_CLOSE)
def did_close(params: types.DidCloseTextDocumentParams):
    server.text_document_publish_diagnostics(
        types.PublishDiagnosticsParams(uri=params.text_document.uri, diagnostics=[])
    )


@server.feature(types.TEXT_DOCUMENT_DID_SAVE)
def did_save(params: types.DidSaveTextDocumentParams):
    doc = server.workspace.get_text_document(params.text_document.uri)
    _validate_document(params.text_document.uri, doc.source)
    _index_document(params.text_document.uri, doc.source)
    # If the saved file is a macro file, refresh that entry in the registry
    _refresh_macro_file(params.text_document.uri, doc.source)


def _uri_to_path(uri: str) -> str:
    """Convert a file:// URI to a local filesystem path."""
    parsed = urlparse(uri)
    path = unquote(parsed.path)
    # On Windows the path starts with /C:/... — strip the leading slash
    if os.name == "nt" and path.startswith("/") and len(path) > 2 and path[2] == ":":
        path = path[1:]
    return path


def _path_to_uri(path: str) -> str:
    """Convert a local filesystem path to a file:// URI."""
    p = Path(path)
    # Use as_posix() so we get forward slashes then url-encode
    posix = p.as_posix()
    # Encode special chars but keep slashes and colons (drive letter) intact
    encoded = quote(posix, safe="/:")
    if os.name == "nt" and not encoded.startswith("/"):
        # Windows: "C:/path" -> "file:///C:/path"
        return "file:///" + encoded
    return "file://" + encoded


def _collect_cmd_files(roots):
    """Walk *roots* and return all .cmd / .mac file paths.

    Skips directories in DEFAULT_IGNORE_DIRS (same set used by the macro
    scanner) so version-control folders, build artefacts, etc. are excluded.
    """
    results = []
    for root in roots:
        root_path = Path(root)
        if not root_path.is_dir():
            continue
        for dirpath, dirnames, filenames in os.walk(root_path):
            # Prune ignored directories in-place so os.walk doesn't recurse
            dirnames[:] = [
                d for d in dirnames if d not in DEFAULT_IGNORE_DIRS
            ]
            for fname in filenames:
                if Path(fname).suffix.lower() in _index_cmd_extensions:
                    results.append(Path(dirpath) / fname)
    return results


def _index_document(uri: str, text: str) -> None:
    """Re-index a single document's macro invocations in _macro_index."""
    if _schema is None:
        return
    path = _uri_to_path(uri)
    if not path:
        return
    try:
        refs = index_file_text(text, _schema, source_file=path)
        _macro_index.update_file(path, refs)
        _macro_index.record_mtime(path)
    except Exception:  # noqa: BLE001
        pass


def _get_command_key_at_position(text: str, line: int, uri: str):
    """Return (origin, command_key, macro_def_or_None, origin_range) for the command at *line*.

    *origin* is one of:
    - ``"registry"``        — command matched a workspace macro in _macro_registry
    - ``"inline"``          — command matched an inline macro create/read in the file
    - ``"definition_site"`` — cursor is on a !USER_ENTERED_COMMAND line
    - ``None``              — not a macro invocation (built-in or unrecognised)

    *origin_range* is a (line, col_start, col_end) tuple marking the command key
    span in the source document.

    Returns None when no match is found.
    """
    if _schema is None:
        return None

    # Check if the cursor is on a !USER_ENTERED_COMMAND comment line in a .mac
    lines = text.splitlines()
    if 0 <= line < len(lines):
        m = _USER_ENTERED_COMMAND_RE.match(lines[line])
        if m:
            command_key = m.group(1).strip().lower()
            col_start = m.start(1)
            col_end = col_start + len(m.group(1).strip())
            macro_def = _macro_registry.lookup_command(command_key) if _macro_registry else None
            return ("definition_site", command_key, macro_def, (line, col_start, col_end))

    # Parse and find the statement at the cursor line
    try:
        statements = _parse_cmd(text)
    except Exception:  # noqa: BLE001
        return None

    stmt = None
    for s in statements:
        if s.is_comment or s.is_blank:
            continue
        if s.line_start <= line <= s.line_end:
            stmt = s
            break
    if stmt is None:
        return None

    tokens = stmt.command_key.split() if stmt.command_key else []
    if not tokens:
        return None

    # If the command resolves as a built-in, it's not a macro
    resolved_key, _ = _schema.resolve_command_key(tokens)
    if resolved_key is not None:
        return None

    command_key = stmt.command_key.lower()
    first_line = lines[stmt.line_start] if 0 <= stmt.line_start < len(lines) else ""
    leading = len(first_line) - len(first_line.lstrip())
    origin_range = (stmt.line_start, leading, leading + len(stmt.command_key))

    # Check registry (workspace .mac files)
    if _macro_registry is not None:
        macro_def = _macro_registry.lookup_command(command_key)
        if macro_def is not None:
            return ("registry", command_key, macro_def, origin_range)

    # Check inline macros defined earlier in the same file
    path = _uri_to_path(uri)
    preceding = [s for s in statements if s.line_end < stmt.line_start]
    inline_macros = extract_macros_from_statements(preceding, _schema, source_file=path)
    for idef in inline_macros:
        if idef.command == command_key:
            return ("inline", command_key, idef, origin_range)

    return None


def _refresh_macro_file(uri: str, text: str) -> None:
    """Re-parse *uri* and update _macro_registry if it matches a macro pattern."""
    global _macro_registry  # noqa: PLW0603
    if _macro_registry is None:
        return
    path = _uri_to_path(uri)
    if not path:
        return

    # Check whether this file matches any configured macro pattern.
    # Strategy: compute the path relative to each known workspace root and test
    # against the full glob pattern (e.g. "macros/*" must NOT match a file
    # outside the macros/ directory). Fall back to filename-only matching for
    # patterns whose last component is not the bare wildcard "*".
    matched = False
    for root in _workspace_roots:
        try:
            rel = Path(path).relative_to(root).as_posix()
            if any(fnmatch.fnmatch(rel, pat) for pat in _macro_patterns):
                matched = True
                break
        except (ValueError, Exception):  # noqa: BLE001
            continue
    if not matched and not _workspace_roots:
        # No workspace roots yet (e.g. first save before INITIALIZED) — fall
        # back to filename matching, but only for patterns whose last segment
        # is not the bare "*" (which would match every file).
        filename = Path(path).name
        for pat in _macro_patterns:
            last = Path(pat).name
            if last != "*" and fnmatch.fnmatch(filename, last):
                matched = True
                break
    if not matched:
        return
    try:
        _macro_registry.unregister_by_file(path)
        macro_def = parse_macro_file(text, source_file=path)
        if macro_def is not None:
            _macro_registry.register(macro_def)
    except Exception:  # noqa: BLE001
        pass


def main():
    """Entry point for the adams-cmd-lsp LSP server."""
    global _schema, _macro_registry, _macro_patterns, _macro_ignore_patterns, _scan_workspace_macros, _macro_show_hint, _workspace_roots, _macro_index  # noqa: PLW0603

    parser = argparse.ArgumentParser(
        prog="adams-cmd-lsp",
        description="Adams CMD Language Server",
    )
    parser.add_argument(
        "--tcp",
        action="store_true",
        help="Use TCP transport instead of stdio (useful for debugging)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=2087,
        help="TCP port (only with --tcp, default: 2087)",
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
        help="Glob patterns for macro file discovery (resolved relative to workspace roots)",
    )
    parser.add_argument(
        "--macro-ignore-paths",
        nargs="+",
        metavar="GLOB",
        default=[],
        help="Glob patterns to exclude from macro scanning",
    )
    parser.add_argument(
        "--scan-workspace-macros",
        action="store_true",
        default=False,
        help="Scan workspace folders for macro files on startup",
    )
    parser.add_argument(
        "--show-macro-hint",
        action=argparse.BooleanOptionalAction,
        default=True,
        help=(
            "Include a hint in E001 messages suggesting 'scanWorkspaceMacros' "
            "when no macro registry is active (default: on)"
        ),
    )
    # vscode-languageclient passes --stdio automatically; accept and ignore it.
    parser.add_argument(
        "--stdio",
        action="store_true",
        help="Use stdio transport (default, passed automatically by VS Code)",
    )
    args = parser.parse_args()

    _schema = Schema.load(args.schema) if args.schema else Schema.load()
    _macro_patterns = args.macro_paths if args.macro_paths else DEFAULT_MACRO_PATTERNS
    _macro_ignore_patterns = args.macro_ignore_paths or []
    _scan_workspace_macros = args.scan_workspace_macros
    _macro_show_hint = args.show_macro_hint

    # Build initial registry and index — always created so did_save can
    # refresh them later. Workspace folders are merged after client connects.
    _macro_registry = MacroRegistry()
    _macro_index = MacroIndex()  # reset in case main() is called more than once

    if args.tcp:
        server.start_tcp("localhost", args.port)
    else:
        server.start_io()


@server.feature(types.TEXT_DOCUMENT_DEFINITION)
def goto_definition(params: types.DefinitionParams):
    """Jump to the definition of the macro invoked at the cursor position.

    Returns a LocationLink so that VS Code underlines the full multi-word
    command key on Ctrl+hover, not just the single word under the cursor.
    """
    uri = params.text_document.uri
    line = params.position.line
    try:
        doc = server.workspace.get_text_document(uri)
        text = doc.source
    except Exception:  # noqa: BLE001
        return None

    result = _get_command_key_at_position(text, line, uri)
    if result is None:
        return None

    origin, _command_key, macro_def, origin_range = result
    src_line, src_col_start, src_col_end = origin_range
    origin_selection = types.Range(
        start=types.Position(line=src_line, character=src_col_start),
        end=types.Position(line=src_line, character=src_col_end),
    )

    if origin == "definition_site":
        # Already at the definition — link back to itself
        return [types.LocationLink(
            target_uri=uri,
            target_range=types.Range(
                start=types.Position(line=line, character=0),
                end=types.Position(line=line, character=0),
            ),
            target_selection_range=types.Range(
                start=types.Position(line=line, character=0),
                end=types.Position(line=line, character=0),
            ),
            origin_selection_range=origin_selection,
        )]

    if macro_def is None:
        return None

    def_uri = _path_to_uri(macro_def.source_file) if macro_def.source_file else uri
    target_range = types.Range(
        start=types.Position(line=macro_def.line, character=0),
        end=types.Position(line=macro_def.line, character=0),
    )
    return [types.LocationLink(
        target_uri=def_uri,
        target_range=target_range,
        target_selection_range=target_range,
        origin_selection_range=origin_selection,
    )]


@server.feature(types.TEXT_DOCUMENT_REFERENCES)
def find_references(params: types.ReferenceParams):
    """Return all workspace invocations of the macro at the cursor position."""
    uri = params.text_document.uri
    line = params.position.line
    include_declaration = (
        params.context.include_declaration
        if params.context is not None else False
    )
    try:
        doc = server.workspace.get_text_document(uri)
        text = doc.source
    except Exception:  # noqa: BLE001
        return []

    result = _get_command_key_at_position(text, line, uri)
    if result is None:
        return []

    origin, command_key, macro_def, _origin_range = result

    # Collect all locations from the persistent index
    refs = _macro_index.get_references(command_key)
    locations = []
    for file_path, ref in refs:
        locations.append(types.Location(
            uri=_path_to_uri(file_path),
            range=types.Range(
                start=types.Position(line=ref.line, character=ref.column),
                end=types.Position(line=ref.line, character=ref.end_column),
            ),
        ))

    # Include the declaration site if requested
    if include_declaration and macro_def is not None and macro_def.source_file:
        locations.append(types.Location(
            uri=_path_to_uri(macro_def.source_file),
            range=types.Range(
                start=types.Position(line=macro_def.line, character=0),
                end=types.Position(line=macro_def.line, character=0),
            ),
        ))

    return locations


@server.feature(
    types.TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL,
    _SEMANTIC_LEGEND,
)
def semantic_tokens_full(params: types.SemanticTokensParams):
    """Provide semantic tokens for macro command invocations and their arguments."""
    uri = params.text_document.uri
    try:
        doc = server.workspace.get_text_document(uri)
        text = doc.source
    except Exception:  # noqa: BLE001
        return types.SemanticTokens(data=[])

    try:
        data = _compute_semantic_tokens(text, uri)
    except Exception:  # noqa: BLE001
        data = []
    return types.SemanticTokens(data=data)


def _compute_semantic_tokens(text, uri):
    """Build the integer-encoded semantic token data for all recognised commands.

    Emits ``keyword`` tokens for command key words of built-in and macro
    commands, and ``parameter`` tokens for recognised argument names.
    Unresolved commands produce no tokens (TextMate fallback applies).

    Returns a flat list of integers in groups of 5:
        [deltaLine, deltaStart, length, tokenType, tokenModifiers]
    sorted by position.
    """
    if _schema is None:
        return []

    try:
        statements = _parse_cmd(text)
    except Exception:  # noqa: BLE001
        return []

    # Resolve built-in command abbreviations so that
    # extract_macros_from_statements can recognise "mac cre" → "macro create"
    for stmt in statements:
        if stmt.is_comment or stmt.is_blank or stmt.is_control_flow:
            continue
        if not stmt.command_key or stmt.resolved_command_key:
            continue
        toks = stmt.command_key.split()
        resolved, _ = _schema.resolve_command_key(toks)
        if resolved:
            stmt.resolved_command_key = resolved

    # Pre-compute inline macros from the whole file for same-file matching
    inline_macros = None

    # Collect raw tokens as (line, col, length, type_index)
    raw_tokens = []

    for stmt in statements:
        if stmt.is_comment or stmt.is_blank or stmt.is_control_flow:
            continue
        if not stmt.command_key:
            continue

        # Skip dot-path property assignments (same as rule_unknown_command)
        if stmt.command_key.startswith('.'):
            continue

        if stmt.resolved_command_key is not None:
            # Built-in command — emit keyword tokens for each command key word
            # and parameter tokens only for schema-resolved argument names.
            for token_text, token_line, token_col in stmt.command_key_tokens:
                raw_tokens.append((token_line, token_col, len(token_text), _TOKEN_TYPE_KEYWORD))

            for arg in stmt.arguments:
                canonical = _schema.resolve_argument_name(stmt.resolved_command_key, arg.name)
                if canonical is not None:
                    raw_tokens.append((arg.name_line, arg.name_column, len(arg.name), _TOKEN_TYPE_PARAMETER))
            continue

        # Normalise multi-space command keys (from continuation-line joining)
        # to single spaces for registry lookup.
        normalised_key = " ".join(stmt.command_key.split())

        # Check workspace macro registry.
        macro_def = None
        if _macro_registry is not None:
            macro_def = _macro_registry.lookup_command(normalised_key)

        # Check inline macros (lazily computed).
        # Unlike _get_command_key_at_position (which uses only preceding stmts
        # for accuracy), we use ALL statements so the entire file highlights
        # consistently — a macro defined on line 50 colours invocations above.
        if macro_def is None:
            if inline_macros is None:
                path = _uri_to_path(uri)
                inline_macros = extract_macros_from_statements(
                    statements, _schema, source_file=path,
                )
            for idef in inline_macros:
                if idef.command == normalised_key:
                    macro_def = idef
                    break

        if macro_def is None:
            continue

        # Macro invocation — emit keyword tokens for each command key word
        # and parameter tokens for all argument names (no schema validation).
        for token_text, token_line, token_col in stmt.command_key_tokens:
            raw_tokens.append((token_line, token_col, len(token_text), _TOKEN_TYPE_KEYWORD))

        for arg in stmt.arguments:
            raw_tokens.append((arg.name_line, arg.name_column, len(arg.name), _TOKEN_TYPE_PARAMETER))

    if not raw_tokens:
        return []

    # Sort by (line, col) and encode as delta format
    raw_tokens.sort(key=lambda t: (t[0], t[1]))
    data = []
    prev_line = 0
    prev_col = 0
    for line, col, length, token_type in raw_tokens:
        delta_line = line - prev_line
        delta_col = col - prev_col if delta_line == 0 else col
        data.extend([delta_line, delta_col, length, token_type, 0])
        prev_line = line
        prev_col = col

    return data


@server.feature(types.WORKSPACE_DID_CHANGE_CONFIGURATION)
def did_change_configuration(params: types.DidChangeConfigurationParams):
    """Update server globals when VS Code settings change.

    The vscode-languageclient library sends changes as:
        {"msc-adams": {"linter": {"scanWorkspaceMacros": true, ...}}}
    All keys are optional — guard against missing keys throughout.
    """
    global _scan_workspace_macros, _macro_patterns, _macro_ignore_patterns, _macro_show_hint  # noqa: PLW0603

    raw = params.settings or {}
    linter_cfg = {}
    if isinstance(raw, dict):
        adams_cfg = raw.get("msc-adams") or {}
        if isinstance(adams_cfg, dict):
            linter_cfg = adams_cfg.get("linter") or {}

    # Capture values before update so we can detect changes
    old_scan = _scan_workspace_macros
    old_patterns = list(_macro_patterns)
    old_ignore = list(_macro_ignore_patterns)

    if "scanWorkspaceMacros" in linter_cfg:
        _scan_workspace_macros = bool(linter_cfg["scanWorkspaceMacros"])
    if "macroPaths" in linter_cfg:
        paths = linter_cfg["macroPaths"]
        if isinstance(paths, list):
            _macro_patterns = paths if paths else DEFAULT_MACRO_PATTERNS
    if "macroIgnorePaths" in linter_cfg:
        ignore = linter_cfg["macroIgnorePaths"]
        if isinstance(ignore, list):
            _macro_ignore_patterns = ignore
    if "showMacroHint" in linter_cfg:
        _macro_show_hint = bool(linter_cfg["showMacroHint"])

    # Re-scan workspace macros if scanning was enabled or patterns changed
    scan_changed = _scan_workspace_macros and (
        not old_scan
        or _macro_patterns != old_patterns
        or _macro_ignore_patterns != old_ignore
    )
    if scan_changed and _macro_registry is not None and _workspace_roots:
        try:
            scan_macro_files(
                _workspace_roots,
                patterns=_macro_patterns,
                ignore_patterns=_macro_ignore_patterns or None,
                registry=_macro_registry,
            )
        except Exception:  # noqa: BLE001
            pass

    # Re-lint all open documents so diagnostics reflect the updated settings
    if server.workspace:
        for uri, doc in list(server.workspace.text_documents.items()):
            _validate_document(uri, doc.source)


@server.feature(types.WORKSPACE_DID_CHANGE_WATCHED_FILES)
def did_change_watched_files(params: types.DidChangeWatchedFilesParams):
    """Update the macro registry when watched .mac files are created, changed, or deleted."""
    if _macro_registry is None:
        return

    changed = False
    for event in params.changes:
        path = _uri_to_path(event.uri)
        if not path:
            continue
        if event.type == types.FileChangeType.Deleted:
            _macro_registry.unregister_by_file(path)
            changed = True
        else:
            # Created or Changed — remove any stale entry then re-parse.
            # Set changed=True now (before the OSError check) so that a failed
            # read still triggers re-validation of open documents; the
            # unregister itself already modified the registry.
            _macro_registry.unregister_by_file(path)
            changed = True
            try:
                text = Path(path).read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            macro_def = parse_macro_file(text, source_file=path)
            if macro_def is not None:
                _macro_registry.register(macro_def)
                _macro_registry._record_mtime(path)

    # Re-lint open documents so diagnostics reflect registry changes
    if changed and server.workspace:
        for uri, doc in list(server.workspace.text_documents.items()):
            _validate_document(uri, doc.source)


@server.feature(types.INITIALIZED)
def on_initialized(params: types.InitializedParams):
    """Scan workspace folders for macro files and build the reference index."""
    global _macro_registry, _workspace_roots  # noqa: PLW0603
    workspace = server.workspace
    if not workspace:
        return
    workspace_paths = []
    try:
        for folder in (workspace.folders or {}).values():
            path = _uri_to_path(folder.uri)
            if os.path.isdir(path):
                workspace_paths.append(path)
    except Exception:  # noqa: BLE001
        return
    # Always record workspace roots so _refresh_macro_file can do accurate
    # relative-path pattern matching even when scanning is disabled.
    _workspace_roots = list(workspace_paths)
    if not workspace_paths:
        return
    # Always build the reference index — it is needed for find-references even
    # when macro scanning is disabled for linting purposes.
    _build_index_for_workspace(workspace_paths)
    if not _scan_workspace_macros:
        return
    if _macro_registry is None:
        return
    # Merge workspace-discovered macros into the existing registry (incremental)
    try:
        scan_macro_files(
            workspace_paths,
            patterns=_macro_patterns,
            ignore_patterns=_macro_ignore_patterns or None,
            registry=_macro_registry,
        )
    except Exception as exc:  # noqa: BLE001
        server.window_log_message(
            types.LogMessageParams(
                type=types.MessageType.Warning,
                message=f"Adams macro scan failed: {exc}",
            )
        )
        return
    # Log all discovered macros to the VS Code output panel
    count = len(_macro_registry)
    if count == 0:
        server.window_log_message(
            types.LogMessageParams(
                type=types.MessageType.Info,
                message="Adams macro scan complete: no macro files found.",
            )
        )
    else:
        lines = [f"Adams macro scan complete: {count} macro(s) discovered."]
        for cmd_key, macro_def in sorted(_macro_registry.items()):
            src = macro_def.source_file or "<unknown>"
            lines.append(f"  {cmd_key}  ({src})")
        server.window_log_message(
            types.LogMessageParams(
                type=types.MessageType.Info,
                message="\n".join(lines),
            )
        )


def _build_index_for_workspace(workspace_paths):
    """Walk *workspace_paths* and index all .cmd/.mac files into _macro_index."""
    if _schema is None:
        return
    if not workspace_paths:
        return
    all_files = _collect_cmd_files(workspace_paths)
    indexed = 0
    for abs_path in all_files:
        path_str = str(abs_path)
        if not _macro_index.needs_refresh(path_str):
            continue
        try:
            text = abs_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        try:
            refs = index_file_text(text, _schema, source_file=path_str)
            _macro_index.update_file(path_str, refs)
            _macro_index.record_mtime(path_str)
            indexed += 1
        except Exception:  # noqa: BLE001
            continue
    if indexed:
        server.window_log_message(
            types.LogMessageParams(
                type=types.MessageType.Info,
                message=(
                    f"Adams reference index built: {indexed} file(s) indexed, "
                    f"{_macro_index.total_references()} macro invocation(s) found."
                ),
            )
        )

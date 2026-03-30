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
from urllib.parse import urlparse, unquote

from pygls.lsp.server import LanguageServer
from lsprotocol import types

from .linter import lint_text
from .schema import Schema
from .diagnostics import Severity
from .macros import scan_macro_files, parse_macro_file, MacroRegistry, DEFAULT_MACRO_PATTERNS


server = LanguageServer("adams-cmd-lsp", "v0.1.0")

# Schema and macro registry are loaded once in main() and stored here
_schema = None
_macro_registry = None
_macro_patterns = DEFAULT_MACRO_PATTERNS
_macro_ignore_patterns: list = []
_scan_workspace_macros = False
_macro_show_hint: bool = True
_workspace_roots: list = []

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
            macro_registry=_macro_registry,
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


@server.feature(types.TEXT_DOCUMENT_DID_CHANGE)
def did_change(params: types.DidChangeTextDocumentParams):
    doc = server.workspace.get_text_document(params.text_document.uri)
    _validate_document(params.text_document.uri, doc.source)


@server.feature(types.TEXT_DOCUMENT_DID_CLOSE)
def did_close(params: types.DidCloseTextDocumentParams):
    server.text_document_publish_diagnostics(
        types.PublishDiagnosticsParams(uri=params.text_document.uri, diagnostics=[])
    )


@server.feature(types.TEXT_DOCUMENT_DID_SAVE)
def did_save(params: types.DidSaveTextDocumentParams):
    doc = server.workspace.get_text_document(params.text_document.uri)
    _validate_document(params.text_document.uri, doc.source)
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
        macro_def = parse_macro_file(text, source_file=path)
        if macro_def is not None:
            _macro_registry.register(macro_def)
    except Exception:  # noqa: BLE001
        pass


def main():
    """Entry point for the adams-cmd-lsp LSP server."""
    global _schema, _macro_registry, _macro_patterns, _macro_ignore_patterns, _scan_workspace_macros, _macro_show_hint, _workspace_roots  # noqa: PLW0603

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

    # Build initial registry — always created so did_save can refresh it later.
    # Workspace folders are merged in after the client connects (see INITIALIZED).
    _macro_registry = MacroRegistry()

    if args.tcp:
        server.start_tcp("localhost", args.port)
    else:
        server.start_io()


@server.feature(types.INITIALIZED)
def on_initialized(params: types.InitializedParams):
    """Scan workspace folders for macro files once the client reports ready."""
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
    if not _scan_workspace_macros:
        return
    if _macro_registry is None:
        return
    if not workspace_paths:
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

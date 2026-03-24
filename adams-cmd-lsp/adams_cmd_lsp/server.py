"""LSP server for Adams CMD language.

Uses pygls 2.x (from pygls.lsp.server import LanguageServer).
Start via:
    python -m adams_cmd_lsp          # stdio (default, for editors)
    adams-cmd-lsp                    # same, via entry point
    adams-cmd-lsp --tcp --port 2087  # TCP, for debugging
"""

import argparse

from pygls.lsp.server import LanguageServer
from lsprotocol import types

from .linter import lint_text
from .schema import Schema
from .diagnostics import Severity


server = LanguageServer("adams-cmd-lsp", "v0.1.0")

# Schema is loaded once in main() and stored here
_schema = None

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
        diagnostics = lint_text(text, schema=_schema)
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
    server.publish_diagnostics(params.text_document.uri, [])


@server.feature(types.TEXT_DOCUMENT_DID_SAVE)
def did_save(params: types.DidSaveTextDocumentParams):
    doc = server.workspace.get_text_document(params.text_document.uri)
    _validate_document(params.text_document.uri, doc.source)


def main():
    """Entry point for the adams-cmd-lsp LSP server."""
    global _schema  # noqa: PLW0603

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
    # vscode-languageclient passes --stdio automatically; accept and ignore it.
    parser.add_argument(
        "--stdio",
        action="store_true",
        help="Use stdio transport (default, passed automatically by VS Code)",
    )
    args = parser.parse_args()

    _schema = Schema.load(args.schema) if args.schema else Schema.load()

    if args.tcp:
        server.start_tcp("localhost", args.port)
    else:
        server.start_io()

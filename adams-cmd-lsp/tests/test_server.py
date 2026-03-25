"""Tests for adams_cmd_lsp.server module.

These tests exercise the helper functions (_to_lsp_diagnostic, _validate_document)
without starting a live LSP server, since an LSP event loop is not available in unit
test context.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

# Guard: skip entire module if pygls/lsprotocol are not installed
try:
    from pygls.lsp.server import LanguageServer  # noqa: F401
    from lsprotocol import types
    _PYGLS_AVAILABLE = True
except ImportError:
    _PYGLS_AVAILABLE = False

pytestmark = pytest.mark.skipif(
    not _PYGLS_AVAILABLE,
    reason="pygls / lsprotocol not installed",
)

if _PYGLS_AVAILABLE:
    from adams_cmd_lsp import server as srv
    from adams_cmd_lsp.diagnostics import Diagnostic, Severity
    from adams_cmd_lsp.schema import Schema


# ---------------------------------------------------------------------------
# _to_lsp_diagnostic
# ---------------------------------------------------------------------------

def test_to_lsp_diagnostic_error():
    d = Diagnostic(
        line=2, column=4, end_line=2, end_column=10,
        code="E001", message="Unknown command: 'foo'",
        severity=Severity.ERROR,
    )
    lsp_d = srv._to_lsp_diagnostic(d)
    assert lsp_d.range.start.line == 2
    assert lsp_d.range.start.character == 4
    assert lsp_d.range.end.line == 2
    assert lsp_d.range.end.character == 10
    assert lsp_d.message == "Unknown command: 'foo'"
    assert lsp_d.code == "E001"
    assert lsp_d.severity == types.DiagnosticSeverity.Error
    assert lsp_d.source == "adams-cmd-lint"


def test_to_lsp_diagnostic_warning():
    d = Diagnostic(
        line=0, column=0, end_line=0, end_column=3,
        code="W005", message="Object name omitted",
        severity=Severity.WARNING,
    )
    lsp_d = srv._to_lsp_diagnostic(d)
    assert lsp_d.severity == types.DiagnosticSeverity.Warning


def test_to_lsp_diagnostic_info():
    d = Diagnostic(
        line=1, column=0, end_line=1, end_column=5,
        code="I006", message="Manual adams_id",
        severity=Severity.INFO,
    )
    lsp_d = srv._to_lsp_diagnostic(d)
    assert lsp_d.severity == types.DiagnosticSeverity.Information


# ---------------------------------------------------------------------------
# _validate_document (unit test: patch publish_diagnostics)
# ---------------------------------------------------------------------------

def test_validate_document_clean(monkeypatch):
    """Clean CMD text should publish an empty diagnostics list."""
    published = []

    def mock_publish(params):
        published.append(params)

    monkeypatch.setattr(srv.server, "text_document_publish_diagnostics", mock_publish)

    # Ensure schema is loaded
    srv._schema = Schema.load()

    srv._validate_document("file:///test.cmd", "model create model_name = my_model\n")
    assert len(published) == 1
    params = published[0]
    assert params.uri == "file:///test.cmd"
    # Valid command should produce no LSP error diagnostics
    errors = [d for d in params.diagnostics if d.severity == types.DiagnosticSeverity.Error]
    assert errors == []


def test_validate_document_with_error(monkeypatch):
    """Unknown command should publish at least one error diagnostic."""
    published = []

    def mock_publish(params):
        published.append(params)

    monkeypatch.setattr(srv.server, "text_document_publish_diagnostics", mock_publish)
    srv._schema = Schema.load()

    srv._validate_document("file:///test.cmd", "not_a_real_command foo=bar\n")
    assert len(published) == 1
    params = published[0]
    codes = [d.code for d in params.diagnostics]
    assert "E001" in codes


def test_validate_document_swallows_lint_exception(monkeypatch):
    """If lint_text raises, _validate_document should publish [] and not crash."""
    published = []

    def mock_publish(params):
        published.append(params)

    def mock_lint(*args, **kwargs):
        raise RuntimeError("unexpected lint error")

    def mock_log(msg):
        pass

    monkeypatch.setattr(srv.server, "text_document_publish_diagnostics", mock_publish)
    monkeypatch.setattr(srv.server, "window_log_message", mock_log)
    monkeypatch.setattr(srv, "lint_text", mock_lint)

    srv._validate_document("file:///test.cmd", "anything\n")
    assert len(published) == 1
    params = published[0]
    assert params.diagnostics == []


# ---------------------------------------------------------------------------
# Severity mapping completeness
# ---------------------------------------------------------------------------

def test_severity_map_covers_all_severities():
    """_SEVERITY_MAP should map all Severity enum members."""
    for sev in Severity:
        assert sev in srv._SEVERITY_MAP, f"Severity.{sev.name} missing from _SEVERITY_MAP"


# ---------------------------------------------------------------------------
# did_close — must clear diagnostics via text_document_publish_diagnostics
# ---------------------------------------------------------------------------

def test_did_close_clears_diagnostics(monkeypatch):
    """Closing a document must publish an empty diagnostics list.

    In pygls 2.x the method is text_document_publish_diagnostics(), NOT the
    pygls 1.x server.publish_diagnostics() shortcut.  This test guards against
    regression to the old API (which raises AttributeError at runtime).
    """
    published = []

    def mock_publish(params):
        published.append(params)

    monkeypatch.setattr(srv.server, "text_document_publish_diagnostics", mock_publish)

    close_params = types.DidCloseTextDocumentParams(
        text_document=types.TextDocumentIdentifier(uri="file:///test.cmd")
    )
    srv.did_close(close_params)

    assert len(published) == 1, "did_close must publish diagnostics exactly once"
    params = published[0]
    assert params.uri == "file:///test.cmd"
    assert params.diagnostics == [], (
        f"did_close must publish empty diagnostics list, got: {params.diagnostics}"
    )

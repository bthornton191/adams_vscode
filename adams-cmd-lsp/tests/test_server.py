"""Tests for adams_cmd_lsp.server module.

These tests exercise the helper functions (_to_lsp_diagnostic, _validate_document)
without starting a live LSP server, since an LSP event loop is not available in unit
test context.
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


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


# ---------------------------------------------------------------------------
# _uri_to_path
# ---------------------------------------------------------------------------

def test_uri_to_path_linux():
    """Linux file:// URI should strip the scheme."""
    path = srv._uri_to_path("file:///home/user/project/tool.mac")
    assert path == "/home/user/project/tool.mac"


def test_uri_to_path_windows_style():
    """Windows-style file:// URI (leading /C:/) should strip the leading slash."""
    path = srv._uri_to_path("file:///C:/Users/user/project/tool.mac")
    # On Windows the function strips the leading '/'
    import os
    if os.name == "nt":
        assert path == "C:/Users/user/project/tool.mac"
    else:
        # On non-Windows, the leading slash is retained (function is OS-aware)
        assert "C:/Users" in path


def test_uri_to_path_encoded_spaces():
    """URL-encoded spaces in path should be decoded."""
    path = srv._uri_to_path("file:///home/user/my%20project/tool.mac")
    assert "my project" in path


# ---------------------------------------------------------------------------
# _refresh_macro_file
# ---------------------------------------------------------------------------

def test_refresh_macro_file_registers_macro(tmp_path):
    """Saving a .mac file with !USER_ENTERED_COMMAND updates the registry."""
    from adams_cmd_lsp.macros import MacroRegistry
    srv._macro_registry = MacroRegistry()
    srv._macro_patterns = ["**/*.mac"]

    mac_path = tmp_path / "tool.mac"
    mac_path.write_text("!USER_ENTERED_COMMAND cdm tool\n!$model:t=model\n", encoding="utf-8")
    uri = mac_path.as_uri()

    srv._refresh_macro_file(uri, mac_path.read_text(encoding="utf-8"))
    assert srv._macro_registry.has_command("cdm tool")


def test_refresh_macro_file_non_mac_ignored(tmp_path):
    """Saving a non-macro file (wrong name pattern) should not touch the registry."""
    from adams_cmd_lsp.macros import MacroRegistry
    srv._macro_registry = MacroRegistry()
    srv._macro_patterns = ["**/*.mac"]

    txt_path = tmp_path / "notes.txt"
    txt_path.write_text("some text\n", encoding="utf-8")
    uri = txt_path.as_uri()

    # Registry should remain empty
    srv._refresh_macro_file(uri, "some text\n")
    assert len(srv._macro_registry) == 0


def test_refresh_macro_file_no_registry():
    """_refresh_macro_file should be a no-op when _macro_registry is None."""
    srv._macro_registry = None
    # Should not raise
    srv._refresh_macro_file("file:///some/file.mac", "!USER_ENTERED_COMMAND foo\n")


def test_refresh_macro_file_no_command(tmp_path):
    """A .mac file with no !USER_ENTERED_COMMAND should not add to registry."""
    from adams_cmd_lsp.macros import MacroRegistry
    srv._macro_registry = MacroRegistry()
    srv._macro_patterns = ["**/*.mac"]

    mac_path = tmp_path / "plain.mac"
    mac_path.write_text("! just a plain macro\npart create\n", encoding="utf-8")
    uri = mac_path.as_uri()

    srv._refresh_macro_file(uri, mac_path.read_text(encoding="utf-8"))
    assert len(srv._macro_registry) == 0


# ---------------------------------------------------------------------------
# _validate_document passes macro_registry to lint_text
# ---------------------------------------------------------------------------

def test_validate_document_passes_macro_registry(monkeypatch):
    """_validate_document must forward _macro_registry to lint_text when scanning enabled."""
    from adams_cmd_lsp.macros import MacroRegistry, MacroDefinition
    received_registry = []

    def mock_lint_text(text, schema=None, min_severity=None, macro_registry=None, show_macro_hint=True):
        received_registry.append(macro_registry)
        return []

    def mock_publish(params):
        pass

    monkeypatch.setattr(srv, "lint_text", mock_lint_text)
    monkeypatch.setattr(srv.server, "text_document_publish_diagnostics", mock_publish)

    reg = MacroRegistry()
    reg.register(MacroDefinition(command="cdm tool", parameters={}))
    srv._macro_registry = reg
    srv._scan_workspace_macros = True  # scanning must be enabled for registry to be forwarded
    srv._schema = Schema.load()

    srv._validate_document("file:///test.cmd", "cdm tool\n")
    assert len(received_registry) == 1
    assert received_registry[0] is reg


def test_validate_document_passes_none_registry_when_scan_disabled(monkeypatch):
    """_validate_document must pass macro_registry=None when scanning is disabled.

    This ensures that E001 messages include the scanWorkspaceMacros hint
    even though the server always maintains an internal MacroRegistry instance.
    """
    from adams_cmd_lsp.macros import MacroRegistry, MacroDefinition
    received_registry = []

    def mock_lint_text(text, schema=None, min_severity=None, macro_registry=None, show_macro_hint=True):
        received_registry.append(macro_registry)
        return []

    def mock_publish(params):
        pass

    monkeypatch.setattr(srv, "lint_text", mock_lint_text)
    monkeypatch.setattr(srv.server, "text_document_publish_diagnostics", mock_publish)

    reg = MacroRegistry()
    reg.register(MacroDefinition(command="cdm tool", parameters={}))
    srv._macro_registry = reg
    srv._scan_workspace_macros = False  # scanning disabled
    srv._schema = Schema.load()

    srv._validate_document("file:///test.cmd", "cdm tool\n")
    assert len(received_registry) == 1
    assert received_registry[0] is None, (
        "When scanning is disabled, lint_text must receive macro_registry=None "
        "so that E001 hints are not suppressed"
    )


# ---------------------------------------------------------------------------
# _refresh_macro_file — pattern matching correctness (Fix 1 regression tests)
# ---------------------------------------------------------------------------

def test_refresh_macro_file_macros_star_pattern_excludes_outside(tmp_path):
    """A file outside the 'macros/' dir must NOT be re-parsed when pattern is 'macros/*'."""
    from adams_cmd_lsp.macros import MacroRegistry

    srv._macro_registry = MacroRegistry()
    srv._macro_patterns = ["macros/*"]
    # Set workspace root so the full relative-path matching is used
    srv._workspace_roots = [str(tmp_path)]

    # File is in tmp_path directly — NOT inside tmp_path/macros/
    outside = tmp_path / "tool.mac"
    outside.write_text("!USER_ENTERED_COMMAND cdm tool\n", encoding="utf-8")
    uri = outside.as_uri()

    srv._refresh_macro_file(uri, outside.read_text(encoding="utf-8"))
    # Should NOT be registered because the file doesn't match "macros/*"
    assert len(srv._macro_registry) == 0


def test_refresh_macro_file_star_star_mac_pattern_excludes_py(tmp_path):
    """A .py file must NOT be re-parsed when pattern is '**/*.mac'."""
    from adams_cmd_lsp.macros import MacroRegistry

    srv._macro_registry = MacroRegistry()
    srv._macro_patterns = ["**/*.mac"]
    srv._workspace_roots = [str(tmp_path)]

    py_file = tmp_path / "helper.py"
    py_file.write_text("# just a Python file\n", encoding="utf-8")
    uri = py_file.as_uri()

    srv._refresh_macro_file(uri, py_file.read_text(encoding="utf-8"))
    assert len(srv._macro_registry) == 0


def test_refresh_macro_file_macros_star_pattern_includes_inside(tmp_path):
    """A .mac file INSIDE 'macros/' dir MUST be re-parsed when pattern is 'macros/*'."""
    from adams_cmd_lsp.macros import MacroRegistry

    macros_dir = tmp_path / "macros"
    macros_dir.mkdir()
    srv._macro_registry = MacroRegistry()
    srv._macro_patterns = ["macros/*"]
    srv._workspace_roots = [str(tmp_path)]

    mac_file = macros_dir / "tool.mac"
    mac_file.write_text("!USER_ENTERED_COMMAND cdm tool\n", encoding="utf-8")
    uri = mac_file.as_uri()

    srv._refresh_macro_file(uri, mac_file.read_text(encoding="utf-8"))
    assert srv._macro_registry.has_command("cdm tool")


# ---------------------------------------------------------------------------
# _refresh_macro_file — fallback filename matching (no workspace roots)
# ---------------------------------------------------------------------------

def test_refresh_macro_file_no_workspace_roots_fallback_matches_mac(tmp_path):
    """When workspace roots are empty, **/*.mac pattern falls back to filename matching."""
    from adams_cmd_lsp.macros import MacroRegistry

    srv._macro_registry = MacroRegistry()
    srv._macro_patterns = ["**/*.mac"]
    srv._workspace_roots = []  # no roots — triggers fallback path

    mac_path = tmp_path / "tool.mac"
    mac_path.write_text("!USER_ENTERED_COMMAND cdm fallback_find\n", encoding="utf-8")
    uri = mac_path.as_uri()

    srv._refresh_macro_file(uri, mac_path.read_text(encoding="utf-8"))
    assert srv._macro_registry.has_command("cdm fallback_find"), (
        "Fallback filename matching should register .mac files when workspace roots are empty"
    )


def test_refresh_macro_file_no_workspace_roots_bare_star_not_matched(tmp_path):
    """When workspace roots are empty, patterns ending in bare '*' must NOT match.

    'macros/*' has last segment '*' — this would match every file, so the
    fallback logic skips it to avoid false positive macro registrations.
    """
    from adams_cmd_lsp.macros import MacroRegistry

    srv._macro_registry = MacroRegistry()
    srv._macro_patterns = ["macros/*"]  # last segment is bare "*"
    srv._workspace_roots = []

    mac_path = tmp_path / "tool.mac"
    mac_path.write_text("!USER_ENTERED_COMMAND cdm bare_star_cmd\n", encoding="utf-8")
    uri = mac_path.as_uri()

    srv._refresh_macro_file(uri, mac_path.read_text(encoding="utf-8"))
    assert len(srv._macro_registry) == 0, (
        "Pattern 'macros/*' (bare '*' last segment) must not match via filename fallback"
    )


# ---------------------------------------------------------------------------
# _refresh_macro_file — silent exception handling (G5)
# ---------------------------------------------------------------------------

def test_refresh_macro_file_parse_exception_swallowed(tmp_path, monkeypatch):
    """_refresh_macro_file must not propagate exceptions from parse_macro_file."""
    from adams_cmd_lsp.macros import MacroRegistry

    srv._macro_registry = MacroRegistry()
    srv._macro_patterns = ["**/*.mac"]
    srv._workspace_roots = [str(tmp_path)]

    def exploding_parse(text, source_file=""):
        raise RuntimeError("Simulated parse failure")

    monkeypatch.setattr(srv, "parse_macro_file", exploding_parse)

    mac_path = tmp_path / "tool.mac"
    mac_path.write_text("!USER_ENTERED_COMMAND cdm boom\n", encoding="utf-8")
    uri = mac_path.as_uri()

    # Must not raise even though parse_macro_file throws
    srv._refresh_macro_file(uri, mac_path.read_text(encoding="utf-8"))
    assert len(srv._macro_registry) == 0


# ---------------------------------------------------------------------------
# _refresh_macro_file — command change documents design limitation (G9)
# ---------------------------------------------------------------------------

def test_refresh_macro_file_old_command_persists_after_change(tmp_path):
    """When a .mac file's command changes, the old command key remains in the registry.

    MacroRegistry has no unregister mechanism, so re-saving a macro file registers
    the new command but does NOT remove the old one. This is a known design limitation.
    """
    from adams_cmd_lsp.macros import MacroRegistry

    macros_dir = tmp_path / "macros"
    macros_dir.mkdir()
    mac_file = macros_dir / "tool.mac"

    mac_file.write_text("!USER_ENTERED_COMMAND cdm old_cmd\n", encoding="utf-8")
    srv._macro_registry = MacroRegistry()
    srv._macro_patterns = ["**/*.mac"]
    srv._workspace_roots = [str(tmp_path)]

    srv._refresh_macro_file(mac_file.as_uri(), mac_file.read_text(encoding="utf-8"))
    assert srv._macro_registry.has_command("cdm old_cmd")

    # Simulate re-save with different command
    new_content = "!USER_ENTERED_COMMAND cdm new_cmd\n"
    srv._refresh_macro_file(mac_file.as_uri(), new_content)

    assert srv._macro_registry.has_command("cdm new_cmd"), (
        "New command should be registered after re-save"
    )
    assert srv._macro_registry.has_command("cdm old_cmd"), (
        "Old command persists — this is a known design limitation of MacroRegistry"
    )


# ---------------------------------------------------------------------------
# on_initialized — workspace scanning lifecycle (G2)
# ---------------------------------------------------------------------------

def _make_mock_server(workspace_path):
    """Return a mock server object whose workspace has a single folder."""
    import types as python_types
    from pathlib import Path
    folder = python_types.SimpleNamespace(uri=Path(workspace_path).as_uri())
    mock_workspace = python_types.SimpleNamespace(folders={"workspace": folder})
    return python_types.SimpleNamespace(
        workspace=mock_workspace,
        window_log_message=lambda params: None,
    )


def test_on_initialized_stores_workspace_roots_when_scan_disabled(tmp_path, monkeypatch):
    """on_initialized must populate _workspace_roots even when scanning is disabled."""
    from adams_cmd_lsp.macros import MacroRegistry
    from pathlib import Path

    monkeypatch.setattr(srv, "server", _make_mock_server(tmp_path))

    srv._macro_registry = MacroRegistry()
    srv._scan_workspace_macros = False
    srv._workspace_roots = []

    srv.on_initialized(types.InitializedParams())

    assert len(srv._workspace_roots) == 1
    assert Path(srv._workspace_roots[0]) == tmp_path


def test_on_initialized_scans_workspace_when_enabled(tmp_path, monkeypatch):
    """on_initialized must scan for macros when _scan_workspace_macros=True."""
    from adams_cmd_lsp.macros import MacroRegistry

    mac_file = tmp_path / "tool.mac"
    mac_file.write_text("!USER_ENTERED_COMMAND cdm init_scan\n", encoding="utf-8")

    monkeypatch.setattr(srv, "server", _make_mock_server(tmp_path))

    srv._macro_registry = MacroRegistry()
    srv._scan_workspace_macros = True
    srv._macro_patterns = ["**/*.mac"]
    srv._macro_ignore_patterns = []
    srv._workspace_roots = []

    srv.on_initialized(types.InitializedParams())

    assert srv._macro_registry.has_command("cdm init_scan"), (
        "on_initialized should scan and register macros when scan is enabled"
    )


def test_on_initialized_logs_discovered_macros(tmp_path, monkeypatch):
    """on_initialized must log the list of discovered macros to the output panel."""
    from adams_cmd_lsp.macros import MacroRegistry

    (tmp_path / "tool.mac").write_text("!USER_ENTERED_COMMAND cdm log_test\n", encoding="utf-8")
    (tmp_path / "other.mac").write_text("!USER_ENTERED_COMMAND cdm log_other\n", encoding="utf-8")

    log_messages = []
    mock_server = _make_mock_server(tmp_path)
    mock_server.window_log_message = lambda params: log_messages.append(params.message)
    monkeypatch.setattr(srv, "server", mock_server)

    srv._macro_registry = MacroRegistry()
    srv._scan_workspace_macros = True
    srv._macro_patterns = ["**/*.mac"]
    srv._macro_ignore_patterns = []
    srv._workspace_roots = []

    srv.on_initialized(types.InitializedParams())

    combined = "\n".join(log_messages)
    assert "cdm log_test" in combined, "Log should mention discovered macro commands"
    assert "cdm log_other" in combined, "Log should mention all discovered macro commands"
    assert "macro(s) discovered" in combined, "Log should include discovery count"


def test_on_initialized_no_scan_when_disabled(tmp_path, monkeypatch):
    """on_initialized must NOT scan for macros when _scan_workspace_macros=False."""
    from adams_cmd_lsp.macros import MacroRegistry

    mac_file = tmp_path / "tool.mac"
    mac_file.write_text("!USER_ENTERED_COMMAND cdm should_not_find\n", encoding="utf-8")

    monkeypatch.setattr(srv, "server", _make_mock_server(tmp_path))

    srv._macro_registry = MacroRegistry()
    srv._scan_workspace_macros = False
    srv._workspace_roots = []

    srv.on_initialized(types.InitializedParams())

    assert not srv._macro_registry.has_command("cdm should_not_find"), (
        "Scan should not happen when _scan_workspace_macros=False"
    )


# ---------------------------------------------------------------------------
# _validate_document — show_macro_hint forwarding (G3)
# ---------------------------------------------------------------------------

def test_validate_document_forwards_show_macro_hint(monkeypatch):
    """_validate_document must forward _macro_show_hint=False to lint_text."""
    received_hints = []

    def mock_lint_text(text, schema=None, min_severity=None, macro_registry=None, show_macro_hint=True):
        received_hints.append(show_macro_hint)
        return []

    def mock_publish(params):
        pass

    monkeypatch.setattr(srv, "lint_text", mock_lint_text)
    monkeypatch.setattr(srv.server, "text_document_publish_diagnostics", mock_publish)

    srv._macro_show_hint = False  # non-default value to verify it is forwarded
    srv._schema = Schema.load()

    srv._validate_document("file:///test.cmd", "model create\n")
    assert received_hints == [False], (
        f"show_macro_hint should be forwarded as False, got: {received_hints}"
    )

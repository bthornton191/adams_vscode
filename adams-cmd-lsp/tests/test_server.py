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


def test_refresh_macro_file_returns_true_when_registered(tmp_path):
    """_refresh_macro_file returns True when a macro was added to the registry."""
    from adams_cmd_lsp.macros import MacroRegistry
    srv._macro_registry = MacroRegistry()
    srv._macro_patterns = ["**/*.mac"]

    mac_path = tmp_path / "tool.mac"
    mac_path.write_text("!USER_ENTERED_COMMAND my tool\n", encoding="utf-8")
    uri = mac_path.as_uri()

    result = srv._refresh_macro_file(uri, mac_path.read_text(encoding="utf-8"))
    assert result is True
    assert srv._macro_registry.has_command("my tool")


def test_refresh_macro_file_returns_false_when_no_match(tmp_path):
    """_refresh_macro_file returns False when the file does not match macro patterns."""
    from adams_cmd_lsp.macros import MacroRegistry
    srv._macro_registry = MacroRegistry()
    srv._macro_patterns = ["**/*.mac"]

    txt_path = tmp_path / "notes.txt"
    txt_path.write_text("!USER_ENTERED_COMMAND my tool\n", encoding="utf-8")
    uri = txt_path.as_uri()

    result = srv._refresh_macro_file(uri, txt_path.read_text(encoding="utf-8"))
    assert result is False


def test_refresh_macro_file_no_registry():
    """_refresh_macro_file should be a no-op when _macro_registry is None."""
    srv._macro_registry = None
    # Should not raise and should return False
    result = srv._refresh_macro_file("file:///some/file.mac", "!USER_ENTERED_COMMAND foo\n")
    assert result is False


def test_refresh_macro_file_no_command(tmp_path):
    """A .mac file with no !USER_ENTERED_COMMAND should not add to registry.

    Returns True (file matched pattern, processed without error) even when
    no command is registered — callers may still re-lint speculatively.
    """
    from adams_cmd_lsp.macros import MacroRegistry
    srv._macro_registry = MacroRegistry()
    srv._macro_patterns = ["**/*.mac"]

    mac_path = tmp_path / "plain.mac"
    mac_path.write_text("! just a plain macro\npart create\n", encoding="utf-8")
    uri = mac_path.as_uri()

    result = srv._refresh_macro_file(uri, mac_path.read_text(encoding="utf-8"))
    assert len(srv._macro_registry) == 0
    assert result is True  # matched pattern and processed without error


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


def test_refresh_macro_file_parse_exception_unregisters_and_returns_true(tmp_path, monkeypatch):
    """_refresh_macro_file returns True and removes the macro when parse_macro_file raises.

    unregister_by_file runs before parse_macro_file; if parsing then throws the
    macro is gone from the registry.  True is returned so callers still re-lint
    other open documents (which need to reflect the removal).
    """
    from adams_cmd_lsp.macros import MacroRegistry, MacroDefinition

    macros_dir = tmp_path / "macros"
    macros_dir.mkdir()
    mac_path = macros_dir / "tool.mac"
    mac_path.write_text("!USER_ENTERED_COMMAND cdm boom\n", encoding="utf-8")

    srv._macro_registry = MacroRegistry()
    srv._macro_patterns = ["**/*.mac"]
    srv._workspace_roots = [str(tmp_path)]

    # Pre-register the macro so we can verify it is removed on parse failure
    srv._macro_registry.register(MacroDefinition(command="cdm boom", parameters={}, source_file=str(mac_path)))
    assert srv._macro_registry.has_command("cdm boom")

    def exploding_parse(text, source_file=""):
        raise RuntimeError("Simulated parse failure")

    monkeypatch.setattr(srv, "parse_macro_file", exploding_parse)

    result = srv._refresh_macro_file(mac_path.as_uri(), mac_path.read_text(encoding="utf-8"))
    # Macro should be unregistered (unregister_by_file ran before parse failed)
    assert not srv._macro_registry.has_command("cdm boom")
    # True so callers know to re-lint
    assert result is True


# ---------------------------------------------------------------------------
# _refresh_macro_file — command change documents design limitation (G9)
# ---------------------------------------------------------------------------

def test_refresh_macro_file_old_command_removed_after_change(tmp_path):
    """When a .mac file's command changes, the old command key is removed from the registry.

    _refresh_macro_file calls unregister_by_file before re-parsing so that stale
    entries from the same file do not accumulate in the registry.
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
    assert not srv._macro_registry.has_command("cdm old_cmd"), (
        "Old command should be removed after re-save with a different command key"
    )


# ---------------------------------------------------------------------------
# did_open — macro registration on open (regression: ref→def and E001)
# ---------------------------------------------------------------------------

def test_did_open_registers_macro_file(tmp_path, monkeypatch):
    """did_open registers .mac file in registry and re-lints other open documents.

    Regression: _refresh_macro_file was not called from did_open, so opening
    test.mac in the editor did not populate the registry.  Ctrl+Click from a
    call site (ref→def) would return nothing and E001 was raised for macro calls.
    """
    from adams_cmd_lsp.macros import MacroRegistry
    import types as python_types

    srv._macro_registry = MacroRegistry()
    srv._macro_patterns = ["**/*.mac"]
    srv._workspace_roots = []  # fallback filename-matching path
    srv._schema = Schema.load()

    mac_path = tmp_path / "custom.mac"
    mac_path.write_text("!USER_ENTERED_COMMAND custom command\n", encoding="utf-8")
    mac_uri = mac_path.as_uri()

    caller_uri = "file:///caller.cmd"

    # Track which URIs are validated via text_document_publish_diagnostics
    validated_uris = []

    mock_workspace = python_types.SimpleNamespace(
        get_text_document=lambda u: python_types.SimpleNamespace(
            source=mac_path.read_text(encoding="utf-8") if u == mac_uri else "custom command\n",
            uri=u,
        ),
        text_documents={
            mac_uri: python_types.SimpleNamespace(
                source="!USER_ENTERED_COMMAND custom command\n", uri=mac_uri
            ),
            caller_uri: python_types.SimpleNamespace(
                source="custom command\n", uri=caller_uri
            ),
        },
        folders={},
    )
    mock_server = python_types.SimpleNamespace(
        workspace=mock_workspace,
        text_document_publish_diagnostics=lambda params: validated_uris.append(params.uri),
    )
    monkeypatch.setattr(srv, "server", mock_server)

    params = types.DidOpenTextDocumentParams(
        text_document=types.TextDocumentItem(
            uri=mac_uri,
            language_id="adams_cmd",
            version=1,
            text="!USER_ENTERED_COMMAND custom command\n",
        )
    )

    srv.did_open(params)

    # Registry must be updated because did_open now calls _refresh_macro_file
    assert srv._macro_registry.has_command("custom command"), (
        "did_open must register macro files so ref→def navigation and E001 suppression work"
    )
    # Caller file must be re-linted so its E001 clears immediately
    assert caller_uri in validated_uris, (
        "did_open must re-lint other open documents after registering a new macro"
    )
    # The mac file itself must not be re-linted by the loop (only once at the top)
    assert validated_uris.count(mac_uri) == 1, (
        "did_open must not re-lint the opened mac file a second time in the re-lint loop"
    )


# ---------------------------------------------------------------------------
# did_save — macro registration re-lint (mirrors did_open behaviour)
# ---------------------------------------------------------------------------

def test_did_save_relints_other_documents(tmp_path, monkeypatch):
    """did_save re-lints other open documents when a .mac file is saved.

    Mirrors the did_open behaviour: saving a .mac file updates the registry
    and re-lints callers so E001 clears immediately.
    """
    from adams_cmd_lsp.macros import MacroRegistry
    import types as python_types

    srv._macro_registry = MacroRegistry()
    srv._macro_patterns = ["**/*.mac"]
    srv._workspace_roots = []  # fallback filename-matching path
    srv._schema = Schema.load()

    mac_path = tmp_path / "custom.mac"
    mac_path.write_text("!USER_ENTERED_COMMAND custom command\n", encoding="utf-8")
    mac_uri = mac_path.as_uri()

    caller_uri = "file:///caller.cmd"
    validated_uris = []

    mac_doc = python_types.SimpleNamespace(
        source="!USER_ENTERED_COMMAND custom command\n", uri=mac_uri
    )
    caller_doc = python_types.SimpleNamespace(source="custom command\n", uri=caller_uri)

    mock_workspace = python_types.SimpleNamespace(
        get_text_document=lambda u: mac_doc if u == mac_uri else caller_doc,
        text_documents={mac_uri: mac_doc, caller_uri: caller_doc},
        folders={},
    )
    mock_server = python_types.SimpleNamespace(
        workspace=mock_workspace,
        text_document_publish_diagnostics=lambda params: validated_uris.append(params.uri),
    )
    monkeypatch.setattr(srv, "server", mock_server)

    params = types.DidSaveTextDocumentParams(
        text_document=types.TextDocumentIdentifier(uri=mac_uri),
    )

    srv.did_save(params)

    assert srv._macro_registry.has_command("custom command"), (
        "did_save must register macro files so ref→def navigation works"
    )
    assert caller_uri in validated_uris, (
        "did_save must re-lint other open documents after registering a macro"
    )
    assert validated_uris.count(mac_uri) == 1, (
        "did_save must not re-lint the saved mac file a second time in the re-lint loop"
    )


def test_did_open_nonmacro_does_not_relint_others(tmp_path, monkeypatch):
    """did_open must not re-lint other documents when a non-macro file is opened."""
    from adams_cmd_lsp.macros import MacroRegistry
    import types as python_types

    srv._macro_registry = MacroRegistry()
    srv._macro_patterns = ["**/*.mac"]
    srv._workspace_roots = []
    srv._schema = Schema.load()

    cmd_path = tmp_path / "script.cmd"
    cmd_path.write_text("model create model_name=.m\n", encoding="utf-8")
    cmd_uri = cmd_path.as_uri()

    caller_uri = "file:///other.cmd"
    validated_uris = []

    mock_workspace = python_types.SimpleNamespace(
        get_text_document=lambda u: python_types.SimpleNamespace(
            source=cmd_path.read_text(encoding="utf-8"), uri=u
        ),
        text_documents={
            cmd_uri: python_types.SimpleNamespace(source="model create model_name=.m\n", uri=cmd_uri),
            caller_uri: python_types.SimpleNamespace(source="model create model_name=.m\n", uri=caller_uri),
        },
        folders={},
    )
    monkeypatch.setattr(srv, "server", python_types.SimpleNamespace(
        workspace=mock_workspace,
        text_document_publish_diagnostics=lambda params: validated_uris.append(params.uri),
    ))

    params = types.DidOpenTextDocumentParams(
        text_document=types.TextDocumentItem(
            uri=cmd_uri,
            language_id="adams_cmd",
            version=1,
            text="model create model_name=.m\n",
        )
    )

    srv.did_open(params)

    assert caller_uri not in validated_uris, (
        "did_open must not re-lint other documents when the opened file is not a macro"
    )


def test_did_save_nonmacro_does_not_relint_others(tmp_path, monkeypatch):
    """did_save must not re-lint other documents when a non-macro file is saved."""
    from adams_cmd_lsp.macros import MacroRegistry
    import types as python_types

    srv._macro_registry = MacroRegistry()
    srv._macro_patterns = ["**/*.mac"]
    srv._workspace_roots = []
    srv._schema = Schema.load()

    cmd_path = tmp_path / "script.cmd"
    cmd_path.write_text("model create model_name=.m\n", encoding="utf-8")
    cmd_uri = cmd_path.as_uri()

    caller_uri = "file:///other.cmd"
    validated_uris = []

    cmd_doc = python_types.SimpleNamespace(source="model create model_name=.m\n", uri=cmd_uri)
    caller_doc = python_types.SimpleNamespace(source="model create model_name=.m\n", uri=caller_uri)

    mock_workspace = python_types.SimpleNamespace(
        get_text_document=lambda u: cmd_doc,
        text_documents={cmd_uri: cmd_doc, caller_uri: caller_doc},
        folders={},
    )
    monkeypatch.setattr(srv, "server", python_types.SimpleNamespace(
        workspace=mock_workspace,
        text_document_publish_diagnostics=lambda params: validated_uris.append(params.uri),
    ))

    params = types.DidSaveTextDocumentParams(
        text_document=types.TextDocumentIdentifier(uri=cmd_uri),
    )

    srv.did_save(params)

    assert caller_uri not in validated_uris, (
        "did_save must not re-lint other documents when the saved file is not a macro"
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


# ---------------------------------------------------------------------------
# _path_to_uri
# ---------------------------------------------------------------------------

def test_path_to_uri_posix():
    """Posix paths produce a file:// URI with forward slashes."""
    import platform
    if platform.system() == "Windows":
        pytest.skip("Posix path test skipped on Windows")
    uri = srv._path_to_uri("/home/user/project/model.cmd")
    assert uri == "file:///home/user/project/model.cmd"


def test_path_to_uri_windows_style(monkeypatch):
    """Windows-style paths produce a file:///C:/ URI."""
    import os as _os
    monkeypatch.setattr(_os, "name", "nt")
    uri = srv._path_to_uri("C:/Users/ben/project/model.cmd")
    assert uri.startswith("file:///C:")
    assert "model.cmd" in uri


def test_path_to_uri_with_spaces():
    """Spaces in the path are percent-encoded."""
    import platform
    if platform.system() == "Windows":
        pytest.skip("Posix path test skipped on Windows")
    uri = srv._path_to_uri("/home/my user/project/model.cmd")
    assert "%20" in uri


def test_path_to_uri_roundtrip(tmp_path):
    """_path_to_uri followed by _uri_to_path must recover the original path."""
    path = str(tmp_path / "test.cmd")
    uri = srv._path_to_uri(path)
    recovered = srv._uri_to_path(uri)
    # Normalise separators for comparison
    from pathlib import Path
    assert Path(recovered) == Path(path)


# ---------------------------------------------------------------------------
# _get_command_key_at_position
# ---------------------------------------------------------------------------

def test_get_command_key_at_position_builtin_returns_none():
    """Built-in commands should never be identified as macros."""
    srv._schema = Schema.load()
    srv._macro_registry = None
    text = "model create model_name=my_model\n"
    result = srv._get_command_key_at_position(text, 0, "file:///test.cmd")
    assert result is None


def test_get_command_key_at_position_comment_returns_none():
    srv._schema = Schema.load()
    srv._macro_registry = None
    text = "! this is a comment\n"
    result = srv._get_command_key_at_position(text, 0, "file:///test.cmd")
    assert result is None


def test_get_command_key_at_position_blank_returns_none():
    srv._schema = Schema.load()
    srv._macro_registry = None
    text = "\n"
    result = srv._get_command_key_at_position(text, 0, "file:///test.cmd")
    assert result is None


def test_get_command_key_at_position_registry_macro(tmp_path):
    """Cursor on a known macro invocation returns ('registry', key, macro_def)."""
    from adams_cmd_lsp.macros import MacroRegistry, MacroDefinition
    mac_file = tmp_path / "wear.mac"
    mac_file.write_text("!USER_ENTERED_COMMAND cdm wear\n", encoding="utf-8")
    reg = MacroRegistry()
    reg.register(MacroDefinition(
        command="cdm wear",
        parameters={},
        source_file=str(mac_file),
        line=0,
    ))
    srv._schema = Schema.load()
    srv._macro_registry = reg
    text = "cdm wear part_name=p1\n"
    result = srv._get_command_key_at_position(text, 0, "file:///test.cmd")
    assert result is not None
    origin, key, macro_def, origin_range = result
    assert origin == "registry"
    assert key == "cdm wear"
    assert macro_def.source_file == str(mac_file)
    assert origin_range == (0, 0, len("cdm wear"))


def test_get_command_key_at_position_definition_site(tmp_path):
    """Cursor on !USER_ENTERED_COMMAND line returns ('definition_site', ...)."""
    from adams_cmd_lsp.macros import MacroRegistry, MacroDefinition
    reg = MacroRegistry()
    reg.register(MacroDefinition(command="cdm wear", parameters={},
                                 source_file="/wear.mac", line=0))
    srv._schema = Schema.load()
    srv._macro_registry = reg
    text = "!USER_ENTERED_COMMAND cdm wear\n"
    result = srv._get_command_key_at_position(text, 0, "file:///wear.mac")
    assert result is not None
    origin, key, _macro_def, origin_range = result
    assert origin == "definition_site"
    assert key == "cdm wear"
    assert origin_range == (0, len("!USER_ENTERED_COMMAND "), len("!USER_ENTERED_COMMAND cdm wear"))


# ---------------------------------------------------------------------------
# goto_definition
# ---------------------------------------------------------------------------

def _make_mock_doc(text, uri):
    """Return a mock document object for monkeypatching server.workspace."""
    import types as python_types
    doc = python_types.SimpleNamespace(source=text, uri=uri)
    workspace = python_types.SimpleNamespace(
        get_text_document=lambda u: doc,
        folders={},
    )
    mock_srv = python_types.SimpleNamespace(workspace=workspace)
    return mock_srv


def test_goto_definition_builtin_returns_none(monkeypatch):
    """goto_definition returns None for built-in commands."""
    uri = "file:///test.cmd"
    text = "model create model_name=m\n"
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._macro_registry = None
    params = types.DefinitionParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=0, character=0),
    )
    result = srv.goto_definition(params)
    assert result is None


def test_goto_definition_registry_macro(tmp_path, monkeypatch):
    """goto_definition returns a LocationLink pointing to the .mac file."""
    from adams_cmd_lsp.macros import MacroRegistry, MacroDefinition
    mac_file = tmp_path / "wear.mac"
    mac_file.write_text("!USER_ENTERED_COMMAND cdm wear\n", encoding="utf-8")
    reg = MacroRegistry()
    reg.register(MacroDefinition(
        command="cdm wear",
        parameters={},
        source_file=str(mac_file),
        line=0,
    ))
    uri = "file:///test.cmd"
    text = "cdm wear part_name=p1\n"
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._macro_registry = reg
    params = types.DefinitionParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=0, character=0),
    )
    result = srv.goto_definition(params)
    assert result is not None
    assert len(result) == 1
    link = result[0]
    assert link.target_selection_range.start.line == 0
    assert "wear.mac" in link.target_uri
    # originSelectionRange should cover the full "cdm wear" command key
    assert link.origin_selection_range.start.character == 0
    assert link.origin_selection_range.end.character == len("cdm wear")


def test_goto_definition_definition_site_no_refs_returns_none(monkeypatch):
    """goto_definition on a !USER_ENTERED_COMMAND line with no refs returns None."""
    from adams_cmd_lsp.macros import MacroRegistry
    from adams_cmd_lsp.references import MacroIndex
    uri = "file:///wear.mac"
    text = "!USER_ENTERED_COMMAND cdm wear\n"
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._macro_registry = MacroRegistry()
    srv._macro_index = MacroIndex()  # empty — no call sites
    params = types.DefinitionParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=0, character=0),
    )
    result = srv.goto_definition(params)
    assert result is None


def test_goto_definition_definition_site_returns_references(monkeypatch):
    """goto_definition on a !USER_ENTERED_COMMAND line returns LocationLinks to call sites."""
    from adams_cmd_lsp.macros import MacroRegistry
    from adams_cmd_lsp.references import MacroIndex, MacroReference
    uri = "file:///wear.mac"
    text = "!USER_ENTERED_COMMAND cdm wear\n"
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._macro_registry = MacroRegistry()
    srv._macro_index = MacroIndex()
    # Seed a call site in an imaginary caller file
    caller_path = "/caller.cmd"
    srv._macro_index.update_file(caller_path, [
        MacroReference(command_key="cdm wear", line=5, column=0, end_column=8),
    ])
    params = types.DefinitionParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=0, character=0),
    )
    result = srv.goto_definition(params)
    assert result is not None
    assert len(result) == 1
    link = result[0]
    assert "caller" in link.target_uri
    assert link.target_range.start.line == 5
    # originSelectionRange covers "cdm wear" after "!USER_ENTERED_COMMAND "
    assert link.origin_selection_range.start.character == len("!USER_ENTERED_COMMAND ")


def test_goto_definition_inline_macro(monkeypatch):
    """goto_definition for an inline macro create returns a LocationLink to its definition line."""
    from adams_cmd_lsp.macros import MacroRegistry
    uri = "file:///setup.cmd"
    text = (
        "macro create macro_name=cdm_wear user_entered_command=\"cdm wear\"\n"
        "model create model_name=m\n"
        "cdm wear part_name=p1\n"
    )
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._macro_registry = MacroRegistry()  # empty — inline only
    params = types.DefinitionParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=2, character=0),  # cursor on "cdm wear"
    )
    result = srv.goto_definition(params)
    assert result is not None
    assert len(result) == 1
    link = result[0]
    assert link.target_selection_range.start.line == 0  # points to macro create line
    # originSelectionRange should cover "cdm wear" on line 2
    assert link.origin_selection_range.start.line == 2
    assert link.origin_selection_range.start.character == 0
    assert link.origin_selection_range.end.character == len("cdm wear")


def test_goto_definition_indented_command(monkeypatch):
    """origin_selection_range must account for leading whitespace."""
    from adams_cmd_lsp.macros import MacroRegistry, MacroDefinition
    reg = MacroRegistry()
    reg.register(MacroDefinition(
        command="cdm wear", parameters={}, source_file="/wear.mac", line=0,
    ))
    uri = "file:///test.cmd"
    text = "    cdm wear part_name=p1\n"
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._macro_registry = reg
    params = types.DefinitionParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=0, character=4),
    )
    result = srv.goto_definition(params)
    assert result is not None
    assert len(result) == 1
    link = result[0]
    assert link.origin_selection_range.start.character == 4
    assert link.origin_selection_range.end.character == 4 + len("cdm wear")


# ---------------------------------------------------------------------------
# hover
# ---------------------------------------------------------------------------

def test_hover_registry_macro_with_description(monkeypatch):
    """Hover on a registry macro invocation returns Markdown with description."""
    from adams_cmd_lsp.macros import MacroRegistry, MacroDefinition
    reg = MacroRegistry()
    reg.register(MacroDefinition(
        command="cdm wear",
        parameters={},
        source_file="/wear.mac",
        line=0,
        description="Compute wear on a contact pair",
    ))
    uri = "file:///test.cmd"
    text = "cdm wear part_name=p1\n"
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._macro_registry = reg
    params = types.HoverParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=0, character=0),
    )
    result = srv.hover(params)
    assert result is not None
    assert result.contents.kind == types.MarkupKind.Markdown
    assert "# cdm wear" in result.contents.value
    assert "Compute wear on a contact pair" in result.contents.value
    # Range should cover the "cdm wear" span
    assert result.range.start.character == 0
    assert result.range.end.character == len("cdm wear")


def test_hover_registry_macro_no_description(monkeypatch):
    """Hover on a registry macro with no description returns command name only."""
    from adams_cmd_lsp.macros import MacroRegistry, MacroDefinition
    reg = MacroRegistry()
    reg.register(MacroDefinition(
        command="cdm tool",
        parameters={},
        source_file="/tool.mac",
        line=0,
        description=None,
    ))
    uri = "file:///test.cmd"
    text = "cdm tool\n"
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._macro_registry = reg
    params = types.HoverParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=0, character=0),
    )
    result = srv.hover(params)
    assert result is not None
    assert result.contents.value == "# cdm tool"


def test_hover_builtin_command_returns_none(monkeypatch):
    """Hover on a built-in command returns None (defers to JS hover provider)."""
    uri = "file:///test.cmd"
    text = "model create model_name=m\n"
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._macro_registry = None
    params = types.HoverParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=0, character=0),
    )
    result = srv.hover(params)
    assert result is None


def test_hover_non_command_line_returns_none(monkeypatch):
    """Hover on a comment or blank line returns None."""
    uri = "file:///test.cmd"
    text = "! this is a comment\n"
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._macro_registry = None
    params = types.HoverParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=0, character=0),
    )
    result = srv.hover(params)
    assert result is None


def test_hover_definition_site_returns_none(monkeypatch):
    """Hover on a !USER_ENTERED_COMMAND line returns None."""
    from adams_cmd_lsp.macros import MacroRegistry, MacroDefinition
    reg = MacroRegistry()
    reg.register(MacroDefinition(
        command="cdm wear",
        parameters={},
        source_file="/wear.mac",
        line=0,
        description="Some description",
    ))
    uri = "file:///wear.mac"
    text = "!USER_ENTERED_COMMAND cdm wear\n"
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._macro_registry = reg
    params = types.HoverParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=0, character=0),
    )
    result = srv.hover(params)
    assert result is None


def test_hover_inline_macro_with_description(monkeypatch):
    """Hover on an inline macro invocation returns its description."""
    from adams_cmd_lsp.macros import MacroRegistry
    uri = "file:///setup.cmd"
    text = (
        'macro create macro_name=cdm_wear user_entered_command="cdm wear" '
        'help_string="Inline help text"\n'
        "cdm wear part_name=p1\n"
    )
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._macro_registry = MacroRegistry()  # empty — inline only
    params = types.HoverParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=1, character=0),  # cursor on "cdm wear" invocation
    )
    result = srv.hover(params)
    assert result is not None
    assert "# cdm wear" in result.contents.value
    assert "Inline help text" in result.contents.value


# ---------------------------------------------------------------------------
# find_references
# ---------------------------------------------------------------------------

def test_find_references_unknown_command_returns_empty(monkeypatch):
    """find_references returns [] when cursor is on a built-in."""
    from adams_cmd_lsp.references import MacroIndex
    uri = "file:///test.cmd"
    text = "model create model_name=m\n"
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._macro_registry = None
    srv._macro_index = MacroIndex()
    params = types.ReferenceParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=0, character=0),
        context=types.ReferenceContext(include_declaration=False),
    )
    result = srv.find_references(params)
    assert result == []


def test_find_references_returns_indexed_locations(tmp_path, monkeypatch):
    """find_references queries the persistent index and returns all locations."""
    from adams_cmd_lsp.macros import MacroRegistry, MacroDefinition
    from adams_cmd_lsp.references import MacroIndex, MacroReference

    mac_file = tmp_path / "wear.mac"
    mac_file.write_text("!USER_ENTERED_COMMAND cdm wear\n", encoding="utf-8")
    reg = MacroRegistry()
    reg.register(MacroDefinition(command="cdm wear", parameters={},
                                 source_file=str(mac_file), line=0))

    idx = MacroIndex()
    ref_a = MacroReference(command_key="cdm wear", line=2, column=0, end_column=8)
    ref_b = MacroReference(command_key="cdm wear", line=5, column=0, end_column=8)
    idx.update_file(str(tmp_path / "a.cmd"), [ref_a])
    idx.update_file(str(tmp_path / "b.cmd"), [ref_b])

    uri = "file:///wear.mac"
    text = "!USER_ENTERED_COMMAND cdm wear\n"
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._macro_registry = reg
    srv._macro_index = idx

    params = types.ReferenceParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=0, character=0),
        context=types.ReferenceContext(include_declaration=False),
    )
    result = srv.find_references(params)
    assert len(result) == 2
    lines = {loc.range.start.line for loc in result}
    assert 2 in lines
    assert 5 in lines


def test_find_references_include_declaration(tmp_path, monkeypatch):
    """include_declaration=True adds the definition site to the results."""
    from adams_cmd_lsp.macros import MacroRegistry, MacroDefinition
    from adams_cmd_lsp.references import MacroIndex, MacroReference

    mac_file = tmp_path / "wear.mac"
    mac_file.write_text("!USER_ENTERED_COMMAND cdm wear\n", encoding="utf-8")
    reg = MacroRegistry()
    reg.register(MacroDefinition(command="cdm wear", parameters={},
                                 source_file=str(mac_file), line=0))

    idx = MacroIndex()
    ref = MacroReference(command_key="cdm wear", line=1, column=0, end_column=8)
    idx.update_file(str(tmp_path / "use.cmd"), [ref])

    uri = "file:///wear.mac"
    text = "!USER_ENTERED_COMMAND cdm wear\n"
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._macro_registry = reg
    srv._macro_index = idx

    params = types.ReferenceParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=0, character=0),
        context=types.ReferenceContext(include_declaration=True),
    )
    result = srv.find_references(params)
    # Should include both the usage (line 1) and the declaration (line 0 in mac_file)
    assert len(result) == 2
    decl_locs = [loc for loc in result if "wear.mac" in loc.uri]
    assert len(decl_locs) == 1
    assert decl_locs[0].range.start.line == 0


# ---------------------------------------------------------------------------
# MacroRegistry.unregister_by_file
# ---------------------------------------------------------------------------

def test_unregister_by_file_removes_entry(tmp_path):
    """unregister_by_file must remove all commands registered from the given file."""
    from adams_cmd_lsp.macros import MacroRegistry, MacroDefinition

    reg = MacroRegistry()
    reg.register(MacroDefinition(command="cdm wear", parameters={}, source_file="/wear.mac"))
    reg.register(MacroDefinition(command="cdm other", parameters={}, source_file="/other.mac"))

    reg.unregister_by_file("/wear.mac")

    assert not reg.has_command("cdm wear"), "Command from deleted file should be removed"
    assert reg.has_command("cdm other"), "Command from other file should remain"


def test_unregister_by_file_clears_mtime(tmp_path):
    """unregister_by_file must clear the mtime cache so the file is re-parsed next scan."""
    from adams_cmd_lsp.macros import MacroRegistry, MacroDefinition

    mac_path = tmp_path / "wear.mac"
    mac_path.write_text("!USER_ENTERED_COMMAND cdm wear\n", encoding="utf-8")

    reg = MacroRegistry()
    reg.register(MacroDefinition(command="cdm wear", parameters={}, source_file=str(mac_path)))
    reg._record_mtime(str(mac_path))
    assert not reg.needs_refresh(str(mac_path)), "Precondition: mtime is cached"

    reg.unregister_by_file(str(mac_path))

    assert reg.needs_refresh(str(mac_path)), "After unregister_by_file mtime should be cleared"


def test_unregister_by_file_multiple_commands_same_file(tmp_path):
    """unregister_by_file removes ALL commands from a file (edge case: multi-command files)."""
    from adams_cmd_lsp.macros import MacroRegistry, MacroDefinition

    reg = MacroRegistry()
    reg.register(MacroDefinition(command="cmd one", parameters={}, source_file="/multi.mac"))
    reg.register(MacroDefinition(command="cmd two", parameters={}, source_file="/multi.mac"))
    reg.register(MacroDefinition(command="cmd three", parameters={}, source_file="/other.mac"))

    reg.unregister_by_file("/multi.mac")

    assert not reg.has_command("cmd one")
    assert not reg.has_command("cmd two")
    assert reg.has_command("cmd three"), "Command from other file must remain"


def test_unregister_by_file_noop_when_not_registered():
    """unregister_by_file is a no-op when the path is not in the registry."""
    from adams_cmd_lsp.macros import MacroRegistry

    reg = MacroRegistry()
    # Must not raise when the path is not registered
    reg.unregister_by_file("/nonexistent.mac")
    assert len(reg) == 0


def test_unregister_by_file_normalizes_path_separators():
    """unregister_by_file must match paths regardless of separator style.

    On Windows, source_file values from workspace scan use backslashes while
    paths from _uri_to_path() use forward slashes. Both must compare equal.
    """
    import platform
    if platform.system() != "Windows":
        pytest.skip("Separator normalization test is Windows-specific")

    from adams_cmd_lsp.macros import MacroRegistry, MacroDefinition

    reg = MacroRegistry()
    # Register with OS-native backslash path (as scan_macro_files would)
    reg.register(MacroDefinition(
        command="cdm sep_test",
        parameters={},
        source_file=r"C:\Users\project\tool.mac",
    ))

    # Unregister using forward-slash path (as _uri_to_path returns)
    reg.unregister_by_file("C:/Users/project/tool.mac")

    assert not reg.has_command("cdm sep_test"), (
        "unregister_by_file must remove entry when paths differ only in separator style"
    )


# ---------------------------------------------------------------------------
# did_change_configuration
# ---------------------------------------------------------------------------

def _make_mock_server_with_docs(docs=None):
    """Return a mock server with a workspace containing the given open documents.

    *docs* is a dict ``{uri: text}``.  Each value is wrapped in a SimpleNamespace
    with a ``.source`` attribute, matching the pygls TextDocument interface.
    """
    import types as python_types
    docs = docs or {}
    text_docs = {
        uri: python_types.SimpleNamespace(source=text)
        for uri, text in docs.items()
    }
    mock_workspace = python_types.SimpleNamespace(
        text_documents=text_docs,
        folders={},
    )
    return python_types.SimpleNamespace(workspace=mock_workspace)


def test_did_change_configuration_updates_scan_flag(monkeypatch):
    """did_change_configuration must update _scan_workspace_macros from settings."""
    monkeypatch.setattr(srv, "server", _make_mock_server_with_docs())
    srv._scan_workspace_macros = False
    srv._workspace_roots = []

    params = types.DidChangeConfigurationParams(
        settings={"msc-adams": {"linter": {"scanWorkspaceMacros": True}}}
    )
    srv.did_change_configuration(params)

    assert srv._scan_workspace_macros is True


def test_did_change_configuration_updates_macro_patterns(monkeypatch):
    """did_change_configuration must update _macro_patterns from settings."""
    monkeypatch.setattr(srv, "server", _make_mock_server_with_docs())
    srv._macro_patterns = ["**/*.mac"]
    srv._scan_workspace_macros = False
    srv._workspace_roots = []

    params = types.DidChangeConfigurationParams(
        settings={"msc-adams": {"linter": {"macroPaths": ["macros/*.mac", "tools/*.mac"]}}}
    )
    srv.did_change_configuration(params)

    assert srv._macro_patterns == ["macros/*.mac", "tools/*.mac"]


def test_did_change_configuration_updates_ignore_patterns(monkeypatch):
    """did_change_configuration must update _macro_ignore_patterns from settings."""
    monkeypatch.setattr(srv, "server", _make_mock_server_with_docs())
    srv._macro_ignore_patterns = []
    srv._scan_workspace_macros = False
    srv._workspace_roots = []

    params = types.DidChangeConfigurationParams(
        settings={"msc-adams": {"linter": {"macroIgnorePaths": ["**/test/**"]}}}
    )
    srv.did_change_configuration(params)

    assert srv._macro_ignore_patterns == ["**/test/**"]


def test_did_change_configuration_updates_show_macro_hint(monkeypatch):
    """did_change_configuration must update _macro_show_hint from settings."""
    monkeypatch.setattr(srv, "server", _make_mock_server_with_docs())
    srv._macro_show_hint = True
    srv._scan_workspace_macros = False
    srv._workspace_roots = []

    params = types.DidChangeConfigurationParams(
        settings={"msc-adams": {"linter": {"showMacroHint": False}}}
    )
    srv.did_change_configuration(params)

    assert srv._macro_show_hint is False


def test_did_change_configuration_triggers_rescan_when_scan_enabled(tmp_path, monkeypatch):
    """Enabling scanWorkspaceMacros via config should trigger a workspace re-scan."""
    from adams_cmd_lsp.macros import MacroRegistry

    mac_file = tmp_path / "new_tool.mac"
    mac_file.write_text("!USER_ENTERED_COMMAND cdm config_scan\n", encoding="utf-8")

    monkeypatch.setattr(srv, "server", _make_mock_server_with_docs())
    srv._macro_registry = MacroRegistry()
    srv._scan_workspace_macros = False
    srv._macro_patterns = ["**/*.mac"]
    srv._macro_ignore_patterns = []
    srv._workspace_roots = [str(tmp_path)]

    params = types.DidChangeConfigurationParams(
        settings={"msc-adams": {"linter": {"scanWorkspaceMacros": True}}}
    )
    srv.did_change_configuration(params)

    assert srv._macro_registry.has_command("cdm config_scan"), (
        "Enabling scanWorkspaceMacros should trigger a workspace scan"
    )


def test_did_change_configuration_no_rescan_when_scan_already_enabled_no_pattern_change(
    tmp_path, monkeypatch
):
    """No rescan when scan was already on and patterns haven't changed."""
    from adams_cmd_lsp.macros import MacroRegistry

    rescan_calls = []
    original_scan = srv.scan_macro_files

    def counting_scan(*args, **kwargs):
        rescan_calls.append(1)
        return original_scan(*args, **kwargs)

    monkeypatch.setattr(srv, "scan_macro_files", counting_scan)
    monkeypatch.setattr(srv, "server", _make_mock_server_with_docs())
    srv._macro_registry = MacroRegistry()
    srv._scan_workspace_macros = True   # already enabled
    srv._macro_patterns = ["**/*.mac"]
    srv._macro_ignore_patterns = []
    srv._workspace_roots = [str(tmp_path)]

    params = types.DidChangeConfigurationParams(
        settings={"msc-adams": {"linter": {"showMacroHint": False}}}  # unrelated change
    )
    srv.did_change_configuration(params)

    assert len(rescan_calls) == 0, "No rescan should occur when scan was already on and patterns didn't change"


def test_did_change_configuration_revalidates_open_docs(monkeypatch):
    """did_change_configuration must re-lint all open documents after the update."""
    from adams_cmd_lsp.macros import MacroRegistry

    validated_uris = []

    def mock_validate(uri, text):
        validated_uris.append(uri)

    monkeypatch.setattr(srv, "_validate_document", mock_validate)
    monkeypatch.setattr(
        srv, "server",
        _make_mock_server_with_docs({
            "file:///a.cmd": "model create\n",
            "file:///b.cmd": "marker create\n",
        })
    )
    srv._macro_registry = MacroRegistry()
    srv._scan_workspace_macros = False
    srv._workspace_roots = []

    params = types.DidChangeConfigurationParams(
        settings={"msc-adams": {"linter": {"showMacroHint": False}}}
    )
    srv.did_change_configuration(params)

    assert set(validated_uris) == {"file:///a.cmd", "file:///b.cmd"}, (
        "did_change_configuration must re-validate all open documents"
    )


def test_did_change_configuration_empty_settings_is_noop(monkeypatch):
    """did_change_configuration with empty settings payload must not crash."""
    monkeypatch.setattr(srv, "server", _make_mock_server_with_docs())
    srv._scan_workspace_macros = False
    srv._workspace_roots = []

    # Should not raise
    srv.did_change_configuration(types.DidChangeConfigurationParams(settings={}))
    srv.did_change_configuration(types.DidChangeConfigurationParams(settings=None))


def test_did_change_configuration_empty_macro_paths_falls_back_to_default(monkeypatch):
    """Setting macroPaths to [] in config must fall back to DEFAULT_MACRO_PATTERNS."""
    from adams_cmd_lsp.macros import DEFAULT_MACRO_PATTERNS

    monkeypatch.setattr(srv, "server", _make_mock_server_with_docs())
    srv._macro_patterns = ["custom/*.mac"]
    srv._scan_workspace_macros = False
    srv._workspace_roots = []

    params = types.DidChangeConfigurationParams(
        settings={"msc-adams": {"linter": {"macroPaths": []}}}
    )
    srv.did_change_configuration(params)

    assert srv._macro_patterns == DEFAULT_MACRO_PATTERNS, (
        "Empty macroPaths list should fall back to DEFAULT_MACRO_PATTERNS, not leave old value"
    )


# ---------------------------------------------------------------------------
# did_change_watched_files
# ---------------------------------------------------------------------------

def test_did_change_watched_files_created_registers_macro(tmp_path, monkeypatch):
    """A Created file event must parse and register the macro."""
    from adams_cmd_lsp.macros import MacroRegistry

    mac_path = tmp_path / "tool.mac"
    mac_path.write_text("!USER_ENTERED_COMMAND cdm watched_create\n", encoding="utf-8")

    monkeypatch.setattr(srv, "server", _make_mock_server_with_docs())
    srv._macro_registry = MacroRegistry()

    params = types.DidChangeWatchedFilesParams(
        changes=[
            types.FileEvent(uri=mac_path.as_uri(), type=types.FileChangeType.Created),
        ]
    )
    srv.did_change_watched_files(params)

    assert srv._macro_registry.has_command("cdm watched_create"), (
        "Created file event should register the macro command"
    )


def test_did_change_watched_files_changed_updates_macro(tmp_path, monkeypatch):
    """A Changed file event must re-parse and update the macro registry."""
    from adams_cmd_lsp.macros import MacroRegistry, MacroDefinition

    mac_path = tmp_path / "tool.mac"
    mac_path.write_text("!USER_ENTERED_COMMAND cdm watched_updated\n", encoding="utf-8")

    reg = MacroRegistry()
    reg.register(MacroDefinition(command="cdm watched_old", parameters={},
                                 source_file=str(mac_path)))
    monkeypatch.setattr(srv, "server", _make_mock_server_with_docs())
    srv._macro_registry = reg

    params = types.DidChangeWatchedFilesParams(
        changes=[
            types.FileEvent(uri=mac_path.as_uri(), type=types.FileChangeType.Changed),
        ]
    )
    srv.did_change_watched_files(params)

    assert srv._macro_registry.has_command("cdm watched_updated"), (
        "Changed file event should register the new command"
    )
    # Old command from this file should be removed by unregister_by_file
    assert not srv._macro_registry.has_command("cdm watched_old"), (
        "Old command from a changed file should be removed"
    )


def test_did_change_watched_files_deleted_removes_macro(tmp_path, monkeypatch):
    """A Deleted file event must remove the macro from the registry."""
    from adams_cmd_lsp.macros import MacroRegistry, MacroDefinition

    mac_path = tmp_path / "gone.mac"

    reg = MacroRegistry()
    reg.register(MacroDefinition(command="cdm deleted_cmd", parameters={},
                                 source_file=str(mac_path)))
    assert reg.has_command("cdm deleted_cmd"), "Precondition: macro is registered"

    monkeypatch.setattr(srv, "server", _make_mock_server_with_docs())
    srv._macro_registry = reg

    params = types.DidChangeWatchedFilesParams(
        changes=[
            types.FileEvent(uri=mac_path.as_uri(), type=types.FileChangeType.Deleted),
        ]
    )
    srv.did_change_watched_files(params)

    assert not srv._macro_registry.has_command("cdm deleted_cmd"), (
        "Deleted file event should remove the macro command"
    )


def test_did_change_watched_files_revalidates_even_when_file_unreadable(tmp_path, monkeypatch):
    """Re-validation must fire even when the new file content cannot be read.

    When a Changed event fires but the file on disk is gone/unreadable, the
    handler still calls unregister_by_file (which modifies the registry) and
    must therefore re-validate open documents even though changed is set before
    the OSError is raised.
    """
    from adams_cmd_lsp.macros import MacroRegistry, MacroDefinition

    validated_uris = []
    monkeypatch.setattr(srv, "_validate_document", lambda u, t: validated_uris.append(u))

    mac_path = tmp_path / "gone.mac"
    # File does NOT exist on disk — Path.read_text() will raise OSError
    reg = MacroRegistry()
    reg.register(MacroDefinition(command="cdm stale", parameters={},
                                 source_file=str(mac_path)))
    monkeypatch.setattr(
        srv, "server",
        _make_mock_server_with_docs({"file:///open.cmd": "cdm stale\n"}),
    )
    srv._macro_registry = reg

    params = types.DidChangeWatchedFilesParams(
        changes=[
            types.FileEvent(uri=mac_path.as_uri(), type=types.FileChangeType.Changed),
        ]
    )
    srv.did_change_watched_files(params)

    assert not reg.has_command("cdm stale"), (
        "unregister_by_file must still remove the stale entry even when file read fails"
    )
    assert "file:///open.cmd" in validated_uris, (
        "Re-validation must fire even when the new file content cannot be read"
    )


def test_did_change_watched_files_no_registry_is_noop(tmp_path, monkeypatch):
    """did_change_watched_files must be a no-op when _macro_registry is None."""
    srv._macro_registry = None
    mac_path = tmp_path / "tool.mac"
    mac_path.write_text("!USER_ENTERED_COMMAND cdm some_cmd\n", encoding="utf-8")
    # Must not raise
    params = types.DidChangeWatchedFilesParams(
        changes=[
            types.FileEvent(uri=mac_path.as_uri(), type=types.FileChangeType.Created),
        ]
    )
    srv.did_change_watched_files(params)


def test_did_change_watched_files_revalidates_open_docs(tmp_path, monkeypatch):
    """did_change_watched_files must re-lint open documents when registry changes."""
    from adams_cmd_lsp.macros import MacroRegistry

    validated_uris = []

    def mock_validate(uri, text):
        validated_uris.append(uri)

    mac_path = tmp_path / "tool.mac"
    mac_path.write_text("!USER_ENTERED_COMMAND cdm revalidate\n", encoding="utf-8")

    monkeypatch.setattr(srv, "_validate_document", mock_validate)
    monkeypatch.setattr(
        srv, "server",
        _make_mock_server_with_docs({"file:///consumer.cmd": "cdm revalidate\n"}),
    )
    srv._macro_registry = MacroRegistry()

    params = types.DidChangeWatchedFilesParams(
        changes=[
            types.FileEvent(uri=mac_path.as_uri(), type=types.FileChangeType.Created),
        ]
    )
    srv.did_change_watched_files(params)

    assert "file:///consumer.cmd" in validated_uris, (
        "did_change_watched_files should re-validate open documents after a registry change"
    )


def test_did_change_watched_files_changed_removes_command_when_no_user_entered_command(
    tmp_path, monkeypatch
):
    """If an updated .mac file no longer has !USER_ENTERED_COMMAND, its entry must be removed."""
    from adams_cmd_lsp.macros import MacroRegistry, MacroDefinition

    mac_path = tmp_path / "tool.mac"
    # Write the file WITHOUT a USER_ENTERED_COMMAND header
    mac_path.write_text("! plain macro with no command header\npart create\n", encoding="utf-8")

    reg = MacroRegistry()
    reg.register(MacroDefinition(command="cdm stale", parameters={},
                                 source_file=str(mac_path)))
    assert reg.has_command("cdm stale"), "Precondition: stale entry exists"

    monkeypatch.setattr(srv, "server", _make_mock_server_with_docs())
    srv._macro_registry = reg

    params = types.DidChangeWatchedFilesParams(
        changes=[
            types.FileEvent(uri=mac_path.as_uri(), type=types.FileChangeType.Changed),
        ]
    )
    srv.did_change_watched_files(params)

    assert not reg.has_command("cdm stale"), (
        "Stale entry should be removed when the file no longer has !USER_ENTERED_COMMAND"
    )


def test_find_references_no_references_in_index(tmp_path, monkeypatch):
    """find_references returns empty list when no invocations are indexed."""
    from adams_cmd_lsp.macros import MacroRegistry, MacroDefinition
    from adams_cmd_lsp.references import MacroIndex

    mac_file = tmp_path / "wear.mac"
    mac_file.write_text("!USER_ENTERED_COMMAND cdm wear\n", encoding="utf-8")
    reg = MacroRegistry()
    reg.register(MacroDefinition(command="cdm wear", parameters={},
                                 source_file=str(mac_file), line=0))

    uri = "file:///wear.mac"
    text = "!USER_ENTERED_COMMAND cdm wear\n"
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._macro_registry = reg
    srv._macro_index = MacroIndex()  # empty index

    params = types.ReferenceParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=0, character=0),
        context=types.ReferenceContext(include_declaration=False),
    )
    result = srv.find_references(params)
    assert result == []


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


# ---------------------------------------------------------------------------
# on_initialized — _build_index_for_workspace call-count regression
# ---------------------------------------------------------------------------

def test_on_initialized_calls_build_index_exactly_once_scan_disabled(tmp_path, monkeypatch):
    """_build_index_for_workspace must be called exactly once when scan is OFF."""
    from adams_cmd_lsp.macros import MacroRegistry

    call_count = []

    def fake_build(paths):
        call_count.append(paths)

    monkeypatch.setattr(srv, "server", _make_mock_server(tmp_path))
    monkeypatch.setattr(srv, "_build_index_for_workspace", fake_build)
    monkeypatch.setattr(srv, "_macro_registry", MacroRegistry())
    monkeypatch.setattr(srv, "_scan_workspace_macros", False)
    monkeypatch.setattr(srv, "_macro_patterns", ["**/*.mac"])
    monkeypatch.setattr(srv, "_macro_ignore_patterns", [])
    monkeypatch.setattr(srv, "_workspace_roots", [])

    srv.on_initialized(types.InitializedParams())

    assert len(call_count) == 1, (
        f"_build_index_for_workspace should be called exactly once, got {len(call_count)}"
    )
    from pathlib import Path
    assert [Path(p) for p in call_count[0]] == [tmp_path], (
        f"_build_index_for_workspace should receive the workspace path, got {call_count[0]}"
    )


def test_on_initialized_calls_build_index_exactly_once_scan_enabled(tmp_path, monkeypatch):
    """_build_index_for_workspace must be called exactly once when scan is ON."""
    from adams_cmd_lsp.macros import MacroRegistry

    call_count = []

    def fake_build(paths):
        call_count.append(paths)

    monkeypatch.setattr(srv, "server", _make_mock_server(tmp_path))
    monkeypatch.setattr(srv, "_build_index_for_workspace", fake_build)
    monkeypatch.setattr(srv, "_macro_registry", MacroRegistry())
    monkeypatch.setattr(srv, "_scan_workspace_macros", True)
    monkeypatch.setattr(srv, "_macro_patterns", ["**/*.mac"])
    monkeypatch.setattr(srv, "_macro_ignore_patterns", [])
    monkeypatch.setattr(srv, "_workspace_roots", [])

    srv.on_initialized(types.InitializedParams())

    assert len(call_count) == 1, (
        f"_build_index_for_workspace should be called exactly once, got {len(call_count)}"
    )
    from pathlib import Path
    assert [Path(p) for p in call_count[0]] == [tmp_path], (
        f"_build_index_for_workspace should receive the workspace path, got {call_count[0]}"
    )


# ---------------------------------------------------------------------------
# main() — _macro_index reinitialization regression
# ---------------------------------------------------------------------------

def test_main_reinitializes_macro_index(monkeypatch):
    """main() must replace _macro_index with a fresh MacroIndex, discarding stale data.

    All module-level globals mutated by main() are restored through monkeypatch so that
    this test does not leak state into subsequent tests.
    """
    import sys
    from adams_cmd_lsp.references import MacroIndex, MacroReference
    from adams_cmd_lsp.macros import MacroRegistry, DEFAULT_MACRO_PATTERNS

    # Capture originals via monkeypatch so teardown restores them automatically
    monkeypatch.setattr(srv, "_schema", srv._schema)
    monkeypatch.setattr(srv, "_macro_registry", srv._macro_registry)
    monkeypatch.setattr(srv, "_macro_index", MacroIndex())
    monkeypatch.setattr(srv, "_macro_patterns", list(srv._macro_patterns))
    monkeypatch.setattr(srv, "_macro_ignore_patterns", list(srv._macro_ignore_patterns))
    monkeypatch.setattr(srv, "_scan_workspace_macros", srv._scan_workspace_macros)
    monkeypatch.setattr(srv, "_macro_show_hint", srv._macro_show_hint)
    monkeypatch.setattr(srv, "_workspace_roots", list(srv._workspace_roots))

    # Populate the index with stale data
    stale_ref = MacroReference(command_key="stale cmd", line=0, column=0, end_column=9)
    srv._macro_index.update_file("/old/file.cmd", [stale_ref])
    assert srv._macro_index.total_references() > 0, "Precondition: index has stale data"

    # Stub out server startup and argparse argv so main() returns without blocking
    monkeypatch.setattr(sys, "argv", ["adams-cmd-lsp"])
    monkeypatch.setattr(srv.server, "start_io", lambda: None)

    srv.main()

    assert isinstance(srv._macro_index, MacroIndex), "_macro_index should be a MacroIndex"
    assert srv._macro_index.total_references() == 0, (
        "main() should reset _macro_index to an empty state"
    )


# ---------------------------------------------------------------------------
# _update_doc_cache / _get_doc_cache
# ---------------------------------------------------------------------------

def test_update_doc_cache_populates_symbols():
    """_update_doc_cache must populate the cache with a SymbolTable."""
    from adams_cmd_lsp.symbols import SymbolTable
    srv._schema = Schema.load()
    uri = "file:///test_cache.cmd"
    srv._doc_cache.pop(uri, None)
    text = "marker create marker_name = .m.p.mkr1 location = 0,0,0\n"
    srv._update_doc_cache(uri, text)
    cached = srv._doc_cache.get(uri)
    assert cached is not None
    statements, symbols = cached
    assert isinstance(symbols, SymbolTable)
    assert symbols.has(".m.p.mkr1")


def test_update_doc_cache_noop_without_schema():
    """_update_doc_cache must be a no-op when _schema is None."""
    srv._schema = None
    uri = "file:///nocache.cmd"
    srv._doc_cache.pop(uri, None)
    srv._update_doc_cache(uri, "model create model_name=m\n")
    assert uri not in srv._doc_cache


def test_get_doc_cache_builds_on_demand():
    """_get_doc_cache must build and return the cache when text is supplied."""
    srv._schema = Schema.load()
    uri = "file:///demand.cmd"
    srv._doc_cache.pop(uri, None)
    text = "part create rigid_body name_and_position part_name = .m.P1\n"
    statements, symbols = srv._get_doc_cache(uri, text)
    assert statements is not None
    assert symbols is not None
    assert symbols.has(".m.P1")


def test_get_doc_cache_returns_none_without_text():
    """_get_doc_cache returns (None, None) when no text is supplied and cache is empty."""
    srv._schema = Schema.load()
    uri = "file:///no_text.cmd"
    srv._doc_cache.pop(uri, None)
    stmts, syms = srv._get_doc_cache(uri)
    assert stmts is None
    assert syms is None


# ---------------------------------------------------------------------------
# _get_object_at_position
# ---------------------------------------------------------------------------

def test_get_object_at_position_on_definition():
    """Cursor on a new_object arg value must return 'definition'."""
    srv._schema = Schema.load()
    text = "marker create marker_name = .m.p.mkr1 location = 0,0,0\n"
    from adams_cmd_lsp.parser import parse as _parse
    from adams_cmd_lsp.object_index import _resolve_command_keys
    from adams_cmd_lsp.symbols import build_symbol_table
    stmts = _parse(text)
    _resolve_command_keys(stmts, srv._schema)
    symbols = build_symbol_table(stmts, srv._schema)
    # ".m.p.mkr1" appears at some column on line 0 — scan the text to find it
    col = text.index(".m.p.mkr1")
    result = srv._get_object_at_position(stmts, srv._schema, symbols, 0, col)
    assert result is not None
    kind, name, v_line, v_col, v_end_col = result
    assert kind == "definition"
    assert name == ".m.p.mkr1"


def test_get_object_at_position_on_reference():
    """Cursor on an existing_object arg value must return 'reference'."""
    srv._schema = Schema.load()
    text = "constraint create joint fixed joint_name=.m.f1 i_marker=.m.p.mkr1 j_marker=.m.ground.cm\n"
    from adams_cmd_lsp.parser import parse as _parse
    from adams_cmd_lsp.object_index import _resolve_command_keys
    from adams_cmd_lsp.symbols import build_symbol_table
    stmts = _parse(text)
    _resolve_command_keys(stmts, srv._schema)
    symbols = build_symbol_table(stmts, srv._schema)
    col = text.index(".m.p.mkr1")
    result = srv._get_object_at_position(stmts, srv._schema, symbols, 0, col)
    assert result is not None
    kind, name, v_line, v_col, v_end_col = result
    assert kind == "reference"
    assert name == ".m.p.mkr1"


def test_get_object_at_position_out_of_range():
    """Cursor not on any arg value must return None."""
    srv._schema = Schema.load()
    text = "marker create marker_name = .m.p.mkr1 location = 0,0,0\n"
    from adams_cmd_lsp.parser import parse as _parse
    from adams_cmd_lsp.object_index import _resolve_command_keys
    from adams_cmd_lsp.symbols import build_symbol_table
    stmts = _parse(text)
    _resolve_command_keys(stmts, srv._schema)
    symbols = build_symbol_table(stmts, srv._schema)
    # Column 0 is on "marker" — the command keyword, not a value
    result = srv._get_object_at_position(stmts, srv._schema, symbols, 0, 0)
    assert result is None


def test_get_object_at_position_skips_eval():
    """Cursor on an eval() value must return None."""
    srv._schema = Schema.load()
    text = "marker create marker_name = (eval(.m.p // '.cm')) location = 0,0,0\n"
    from adams_cmd_lsp.parser import parse as _parse
    from adams_cmd_lsp.object_index import _resolve_command_keys
    from adams_cmd_lsp.symbols import build_symbol_table
    stmts = _parse(text)
    _resolve_command_keys(stmts, srv._schema)
    symbols = build_symbol_table(stmts, srv._schema)
    col = text.index("(eval")
    result = srv._get_object_at_position(stmts, srv._schema, symbols, 0, col)
    assert result is None


# ---------------------------------------------------------------------------
# goto_definition — Adams object navigation
# ---------------------------------------------------------------------------

def test_goto_definition_jumps_to_marker_definition(monkeypatch):
    """Ctrl+clicking a marker reference must navigate to the create command."""
    from adams_cmd_lsp.macros import MacroRegistry
    from adams_cmd_lsp.object_index import ObjectIndex
    uri = "file:///model.cmd"
    text = (
        "marker create marker_name = .m.p.mkr1 location = 0,0,0\n"
        "constraint create joint fixed joint_name=.m.f1 "
        "i_marker=.m.p.mkr1 j_marker=.m.ground.cm\n"
    )
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._macro_registry = MacroRegistry()
    srv._object_index = ObjectIndex()
    srv._doc_cache.pop(uri, None)

    # Cursor on ".m.p.mkr1" in the i_marker= argument on line 1
    col = text.splitlines()[1].index(".m.p.mkr1")
    params = types.DefinitionParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=1, character=col),
    )
    result = srv.goto_definition(params)
    assert result is not None, "Should navigate to the marker definition"
    assert len(result) == 1
    link = result[0]
    assert link.target_uri == uri
    assert link.target_selection_range.start.line == 0  # marker create is on line 0
    # originSelectionRange must cover the value text
    assert link.origin_selection_range.start.line == 1
    assert link.origin_selection_range.start.character == col


def test_goto_definition_leaf_name_fallback(monkeypatch):
    """Navigating from a leaf-only reference must resolve via leaf-name lookup."""
    from adams_cmd_lsp.macros import MacroRegistry
    from adams_cmd_lsp.object_index import ObjectIndex
    uri = "file:///model.cmd"
    # leaf name "mkr1" is used as i_marker (without full path)
    text = (
        "marker create marker_name = .m.p.mkr1 location = 0,0,0\n"
        "constraint create joint fixed joint_name=.m.f1 "
        "i_marker=mkr1 j_marker=.m.ground.cm\n"
    )
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._macro_registry = MacroRegistry()
    srv._object_index = ObjectIndex()
    srv._doc_cache.pop(uri, None)

    col = text.splitlines()[1].index("mkr1")
    params = types.DefinitionParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=1, character=col),
    )
    result = srv.goto_definition(params)
    assert result is not None, "Leaf-name lookup must resolve mkr1 to .m.p.mkr1 definition"
    link = result[0]
    assert link.target_selection_range.start.line == 0


def test_goto_definition_on_definition_no_refs_returns_none(monkeypatch):
    """Ctrl+clicking a definition with no references must return None."""
    from adams_cmd_lsp.macros import MacroRegistry
    from adams_cmd_lsp.object_index import ObjectIndex
    uri = "file:///model.cmd"
    # Only a definition, no existing_object references to it
    text = "marker create marker_name = .m.p.mkr1 location = 0,0,0\n"
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._macro_registry = MacroRegistry()
    srv._object_index = ObjectIndex()
    srv._doc_cache.pop(uri, None)

    col = text.index(".m.p.mkr1")
    params = types.DefinitionParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=0, character=col),
    )
    result = srv.goto_definition(params)
    assert result is None, "No references exist, so goto_definition should return None"


def test_goto_definition_on_definition_returns_references(monkeypatch):
    """Ctrl+clicking a definition with references must navigate to those references."""
    from adams_cmd_lsp.macros import MacroRegistry
    from adams_cmd_lsp.object_index import ObjectIndex
    uri = "file:///model.cmd"
    text = (
        "marker create marker_name = .m.p.mkr1 location = 0,0,0\n"
        "constraint create joint fixed joint_name=.m.f1 "
        "i_marker=.m.p.mkr1 j_marker=.m.ground.cm\n"
    )
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._macro_registry = MacroRegistry()
    srv._object_index = ObjectIndex()
    srv._doc_cache.pop(uri, None)

    # Cursor on the definition value (marker_name= arg on line 0)
    col = text.splitlines()[0].index(".m.p.mkr1")
    params = types.DefinitionParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=0, character=col),
    )
    result = srv.goto_definition(params)
    assert result is not None, "Definition with references should navigate to them"
    target_lines = [link.target_range.start.line for link in result]
    # The i_marker reference is on line 1; definition line (0) must not appear
    assert 1 in target_lines, f"Expected reference on line 1, got: {target_lines}"
    assert 0 not in target_lines, "Definition site must not appear in reference results"


def test_goto_definition_on_definition_cross_file_references(monkeypatch, tmp_path):
    """Ctrl+clicking a definition must include cross-file references from _object_index."""
    from adams_cmd_lsp.macros import MacroRegistry
    from adams_cmd_lsp.object_index import ObjectIndex, IndexedReference

    uri = "file:///file_a.cmd"
    # Current file: only the definition
    text_a = "marker create marker_name = .m.p.mkr1 location = 0,0,0\n"

    # Other file: references the marker
    other_path = str(tmp_path / "file_b.cmd")
    (tmp_path / "file_b.cmd").write_text(
        "constraint create joint fixed joint_name=.m.f1 "
        "i_marker=.m.p.mkr1 j_marker=.m.ground.cm\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(srv, "server", _make_mock_doc(text_a, uri))
    srv._schema = Schema.load()
    srv._macro_registry = MacroRegistry()
    srv._object_index = ObjectIndex()
    srv._object_index.update_file(
        other_path,
        [],
        [IndexedReference(
            name=".m.p.mkr1", object_type="Marker",
            line=0, column=0, end_column=10,
            source_file=other_path,
        )],
    )
    srv._doc_cache.pop(uri, None)

    col = text_a.index(".m.p.mkr1")
    params = types.DefinitionParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=0, character=col),
    )
    result = srv.goto_definition(params)
    assert result is not None, "Expected cross-file reference LocationLink"
    cross_uris = [link.target_uri for link in result if "file_b" in link.target_uri]
    assert len(cross_uris) >= 1, f"Expected a LocationLink pointing to file_b, got: {[l.target_uri for l in result]}"


# ---------------------------------------------------------------------------
# find_references — Adams object navigation
# ---------------------------------------------------------------------------

def test_find_references_finds_marker_usages(monkeypatch):
    """find_references on a marker create must return all usage sites."""
    from adams_cmd_lsp.macros import MacroRegistry
    from adams_cmd_lsp.references import MacroIndex
    from adams_cmd_lsp.object_index import ObjectIndex
    uri = "file:///model.cmd"
    text = (
        "marker create marker_name = .m.p.mkr1 location = 0,0,0\n"
        "constraint create joint fixed joint_name=.m.f1 "
        "i_marker=.m.p.mkr1 j_marker=.m.ground.cm\n"
    )
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._macro_registry = MacroRegistry()
    srv._macro_index = MacroIndex()
    srv._object_index = ObjectIndex()
    srv._doc_cache.pop(uri, None)

    # Cursor on ".m.p.mkr1" in the marker_name= argument (definition site, line 0)
    col = text.splitlines()[0].index(".m.p.mkr1")
    params = types.ReferenceParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=0, character=col),
        context=types.ReferenceContext(include_declaration=False),
    )
    result = srv.find_references(params)
    # Must include the i_marker reference on line 1
    ref_lines = [loc.range.start.line for loc in result]
    assert 1 in ref_lines, f"Expected reference on line 1, got lines: {ref_lines}"


def test_find_references_include_declaration_for_object(monkeypatch):
    """include_declaration=True must also return the object's definition location."""
    from adams_cmd_lsp.macros import MacroRegistry
    from adams_cmd_lsp.references import MacroIndex
    from adams_cmd_lsp.object_index import ObjectIndex
    uri = "file:///model.cmd"
    text = (
        "marker create marker_name = .m.p.mkr1 location = 0,0,0\n"
        "constraint create joint fixed joint_name=.m.f1 "
        "i_marker=.m.p.mkr1 j_marker=.m.ground.cm\n"
    )
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._macro_registry = MacroRegistry()
    srv._macro_index = MacroIndex()
    srv._object_index = ObjectIndex()
    srv._doc_cache.pop(uri, None)

    col = text.splitlines()[0].index(".m.p.mkr1")
    params = types.ReferenceParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=0, character=col),
        context=types.ReferenceContext(include_declaration=True),
    )
    result = srv.find_references(params)
    ref_lines = [loc.range.start.line for loc in result]
    # Must include both the definition (line 0) and the usage (line 1)
    assert 0 in ref_lines, "include_declaration=True must add the definition location"
    assert 1 in ref_lines, "Reference on line 1 must still be included"


# ---------------------------------------------------------------------------
# document_symbol
# ---------------------------------------------------------------------------

def test_document_symbol_returns_created_objects(monkeypatch):
    """document_symbol must return a SymbolInformation for each created object."""
    from lsprotocol import types as lsp_types
    uri = "file:///model.cmd"
    text = (
        "model create model_name = my_model\n"
        "part create rigid_body name_and_position part_name = my_model.PART_1\n"
        "marker create marker_name = my_model.PART_1.CM location = 0,0,0\n"
    )
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._doc_cache.pop(uri, None)

    params = types.DocumentSymbolParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
    )
    result = srv.document_symbol(params)
    assert len(result) > 0, "Expected at least one symbol"
    names = [s.name for s in result]
    assert any("PART_1" in n for n in names)
    assert any("CM" in n for n in names)
    # Builtins must be excluded
    assert not any(n.lower().lstrip('.') == "ground" for n in names)


def test_document_symbol_correct_kinds(monkeypatch):
    """document_symbol must use correct SymbolKind for Part and Marker."""
    uri = "file:///model.cmd"
    text = (
        "part create rigid_body name_and_position part_name = .m.P1\n"
        "marker create marker_name = .m.P1.CM location = 0,0,0\n"
    )
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._doc_cache.pop(uri, None)

    params = types.DocumentSymbolParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
    )
    result = srv.document_symbol(params)
    by_name = {s.name: s for s in result}

    part_sym = by_name.get(".m.P1") or by_name.get("m.P1")
    marker_sym = by_name.get(".m.P1.CM") or by_name.get("m.P1.CM")

    if part_sym:
        assert part_sym.kind == types.SymbolKind.Class
    if marker_sym:
        assert marker_sym.kind == types.SymbolKind.Field


def test_document_symbol_empty_file(monkeypatch):
    """document_symbol must return empty list for a comment-only file."""
    uri = "file:///empty.cmd"
    text = "! just a comment\n"
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._doc_cache.pop(uri, None)

    params = types.DocumentSymbolParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
    )
    result = srv.document_symbol(params)
    # Only builtins in the table — document_symbol must exclude them
    assert result == []


# ---------------------------------------------------------------------------
# _refresh_object_index_for_file — direct tests
# ---------------------------------------------------------------------------

def test_refresh_object_index_for_file_indexes_definitions():
    """_refresh_object_index_for_file must index definitions into _object_index."""
    from adams_cmd_lsp.object_index import ObjectIndex
    srv._schema = Schema.load()
    srv._object_index = ObjectIndex()
    text = "marker create marker_name = .m.p.mkr1 location = 0,0,0\n"
    # Use a synthetic path; no real file needed
    srv._refresh_object_index_for_file("file:///synth.cmd", text)
    defs = srv._object_index.get_definitions(".m.p.mkr1")
    assert len(defs) == 1, f"Expected 1 definition, got {len(defs)}"
    assert defs[0].object_type == "Marker"


def test_refresh_object_index_for_file_indexes_references():
    """_refresh_object_index_for_file must also index reference sites."""
    from adams_cmd_lsp.object_index import ObjectIndex
    srv._schema = Schema.load()
    srv._object_index = ObjectIndex()
    text = (
        "marker create marker_name = .m.p.mkr1 location = 0,0,0\n"
        "constraint create joint fixed joint_name=.m.f1 "
        "i_marker=.m.p.mkr1 j_marker=.m.ground.cm\n"
    )
    srv._refresh_object_index_for_file("file:///synth.cmd", text)
    refs = srv._object_index.get_references(".m.p.mkr1")
    assert len(refs) == 1, f"Expected 1 reference, got {len(refs)}"


def test_refresh_object_index_for_file_noop_without_schema():
    """_refresh_object_index_for_file must be a no-op when _schema is None."""
    from adams_cmd_lsp.object_index import ObjectIndex
    srv._schema = None
    srv._object_index = ObjectIndex()
    srv._refresh_object_index_for_file(
        "file:///synth.cmd", "marker create marker_name = .m.p.mkr1\n"
    )
    assert srv._object_index.total_definitions() == 0


# ---------------------------------------------------------------------------
# Cross-file Go to Definition and Find All References
# ---------------------------------------------------------------------------

def test_goto_definition_cross_file(monkeypatch, tmp_path):
    """goto_definition must navigate to a definition stored in _object_index (cross-file)."""
    from adams_cmd_lsp.macros import MacroRegistry
    from adams_cmd_lsp.object_index import ObjectIndex, IndexedDefinition

    # "current" file: only a reference to .m.p.mkr1
    uri_a = "file:///file_a.cmd"
    text_a = (
        "constraint create joint fixed joint_name=.m.f1 "
        "i_marker=.m.p.mkr1 j_marker=.m.ground.cm\n"
    )

    # "other" file where .m.p.mkr1 was defined (stored in the object index)
    other_path = str(tmp_path / "file_b.cmd")
    (tmp_path / "file_b.cmd").write_text(
        "marker create marker_name = .m.p.mkr1 location = 0,0,0\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(srv, "server", _make_mock_doc(text_a, uri_a))
    srv._schema = Schema.load()
    srv._macro_registry = MacroRegistry()
    srv._object_index = ObjectIndex()
    srv._object_index.update_file(
        other_path,
        [IndexedDefinition(name=".m.p.mkr1", object_type="Marker", line=0, source_file=other_path)],
        [],
    )
    srv._doc_cache.pop(uri_a, None)

    col = text_a.index(".m.p.mkr1")
    params = types.DefinitionParams(
        text_document=types.TextDocumentIdentifier(uri=uri_a),
        position=types.Position(line=0, character=col),
    )
    result = srv.goto_definition(params)
    assert result is not None, "Expected cross-file LocationLink"
    assert len(result) == 1
    link = result[0]
    # target must point to the OTHER file, not the current one
    assert "file_a" not in link.target_uri
    assert "file_b" in link.target_uri
    assert link.target_selection_range.start.line == 0


def test_find_references_cross_file(monkeypatch, tmp_path):
    """find_references must include references stored in _object_index (cross-file)."""
    from adams_cmd_lsp.macros import MacroRegistry
    from adams_cmd_lsp.references import MacroIndex
    from adams_cmd_lsp.object_index import ObjectIndex, IndexedReference

    # "current" file: the definition site
    uri_a = "file:///file_a.cmd"
    text_a = "marker create marker_name = .m.p.mkr1 location = 0,0,0\n"

    # "other" file that references the marker (stored in object index)
    other_path = str(tmp_path / "file_b.cmd")
    (tmp_path / "file_b.cmd").write_text(
        "constraint create joint fixed joint_name=.m.f1 "
        "i_marker=.m.p.mkr1 j_marker=.m.ground.cm\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(srv, "server", _make_mock_doc(text_a, uri_a))
    srv._schema = Schema.load()
    srv._macro_registry = MacroRegistry()
    srv._macro_index = MacroIndex()
    srv._object_index = ObjectIndex()
    srv._object_index.update_file(
        other_path,
        [],
        [IndexedReference(
            name=".m.p.mkr1", object_type="Marker",
            line=0, column=0, end_column=10,
            source_file=other_path,
        )],
    )
    srv._doc_cache.pop(uri_a, None)

    # cursor on the definition (.m.p.mkr1 in marker_name=)
    col = text_a.index(".m.p.mkr1")
    params = types.ReferenceParams(
        text_document=types.TextDocumentIdentifier(uri=uri_a),
        position=types.Position(line=0, character=col),
        context=types.ReferenceContext(include_declaration=False),
    )
    result = srv.find_references(params)
    # Must include the cross-file reference from file_b
    cross_uris = [loc.uri for loc in result if "file_b" in loc.uri]
    assert len(cross_uris) >= 1, (
        f"Expected at least one cross-file reference in file_b, got uris: {[l.uri for l in result]}"
    )


# ---------------------------------------------------------------------------
# $variable navigation helpers (unit tests)
# ---------------------------------------------------------------------------

def test_get_dollar_var_at_position_basic():
    """_get_dollar_var_at_position returns the $var token when cursor is within it."""
    line_text = "var set var=$_self.model obj=.m"
    result = srv._get_dollar_var_at_position(line_text, 12)  # cursor on '$'
    assert result is not None
    token, col, end_col = result
    assert token == "$_self.model"
    assert line_text[col:end_col] == "$_self.model"


def test_get_dollar_var_at_position_mid_token():
    """Cursor in the middle of the $var token is still matched."""
    line_text = "var set var=$_self.model obj=.m"
    # cursor at 'l' in 'model'
    result = srv._get_dollar_var_at_position(line_text, 20)
    assert result is not None
    token, _, _ = result
    assert token == "$_self.model"


def test_get_dollar_var_at_position_with_attribute_chain():
    """$var followed by attribute access still returns the full token."""
    line_text = "(eval($_self.model.object_value.name))"
    result = srv._get_dollar_var_at_position(line_text, 6)
    assert result is not None
    token, col, end_col = result
    assert token == "$_self.model.object_value.name"


def test_get_dollar_var_at_position_no_dollar():
    """Returns None when cursor is not within a $variable token."""
    result = srv._get_dollar_var_at_position("model create model_name=.m", 10)
    assert result is None


def test_find_variable_references_in_text():
    """_find_variable_references_in_text finds all occurrences of the var."""
    text = (
        "var set var=$_self.model obj=.demo_model\n"
        "\n"
        "var set var=$_self.py_str str=(eval($_self.py_str)), (eval($_self.model.name))\n"
    )
    results = srv._find_variable_references_in_text(text, "$_self.model")
    lines = [r[0] for r in results]
    # Should appear on line 0 (definition) and line 2 (inside eval)
    assert 0 in lines
    assert 2 in lines


def test_find_variable_references_no_false_positive_longer_name():
    """$_self.model must not match $_self.model_name."""
    text = "var set var=$_self.model_name str=x\nvar set var=$_self.model obj=.m\n"
    results = srv._find_variable_references_in_text(text, "$_self.model")
    cols_per_line = {r[0]: r[1] for r in results}
    # Line 0 should NOT be a match (it's $_self.model_name)
    assert 0 not in cols_per_line
    # Line 1 IS a match
    assert 1 in cols_per_line


# ---------------------------------------------------------------------------
# $variable goto_definition (integration tests)
# ---------------------------------------------------------------------------

def test_goto_definition_dollar_var_reference_jumps_to_def(monkeypatch):
    """Ctrl+Click on $variable reference navigates to its var set definition."""
    uri = "file:///test.cmd"
    text = (
        "var set var=$_self.model obj=.demo_model\n"
        "\n"
        "var set var=$_self.py_str str=(eval($_self.model.name))\n"
    )
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._macro_registry = None
    srv._doc_cache.pop(uri, None)

    # Cursor on $_self.model in line 2 (inside the eval expression)
    line2_text = text.splitlines()[2]
    col = line2_text.index("$_self.model")  # first occurrence is inside str=(eval(...)

    params = types.DefinitionParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=2, character=col + 3),  # middle of the token
    )
    result = srv.goto_definition(params)
    assert result is not None and len(result) == 1, (
        f"Expected exactly 1 LocationLink, got: {result}"
    )
    link = result[0]
    # target should be line 0 (var set var=$_self.model)
    assert link.target_range.start.line == 0, (
        f"Expected target line 0 (definition), got line {link.target_range.start.line}"
    )


def test_goto_definition_dollar_var_definition_site_returns_references(monkeypatch):
    """Ctrl+Click on var set var=$var definition site returns references."""
    uri = "file:///test.cmd"
    text = (
        "var set var=$_self.model obj=.demo_model\n"
        "\n"
        "var set var=$_self.py_str str=(eval($_self.model.name))\n"
    )
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._macro_registry = None
    srv._doc_cache.pop(uri, None)

    # Cursor on $_self.model in its var set definition (line 0)
    col = text.splitlines()[0].index("$_self.model")

    params = types.DefinitionParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=0, character=col + 2),
    )
    result = srv.goto_definition(params)
    # Should return the reference on line 2
    assert result is not None and len(result) >= 1, (
        f"Expected references from definition site, got: {result}"
    )
    target_lines = {link.target_range.start.line for link in result}
    assert 2 in target_lines, f"Expected reference on line 2, got lines {target_lines}"


def test_goto_definition_dollar_var_undefined_returns_none(monkeypatch):
    """Ctrl+Click on undeclared $variable returns None."""
    uri = "file:///test.cmd"
    text = "var set var=$_self.py_str str=(eval($_self.undeclared))\n"
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._macro_registry = None
    srv._doc_cache.pop(uri, None)

    col = text.index("$_self.undeclared")
    params = types.DefinitionParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=0, character=col + 3),
    )
    result = srv.goto_definition(params)
    assert result is None


# ---------------------------------------------------------------------------
# $variable find_references (integration tests)
# ---------------------------------------------------------------------------

def test_find_references_dollar_var_from_reference(monkeypatch):
    """Shift+F12 on a $variable reference returns all occurrences."""
    uri = "file:///test.cmd"
    text = (
        "var set var=$_self.model obj=.demo_model\n"
        "\n"
        "var set var=$_self.py_str str=(eval($_self.model.name))\n"
    )
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._macro_registry = None
    srv._doc_cache.pop(uri, None)

    line2_text = text.splitlines()[2]
    col = line2_text.index("$_self.model")

    params = types.ReferenceParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=2, character=col + 2),
        context=types.ReferenceContext(include_declaration=True),
    )
    result = srv.find_references(params)
    lines = [loc.range.start.line for loc in result]
    assert 0 in lines, "Expected definition line 0 to be included with include_declaration=True"
    assert 2 in lines, "Expected line 2 as a reference"


def test_find_references_dollar_var_from_definition_site(monkeypatch):
    """Shift+F12 on variable_name def site returns all references."""
    uri = "file:///test.cmd"
    text = (
        "var set var=$_self.model obj=.demo_model\n"
        "\n"
        "var set var=$_self.py_str str=(eval($_self.model.name))\n"
    )
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._macro_registry = None
    srv._doc_cache.pop(uri, None)

    col = text.splitlines()[0].index("$_self.model")

    params = types.ReferenceParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=0, character=col + 2),
        context=types.ReferenceContext(include_declaration=False),
    )
    result = srv.find_references(params)
    lines = [loc.range.start.line for loc in result]
    assert 2 in lines, f"Expected reference on line 2, got {lines}"


# ---------------------------------------------------------------------------
# Boundary / edge-case tests (guard off-by-one, null arg.value, etc.)
# ---------------------------------------------------------------------------

def test_get_dollar_var_at_position_cursor_just_past_end():
    """Cursor one character past the token end must NOT match."""
    line_text = "var set var=$_self.model obj=.m"
    # '$_self.model' starts at 12, len=12, so exclusive end = 24
    result = srv._get_dollar_var_at_position(line_text, 24)
    assert result is None, f"Should be None (cursor at exclusive end), got {result}"


def test_get_dollar_var_at_position_cursor_at_last_char():
    """Cursor on the last character of the token IS within the token."""
    line_text = "var set var=$_self.model obj=.m"
    # '$_self.model' occupies [12, 24), last char index = 23
    result = srv._get_dollar_var_at_position(line_text, 23)
    assert result is not None
    token, _, _ = result
    assert token == "$_self.model"


def test_find_variable_def_at_position_cursor_just_past_end():
    """Cursor one position past the variable_name arg end must return None."""
    from adams_cmd_lsp.parser import parse as _parse
    from adams_cmd_lsp.object_index import _resolve_command_keys
    text = "var set var=$_self.model obj=.demo_model\n"
    schema = Schema.load()
    stmts = _parse(text)
    _resolve_command_keys(stmts, schema)
    col = text.index("$_self.model")
    val_len = len("$_self.model")
    result = srv._find_variable_def_at_position(stmts, schema, 0, col + val_len)
    assert result is None, f"Cursor past end should return None, got {result}"


def test_find_variable_def_at_position_cursor_at_last_char():
    """Cursor on the last character of the variable_name arg IS valid."""
    from adams_cmd_lsp.parser import parse as _parse
    from adams_cmd_lsp.object_index import _resolve_command_keys
    text = "var set var=$_self.model obj=.demo_model\n"
    schema = Schema.load()
    stmts = _parse(text)
    _resolve_command_keys(stmts, schema)
    col = text.index("$_self.model")
    val_len = len("$_self.model")
    result = srv._find_variable_def_at_position(stmts, schema, 0, col + val_len - 1)
    assert result is not None
    var_name, _, _, _ = result
    assert var_name == "$_self.model"


def test_find_variable_definition_null_arg_value():
    """_find_variable_definition_in_statements handles None arg.value gracefully."""
    from adams_cmd_lsp.parser import parse as _parse
    from adams_cmd_lsp.object_index import _resolve_command_keys
    text = "var set var=$_self.model obj=.demo_model\n"
    schema = Schema.load()
    stmts = _parse(text)
    _resolve_command_keys(stmts, schema)
    # Inject a statement with a None-value argument to simulate malformed CMD
    for stmt in stmts:
        for arg in stmt.arguments:
            original = arg.value
            arg.value = None  # force the null path
            try:
                # Must not raise AttributeError; injected arg has None value so no match
                result = srv._find_variable_definition_in_statements(stmts, schema, "$_self.model")
                assert result is None, f"Null arg.value should cause a miss, got {result}"
            finally:
                arg.value = original  # restore
            break
        break


def test_find_variable_definition_prefix_reduction_three_parts():
    """_find_variable_definition_in_statements reduces a 3-part chain correctly."""
    from adams_cmd_lsp.parser import parse as _parse
    from adams_cmd_lsp.object_index import _resolve_command_keys
    text = "var set var=$_self.model obj=.demo_model\n"
    schema = Schema.load()
    stmts = _parse(text)
    _resolve_command_keys(stmts, schema)
    # Token '$_self.model.object_value.name' — only '$_self.model' is defined
    result = srv._find_variable_definition_in_statements(stmts, schema, "$_self.model.object_value.name")
    assert result is not None, "Should find definition via prefix reduction"
    matched_name, def_line, _, _ = result
    assert matched_name == "$_self.model"
    assert def_line == 0


# ---------------------------------------------------------------------------
# include_declaration=True tests (no duplicate location)
# ---------------------------------------------------------------------------

def test_find_references_dollar_var_include_declaration_no_duplicates(monkeypatch):
    """include_declaration=True must not produce duplicate locations."""
    uri = "file:///test.cmd"
    text = (
        "var set var=$_self.model obj=.demo_model\n"
        "\n"
        "var set var=$_self.py_str str=(eval($_self.model.name))\n"
    )
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._macro_registry = None
    srv._doc_cache.pop(uri, None)

    col = text.splitlines()[0].index("$_self.model")

    params = types.ReferenceParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=0, character=col + 2),
        context=types.ReferenceContext(include_declaration=True),
    )
    result = srv.find_references(params)
    # All (line, char) pairs must be unique — no duplicates
    positions = [(loc.range.start.line, loc.range.start.character) for loc in result]
    assert len(positions) == len(set(positions)), (
        f"Duplicate locations found: {positions}"
    )
    lines = [loc.range.start.line for loc in result]
    assert 0 in lines  # declaration is included (it's an occurrence of $var)
    assert 2 in lines  # reference in eval()


def test_find_references_dollar_var_from_reference_include_declaration_no_duplicates(monkeypatch):
    """include_declaration=True from a reference site must not duplicate any location."""
    uri = "file:///test.cmd"
    text = (
        "var set var=$_self.model obj=.demo_model\n"
        "\n"
        "var set var=$_self.py_str str=(eval($_self.model.name))\n"
    )
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._macro_registry = None
    srv._doc_cache.pop(uri, None)

    line2_text = text.splitlines()[2]
    col = line2_text.index("$_self.model")

    params = types.ReferenceParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=2, character=col + 2),
        context=types.ReferenceContext(include_declaration=True),
    )
    result = srv.find_references(params)
    positions = [(loc.range.start.line, loc.range.start.character) for loc in result]
    assert len(positions) == len(set(positions)), (
        f"Duplicate locations found: {positions}"
    )


def test_find_references_dollar_var_exclude_declaration(monkeypatch):
    """include_declaration=False excludes the definition; True includes it."""
    uri = "file:///test.cmd"
    text = (
        "var set var=$_self.model obj=.demo_model\n"
        "\n"
        "var set var=$_self.py_str str=(eval($_self.model.name))\n"
    )
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._macro_registry = None
    srv._doc_cache.pop(uri, None)

    col = text.splitlines()[0].index("$_self.model")

    # include_declaration=False: definition (line 0) must not appear
    params = types.ReferenceParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=0, character=col + 2),
        context=types.ReferenceContext(include_declaration=False),
    )
    result = srv.find_references(params)
    lines = [loc.range.start.line for loc in result]
    def_col = col
    def_positions = [
        (loc.range.start.line, loc.range.start.character)
        for loc in result
        if loc.range.start.line == 0 and loc.range.start.character == def_col
    ]
    assert def_positions == [], (
        f"include_declaration=False: definition should be excluded, got {def_positions}"
    )
    assert 2 in lines, f"include_declaration=False: ref on line 2 missing from {lines}"

    # include_declaration=True: definition (line 0) MUST appear, no duplicates
    srv._doc_cache.pop(uri, None)
    params_incl = types.ReferenceParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=0, character=col + 2),
        context=types.ReferenceContext(include_declaration=True),
    )
    result_incl = srv.find_references(params_incl)
    lines_incl = [loc.range.start.line for loc in result_incl]
    positions_incl = [
        (loc.range.start.line, loc.range.start.character) for loc in result_incl
    ]
    assert len(positions_incl) == len(set(positions_incl)), (
        f"include_declaration=True: duplicates found: {positions_incl}"
    )
    assert 0 in lines_incl, f"include_declaration=True: definition line 0 missing"
    assert 2 in lines_incl, f"include_declaration=True: ref on line 2 missing"


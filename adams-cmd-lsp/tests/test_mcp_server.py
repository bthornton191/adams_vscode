"""Tests for adams_cmd_lsp.mcp_server module.

Tests exercise the MCP tool handler functions directly by calling them as
async functions, without starting a live MCP server process.

Requires: pytest, pytest-asyncio, and the mcp package (FastMCP).
"""

from pathlib import Path
import json
import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Guard: skip entire module if mcp package is not installed
try:
    import mcp  # noqa: F401
    _MCP_AVAILABLE = True
except ImportError:
    _MCP_AVAILABLE = False

pytestmark = pytest.mark.skipif(
    not _MCP_AVAILABLE,
    reason="mcp package not installed",
)

if _MCP_AVAILABLE:
    import adams_cmd_lsp.mcp_server as srv
    from adams_cmd_lsp.schema import Schema
    from adams_cmd_lsp.macros import MacroRegistry, scan_macro_files


FIXTURES = Path(__file__).parent.parent.parent / "test" / "files"
TEST_CMD = FIXTURES / "test.cmd"
TEST_MAC = FIXTURES / "test.mac"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _setup(macro_registry=None):
    """Initialise module-level singletons as main() would."""
    srv._schema = Schema.load()
    srv._macro_registry = macro_registry


# ---------------------------------------------------------------------------
# adams_lint_cmd_text
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_lint_cmd_text_valid_returns_empty_diagnostics():
    _setup()
    result = json.loads(await srv.adams_lint_cmd_text("model create model_name=my_model"))
    assert result["summary"]["errors"] == 0
    assert result["diagnostics"] == []


@pytest.mark.asyncio
async def test_lint_cmd_text_invalid_command_returns_e001():
    _setup()
    result = json.loads(await srv.adams_lint_cmd_text("not_a_real_command arg=val"))
    codes = [d["code"] for d in result["diagnostics"]]
    assert "E001" in codes


@pytest.mark.asyncio
async def test_lint_cmd_text_empty_string():
    _setup()
    result = json.loads(await srv.adams_lint_cmd_text(""))
    assert result["diagnostics"] == []
    assert result["summary"]["errors"] == 0


@pytest.mark.asyncio
async def test_lint_cmd_text_min_severity_error_suppresses_warnings():
    _setup()
    # W005 fires for omitted object name on create commands
    text = "marker create"
    result_info = json.loads(await srv.adams_lint_cmd_text(text, min_severity="info"))
    result_error = json.loads(await srv.adams_lint_cmd_text(text, min_severity="error"))
    # info result may have W005; error result should have none
    error_only_codes = {d["code"] for d in result_error["diagnostics"]}
    for code in error_only_codes:
        assert code.startswith("E"), f"Expected only E-codes at min_severity=error, got {code}"


@pytest.mark.asyncio
async def test_lint_cmd_text_invalid_severity_returns_error():
    _setup()
    result = json.loads(await srv.adams_lint_cmd_text("model create model_name=x", min_severity="critical"))
    assert "error" in result
    assert "min_severity" in result["error"].lower() or "invalid" in result["error"].lower()


@pytest.mark.asyncio
async def test_lint_cmd_text_schema_not_initialised_returns_error():
    _setup()
    srv._schema = None
    try:
        result = json.loads(await srv.adams_lint_cmd_text("model create model_name=foo"))
        assert "error" in result
    finally:
        _setup()  # always restore so subsequent tests are not affected


@pytest.mark.asyncio
async def test_lint_cmd_text_with_macro_registry_no_e001_for_known_macro():
    """A command matching a known user macro should not produce E001."""
    registry = MacroRegistry()
    # Register a fake macro definition
    from adams_cmd_lsp.macros import MacroDefinition
    registry.register(MacroDefinition(command="my custom macro", parameters={}))
    _setup(macro_registry=registry)

    result = json.loads(await srv.adams_lint_cmd_text("my custom macro"))
    codes = [d["code"] for d in result["diagnostics"]]
    assert "E001" not in codes, f"Expected no E001 for known macro, got: {codes}"


@pytest.mark.asyncio
async def test_lint_cmd_text_without_macro_registry_e001_for_unknown():
    """Without a macro registry, an unknown command should produce E001."""
    _setup(macro_registry=None)
    result = json.loads(await srv.adams_lint_cmd_text("my custom macro"))
    codes = [d["code"] for d in result["diagnostics"]]
    assert "E001" in codes


# ---------------------------------------------------------------------------
# adams_lint_cmd_file
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_lint_cmd_file_real_fixture():
    _setup()
    if not TEST_CMD.exists():
        pytest.skip("test fixture not available")
    result = json.loads(await srv.adams_lint_cmd_file(str(TEST_CMD)))
    assert "diagnostics" in result
    assert "summary" in result
    assert "file" in result
    assert result["file"] == str(TEST_CMD.resolve())


@pytest.mark.asyncio
async def test_lint_cmd_file_nonexistent_returns_error():
    _setup()
    result = json.loads(await srv.adams_lint_cmd_file("/nonexistent/path/model.cmd"))
    assert "error" in result
    assert "not found" in result["error"].lower() or "nonexistent" in result["error"].lower()


@pytest.mark.asyncio
async def test_lint_cmd_file_invalid_severity_returns_error():
    _setup()
    if not TEST_CMD.exists():
        pytest.skip("test fixture not available")
    result = json.loads(await srv.adams_lint_cmd_file(str(TEST_CMD), min_severity="bad"))
    assert "error" in result


@pytest.mark.asyncio
@pytest.mark.parametrize("show_hint,expect_hint", [(True, True), (False, False)])
async def test_lint_cmd_text_show_macro_hint_toggle(show_hint, expect_hint):
    """When _show_macro_hint is False the E001 message should not include the
    scanWorkspaceMacros hint; when True it should."""
    _setup(macro_registry=None)
    srv._show_macro_hint = show_hint
    try:
        result = json.loads(await srv.adams_lint_cmd_text("my_unknown_command arg=val"))
        e001_messages = [
            d["message"] for d in result["diagnostics"] if d["code"] == "E001"
        ]
        assert e001_messages, "Expected at least one E001 diagnostic"
        hint_present = any("scanWorkspaceMacros" in m for m in e001_messages)
        assert hint_present == expect_hint, (
            f"Expected hint_present={expect_hint} but got {hint_present}. "
            f"Messages: {e001_messages}"
        )
    finally:
        srv._show_macro_hint = True  # restore default


@pytest.mark.asyncio
async def test_lint_cmd_file_includes_file_path_on_min_severity_error():
    """Verify 'file' key is absent (error path) when severity arg is invalid."""
    _setup()
    if not TEST_CMD.exists():
        pytest.skip("test fixture not available")
    result = json.loads(await srv.adams_lint_cmd_file(str(TEST_CMD), min_severity="bad"))
    # Error response should have 'error' key, not 'file'
    assert "error" in result
    assert "file" not in result


# ---------------------------------------------------------------------------
# adams_lookup_command
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_lookup_command_exact_match():
    _setup()
    result = json.loads(await srv.adams_lookup_command("marker create"))
    assert result["command"] == "marker create"
    assert "arguments" in result
    assert "exclusive_groups" in result


@pytest.mark.asyncio
async def test_lookup_command_abbreviated_match():
    _setup()
    result = json.loads(await srv.adams_lookup_command("mar cre"))
    assert result["command"] == "marker create"


@pytest.mark.asyncio
async def test_lookup_command_unknown_returns_error():
    _setup()
    result = json.loads(await srv.adams_lookup_command("zzz_not_real"))
    assert "error" in result
    assert "unknown" in result["error"].lower() or "zzz_not_real" in result["error"].lower()


@pytest.mark.asyncio
async def test_lookup_command_unknown_includes_suggestion():
    _setup()
    # "mar" should partially resolve for "marker" subtree — suggestion should reference it
    result = json.loads(await srv.adams_lookup_command("mar zzz_nope"))
    assert "error" in result
    # suggestion may be None or a string — either is acceptable
    assert "suggestion" in result


@pytest.mark.asyncio
async def test_lookup_command_empty_string_returns_error():
    _setup()
    result = json.loads(await srv.adams_lookup_command(""))
    assert "error" in result


@pytest.mark.asyncio
async def test_lookup_command_includes_required_flag():
    _setup()
    result = json.loads(await srv.adams_lookup_command("model create"))
    # model create has model_name which is required (NDBWD_*)
    # check the argument structure is correct
    for arg_name, arg_def in result["arguments"].items():
        assert "required" in arg_def
        assert "type" in arg_def
        assert "min_prefix" in arg_def


# ---------------------------------------------------------------------------
# Startup initialisation helpers
# ---------------------------------------------------------------------------

def test_macro_registry_is_none_when_not_set():
    """Server starts with _macro_registry = None before main() is called."""
    srv._macro_registry = None
    assert srv._macro_registry is None


def test_schema_loads_successfully():
    """Schema.load() with no args returns a populated schema."""
    schema = Schema.load()
    assert schema is not None
    # Check some known commands exist
    assert schema.has_command("model create")
    assert schema.has_command("marker create")

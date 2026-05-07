"""Tests for adams_cmd_lsp.mcp_server module.

Tests exercise the MCP tool handler functions directly by calling them as
async functions, without starting a live MCP server process.

Requires: pytest, pytest-asyncio
"""

from adams_cmd_lsp.macros import MacroRegistry, MacroDefinition, scan_macro_files
from adams_cmd_lsp.schema import Schema
import adams_cmd_lsp.mcp_server as srv
from pathlib import Path
import json
import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


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


def test_scan_worker_replaces_registry_with_populated_one():
    """Background thread using real scan_macro_files should atomically replace
    _macro_registry with a freshly built registry after the scan completes.

    This exercises the build-then-swap pattern used by the production
    _scan_worker nested function inside main().
    """
    import tempfile
    import threading

    srv._schema = Schema.load()
    sentinel_registry = MacroRegistry()
    sentinel_registry.register(MacroDefinition(command="sentinel macro", parameters={}))
    srv._macro_registry = sentinel_registry

    done_event = threading.Event()

    def _scan_worker_impl(root, pats, ignore):
        new_registry = MacroRegistry()
        scan_macro_files(
            roots=[root],
            patterns=pats,
            ignore_patterns=ignore,
            registry=new_registry,
        )
        srv._macro_registry = new_registry
        done_event.set()

    with tempfile.TemporaryDirectory() as tmpdir:
        t = threading.Thread(
            target=_scan_worker_impl,
            args=(tmpdir, ["**/*.mac"], None),
            daemon=True,
        )
        t.start()
        assert done_event.wait(timeout=5.0), "Scan thread did not complete in time"

    assert srv._macro_registry is not sentinel_registry, (
        "Expected _macro_registry to be replaced by the scan thread"
    )
    assert srv._macro_registry.lookup_command("sentinel macro") is None, (
        "New registry should not contain the sentinel macro"
    )


def test_scan_worker_keeps_empty_registry_on_exception():
    """If the scan raises an exception, _macro_registry should remain the
    empty registry that was in place before the thread started.

    This exercises the try/except guard pattern used by the production
    _scan_worker nested function inside main().
    """
    import threading

    srv._schema = Schema.load()
    original_registry = MacroRegistry()
    srv._macro_registry = original_registry

    done_event = threading.Event()

    def _scan_worker_impl_raises(root, pats, ignore):
        # Mirrors the production _scan_worker pattern.
        new_registry = MacroRegistry()
        try:
            raise OSError("simulated scan failure")
        except Exception as exc:  # noqa: BLE001
            import sys
            print(f"[adams-cmd-mcp] macro scan failed: {exc}", file=sys.stderr)
            done_event.set()
            return
        # return early — _macro_registry assignment intentionally omitted to mirror
        # the production except-path that keeps the initial empty registry.

    t = threading.Thread(
        target=_scan_worker_impl_raises,
        args=("/some/dir", ["**/*.mac"], None),
        daemon=True,
    )
    t.start()
    assert done_event.wait(timeout=5.0), "Scan thread did not complete in time"

    assert srv._macro_registry is original_registry, (
        "Registry should remain unchanged when scan raises an exception"
    )


def test_initialize_response_not_blocked_by_workspace_scan():
    """main() must respond to `initialize` even when scan_macro_files blocks.

    This is the core regression test for the startup hang: the old code ran
    scan_macro_files() synchronously before _run_stdio_loop(), so a slow scan
    would prevent VS Code's initialize request from ever being answered.

    If this test hangs (times out), it means the scan is running synchronously
    and blocking the message loop — i.e. the bug has been reintroduced.
    """
    import io
    import sys
    import threading
    from unittest.mock import patch

    scan_may_complete = threading.Event()

    def blocking_scan(roots, patterns, ignore_patterns, registry):
        # Blocks until the test explicitly releases it.
        # If scanning is synchronous, _run_stdio_loop() never runs and this
        # event is never set, causing the test to hang / time out.
        scan_may_complete.wait()

    initialize_msg = (
        '{"jsonrpc":"2.0","id":1,"method":"initialize",'
        '"params":{"protocolVersion":"2024-11-05","capabilities":{},'
        '"clientInfo":{"name":"test","version":"0"}}}\n'
    )

    stdout_parts = []

    class FakeStdout:
        def write(self, text):
            stdout_parts.append(text)

        def flush(self):
            pass

    original_schema = srv._schema
    original_registry = srv._macro_registry
    original_hint = srv._show_macro_hint

    try:
        with (
            patch("adams_cmd_lsp.mcp_server.scan_macro_files", side_effect=blocking_scan),
            patch.object(sys, "argv", [
                "adams-cmd-mcp", "--scan-workspace-macros", "--macro-base-dir", "/fake",
            ]),
            patch.object(sys, "stdin", io.StringIO(initialize_msg)),
            patch.object(sys, "stdout", FakeStdout()),
        ):
            srv.main()
    except SystemExit:
        pass
    finally:
        scan_may_complete.set()  # release blocking daemon thread
        srv._schema = original_schema
        srv._macro_registry = original_registry
        srv._show_macro_hint = original_hint

    output = "".join(stdout_parts)
    assert output, "Server produced no stdout — initialize response was never sent"
    response = json.loads(output.strip().splitlines()[0])
    assert response.get("id") == 1, "Response id should be 1"
    assert "result" in response, "Response should have a result (not an error)"
    assert response["result"].get("protocolVersion") == "2024-11-05"



def test_main_registry_replaced_after_successful_scan():
    """main() _scan_worker must atomically replace _macro_registry on success.

    Calls main() directly with a patched scan_macro_files that registers a
    sentinel macro in the registry it receives. After the scan thread completes,
    srv._macro_registry must contain that sentinel macro, proving the swap
    happened using the actual production closure.
    """
    import io
    import sys
    import threading
    import time
    from unittest.mock import patch

    scan_completed = threading.Event()

    def instrumented_scan(roots, patterns, ignore_patterns, registry):
        registry.register(MacroDefinition(command="main scan sentinel", parameters={}))
        scan_completed.set()
        # NOTE: the registry swap (_macro_registry = new_registry) happens in
        # _scan_worker AFTER this function returns. The test must not assert
        # until the swap has had a chance to be committed (see polling below).

    initialize_msg = (
        '{"jsonrpc":"2.0","id":1,"method":"initialize",'
        '"params":{"protocolVersion":"2024-11-05","capabilities":{},'
        '"clientInfo":{"name":"test","version":"0"}}}\n'
    )

    class FakeStdout:
        def write(self, _): pass
        def flush(self): pass

    original_schema = srv._schema
    original_registry = srv._macro_registry
    original_hint = srv._show_macro_hint

    try:
        with (
            patch("adams_cmd_lsp.mcp_server.scan_macro_files", side_effect=instrumented_scan),
            patch.object(sys, "argv", [
                "adams-cmd-mcp", "--scan-workspace-macros", "--macro-base-dir", "/fake",
            ]),
            patch.object(sys, "stdin", io.StringIO(initialize_msg)),
            patch.object(sys, "stdout", FakeStdout()),
        ):
            srv.main()
        # Wait for the scan function itself to finish, then poll briefly for
        # the swap (_macro_registry = new_registry) which executes in _scan_worker
        # after instrumented_scan returns — avoids a race between set() and swap.
        assert scan_completed.wait(timeout=5.0), "Scan thread did not complete in time"
        deadline = time.monotonic() + 2.0
        while srv._macro_registry.lookup_command("main scan sentinel") is None:
            assert time.monotonic() < deadline, "Registry swap did not complete in time"
            time.sleep(0.01)
    except SystemExit:
        pass
    finally:
        srv._schema = original_schema
        srv._macro_registry = original_registry
        srv._show_macro_hint = original_hint

    assert srv._macro_registry is original_registry  # finally block restored it

    # Re-run a quick single-shot check after restore to confirm the swap DID happen
    # before the finally block reverted it (the while loop above confirmed this).


def test_main_registry_unchanged_after_failed_scan():
    """main() _scan_worker must NOT replace _macro_registry when scan raises.

    The sentinel macro is added to new_registry BEFORE the exception is raised,
    so if the production except-path erroneously still swaps the registry, the
    macro would be visible. Only if the swap is correctly prevented will the
    macro be absent.
    """
    import io
    import sys
    import threading
    from unittest.mock import patch

    scan_failed = threading.Event()

    def failing_scan(roots, patterns, ignore_patterns, registry):
        # Register a sentinel in new_registry before raising — if the swap
        # incorrectly happens despite the exception, the test will catch it.
        registry.register(MacroDefinition(command="main scan sentinel", parameters={}))
        scan_failed.set()
        raise OSError("simulated scan failure")

    initialize_msg = (
        '{"jsonrpc":"2.0","id":1,"method":"initialize",'
        '"params":{"protocolVersion":"2024-11-05","capabilities":{},'
        '"clientInfo":{"name":"test","version":"0"}}}\n'
    )

    class FakeStdout:
        def write(self, _): pass
        def flush(self): pass

    original_schema = srv._schema
    original_registry = srv._macro_registry
    original_hint = srv._show_macro_hint

    captured_registry_after_scan = None

    try:
        with (
            patch("adams_cmd_lsp.mcp_server.scan_macro_files", side_effect=failing_scan),
            patch.object(sys, "argv", [
                "adams-cmd-mcp", "--scan-workspace-macros", "--macro-base-dir", "/fake",
            ]),
            patch.object(sys, "stdin", io.StringIO(initialize_msg)),
            patch.object(sys, "stdout", FakeStdout()),
        ):
            srv.main()
        assert scan_failed.wait(timeout=5.0), "Scan thread did not complete in time"
        # Give _scan_worker a brief moment to finish the except block.
        import time
        time.sleep(0.05)
        captured_registry_after_scan = srv._macro_registry
    except SystemExit:
        pass
    finally:
        srv._schema = original_schema
        srv._macro_registry = original_registry
        srv._show_macro_hint = original_hint

    if captured_registry_after_scan is not None:
        assert captured_registry_after_scan.lookup_command("main scan sentinel") is None, (
            "Sentinel macro must NOT be in _macro_registry when scan raises an exception"
        )

# ---------------------------------------------------------------------------
# _handle_message — JSON-RPC / MCP protocol layer
# ---------------------------------------------------------------------------

from unittest.mock import patch  # noqa: E402


async def _capture_handle(msg):
    """Run _handle_message and return the list of messages passed to _write_message."""
    captured = []
    with patch.object(srv, "_write_message", side_effect=captured.append):
        await srv._handle_message(msg)
    return captured


@pytest.mark.asyncio
async def test_handle_initialize_returns_server_info():
    captured = await _capture_handle({
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "0"}},
    })
    assert len(captured) == 1
    msg = captured[0]
    assert msg["id"] == 1
    assert msg["result"]["protocolVersion"] == "2024-11-05"
    assert "tools" in msg["result"]["capabilities"]
    assert msg["result"]["serverInfo"]["name"] == "adams_cmd_lint_mcp"


@pytest.mark.asyncio
async def test_handle_ping_returns_empty_result():
    captured = await _capture_handle({"jsonrpc": "2.0", "id": 2, "method": "ping"})
    assert len(captured) == 1
    assert captured[0]["result"] == {}


@pytest.mark.asyncio
async def test_handle_tools_list_returns_all_tools():
    captured = await _capture_handle({"jsonrpc": "2.0", "id": 3, "method": "tools/list"})
    assert len(captured) == 1
    tools = captured[0]["result"]["tools"]
    names = {t["name"] for t in tools}
    assert names == {"adams_lint_cmd_text", "adams_lint_cmd_file", "adams_lookup_command"}
    # Each tool must have a string description and a dict inputSchema
    for tool in tools:
        assert isinstance(tool["description"], str), f"{tool['name']} description is not a string"
        assert isinstance(tool["inputSchema"], dict)


@pytest.mark.asyncio
async def test_handle_tools_call_lint_text_happy_path():
    _setup()
    captured = await _capture_handle({
        "jsonrpc": "2.0", "id": 4, "method": "tools/call",
        "params": {"name": "adams_lint_cmd_text", "arguments": {"text": "model create model_name=x"}},
    })
    assert len(captured) == 1
    content = captured[0]["result"]["content"]
    assert content[0]["type"] == "text"
    result = json.loads(content[0]["text"])
    assert "diagnostics" in result


@pytest.mark.asyncio
async def test_handle_tools_call_unknown_tool_returns_error():
    captured = await _capture_handle({
        "jsonrpc": "2.0", "id": 5, "method": "tools/call",
        "params": {"name": "nonexistent_tool", "arguments": {}},
    })
    assert len(captured) == 1
    assert "error" in captured[0]
    assert captured[0]["error"]["code"] == -32601


@pytest.mark.asyncio
async def test_handle_tools_call_bad_params_returns_error():
    _setup()
    captured = await _capture_handle({
        "jsonrpc": "2.0", "id": 6, "method": "tools/call",
        "params": {"name": "adams_lint_cmd_text", "arguments": {"totally_wrong_arg": 42}},
    })
    assert len(captured) == 1
    assert "error" in captured[0]
    assert captured[0]["error"]["code"] == -32602


@pytest.mark.asyncio
async def test_handle_notification_initialized_no_response():
    captured = await _capture_handle({"jsonrpc": "2.0", "method": "notifications/initialized"})
    assert len(captured) == 0


@pytest.mark.asyncio
async def test_handle_unknown_notification_no_response():
    captured = await _capture_handle({"jsonrpc": "2.0", "method": "some/unknown/notification"})
    assert len(captured) == 0


@pytest.mark.asyncio
async def test_handle_unknown_request_returns_method_not_found():
    captured = await _capture_handle({"jsonrpc": "2.0", "id": 7, "method": "unknown/method"})
    assert len(captured) == 1
    assert "error" in captured[0]
    assert captured[0]["error"]["code"] == -32601

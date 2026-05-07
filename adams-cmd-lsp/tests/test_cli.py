"""Tests for adams_cmd_lsp.cli module (CLI linter)."""

from adams_cmd_lsp.diagnostics import Diagnostic, Severity
from adams_cmd_lsp.cli import _output_text, _output_json, _output_gcc, main
import pytest
from unittest.mock import patch
from pathlib import Path
import sys
import os
import io
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


FIXTURES = Path(__file__).parent.parent.parent / "test" / "files"

# ---------------------------------------------------------------------------
# Helper: build a minimal Diagnostic list
# ---------------------------------------------------------------------------


def _diags():
    return [
        Diagnostic(
            line=0, column=0, end_line=0, end_column=5,
            code="E001", message="Unknown command: 'xyz'",
            severity=Severity.ERROR,
        ),
        Diagnostic(
            line=1, column=4, end_line=1, end_column=9,
            code="W005", message="Object name 'foo' omitted",
            severity=Severity.WARNING,
        ),
        Diagnostic(
            line=2, column=0, end_line=2, end_column=3,
            code="I006", message="Manual adams_id assigned",
            severity=Severity.INFO,
        ),
    ]


# ---------------------------------------------------------------------------
# _output_text
# ---------------------------------------------------------------------------

def test_output_text_format():
    buf = io.StringIO()
    _output_text("foo.cmd", _diags(), file=buf)
    out = buf.getvalue()
    # 1-based lines
    assert "foo.cmd:1:1: E001" in out
    assert "foo.cmd:2:5: W005" in out
    assert "1 error(s)" in out
    assert "1 warning(s)" in out


def test_output_text_no_diags():
    buf = io.StringIO()
    _output_text("empty.cmd", [], file=buf)
    out = buf.getvalue()
    assert "0 error(s)" in out
    assert "0 warning(s)" in out


# ---------------------------------------------------------------------------
# _output_json
# ---------------------------------------------------------------------------

def test_output_json_structure():
    buf = io.StringIO()
    _output_json("foo.cmd", _diags(), file=buf)
    result = json.loads(buf.getvalue())
    assert result["file"] == "foo.cmd"
    assert len(result["diagnostics"]) == 3
    assert result["summary"]["errors"] == 1
    assert result["summary"]["warnings"] == 1
    assert result["summary"]["info"] == 1


def test_output_json_1_based_lines():
    buf = io.StringIO()
    _output_json("f.cmd", _diags(), file=buf)
    result = json.loads(buf.getvalue())
    d0 = result["diagnostics"][0]
    # line 0 (0-based) → 1 (1-based)
    assert d0["line"] == 1
    assert d0["column"] == 1


def test_output_json_no_diags():
    buf = io.StringIO()
    _output_json("empty.cmd", [], file=buf)
    result = json.loads(buf.getvalue())
    assert result["diagnostics"] == []
    assert result["summary"]["errors"] == 0


# ---------------------------------------------------------------------------
# _output_gcc
# ---------------------------------------------------------------------------

def test_output_gcc_format():
    buf = io.StringIO()
    _output_gcc("foo.cmd", _diags(), file=buf)
    lines = buf.getvalue().strip().splitlines()
    assert len(lines) == 3
    assert "foo.cmd:1:1: error:" in lines[0]
    assert "[E001]" in lines[0]
    assert "foo.cmd:2:5: warning:" in lines[1]
    assert "[W005]" in lines[1]


# ---------------------------------------------------------------------------
# main() integration via argv patching
# ---------------------------------------------------------------------------

def test_main_no_files_exits_2():
    with patch("sys.argv", ["adams-cmd-lint"]):
        with pytest.raises(SystemExit) as exc:
            main()
    # argparse exits with 2 when required args are missing
    assert exc.value.code == 2


def test_main_missing_file_exits_2(tmp_path):
    missing = str(tmp_path / "nonexistent.cmd")
    with patch("sys.argv", ["adams-cmd-lint", missing]):
        with pytest.raises(SystemExit) as exc:
            main()
    assert exc.value.code == 2


def test_main_clean_file_exits_0(tmp_path):
    """A clean file should exit 0."""
    cmd_file = tmp_path / "clean.cmd"
    cmd_file.write_text("model create model_name = my_model\n", encoding="utf-8")
    with patch("sys.argv", ["adams-cmd-lint", str(cmd_file)]):
        captured = io.StringIO()
        with pytest.raises(SystemExit) as exc:
            with patch("sys.stdout", captured):
                main()
    assert exc.value.code == 0


def test_main_error_file_exits_1(tmp_path):
    """A file with errors should exit 1."""
    cmd_file = tmp_path / "bad.cmd"
    cmd_file.write_text("not_a_real_command foo=bar\n", encoding="utf-8")
    with patch("sys.argv", ["adams-cmd-lint", str(cmd_file)]):
        captured = io.StringIO()
        with pytest.raises(SystemExit) as exc:
            with patch("sys.stdout", captured):
                main()
    assert exc.value.code == 1


def test_main_json_format(tmp_path):
    """--format json produces valid JSON output."""
    cmd_file = tmp_path / "test.cmd"
    cmd_file.write_text("model create model_name = my_model\n", encoding="utf-8")
    with patch("sys.argv", ["adams-cmd-lint", "--format", "json", str(cmd_file)]):
        captured = io.StringIO()
        with pytest.raises(SystemExit):
            with patch("sys.stdout", captured):
                main()
    result = json.loads(captured.getvalue())
    assert "diagnostics" in result
    assert "summary" in result


def test_main_severity_filter(tmp_path):
    """--severity error should suppress warnings/info."""
    cmd_file = tmp_path / "test.cmd"
    # marker create without name produces W005 (warning), not E005
    cmd_file.write_text("marker create location=0,0,0\n", encoding="utf-8")
    with patch("sys.argv", ["adams-cmd-lint", "--severity", "error", str(cmd_file)]):
        captured = io.StringIO()
        with pytest.raises(SystemExit) as exc:
            with patch("sys.stdout", captured):
                main()
    # No errors → exit 0
    assert exc.value.code == 0
    # Output should not mention W005
    assert "W005" not in captured.getvalue()


@pytest.mark.skipif(not FIXTURES.exists(), reason="fixtures not available")
def test_main_fixture_test_measures_final(tmp_path):
    """test_measures_final.cmd should exit 0 with --severity error."""
    src = FIXTURES / "test_measures_final.cmd"
    if not src.exists():
        return
    with patch("sys.argv", ["adams-cmd-lint", "--severity", "error", str(src)]):
        captured = io.StringIO()
        with pytest.raises(SystemExit) as exc:
            with patch("sys.stdout", captured):
                main()
    assert exc.value.code == 0, f"Unexpected errors:\n{captured.getvalue()}"


# ---------------------------------------------------------------------------
# --macro-paths integration
# ---------------------------------------------------------------------------

def test_macro_paths_suppresses_e001(tmp_path):
    """--macro-paths glob should prevent E001 for commands defined in macro files."""
    macro_dir = tmp_path / "macros"
    macro_dir.mkdir()
    (macro_dir / "tool.mac").write_text(
        "!USER_ENTERED_COMMAND cdm tool\n!$model:t=model\n",
        encoding="utf-8",
    )
    cmd_file = tmp_path / "caller.cmd"
    cmd_file.write_text("cdm tool model=.m\n", encoding="utf-8")

    captured = io.StringIO()
    with patch("sys.argv", [
        "adams-cmd-lint",
        "--severity", "error",
        str(cmd_file),
        "--macro-base-dir", str(tmp_path),
        "--macro-paths", "**/*.mac",
    ]):
        with pytest.raises(SystemExit) as exc:
            with patch("sys.stdout", captured):
                main()
    assert exc.value.code == 0, (
        f"E001 should be suppressed via --macro-paths, got:\n{captured.getvalue()}"
    )


def test_macro_paths_arg_validation_fires(tmp_path):
    """--macro-paths should cause E002 for arguments not in the macro's parameter list."""
    macro_dir = tmp_path / "macros"
    macro_dir.mkdir()
    (macro_dir / "tool.mac").write_text(
        "!USER_ENTERED_COMMAND cdm tool\n!$model:t=model\n",
        encoding="utf-8",
    )
    cmd_file = tmp_path / "caller.cmd"
    cmd_file.write_text("cdm tool model=.m bad_arg=123\n", encoding="utf-8")

    captured = io.StringIO()
    with patch("sys.argv", [
        "adams-cmd-lint",
        "--severity", "error",
        str(cmd_file),
        "--macro-base-dir", str(tmp_path),
        "--macro-paths", "**/*.mac",
    ]):
        with pytest.raises(SystemExit) as exc:
            with patch("sys.stdout", captured):
                main()
    assert exc.value.code == 1, (
        f"E002 should fire for unknown macro arg, got code {exc.value.code}:\n{captured.getvalue()}"
    )
    assert "bad_arg" in captured.getvalue()


def test_macro_paths_nonexistent_base_dir_is_ignored(tmp_path):
    """A nonexistent --macro-base-dir should not crash the CLI."""
    cmd_file = tmp_path / "test.cmd"
    cmd_file.write_text("model create model_name=.m\n", encoding="utf-8")

    with patch("sys.argv", [
        "adams-cmd-lint",
        str(cmd_file),
        "--macro-base-dir", str(tmp_path / "nonexistent"),
        "--macro-paths", "**/*.mac",
    ]):
        with pytest.raises(SystemExit) as exc:
            main()
    assert exc.value.code == 0


def test_macro_paths_no_base_dir_uses_cwd(tmp_path):
    """Without --macro-base-dir, CWD is used as the base."""
    import os
    (tmp_path / "tool.mac").write_text(
        "!USER_ENTERED_COMMAND my tool\n", encoding="utf-8"
    )
    cmd_file = tmp_path / "caller.cmd"
    cmd_file.write_text("my tool\n", encoding="utf-8")

    captured = io.StringIO()
    orig_cwd = os.getcwd()
    try:
        os.chdir(str(tmp_path))
        with patch("sys.argv", [
            "adams-cmd-lint",
            "--severity", "error",
            str(cmd_file),
            "--macro-paths", "**/*.mac",
        ]):
            with pytest.raises(SystemExit) as exc:
                with patch("sys.stdout", captured):
                    main()
    finally:
        os.chdir(orig_cwd)
    assert exc.value.code == 0, (
        f"E001 should be suppressed when CWD used as base:\n{captured.getvalue()}"
    )


def test_e001_message_contains_hint_when_no_macro_paths(tmp_path):
    """E001 message should suggest scanWorkspaceMacros when no macro paths given."""
    cmd_file = tmp_path / "test.cmd"
    cmd_file.write_text("cdm unknown_tool\n", encoding="utf-8")

    captured = io.StringIO()
    with patch("sys.argv", [
        "adams-cmd-lint",
        "--severity", "error",
        str(cmd_file),
    ]):
        with pytest.raises(SystemExit):
            with patch("sys.stdout", captured):
                main()
    assert "scanWorkspaceMacros" in captured.getvalue()


def test_macro_ignore_paths_excludes_matched(tmp_path):
    """--macro-ignore-paths excludes macros in matched directories."""
    generated = tmp_path / "generated"
    generated.mkdir()
    macros = tmp_path / "macros"
    macros.mkdir()

    # Two macros: one in generated/ (should be ignored), one in macros/ (should be found)
    (generated / "auto.mac").write_text(
        "!USER_ENTERED_COMMAND auto cmd\n", encoding="utf-8"
    )
    (macros / "manual.mac").write_text(
        "!USER_ENTERED_COMMAND manual cmd\n", encoding="utf-8"
    )

    # Caller invokes "manual cmd" — should be OK (found)
    # Caller also invokes "auto cmd" — should cause E001 because it was ignored
    cmd_file = tmp_path / "caller.cmd"
    cmd_file.write_text("manual cmd\nauto cmd\n", encoding="utf-8")

    captured = io.StringIO()
    with patch("sys.argv", [
        "adams-cmd-lint",
        "--severity", "error",
        str(cmd_file),
        "--macro-base-dir", str(tmp_path),
        "--macro-paths", "**/*.mac",
        "--macro-ignore-paths", "generated/**",
    ]):
        with pytest.raises(SystemExit) as exc:
            with patch("sys.stdout", captured):
                main()
    output = captured.getvalue()
    # "auto cmd" should still be unknown (was excluded)
    assert exc.value.code == 1, (
        f"E001 expected for excluded macro 'auto cmd', got code {exc.value.code}:\n{output}"
    )
    assert "auto cmd" in output or "E001" in output


def test_macro_paths_multiple_patterns(tmp_path):
    """--macro-paths with two patterns should discover macros matching either pattern."""
    mac_dir = tmp_path / "macros"
    mac_dir.mkdir()
    (mac_dir / "standard.mac").write_text(
        "!USER_ENTERED_COMMAND cdm standard\n", encoding="utf-8"
    )
    (mac_dir / "special.cmd").write_text(
        "!USER_ENTERED_COMMAND cdm special\n", encoding="utf-8"
    )

    cmd_file = tmp_path / "caller.cmd"
    cmd_file.write_text("cdm standard\ncdm special\n", encoding="utf-8")

    captured = io.StringIO()
    with patch("sys.argv", [
        "adams-cmd-lint",
        "--severity", "error",
        str(cmd_file),
        "--macro-base-dir", str(tmp_path),
        "--macro-paths", "macros/*.mac", "macros/*.cmd",
    ]):
        with pytest.raises(SystemExit) as exc:
            with patch("sys.stdout", captured):
                main()
    assert exc.value.code == 0, (
        f"Both commands should be found via two patterns, got:\n{captured.getvalue()}"
    )

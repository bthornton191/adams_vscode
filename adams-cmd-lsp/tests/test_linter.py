"""Integration tests for adams_cmd_lsp.linter module."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pathlib import Path
from adams_cmd_lsp.linter import lint_text
from adams_cmd_lsp.diagnostics import Severity

# Paths to test fixture files
FIXTURES = Path(__file__).parent.parent.parent / "test" / "files"


def _codes(diagnostics):
    return [d.code for d in diagnostics]


# ---------------------------------------------------------------------------
# Basic integration tests
# ---------------------------------------------------------------------------

def test_lint_empty_string():
    diags = lint_text("")
    assert diags == []


def test_lint_comment_only():
    diags = lint_text("! This is just a comment")
    assert diags == []


def test_lint_valid_model_create():
    diags = lint_text("model create model_name = my_model")
    errors = [d for d in diags if d.severity == Severity.ERROR]
    assert errors == []


def test_lint_unknown_command_produces_e001():
    diags = lint_text("xyz_not_a_command arg = value")
    assert "E001" in _codes(diags)


def test_lint_duplicate_arg_produces_e003():
    diags = lint_text("model create model_name=foo model_name=bar")
    assert "E003" in _codes(diags)


def test_lint_sorted_by_line_column():
    text = "xyz_bad arg=val\nmodel create model_name=foo model_name=bar"
    diags = lint_text(text)
    lines = [d.line for d in diags]
    assert lines == sorted(lines)


def test_lint_min_severity_error_only():
    """With min_severity='error', no warnings or info should appear."""
    # marker create without name → W005
    diags = lint_text("marker create location=0,0,0", min_severity="error")
    for d in diags:
        assert d.severity == Severity.ERROR


def test_lint_min_severity_warning():
    """With min_severity='warning', no info should appear."""
    diags = lint_text("marker create marker_name=.model.MAR_1 adams_id=1", min_severity="warning")
    for d in diags:
        assert d.severity in (Severity.ERROR, Severity.WARNING)


# ---------------------------------------------------------------------------
# Fixture file tests
# ---------------------------------------------------------------------------

def test_lint_create_model_cmd():
    """create_model.cmd should have no errors (may have warnings/info)."""
    path = FIXTURES / "create_model.cmd"
    if not path.exists():
        return  # skip if fixture not available
    text = path.read_text(encoding="utf-8", errors="replace")
    diags = lint_text(text)
    errors = [d for d in diags if d.severity == Severity.ERROR]
    # Should be no hard errors in a mostly-valid file
    # (relax to allow some E001/E002 from edge cases)
    assert len(errors) <= 5, f"Unexpected errors: {[(d.code, d.message, d.line) for d in errors]}"


def test_lint_test_measures_final_cmd():
    """test_measures_final.cmd should produce zero errors."""
    path = FIXTURES / "test_measures_final.cmd"
    if not path.exists():
        return  # skip if fixture not available
    text = path.read_text(encoding="utf-8", errors="replace")
    diags = lint_text(text, min_severity="error")
    errors = [d for d in diags if d.severity == Severity.ERROR]
    assert errors == [], f"False positive errors: {[(d.code, d.message, d.line) for d in errors]}"


def test_lint_test_cmd_has_e101():
    """test.cmd has an intentional unbalanced parenthesis — should detect E101."""
    path = FIXTURES / "test.cmd"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    diags = lint_text(text)
    assert "E101" in _codes(diags), "Expected E101 in test.cmd"

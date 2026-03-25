"""Tests for adams_cmd_lsp.rules module."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from adams_cmd_lsp.schema import Schema
from adams_cmd_lsp.parser import parse
from adams_cmd_lsp.symbols import build_symbol_table
from adams_cmd_lsp.rules import (
    rule_unknown_command,
    rule_invalid_argument,
    rule_duplicate_argument,
    rule_invalid_enum_value,
    rule_missing_required,
    rule_manual_adams_id,
    rule_exclusive_conflict,
    rule_unbalanced_parens,
    rule_unclosed_quote,
    rule_control_flow_balance,
    rule_type_mismatch,
)
from adams_cmd_lsp.diagnostics import Severity


SCHEMA = Schema.load()


def _lint(text, rule_fn=None, rules=None):
    """Parse text, build symbols, and run one or more rules."""
    stmts = parse(text)
    symbols = build_symbol_table(stmts, SCHEMA)
    diagnostics = []
    if rule_fn:
        diagnostics = rule_fn(stmts, SCHEMA, symbols)
    elif rules:
        for r in rules:
            diagnostics.extend(r(stmts, SCHEMA, symbols))
    return diagnostics


def _codes(diagnostics):
    return [d.code for d in diagnostics]


# ---------------------------------------------------------------------------
# E001 — Unknown command
# ---------------------------------------------------------------------------

def test_e001_known_command():
    diags = _lint("model create model_name = my_model", rule_fn=rule_unknown_command)
    assert "E001" not in _codes(diags)


def test_e001_unknown_command():
    diags = _lint("xyz create something = value", rule_fn=rule_unknown_command)
    assert "E001" in _codes(diags)


def test_e001_abbreviated_resolves():
    """'mar cre' should resolve to 'marker create' — no E001."""
    diags = _lint("mar cre marker_name = .model.MAR_1", rule_fn=rule_unknown_command)
    assert "E001" not in _codes(diags)


def test_e001_comment_ignored():
    diags = _lint("! this is a comment", rule_fn=rule_unknown_command)
    assert diags == []


def test_e001_blank_ignored():
    diags = _lint("\n\n", rule_fn=rule_unknown_command)
    assert diags == []


def test_e001_sets_resolved_key():
    """rule_unknown_command should set stmt.resolved_command_key as a side-effect."""
    stmts = parse("mar cre marker_name = .model.MAR_1")
    symbols = build_symbol_table(stmts, SCHEMA)
    rule_unknown_command(stmts, SCHEMA, symbols)
    cmd_stmts = [s for s in stmts if not s.is_blank and not s.is_comment]
    assert cmd_stmts[0].resolved_command_key == "marker create"


# ---------------------------------------------------------------------------
# E002 — Invalid argument
# ---------------------------------------------------------------------------

def test_e002_valid_arg():
    diags = _lint("model create model_name = my_model", rules=[rule_unknown_command, rule_invalid_argument])
    assert "E002" not in _codes(diags)


def test_e002_invalid_arg():
    diags = _lint("model create not_a_real_arg = value", rules=[rule_unknown_command, rule_invalid_argument])
    assert "E002" in _codes(diags)


def test_e002_abbreviated_arg():
    """Abbreviated argument that resolves → no E002."""
    diags = _lint("model create model_n = my_model", rules=[rule_unknown_command, rule_invalid_argument])
    assert "E002" not in _codes(diags)


# ---------------------------------------------------------------------------
# E003 — Duplicate argument
# ---------------------------------------------------------------------------

def test_e003_no_duplicates():
    diags = _lint(
        "part create rigid_body name_and_position part_name=.model.P1 location=0,0,0",
        rules=[rule_unknown_command, rule_duplicate_argument],
    )
    assert "E003" not in _codes(diags)


def test_e003_duplicate():
    diags = _lint(
        "model create model_name=foo model_name=bar",
        rules=[rule_unknown_command, rule_duplicate_argument],
    )
    assert "E003" in _codes(diags)


def test_e003_abbreviation_resolves_to_same():
    """Two abbreviations resolving to the same canonical arg → E003."""
    diags = _lint(
        "model create model_n=foo model_na=bar",
        rules=[rule_unknown_command, rule_duplicate_argument],
    )
    assert "E003" in _codes(diags)


# ---------------------------------------------------------------------------
# E004 — Invalid enum value
# ---------------------------------------------------------------------------

def test_e004_valid_enum():
    diags = _lint(
        "model merge model_name=my_model duplicate_parts=merge",
        rules=[rule_unknown_command, rule_invalid_enum_value],
    )
    assert "E004" not in _codes(diags)


def test_e004_invalid_enum():
    diags = _lint(
        "model merge model_name=my_model duplicate_parts=invalid_value",
        rules=[rule_unknown_command, rule_invalid_enum_value],
    )
    assert "E004" in _codes(diags)


def test_e004_runtime_expr_skipped():
    """Runtime expressions like $var or (eval(...)) should not be flagged."""
    diags = _lint(
        "model merge model_name=my_model duplicate_parts=$my_mode",
        rules=[rule_unknown_command, rule_invalid_enum_value],
    )
    assert "E004" not in _codes(diags)


# ---------------------------------------------------------------------------
# E005 / W005 — Missing required argument
# ---------------------------------------------------------------------------

def test_e005_required_present():
    diags = _lint(
        "model create model_name = my_model",
        rules=[rule_unknown_command, rule_missing_required],
    )
    assert "E005" not in _codes(diags)
    assert "W005" not in _codes(diags)


def test_w005_new_object_name_omitted():
    """Omitting a NDBWD_* required arg → W005, not E005."""
    # marker create requires marker_name (NDBWD_MARKER type)
    diags = _lint(
        "marker create location = 0,0,0",
        rules=[rule_unknown_command, rule_missing_required],
    )
    codes = _codes(diags)
    assert "W005" in codes
    assert "E005" not in codes


def test_adams_id_omitted_no_diagnostic():
    """Omitting adams_id should produce no diagnostic at all."""
    diags = _lint(
        "marker create marker_name = .model.MAR_1",
        rules=[rule_unknown_command, rule_missing_required],
    )
    assert "E005" not in _codes(diags)


def test_e005_exclusive_group_suppression():
    """Required arg suppressed because another group member is provided."""
    # marker create: orientation and along_axis_orientation are mutually exclusive
    # If along_axis_orientation is provided, orientation should NOT be flagged as missing
    diags = _lint(
        "marker create marker_name=.model.MAR_1 along_axis_orientation=1,0,0",
        rules=[rule_unknown_command, rule_missing_required],
    )
    codes = _codes(diags)
    # E005 for orientation should be suppressed
    assert not any("orientation" in d.message for d in diags if d.code == "E005")


# ---------------------------------------------------------------------------
# I006 — Manual Adams ID
# ---------------------------------------------------------------------------

def test_i006_adams_id_assigned():
    diags = _lint(
        "marker create marker_name=.model.MAR_1 adams_id=42",
        rules=[rule_unknown_command, rule_manual_adams_id],
    )
    assert "I006" in _codes(diags)


def test_i006_no_adams_id():
    diags = _lint(
        "marker create marker_name=.model.MAR_1",
        rules=[rule_unknown_command, rule_manual_adams_id],
    )
    assert "I006" not in _codes(diags)


# ---------------------------------------------------------------------------
# E006 — Mutual exclusion conflict
# ---------------------------------------------------------------------------

def test_e006_no_conflict():
    diags = _lint(
        "marker create marker_name=.model.MAR_1 orientation=0,0,0",
        rules=[rule_unknown_command, rule_exclusive_conflict],
    )
    assert "E006" not in _codes(diags)


def test_e006_conflict():
    diags = _lint(
        "marker create marker_name=.model.MAR_1 "
        "orientation=0,0,0 along_axis_orientation=1,0,0",
        rules=[rule_unknown_command, rule_exclusive_conflict],
    )
    assert "E006" in _codes(diags)


# ---------------------------------------------------------------------------
# E101 — Unbalanced parentheses
# ---------------------------------------------------------------------------

def test_e101_balanced():
    diags = _lint("var set var=x real=(eval(abs(1)))", rule_fn=rule_unbalanced_parens)
    assert "E101" not in _codes(diags)


def test_e101_unclosed():
    diags = _lint("var set var=x real=(eval(abs(1))", rule_fn=rule_unbalanced_parens)
    assert "E101" in _codes(diags)


def test_e101_extra_close():
    diags = _lint("var set var=x real=(eval(abs(1))))", rule_fn=rule_unbalanced_parens)
    assert "E101" in _codes(diags)


def test_e101_in_string_ignored():
    diags = _lint('model create model_name=x title="(unclosed in string"', rule_fn=rule_unbalanced_parens)
    assert "E101" not in _codes(diags)


# ---------------------------------------------------------------------------
# E102 — Unclosed quote
# ---------------------------------------------------------------------------

def test_e102_closed_quote():
    diags = _lint('model create model_name=x title="My Model"', rule_fn=rule_unclosed_quote)
    assert "E102" not in _codes(diags)


def test_e102_unclosed_quote():
    diags = _lint('model create model_name=x title="unclosed', rule_fn=rule_unclosed_quote)
    assert "E102" in _codes(diags)


def test_e102_no_quotes():
    diags = _lint("model create model_name=my_model", rule_fn=rule_unclosed_quote)
    assert "E102" not in _codes(diags)


# ---------------------------------------------------------------------------
# E104 — Control flow balance
# ---------------------------------------------------------------------------

def test_e104_balanced_if_end():
    text = "if condition = (x > 0)\nend"
    diags = _lint(text, rule_fn=rule_control_flow_balance)
    assert "E104" not in _codes(diags)


def test_e104_if_without_end():
    text = "if condition = (x > 0)"
    diags = _lint(text, rule_fn=rule_control_flow_balance)
    assert "E104" in _codes(diags)


def test_e104_end_without_if():
    text = "end"
    diags = _lint(text, rule_fn=rule_control_flow_balance)
    assert "E104" in _codes(diags)


def test_e104_else_without_if():
    text = "else"
    diags = _lint(text, rule_fn=rule_control_flow_balance)
    assert "E104" in _codes(diags)


def test_e104_nested_balanced():
    text = "if condition=(1)\n  if condition=(2)\n  end\nend"
    diags = _lint(text, rule_fn=rule_control_flow_balance)
    assert "E104" not in _codes(diags)


def test_e104_for_without_end():
    text = "for variable_name = i from = 1 to = 10"
    diags = _lint(text, rule_fn=rule_control_flow_balance)
    assert "E104" in _codes(diags)


def test_e104_for_end_balanced():
    text = "for variable_name = i from = 1 to = 10\nend"
    diags = _lint(text, rule_fn=rule_control_flow_balance)
    assert "E104" not in _codes(diags)


# ---------------------------------------------------------------------------
# E101 — Single-quoted string false-positive regression
# ---------------------------------------------------------------------------

def test_e101_no_false_positive_single_quoted_exclamation():
    """'!!' inside a single-quoted string must NOT trigger E101 (false-positive).

    The line 'var set var=.mdi.tmpstr str=(eval(str_print('HELLO WORLD!!')))' has
    balanced parentheses. Previously, _find_comment_start() treated '!!' as an
    inline comment, stripping the closing ')))' before the paren counter ran,
    which incorrectly produced an E101 diagnostic.
    """
    line = "var set var=.mdi.tmpstr str=(eval(str_print('HELLO WORLD!!')))"
    diags = _lint(line, rule_fn=rule_unbalanced_parens)
    assert "E101" not in _codes(diags)


def test_e101_single_quoted_parens_balanced():
    """Parens inside single-quoted string should not contribute to paren depth."""
    line = "var set var=.mdi.tmpstr str='(not a paren)'"
    diags = _lint(line, rule_fn=rule_unbalanced_parens)
    assert "E101" not in _codes(diags)


def test_e101_still_detects_real_unbalanced():
    """Genuine unbalanced parens outside any string are still flagged."""
    line = "model create model_name=(unclosed"
    diags = _lint(line, rule_fn=rule_unbalanced_parens)
    assert "E101" in _codes(diags)


# ---------------------------------------------------------------------------
# E101 — '!' as NOT operator / '!=' inside parentheses false-positive regressions
# ---------------------------------------------------------------------------

def test_e101_no_false_positive_not_operator_in_parens():
    """'!' as logical NOT inside parens must NOT trigger E101.

    'if condition=(eval(!DB_EXISTS(".part")))' has balanced parens.
    Previously, _find_comment_start() truncated at '!', stripping the
    closing ')))' and producing a false E101.
    """
    line = 'if condition=(eval(!DB_EXISTS(".part")))'
    diags = _lint(line, rule_fn=rule_unbalanced_parens)
    assert "E101" not in _codes(diags)


def test_e101_no_false_positive_not_equal_in_parens():
    """'!=' operator inside parens must NOT trigger E101.

    'if condition=(eval($oml_pitch != 0))' has balanced parens.
    Previously, _find_comment_start() truncated at '!=', leaving
    unclosed '(' and producing a false E101.
    """
    line = "if condition=(eval($oml_pitch != 0))"
    diags = _lint(line, rule_fn=rule_unbalanced_parens)
    assert "E101" not in _codes(diags)


def test_e101_no_false_positive_logical_and_before_not_operator():
    """'&&' before '!' inside nested parens must NOT trigger E101.

    'if condition=((eval("$x" == "yes") && !DB_EXISTS(".bp")))' is fully
    balanced. Previously, the '!' caused truncation after '&&', leaving
    two unclosed parens and producing a false E101.
    """
    line = 'if condition=((eval("$x" == "yes") && !DB_EXISTS(".bp")))'
    diags = _lint(line, rule_fn=rule_unbalanced_parens)
    assert "E101" not in _codes(diags)


# ---------------------------------------------------------------------------
# E006 — false positive: joint commands with both i_marker_name and j_marker_name
# ---------------------------------------------------------------------------

def test_e006_no_false_positive_joint_fixed_i_and_j_marker():
    """constraint create joint fixed with i_marker_name AND j_marker_name must NOT fire E006.

    These two args belong to different exclusive groups (i-side vs j-side).
    Previously the schema had a single 4-member group that incorrectly flagged
    this valid combination as a mutual exclusion conflict.
    """
    diags = _lint(
        "constraint create joint fixed &\n"
        "  joint_name = .model.JOINT_1 &\n"
        "  i_marker_name = .model.PART_1.MAR_1 &\n"
        "  j_marker_name = .model.PART_2.MAR_2",
        rules=[rule_unknown_command, rule_exclusive_conflict],
    )
    assert "E006" not in _codes(diags)


def test_e006_no_false_positive_joint_translational_i_and_j_marker():
    """constraint create joint translational with i_marker_name AND j_marker_name must NOT fire E006."""
    diags = _lint(
        "constraint create joint translational &\n"
        "  joint_name = .model.JOINT_1 &\n"
        "  i_marker_name = .model.PART_1.MAR_1 &\n"
        "  j_marker_name = .model.PART_2.MAR_2",
        rules=[rule_unknown_command, rule_exclusive_conflict],
    )
    assert "E006" not in _codes(diags)


def test_e006_no_false_positive_joint_revolute_i_and_j_marker():
    """constraint create joint revolute with i_marker_name AND j_marker_name must NOT fire E006."""
    diags = _lint(
        "constraint create joint revolute &\n"
        "  joint_name = .model.JOINT_1 &\n"
        "  i_marker_name = .model.PART_1.MAR_1 &\n"
        "  j_marker_name = .model.PART_2.MAR_2",
        rules=[rule_unknown_command, rule_exclusive_conflict],
    )
    assert "E006" not in _codes(diags)


def test_e006_still_fires_for_i_marker_and_i_part_conflict():
    """Providing both i_marker_name AND i_part_name on the same joint MUST fire E006.

    These two args are mutually exclusive (two ways to specify the I-side body).
    """
    diags = _lint(
        "constraint create joint fixed &\n"
        "  joint_name = .model.JOINT_1 &\n"
        "  i_marker_name = .model.PART_1.MAR_1 &\n"
        "  i_part_name = .model.PART_1 &\n"
        "  j_marker_name = .model.PART_2.MAR_2",
        rules=[rule_unknown_command, rule_exclusive_conflict],
    )
    assert "E006" in _codes(diags)


def test_e006_still_fires_for_j_marker_and_j_part_conflict():
    """Providing both j_marker_name AND j_part_name on the same joint MUST fire E006."""
    diags = _lint(
        "constraint create joint revolute &\n"
        "  joint_name = .model.JOINT_1 &\n"
        "  i_marker_name = .model.PART_1.MAR_1 &\n"
        "  j_marker_name = .model.PART_2.MAR_2 &\n"
        "  j_part_name = .model.PART_2",
        rules=[rule_unknown_command, rule_exclusive_conflict],
    )
    assert "E006" in _codes(diags)


# ---------------------------------------------------------------------------
# E005 — false positive: force create direct single_component_force with function=
# ---------------------------------------------------------------------------

def test_e005_no_false_positive_force_with_function_and_markers():
    """force create direct single_component_force with function= and i/j_marker_name must NOT fire E005.

    function= and user_function= are mutually exclusive (choose one form).
    i_marker_name and i_part_name are mutually exclusive (choose one form for I-side).
    j_marker_name and j_part_name are mutually exclusive (choose one form for J-side).
    Previously none of these had exclusive groups, so the linter fired E005 for
    user_function, i_part_name, and j_part_name even when valid alternatives were given.
    """
    diags = _lint(
        'force create direct single_component_force &\n'
        '  single_component_force_name = .model.SForce_1 &\n'
        '  adams_id = 1 &\n'
        '  i_marker_name = .model.Part_1.MAR_1 &\n'
        '  j_marker_name = .model.Part_2.MAR_2 &\n'
        '  action_only = off &\n'
        '  function = "0.0"',
        rules=[rule_unknown_command, rule_missing_required],
    )
    assert "E005" not in _codes(diags)


def test_e005_no_false_positive_differential_equation_with_function():
    """part create equation differential_equation with function= must NOT fire E005 for user_function."""
    diags = _lint(
        "part create equation differential_equation &\n"
        "  differential_equation_name = .model.DIFF_1 &\n"
        "  initial_condition = 0.0 &\n"
        '  function = "0.0"',
        rules=[rule_unknown_command, rule_missing_required],
    )
    e005_msgs = [d.message for d in diags if d.code == "E005"]
    assert not any("user_function" in m for m in e005_msgs)


def test_e005_no_false_positive_motion_generator_with_function():
    """constraint create motion_generator with function= must NOT fire E005 for user_function."""
    diags = _lint(
        "constraint create motion_generator &\n"
        "  motion_name = .model.MOT_1 &\n"
        "  i_marker_name = .model.PART_1.MAR_1 &\n"
        "  j_marker_name = .model.GROUND.MAR_G &\n"
        '  function = "0.0"',
        rules=[rule_unknown_command, rule_missing_required],
    )
    e005_msgs = [d.message for d in diags if d.code == "E005"]
    assert not any("user_function" in m for m in e005_msgs)


def test_e005_no_false_positive_variable_with_function():
    """data_element create variable with function= must NOT fire E005 for user_function."""
    diags = _lint(
        "data_element create variable &\n"
        "  variable_name = .model.VAR_1 &\n"
        '  function = "0.0"',
        rules=[rule_unknown_command, rule_missing_required],
    )
    e005_msgs = [d.message for d in diags if d.code == "E005"]
    assert not any("user_function" in m for m in e005_msgs)


# ---------------------------------------------------------------------------
# I202 — false positive: model_name without leading dot resolved as .model
# ---------------------------------------------------------------------------

def test_i202_no_false_positive_model_name_referenced_with_leading_dot():
    """Model created without leading dot, referenced with leading dot, must NOT fire I202.

    'model create model_name = model' stores 'model' in the symbol table.
    'simulation single_run transient model_name = .model' looks up '.model'.
    In Adams, 'model' and '.model' are the same path. The symbol table must
    normalize both to '.model' so the lookup succeeds.
    """
    from adams_cmd_lsp.rules import rule_type_mismatch
    text = (
        "model create model_name = model\n"
        "simulation single_run transient model_name = .model"
    )
    diags = _lint(text, rules=[rule_unknown_command, rule_type_mismatch])
    i202_diags = [d for d in diags if d.code == "I202" and ".model" in d.message]
    assert len(i202_diags) == 0

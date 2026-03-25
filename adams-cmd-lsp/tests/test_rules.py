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
    _types_compatible,
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


# ---------------------------------------------------------------------------
# W103 — dangling continuation '&' merging commands / at EOF
# ---------------------------------------------------------------------------

def test_w103_merged_commands_fires():
    """Two commands merged by a dangling '&' must produce W103, not E001.

    When a line ends with '&' but the NEXT line starts a new command instead
    of continuing the arguments, Adams sees the two command keywords run
    together as a single unknown key.  The linter must detect this split and
    emit W103 rather than E001.
    """
    from adams_cmd_lsp.rules import rule_unknown_command
    # Trailing '&' on first command causes merger into one statement with
    # a key that looks like two concatenated commands.
    text = (
        "model create model_name = .model1 &\n"
        "model create model_name = .model2\n"
    )
    diags = _lint(text, rules=[rule_unknown_command])
    codes = [d.code for d in diags]
    assert "W103" in codes, f"Expected W103 but got: {diags}"
    assert "E001" not in codes, f"E001 must not fire when W103 fires: {diags}"


def test_w103_merged_commands_message_identifies_both():
    """W103 message must name both merged commands."""
    from adams_cmd_lsp.rules import rule_unknown_command
    text = (
        "model create model_name = .model1 &\n"
        "model create model_name = .model2\n"
    )
    diags = _lint(text, rules=[rule_unknown_command])
    w103 = [d for d in diags if d.code == "W103"]
    assert len(w103) == 1
    msg = w103[0].message.lower()
    assert "model create" in msg or "merged" in msg


def test_w103_no_false_positive_on_valid_continuation():
    """A valid multi-line command with '&' must NOT trigger W103."""
    from adams_cmd_lsp.rules import rule_unknown_command
    text = (
        "part create rigid_body name_and_position &\n"
        "  part_name = .model.PART_1\n"
    )
    diags = _lint(text, rules=[rule_unknown_command])
    codes = [d.code for d in diags]
    assert "W103" not in codes, f"W103 must not fire for valid continuation: {diags}"
    assert "E001" not in codes, f"E001 must not fire for valid continuation: {diags}"


def test_w103_eof_dangling_continuation():
    """A trailing '&' at end-of-file must produce W103."""
    from adams_cmd_lsp.linter import lint_text
    text = "model create model_name = .model1 &\n"
    diags = lint_text(text)
    codes = [d.code for d in diags]
    assert "W103" in codes, f"Expected W103 for dangling & at EOF but got: {diags}"


def test_w103_eof_no_false_positive_without_trailing_amp():
    """A file that ends without '&' must NOT trigger the EOF W103."""
    from adams_cmd_lsp.linter import lint_text
    text = "model create model_name = .model1\n"
    diags = lint_text(text)
    codes = [d.code for d in diags]
    assert "W103" not in codes, f"W103 must not fire without trailing & at EOF: {diags}"


# ---------------------------------------------------------------------------
# E005 — false positive: translational_spring_damper with markers only
# ---------------------------------------------------------------------------

def test_e005_no_false_positive_spring_damper_with_markers_only():
    """Spring/damper with i_marker_name and j_marker_name must NOT fire E005
    for missing i_part_name / j_part_name.

    The user can provide markers OR parts (+ location/orientation), but not
    both for the same body.  The schema exclusive groups handle this.
    """
    text = (
        "force create element_like translational_spring_damper &\n"
        "    spring_damper_name = .model.spring &\n"
        "    i_marker_name = .model.part1.mkr1 &\n"
        "    j_marker_name = .model.part2.mkr2 &\n"
        "    stiffness = 10.0 &\n"
        "    damping = 0.1\n"
    )
    diags = _lint(text, rules=[rule_unknown_command, rule_missing_required])
    e005_diags = [d for d in diags if d.code == "E005"]
    assert len(e005_diags) == 0, f"E005 false positives: {e005_diags}"


def test_e006_spring_damper_conflict_i_marker_and_i_part():
    """Providing both i_marker_name and i_part_name for a spring/damper must fire E006."""
    text = (
        "force create element_like translational_spring_damper &\n"
        "    spring_damper_name = .model.spring &\n"
        "    i_marker_name = .model.part1.mkr1 &\n"
        "    i_part_name = .model.part1 &\n"
        "    j_marker_name = .model.part2.mkr2 &\n"
        "    stiffness = 10.0\n"
    )
    diags = _lint(text, rules=[rule_unknown_command, rule_exclusive_conflict])
    e006_diags = [d for d in diags if d.code == "E006"]
    assert len(e006_diags) == 1, f"Expected 1 E006 but got: {e006_diags}"


# ---------------------------------------------------------------------------
# Coupler: user_function not required; joint_name multi-value no I202
# ---------------------------------------------------------------------------

def test_e005_no_false_positive_coupler_without_user_function():
    """Coupler with motion_multipliers but no user_function must NOT fire E005.

    user_function is an optional alternative coupling expression; the normal
    usage is to supply motion_multipliers with no user_function.
    """
    text = (
        "constraint create complex_joint coupler &\n"
        "    coupler_name       = .model.coupler1 &\n"
        "    joint_name         = .model.rev1, .model.rev2 &\n"
        "    type_of_freedom    = rot_rot &\n"
        "    motion_multipliers = 1.0, -0.333\n"
    )
    diags = _lint(text, rules=[rule_unknown_command, rule_missing_required])
    e005_diags = [d for d in diags if d.code == "E005"]
    assert len(e005_diags) == 0, f"E005 false positives on coupler: {e005_diags}"


def test_i202_no_false_positive_coupler_joint_name_multi_value():
    """joint_name = .model.rev1, .model.rev2 must NOT fire I202.

    Coupler joint_name takes a comma-separated list of 2-3 joint names.
    The linter must not treat the whole string as a single reference.
    """
    text = (
        "constraint create complex_joint coupler &\n"
        "    coupler_name       = .model.coupler1 &\n"
        "    joint_name         = .model.rev1, .model.rev2 &\n"
        "    motion_multipliers = 1.0, -1.0\n"
    )
    diags = _lint(text, rules=[rule_unknown_command, rule_type_mismatch])
    i202_diags = [d for d in diags if d.code == "I202"]
    assert len(i202_diags) == 0, f"I202 false positives on coupler joint_name: {i202_diags}"


# ---------------------------------------------------------------------------
# motion_generator: markers not required when joint_name supplied; axis optional
# ---------------------------------------------------------------------------

def test_e005_no_false_positive_motion_generator_with_joint_name():
    """motion_generator with joint_name must NOT fire E005 for missing markers or axis.

    When joint_name is supplied, i_marker_name, j_marker_name, and axis are
    all irrelevant.
    """
    text = (
        "constraint create motion_generator &\n"
        "    motion_name     = .model.motion1 &\n"
        "    joint_name      = .model.rev1 &\n"
        "    type_of_freedom = rotational &\n"
        "    function        = \"HAVSIN(TIME, 0.0, 0.5, 0.0, 120D)\"\n"
    )
    diags = _lint(text, rules=[rule_unknown_command, rule_missing_required])
    e005_diags = [d for d in diags if d.code == "E005"]
    assert len(e005_diags) == 0, (
        f"E005 false positives on motion_generator with joint_name: {e005_diags}"
    )


def test_e005_no_false_positive_motion_generator_with_markers_no_axis():
    """motion_generator with markers but no axis must NOT fire E005 for axis.

    axis is optional when using markers.
    """
    text = (
        "constraint create motion_generator &\n"
        "    motion_name     = .model.motion1 &\n"
        "    i_marker_name   = .model.part1.mkr1 &\n"
        "    j_marker_name   = .model.part1.mkr2 &\n"
        "    type_of_freedom = rotational &\n"
        "    function        = \"HAVSIN(TIME, 0.0, 0.5, 0.0, 120D)\"\n"
    )
    diags = _lint(text, rules=[rule_unknown_command, rule_missing_required])
    e005_diags = [d for d in diags if d.code == "E005"]
    assert len(e005_diags) == 0, (
        f"E005 false positives on motion_generator axis: {e005_diags}"
    )


# ---------------------------------------------------------------------------
# E005 — part_name omission is an error, not a warning
# ---------------------------------------------------------------------------

def test_e005_part_name_omitted_fires_error_not_warning():
    """Omitting part_name on 'part create rigid_body' must fire E005, not W005.

    Adams does not auto-generate part names — omitting part_name causes an
    Adams error at runtime.
    """
    diags = _lint(
        "part create rigid_body name_and_position cm_position = 0.0, 0.0, 0.0",
        rules=[rule_unknown_command, rule_missing_required],
    )
    codes = _codes(diags)
    assert "E005" in codes, "Expected E005 for missing part_name"
    assert "W005" not in codes, "Got W005 but expected E005 for part_name"


def test_e005_part_name_provided_no_diagnostic():
    """Providing part_name on 'part create rigid_body' must NOT fire E005 or W005."""
    diags = _lint(
        "part create rigid_body name_and_position part_name = .model.part1",
        rules=[rule_unknown_command, rule_missing_required],
    )
    assert "E005" not in _codes(diags)
    assert "W005" not in _codes(diags)


def test_w005_still_fires_for_non_part_new_object():
    """Omitting marker_name (NDBWD_MARKER) must still fire W005, not E005.

    Only NDBWD_PART was escalated to E005; other auto-nameable objects keep W005.
    """
    diags = _lint(
        "marker create location = 0,0,0",
        rules=[rule_unknown_command, rule_missing_required],
    )
    codes = _codes(diags)
    assert "W005" in codes, "Expected W005 for missing marker_name"
    assert "E005" not in codes, "Got E005 but expected only W005 for marker_name"


# ---------------------------------------------------------------------------
# I202 — dynamic prefix suppression (eval expressions in loops)
# ---------------------------------------------------------------------------

def test_i202_suppressed_when_name_matches_eval_prefix():
    """Reference to a name created via (eval(...)) in a loop must NOT fire I202.

    The marker is created inside a for-loop with a name built by concatenation:
        marker_name = (eval(".model.mass_" // RTOI(i) // ".cm"))
    After the loop, a reference to .model.mass_1.cm must be suppressed because
    the linter knows a dynamic prefix '.model.mass_' was registered.
    """
    text = (
        "! Create markers in a loop\n"
        "for variable_name = i  start_value = 1  end_value = 3\n"
        "    marker create &\n"
        '        marker_name = (eval(".model.mass_" // RTOI(i) // ".cm")) &\n'
        "        location    = 0.0, 0.0, 0.0\n"
        "end\n"
        "! Reference a loop-created marker\n"
        "constraint create joint spherical &\n"
        "    joint_name    = .model.sph_fix &\n"
        "    i_marker_name = .model.mass_1.cm &\n"
        "    j_marker_name = .model.ground.anchor\n"
    )
    diags = _lint(text, rules=[rule_unknown_command, rule_type_mismatch])
    i202_diags = [d for d in diags if d.code == "I202"]
    # .model.mass_1.cm should be suppressed (matches dynamic prefix .model.mass_)
    suppressed = [d for d in i202_diags if ".model.mass_1.cm" in d.message]
    assert len(suppressed) == 0, (
        f"I202 should be suppressed for eval-created marker, got: {suppressed}"
    )


def test_i202_still_fires_for_unrelated_unresolved_reference():
    """I202 must still fire for references that don't match any dynamic prefix."""
    text = (
        "! Create markers in a loop with prefix .model.mass_\n"
        "for variable_name = i  start_value = 1  end_value = 3\n"
        "    marker create &\n"
        '        marker_name = (eval(".model.mass_" // RTOI(i) // ".cm")) &\n'
        "        location    = 0.0, 0.0, 0.0\n"
        "end\n"
        "! Reference a completely unrelated marker that was never defined\n"
        "constraint create joint spherical &\n"
        "    joint_name    = .model.sph_fix &\n"
        "    i_marker_name = .model.nonexistent_marker &\n"
        "    j_marker_name = .model.also_nonexistent\n"
    )
    diags = _lint(text, rules=[rule_unknown_command, rule_type_mismatch])
    i202_diags = [d for d in diags if d.code == "I202"]
    unrelated = [d for d in i202_diags if "nonexistent" in d.message or "also_nonexistent" in d.message]
    assert len(unrelated) > 0, (
        "I202 must still fire for references unrelated to any dynamic prefix"
    )


# ---------------------------------------------------------------------------
# Regression: spline inline data (file_name vs x/y exclusive groups)
# ---------------------------------------------------------------------------

def test_e005_no_false_positive_spline_inline_data():
    """Spline with inline x/y data should not require file_name (they are exclusive)."""
    text = (
        "data_element create spline &\n"
        "    spline_name = .model.my_spline &\n"
        "    x = -1.0, 0.0, 1.0, 2.0 &\n"
        "    y = 0.0, 1.0, 0.0, -1.0\n"
    )
    diags = _lint(text, rules=[rule_missing_required])
    e005_for_file = [d for d in diags if d.code == "E005" and "file_name" in d.message]
    assert len(e005_for_file) == 0, (
        f"E005 should not fire for file_name when x/y are provided, got: {e005_for_file}"
    )


def test_e005_no_false_positive_spline_with_file():
    """Spline with file_name should not require x or y (they are exclusive)."""
    text = (
        "data_element create spline &\n"
        "    spline_name = .model.my_spline &\n"
        '    file_name = "spline_data.csv"\n'
    )
    diags = _lint(text, rules=[rule_missing_required])
    e005_for_xy = [d for d in diags if d.code == "E005" and ("'x'" in d.message or "'y'" in d.message)]
    assert len(e005_for_xy) == 0, (
        f"E005 should not fire for x/y when file_name is provided, got: {e005_for_xy}"
    )


# ---------------------------------------------------------------------------
# Regression: general_force j_floating_marker_name vs j_part_name
# ---------------------------------------------------------------------------

def test_e005_no_false_positive_general_force_with_j_part_name():
    """general_force with j_part_name should not require j_floating_marker_name."""
    text = (
        "part create rigid_body name_and_position &\n"
        "    part_name = .model.part_1\n"
        "marker create &\n"
        "    marker_name = .model.part_1.i_marker &\n"
        "    location = 0.0, 0.0, 0.0\n"
        "marker create &\n"
        "    marker_name = .model.part_1.ref_marker &\n"
        "    location = 0.0, 0.0, 0.0\n"
        "force create direct general_force &\n"
        "    general_force_name = .model.gforce_1 &\n"
        "    i_marker_name = .model.part_1.i_marker &\n"
        "    j_part_name = .model.part_1 &\n"
        "    ref_marker_name = .model.part_1.ref_marker &\n"
        "    x_force_function = 0.0 &\n"
        "    y_force_function = 0.0 &\n"
        "    z_force_function = 0.0 &\n"
        "    x_torque_function = 0.0 &\n"
        "    y_torque_function = 0.0 &\n"
        "    z_torque_function = 0.0\n"
    )
    diags = _lint(text, rules=[rule_missing_required])
    e005_jfloat = [d for d in diags if d.code == "E005" and "j_floating_marker" in d.message]
    assert len(e005_jfloat) == 0, (
        f"E005 should not fire for j_floating_marker_name when j_part_name is provided, got: {e005_jfloat}"
    )


# ---------------------------------------------------------------------------
# Regression: user_function is optional on most force commands
# ---------------------------------------------------------------------------

def test_e005_no_false_positive_general_force_without_user_function():
    """general_force using built-in force functions should not require user_function."""
    text = (
        "part create rigid_body name_and_position &\n"
        "    part_name = .model.part_1\n"
        "marker create &\n"
        "    marker_name = .model.part_1.i_marker &\n"
        "    location = 0.0, 0.0, 0.0\n"
        "marker create &\n"
        "    marker_name = .model.part_1.ref_marker &\n"
        "    location = 0.0, 0.0, 0.0\n"
        "force create direct general_force &\n"
        "    general_force_name = .model.gforce_1 &\n"
        "    i_marker_name = .model.part_1.i_marker &\n"
        "    j_part_name = .model.part_1 &\n"
        "    ref_marker_name = .model.part_1.ref_marker &\n"
        "    x_force_function = 0.0 &\n"
        "    y_force_function = 0.0 &\n"
        "    z_force_function = 0.0 &\n"
        "    x_torque_function = 0.0 &\n"
        "    y_torque_function = 0.0 &\n"
        "    z_torque_function = 0.0\n"
    )
    diags = _lint(text, rules=[rule_missing_required])
    e005_uf = [d for d in diags if d.code == "E005" and "user_function" in d.message]
    assert len(e005_uf) == 0, (
        f"E005 should not fire for user_function when built-in functions are used, got: {e005_uf}"
    )


# ---------------------------------------------------------------------------
# Regression: Part used as Body (W201 type hierarchy)
# ---------------------------------------------------------------------------

def test_w201_no_false_positive_part_used_as_body():
    """A Part passed to a DB_BODY argument should not fire W201 (Part is-a Body)."""
    text = (
        "part create rigid_body name_and_position &\n"
        "    part_name = .model.part_1\n"
        "marker create &\n"
        "    marker_name = .model.part_1.i_marker &\n"
        "    location = 0.0, 0.0, 0.0\n"
        "marker create &\n"
        "    marker_name = .model.ground.j_marker &\n"
        "    location = 0.0, 0.0, 0.0\n"
        "marker create &\n"
        "    marker_name = .model.part_1.ref_marker &\n"
        "    location = 0.0, 0.0, 0.0\n"
        "force create direct general_force &\n"
        "    general_force_name = .model.gforce_1 &\n"
        "    i_marker_name = .model.part_1.i_marker &\n"
        "    j_part_name = .model.part_1 &\n"
        "    ref_marker_name = .model.part_1.ref_marker &\n"
        "    x_force_function = 0.0 &\n"
        "    y_force_function = 0.0 &\n"
        "    z_force_function = 0.0 &\n"
        "    x_torque_function = 0.0 &\n"
        "    y_torque_function = 0.0 &\n"
        "    z_torque_function = 0.0\n"
    )
    diags = _lint(text, rules=[rule_type_mismatch])
    w201_part = [d for d in diags if d.code == "W201" and ".model.part_1" in d.message]
    assert len(w201_part) == 0, (
        f"W201 should not fire when Part is passed where Body is expected, got: {w201_part}"
    )


def test_w201_still_fires_for_real_type_mismatch():
    """W201 should fire when a Marker is passed where Body is expected."""
    text = (
        "part create rigid_body name_and_position &\n"
        "    part_name = .model.part_1\n"
        "marker create &\n"
        "    marker_name = .model.part_1.some_marker &\n"
        "    location = 0.0, 0.0, 0.0\n"
        "marker create &\n"
        "    marker_name = .model.part_1.ref_marker &\n"
        "    location = 0.0, 0.0, 0.0\n"
        "force create direct general_force &\n"
        "    general_force_name = .model.gforce_1 &\n"
        "    i_marker_name = .model.part_1.some_marker &\n"
        "    j_part_name = .model.part_1.some_marker &\n"
        "    ref_marker_name = .model.part_1.ref_marker &\n"
        "    x_force_function = 0.0 &\n"
        "    y_force_function = 0.0 &\n"
        "    z_force_function = 0.0 &\n"
        "    x_torque_function = 0.0 &\n"
        "    y_torque_function = 0.0 &\n"
        "    z_torque_function = 0.0\n"
    )
    diags = _lint(text, rules=[rule_type_mismatch])
    w201_marker = [d for d in diags if d.code == "W201" and "Marker" in d.message and "Body" in d.message]
    assert len(w201_marker) > 0, (
        "W201 should fire when a Marker is passed where Body is expected"
    )


# ---------------------------------------------------------------------------
# Regression: single_component_force with action_only = on
# ---------------------------------------------------------------------------

def test_e005_no_false_positive_single_component_force_action_only():
    """action_only=on means no j-body; E005 must not fire for j_marker_name or j_part_name."""
    text = (
        "force create direct single_component_force &\n"
        "    single_component_force_name = .model.sf1 &\n"
        "    i_marker_name = .model.part_1.cm &\n"
        "    action_only = on &\n"
        "    function = 0.0\n"
    )
    diags = _lint(text, rule_fn=rule_missing_required)
    e005_j = [d for d in diags if d.code == "E005" and ("j_marker_name" in d.message or "j_part_name" in d.message)]
    assert len(e005_j) == 0, (
        f"E005 must not fire for j-body args when action_only=on, got: {e005_j}"
    )


def test_e005_still_fires_single_component_force_without_action_only():
    """Without action_only=on, j-body IS required; E005 must fire when omitted."""
    text = (
        "force create direct single_component_force &\n"
        "    single_component_force_name = .model.sf1 &\n"
        "    i_marker_name = .model.part_1.cm &\n"
        "    function = 0.0\n"
    )
    diags = _lint(text, rule_fn=rule_missing_required)
    e005_j = [d for d in diags if d.code == "E005" and ("j_marker_name" in d.message or "j_part_name" in d.message)]
    assert len(e005_j) > 0, (
        "E005 must fire for j-body args when action_only is not on"
    )


def test_e005_still_fires_single_component_force_action_only_off():
    """action_only=off (explicit) still requires j-body; E005 must fire when omitted."""
    text = (
        "force create direct single_component_force &\n"
        "    single_component_force_name = .model.sf1 &\n"
        "    i_marker_name = .model.part_1.cm &\n"
        "    action_only = off &\n"
        "    function = 0.0\n"
    )
    diags = _lint(text, rule_fn=rule_missing_required)
    e005_j = [d for d in diags if d.code == "E005" and ("j_marker_name" in d.message or "j_part_name" in d.message)]
    assert len(e005_j) > 0, (
        "E005 must fire for j-body args when action_only=off"
    )


# ---------------------------------------------------------------------------
# Regression: material create — poissons_ratio and youngs_modulus are NOT exclusive
# ---------------------------------------------------------------------------

def test_e006_no_false_positive_material_create_youngs_and_poissons():
    """youngs_modulus and poissons_ratio must both be providable; E006 must not fire."""
    text = (
        "material create &\n"
        "    material_name = .model.steel &\n"
        "    density = 7801.0 &\n"
        "    youngs_modulus = 2.07E+11 &\n"
        "    poissons_ratio = 0.29\n"
    )
    diags = _lint(text, rule_fn=rule_exclusive_conflict)
    e006 = [d for d in diags if d.code == "E006"]
    assert len(e006) == 0, (
        f"E006 must not fire for youngs_modulus + poissons_ratio together, got: {e006}"
    )


# ---------------------------------------------------------------------------
# Regression: interface field set — database_fields vs strings are exclusive
# ---------------------------------------------------------------------------

def test_e006_interface_field_set_database_fields_and_strings_conflict():
    """Providing both database_fields and strings must fire E006."""
    text = (
        "interface field set &\n"
        "    field_name = .gui.my_field &\n"
        '    database_fields = ".model.part_1" &\n'
        '    strings = "foo"\n'
    )
    diags = _lint(text, rule_fn=rule_exclusive_conflict)
    e006 = [d for d in diags if d.code == "E006"]
    assert len(e006) > 0, (
        "E006 must fire when both database_fields and strings are provided"
    )


def test_e006_interface_field_set_database_fields_only_no_conflict():
    """database_fields alone must not fire E006."""
    text = (
        "interface field set &\n"
        "    field_name = .gui.my_field &\n"
        '    database_fields = ".model.part_1"\n'
    )
    diags = _lint(text, rule_fn=rule_exclusive_conflict)
    e006 = [d for d in diags if d.code == "E006"]
    assert len(e006) == 0, (
        f"E006 must not fire for database_fields alone, got: {e006}"
    )


# ---------------------------------------------------------------------------
# Regression: quoted enum values must be accepted (no E004)
# ---------------------------------------------------------------------------

def test_e004_no_false_positive_quoted_enum_double_quotes():
    """icon_visibility=\"off\" (double-quoted) must be accepted as a valid enum value."""
    text = (
        'defaults attributes icon_visibility = "off"\n'
    )
    diags = _lint(text, rule_fn=rule_invalid_enum_value)
    e004 = [d for d in diags if d.code == "E004"]
    assert len(e004) == 0, (
        f"E004 must not fire for a quoted enum value, got: {e004}"
    )


def test_e004_no_false_positive_quoted_enum_single_quotes():
    """icon_visibility='on' (single-quoted) must be accepted as a valid enum value."""
    text = (
        "defaults attributes icon_visibility = 'on'\n"
    )
    diags = _lint(text, rule_fn=rule_invalid_enum_value)
    e004 = [d for d in diags if d.code == "E004"]
    assert len(e004) == 0, (
        f"E004 must not fire for a single-quoted enum value, got: {e004}"
    )


def test_e004_still_fires_for_invalid_quoted_enum():
    """A quoted but genuinely invalid enum value must still fire E004."""
    text = (
        'defaults attributes icon_visibility = "always_on"\n'
    )
    diags = _lint(text, rule_fn=rule_invalid_enum_value)
    e004 = [d for d in diags if d.code == "E004"]
    assert len(e004) > 0, (
        "E004 must still fire for an invalid value even when quoted"
    )


# ---------------------------------------------------------------------------
# xy_plots curve create — false-positive E005 tests
# ---------------------------------------------------------------------------

def test_e005_no_false_positive_xy_plots_curve_create_ddata():
    """Providing ddata must suppress E005 for all other dependent-axis args.

    Real-world pattern:
      xy_plot curve create curve=.plot_1.curve_1 create_page=no
          calculate_axis_limits=no ddata=... run=... auto_axis=UNITS
    Should produce zero E005 diagnostics.
    """
    text = (
        "xy_plots curve create curve_name=.plot_1.curve_1 "
        "create_page=no calculate_axis_limits=no "
        "ddata=.MODEL_1.Last_Run.Bearing_1.Ang_Disp "
        "run_name=.MODEL_1.Last_Run auto_axis=units\n"
    )
    diags = _lint(text, rule_fn=rule_missing_required)
    e005 = [d for d in diags if d.code == "E005"]
    assert len(e005) == 0, (
        f"E005 must not fire when ddata is provided, got: {e005}"
    )


def test_e005_no_false_positive_xy_plots_curve_create_vaxis_data():
    """Providing vaxis_data must suppress E005 for all other dependent-axis args."""
    text = (
        "xy_plots curve create curve_name=.plot_1.curve_1 "
        "vaxis_data=.MODEL_1.Last_Run.Bearing_1.Ang_Disp\n"
    )
    diags = _lint(text, rule_fn=rule_missing_required)
    e005 = [d for d in diags if d.code == "E005"]
    assert len(e005) == 0, (
        f"E005 must not fire when vaxis_data is provided, got: {e005}"
    )


def test_e005_no_false_positive_xy_plots_curve_create_plot_name_optional():
    """plot_name must not be required when curve_name path implies the plot."""
    text = (
        "xy_plots curve create curve_name=.plot_1.curve_1 "
        "ddata=.MODEL_1.Last_Run.Bearing_1.Ang_Disp\n"
    )
    diags = _lint(text, rule_fn=rule_missing_required)
    plot_name_e005 = [
        d for d in diags if d.code == "E005" and "plot_name" in d.message
    ]
    assert len(plot_name_e005) == 0, (
        f"plot_name must not be required (derivable from curve path), got: {plot_name_e005}"
    )


def test_e005_still_fires_xy_plots_curve_create_no_dependent_data():
    """E005 must fire when no dependent-axis argument is provided at all."""
    text = (
        "xy_plots curve create curve_name=.plot_1.curve_1 create_page=no\n"
    )
    diags = _lint(text, rule_fn=rule_missing_required)
    # At least one of the group members should be flagged as required
    dependent_axis_args = {
        "vaxis_data", "vmeasure", "y_expression_text", "y_values",
        "ddata", "dmeasure", "dexpression_text", "dvalues",
    }
    e005_args = {
        d.message.split("'")[1]
        for d in diags
        if d.code == "E005" and "'" in d.message
    }
    assert e005_args & dependent_axis_args, (
        f"At least one dependent-axis arg must be flagged when none are provided, "
        f"got E005 for: {e005_args}"
    )


# ---------------------------------------------------------------------------
# view management orient — must NOT fire E001 (command must be in schema)
# ---------------------------------------------------------------------------

def test_e001_no_false_positive_view_management_orient():
    """view management orient is a valid Adams command and must not fire E001."""
    text = (
        "view management orient view=.myview up_axis=Y_pos forward_axis=Z_neg\n"
    )
    diags = _lint(text, rule_fn=rule_unknown_command)
    e001 = [d for d in diags if d.code == "E001"]
    assert len(e001) == 0, (
        f"E001 must not fire for 'view management orient', got: {e001}"
    )


def test_e001_view_management_orient_abbreviated():
    """view management orient must be recognised when abbreviated (e.g. 'view man ori')."""
    text = "view man ori view=.myview up_axis=Y_pos\n"
    diags = _lint(text, rule_fn=rule_unknown_command)
    e001 = [d for d in diags if d.code == "E001"]
    assert len(e001) == 0, (
        f"E001 must not fire for abbreviated 'view man ori', got: {e001}"
    )


# ---------------------------------------------------------------------------
# data_element create matrix full — false-positive E005 for result_set_component_names
# ---------------------------------------------------------------------------

def test_e005_no_false_positive_matrix_full_inline_values():
    """Providing 'values' must suppress E005 for 'result_set_component_names'.

    Real-world pattern:
      data_element create matrix full matrix_name=.MAT1 row=1 col=3 value=1,2,3
    Should produce zero E005 diagnostics.
    """
    text = (
        "data_element create matrix full "
        "matrix_name=.MODEL.MAT1 values=1.0,2.0,3.0 units=length\n"
    )
    diags = _lint(text, rule_fn=rule_missing_required)
    e005 = [d for d in diags if d.code == "E005"]
    assert len(e005) == 0, (
        f"E005 must not fire when 'values' is provided, got: {e005}"
    )


def test_e005_no_false_positive_matrix_full_result_set():
    """Providing 'result_set_component_names' must suppress E005 for 'values'."""
    text = (
        "data_element create matrix full "
        "matrix_name=.MODEL.MAT1 "
        "result_set_component_names=.MODEL.Last_Run.Comp1\n"
    )
    diags = _lint(text, rule_fn=rule_missing_required)
    e005 = [d for d in diags if d.code == "E005"]
    assert len(e005) == 0, (
        f"E005 must not fire when 'result_set_component_names' is provided, got: {e005}"
    )


def test_e005_still_fires_matrix_full_no_data_source():
    """E005 must fire when neither 'values' nor 'result_set_component_names' is provided."""
    text = (
        "data_element create matrix full matrix_name=.MODEL.MAT1\n"
    )
    diags = _lint(text, rule_fn=rule_missing_required)
    data_args = {"values", "result_set_component_names"}
    e005_args = {
        d.message.split("'")[1]
        for d in diags
        if d.code == "E005" and "'" in d.message
    }
    assert e005_args & data_args, (
        f"E005 must fire for at least one data-source arg when none are provided, "
        f"got E005 for: {e005_args}"
    )


# ---------------------------------------------------------------------------
# i_marker_name / i_part_name / location exclusive-group tests
#
# Adams semantics: providing i_marker_name (an existing marker) is sufficient —
# the marker already encodes both the part and the location.  When i_marker_name
# is given, E005 must NOT fire for i_part_name or location, and vice versa.
# This pattern applies to higher_pair_contact, primitive joints, and element_like
# forces.
# ---------------------------------------------------------------------------

def test_e005_no_false_positive_higher_pair_point_curve_i_marker():
    """Providing i_marker_name on higher_pair_contact point_curve must suppress
    E005 for i_part_name AND location."""
    text = (
        "constraint create higher_pair_contact point_curve "
        "point_curve_name=.MODEL.pc1 curve_name=.MODEL.crv1 "
        "i_marker_name=.MODEL.part1.mkr1\n"
    )
    diags = _lint(text, rule_fn=rule_missing_required)
    bad = [d for d in diags if d.code == "E005" and
           any(n in d.message for n in ("i_part_name", "location"))]
    assert len(bad) == 0, (
        f"E005 must not fire for i_part_name or location when i_marker_name is "
        f"provided on higher_pair_contact point_curve, got: {bad}"
    )


def test_e005_no_false_positive_primitive_joint_inline_i_j_marker():
    """Providing i_marker_name and j_marker_name on a primitive joint must suppress
    E005 for i_part_name and j_part_name respectively."""
    text = (
        "constraint create primitive_joint inline "
        "joint_name=.MODEL.j1 "
        "i_marker_name=.MODEL.part1.mkr1 "
        "j_marker_name=.MODEL.part2.mkr2\n"
    )
    diags = _lint(text, rule_fn=rule_missing_required)
    bad = [d for d in diags if d.code == "E005" and
           any(n in d.message for n in ("i_part_name", "j_part_name"))]
    assert len(bad) == 0, (
        f"E005 must not fire for i_part_name or j_part_name when markers are "
        f"provided on primitive_joint inline, got: {bad}"
    )


def test_e005_no_false_positive_element_like_beam_i_j_marker():
    """Providing i_marker_name and j_marker_name on force element_like beam must
    suppress E005 for i_part_name and j_part_name."""
    text = (
        "force create element_like beam "
        "beam_name=.MODEL.beam1 "
        "i_marker_name=.MODEL.part1.mkr1 "
        "j_marker_name=.MODEL.part2.mkr2\n"
    )
    diags = _lint(text, rule_fn=rule_missing_required)
    bad = [d for d in diags if d.code == "E005" and
           any(n in d.message for n in ("i_part_name", "j_part_name"))]
    assert len(bad) == 0, (
        f"E005 must not fire for i_part_name or j_part_name when markers are "
        f"provided on force element_like beam, got: {bad}"
    )


def test_e005_no_false_positive_element_like_bushing_i_j_marker():
    """Providing i_marker_name and j_marker_name on force element_like bushing."""
    text = (
        "force create element_like bushing "
        "bushing_name=.MODEL.bush1 "
        "i_marker_name=.MODEL.part1.mkr1 "
        "j_marker_name=.MODEL.part2.mkr2\n"
    )
    diags = _lint(text, rule_fn=rule_missing_required)
    bad = [d for d in diags if d.code == "E005" and
           any(n in d.message for n in ("i_part_name", "j_part_name"))]
    assert len(bad) == 0, (
        f"E005 must not fire for i_part_name or j_part_name on bushing, got: {bad}"
    )


# ===========================================================================
# Tests for this session's fixes
# ===========================================================================

# ---------------------------------------------------------------------------
# I202 — Built-in symbols must not fire I202
# ---------------------------------------------------------------------------

def test_i202_no_false_positive_ground_builtin():
    """'ground' (bare, no model prefix) must not fire I202."""
    text = (
        "marker create marker_name=.model.ground.cm "
        "adams_id=1 part_name=ground\n"
    )
    diags = _lint(text, rule_fn=rule_type_mismatch)
    i202 = [d for d in diags if d.code == "I202" and "ground" in d.message.lower()]
    assert len(i202) == 0, f"I202 must not fire for built-in 'ground', got: {i202}"


def test_i202_no_false_positive_model_qualified_ground():
    """.MODEL_1.ground and .MODEL_1.ground.mkr must not fire I202 (ground is a builtin part)."""
    from adams_cmd_lsp.symbols import SymbolTable
    from adams_cmd_lsp.parser import parse as _parse
    # Test that the path component suppression works for both .MODEL_1.ground
    # and .MODEL_1.ground.mkr (a marker on ground)
    text = (
        "constraint create joint fixed "
        "joint_name=.model.j1 "
        "i_marker_name=.model.part1.mkr1 "
        "j_marker_name=.MODEL_1.ground.mkr\n"
    )
    stmts = _parse(text)
    sym = SymbolTable()
    sym.register(".model.part1.mkr1", "Marker", 0)
    sym.register(".model.j1", "Joint", 0)
    # .MODEL_1.ground.mkr is NOT registered — but it should be suppressed because
    # 'ground' appears as a path component.
    diags = rule_type_mismatch(stmts, SCHEMA, sym)
    i202_ground = [d for d in diags if d.code == "I202" and "ground" in d.message.lower()]
    assert len(i202_ground) == 0, (
        f"I202 must not fire for paths containing 'ground' as a component, got: {i202_ground}"
    )


def test_i202_no_false_positive_color_constants():
    """Built-in color names RED, GREEN, BLUE, etc. must not fire I202."""
    # Use defaults attributes which takes a color argument
    for color in ["RED", "GREEN", "BLUE", "WHITE", "BLACK", "YELLOW", "CYAN", "MAIZE"]:
        text = f"defaults attributes color = {color}\n"
        diags = _lint(text, rule_fn=rule_type_mismatch)
        i202 = [d for d in diags if d.code == "I202" and color.lower() in d.message.lower()]
        assert len(i202) == 0, (
            f"I202 must not fire for built-in color '{color}', got: {i202}"
        )


def test_i202_no_false_positive_materials_library():
    """.materials.steel must not fire I202 (built-in materials library)."""
    # part modify with material_type referencing the built-in materials library
    text = "part modify rigid_body name_and_position part_name=.model.p1 material_type=.materials.steel\n"
    diags = _lint(text, rule_fn=rule_type_mismatch)
    i202_mat = [d for d in diags if d.code == "I202" and ".materials." in d.message]
    assert len(i202_mat) == 0, (
        f"I202 must not fire for .materials.* references, got: {i202_mat}"
    )


def test_i202_no_false_positive_color_r_string():
    """COLOR_R...G...B... custom color strings must not fire I202."""
    text = 'defaults attributes color = "COLOR_R128G64B255"\n'
    diags = _lint(text, rule_fn=rule_type_mismatch)
    i202 = [d for d in diags if d.code == "I202" and "COLOR_R" in d.message.upper()]
    assert len(i202) == 0, (
        f"I202 must not fire for COLOR_R...G...B... custom color strings, got: {i202}"
    )


# ---------------------------------------------------------------------------
# W201 — Type widening: Part/Marker used as Rframe/Triad/Force/etc.
# ---------------------------------------------------------------------------

def test_w201_no_false_positive_part_as_rframe():
    """A Part passed where Rframe is expected must NOT fire W201 (Part is-a Rframe)."""
    from adams_cmd_lsp.symbols import SymbolTable
    from adams_cmd_lsp.parser import parse as _parse
    # Build a minimal symbol table with a Part
    sym = SymbolTable()
    sym.register(".model.p1", "Part", 0)
    # Simulate a command that expects Rframe for some argument by checking type compatibility
    assert _types_compatible("Part", "Rframe"), "Part must be compatible with Rframe"


def test_w201_no_false_positive_marker_as_triad():
    """A Marker passed where Triad is expected must NOT fire W201 (Marker is-a Triad)."""
    assert _types_compatible("Marker", "Triad"), "Marker must be compatible with Triad"


def test_w201_no_false_positive_marker_as_position():
    """A Marker passed where Position is expected must NOT fire W201."""
    assert _types_compatible("Marker", "Position"), "Marker must be compatible with Position"


def test_w201_no_false_positive_sforce_as_force():
    """An Sforce passed where Force is expected must NOT fire W201."""
    assert _types_compatible("Sforce", "Force"), "Sforce must be compatible with Force"


def test_w201_no_false_positive_vforce_as_force():
    """A Vforce passed where Force is expected must NOT fire W201."""
    assert _types_compatible("Vforce", "Force"), "Vforce must be compatible with Force"


def test_w201_no_false_positive_bushing_as_force():
    """A Bushing passed where Force is expected must NOT fire W201."""
    assert _types_compatible("Bushing", "Force"), "Bushing must be compatible with Force"


def test_w201_no_false_positive_spring_as_force():
    """A Spring passed where Force is expected must NOT fire W201."""
    assert _types_compatible("Spring", "Force"), "Spring must be compatible with Force"


def test_w201_no_false_positive_mea_object_as_measure():
    """A Mea_object passed where Measure is expected must NOT fire W201."""
    assert _types_compatible("Mea_object", "Measure"), "Mea_object must be compatible with Measure"


def test_w201_no_false_positive_run_as_mechanism():
    """A Run passed where Mechanism is expected must NOT fire W201."""
    assert _types_compatible("Run", "Mechanism"), "Run must be compatible with Mechanism"


def test_w201_type_widening_is_case_insensitive():
    """Type compatibility check must be case-insensitive."""
    assert _types_compatible("part", "RFRAME"), "part (lower) must be compatible with RFRAME"
    assert _types_compatible("MARKER", "triad"), "MARKER must be compatible with triad (lower)"


# ---------------------------------------------------------------------------
# E006 — False positives: contact create stiffness+damping together
# ---------------------------------------------------------------------------

def test_e006_no_false_positive_contact_create_stiffness_and_damping():
    """contact create with stiffness AND damping together must NOT fire E006.

    Previously these were in a false exclusive group. Penalty-method contact
    requires both stiffness and damping simultaneously.
    """
    text = (
        "contact create contact_name=.model.CONTACT_1 "
        "i_geometry_name=.model.part1.geom1 "
        "j_geometry_name=.model.part2.geom2 "
        "stiffness=1.0E+5 damping=10.0 exponent=2.2 dmax=0.01\n"
    )
    diags = _lint(text, rules=[rule_unknown_command, rule_exclusive_conflict])
    e006 = [d for d in diags if d.code == "E006"]
    assert len(e006) == 0, (
        f"E006 must not fire for contact stiffness+damping+exponent+dmax together, got: {e006}"
    )


def test_e006_no_false_positive_contact_create_friction_params():
    """contact create with mu_static, mu_dynamic, and coulomb_friction together must NOT fire E006."""
    text = (
        "contact create contact_name=.model.CONTACT_1 "
        "i_geometry_name=.model.part1.geom1 "
        "j_geometry_name=.model.part2.geom2 "
        "stiffness=1.0E+5 damping=10.0 "
        "coulomb_friction=on mu_static=0.3 mu_dynamic=0.25\n"
    )
    diags = _lint(text, rules=[rule_unknown_command, rule_exclusive_conflict])
    e006 = [d for d in diags if d.code == "E006"]
    assert len(e006) == 0, (
        f"E006 must not fire for contact friction params together, got: {e006}"
    )


def test_e006_no_false_positive_part_copy_part_name_and_new_part_name():
    """part copy with both part_name and new_part_name must NOT fire E006.

    Both args are required simultaneously — they specify source and destination.
    """
    text = (
        "part copy part_name=.model.part1 new_part_name=.model.part1_copy\n"
    )
    diags = _lint(text, rules=[rule_unknown_command, rule_exclusive_conflict])
    e006 = [d for d in diags if d.code == "E006"]
    assert len(e006) == 0, (
        f"E006 must not fire for part copy part_name + new_part_name, got: {e006}"
    )


# ---------------------------------------------------------------------------
# E005 — False positives: section create cross-section dimensions
# ---------------------------------------------------------------------------

def test_e005_no_false_positive_section_create_cyl_radius():
    """section create circular with only cyl_radius must NOT fire E005.

    All other cross-section dimension types (ib_*, rect_*, etc.) should NOT
    be required when cyl_radius is provided.
    """
    text = (
        "geometry create shape section "
        "section_name=.model.section1 cyl_radius=0.01\n"
    )
    diags = _lint(text, rules=[rule_unknown_command, rule_missing_required])
    # Cross-section dimension args should not all be flagged
    cross_section_args = {"ib_height", "ib_base", "ib_flange", "ib_web",
                          "rect_height", "rect_base", "major_radius", "minor_radius"}
    e005_cross = [d for d in diags if d.code == "E005" and
                  any(a in d.message for a in cross_section_args)]
    assert len(e005_cross) == 0, (
        f"E005 must not fire for other cross-section dims when cyl_radius is provided, got: {e005_cross}"
    )


def test_e005_no_false_positive_section_create_rect():
    """section create rectangular with rect_height and rect_base must NOT fire E005 for cyl_radius."""
    text = (
        "geometry create shape section "
        "section_name=.model.section1 rect_height=0.02 rect_base=0.01\n"
    )
    diags = _lint(text, rules=[rule_unknown_command, rule_missing_required])
    e005_cyl = [d for d in diags if d.code == "E005" and "cyl_radius" in d.message]
    assert len(e005_cyl) == 0, (
        f"E005 must not fire for cyl_radius when rect dimensions are provided, got: {e005_cyl}"
    )


# ---------------------------------------------------------------------------
# E005 — False positives: geometry create shape force attachment alternatives
# ---------------------------------------------------------------------------

def test_e005_no_false_positive_geometry_create_shape_force_joint_name():
    """geometry create shape force with joint_name must NOT fire E005 for the other attachment args."""
    text = (
        "geometry create shape force "
        "force_name=.model.force_geom1 "
        "joint_name=.model.j1\n"
    )
    diags = _lint(text, rules=[rule_unknown_command, rule_missing_required])
    attachment_args = {"jprim_name", "curve_curve_name", "point_curve_name"}
    e005_attach = [d for d in diags if d.code == "E005" and
                   any(a in d.message for a in attachment_args)]
    assert len(e005_attach) == 0, (
        f"E005 must not fire for other attachment args when joint_name is given, got: {e005_attach}"
    )


def test_e005_no_false_positive_geometry_create_shape_force_jprim_name():
    """geometry create shape force with jprim_name must NOT fire E005 for joint_name."""
    text = (
        "geometry create shape force "
        "force_name=.model.force_geom1 "
        "jprim_name=.model.jprim1\n"
    )
    diags = _lint(text, rules=[rule_unknown_command, rule_missing_required])
    e005_joint = [d for d in diags if d.code == "E005" and "joint_name" in d.message]
    assert len(e005_joint) == 0, (
        f"E005 must not fire for joint_name when jprim_name is provided, got: {e005_joint}"
    )


# ---------------------------------------------------------------------------
# E005 — False positives: clearance create i_flex vs i_geometry
# ---------------------------------------------------------------------------

def test_e005_no_false_positive_clearance_create_with_i_flex():
    """clearance create with i_flex must NOT fire E005 for i_geometry and i_part.

    i_flex is in mutually exclusive groups with i_geometry and i_part —
    providing i_flex means the other two are not needed.
    Similarly j_flex is in exclusive groups with j_geometry and j_part.
    """
    text = (
        "clearance create clearance_name=.model.CLEARANCE_1 "
        "i_flex=.model.flex1 j_flex=.model.flex2\n"
    )
    diags = _lint(text, rules=[rule_unknown_command, rule_missing_required])
    e005_geom = [d for d in diags if d.code == "E005" and
                 any(a in d.message for a in ("i_geometry", "i_part", "j_geometry", "j_part"))]
    assert len(e005_geom) == 0, (
        f"E005 must not fire for i/j_geometry or i/j_part when i/j_flex is given, got: {e005_geom}"
    )


# ---------------------------------------------------------------------------
# E004 — Comma-separated lists of valid enum values must be accepted
# ---------------------------------------------------------------------------

def test_e004_no_false_positive_comma_separated_on_off():
    """visibility_between_markers = 'on, on' must NOT fire E004.

    Adams allows comma-separated lists of on/off for multi-marker visibility.
    """
    text = (
        "curve create curve_name=.model.curve1 "
        "visibility_between_markers='on, on'\n"
    )
    diags = _lint(text, rules=[rule_unknown_command, rule_invalid_enum_value])
    e004 = [d for d in diags if d.code == "E004" and "visibility_between_markers" in d.message]
    assert len(e004) == 0, (
        f"E004 must not fire for comma-separated 'on, on' list, got: {e004}"
    )


def test_e004_comma_list_all_valid_enum_values():
    """A comma-separated list where every element is a valid enum must pass E004."""
    # Test via the type compatibility logic directly with a known enum arg
    # If the schema has an on/off enum, "on, on" should pass
    from adams_cmd_lsp.rules import rule_invalid_enum_value
    from adams_cmd_lsp.parser import parse as _parse
    stmts = _parse("defaults attributes visibility = on\n")
    sym = __import__("adams_cmd_lsp.symbols", fromlist=["build_symbol_table"]).build_symbol_table(stmts, SCHEMA)
    diags = rule_invalid_enum_value(stmts, SCHEMA, sym)
    e004 = [d for d in diags if d.code == "E004"]
    assert len(e004) == 0, f"E004 must not fire for valid single enum 'on', got: {e004}"


def test_e004_no_false_positive_catiav4_type():
    """file geometry write type_of_geometry=catiav4 must NOT fire E004."""
    text = "file geometry write file_name=test.CATPart type_of_geometry=catiav4\n"
    diags = _lint(text, rules=[rule_unknown_command, rule_invalid_enum_value])
    e004 = [d for d in diags if d.code == "E004" and "catiav4" in d.message.lower()]
    assert len(e004) == 0, (
        f"E004 must not fire for type_of_geometry=catiav4, got: {e004}"
    )


def test_e004_no_false_positive_catiav5_type():
    """file geometry write type_of_geometry=catiav5 must NOT fire E004."""
    text = "file geometry write file_name=test.CATProduct type_of_geometry=catiav5\n"
    diags = _lint(text, rules=[rule_unknown_command, rule_invalid_enum_value])
    e004 = [d for d in diags if d.code == "E004" and "catiav5" in d.message.lower()]
    assert len(e004) == 0, (
        f"E004 must not fire for type_of_geometry=catiav5, got: {e004}"
    )


def test_e004_no_false_positive_acis_type():
    """file geometry write type_of_geometry=acis must NOT fire E004."""
    text = "file geometry write file_name=test.sat type_of_geometry=acis\n"
    diags = _lint(text, rules=[rule_unknown_command, rule_invalid_enum_value])
    e004 = [d for d in diags if d.code == "E004" and "acis" in d.message.lower()]
    assert len(e004) == 0, (
        f"E004 must not fire for type_of_geometry=acis, got: {e004}"
    )


def test_e004_no_false_positive_vda_type():
    """file geometry write type_of_geometry=vda must NOT fire E004."""
    text = "file geometry write file_name=test.vda type_of_geometry=vda\n"
    diags = _lint(text, rules=[rule_unknown_command, rule_invalid_enum_value])
    e004 = [d for d in diags if d.code == "E004" and "vda" in d.message.lower()]
    assert len(e004) == 0, (
        f"E004 must not fire for type_of_geometry=vda, got: {e004}"
    )


# ---------------------------------------------------------------------------
# Batch-3 tests
# ---------------------------------------------------------------------------

# E006 — false exclusive groups removed

def test_e006_no_false_positive_marker_vx_vy_vz():
    """marker modify vx=1 vy=2 vz=3 must NOT fire E006 (vx/vy/vz are NOT exclusive)."""
    text = "marker modify marker=.m.p.m1 vx=1 vy=2 vz=3\n"
    diags = _lint(text, rule_fn=rule_exclusive_conflict)
    e006 = [d for d in diags if d.code == "E006"]
    assert len(e006) == 0, f"E006 must not fire for vx/vy/vz together, got: {e006}"


def test_e006_no_false_positive_contact_flip_normal():
    """contact modify i_flip_normal=no j_flip_normal=yes must NOT fire E006."""
    text = 'contact modify contact_name=c1 i_flip_normal="no" j_flip_normal="yes"\n'
    diags = _lint(text, rule_fn=rule_exclusive_conflict)
    e006 = [d for d in diags if d.code == "E006"]
    assert len(e006) == 0, f"E006 must not fire for i/j_flip_normal together, got: {e006}"


def test_e006_no_false_positive_ptemplate_height_width():
    """ptemplate create height=10 width=20 must NOT fire E006."""
    text = "ptemplate create ptemplate_name=pt1 height=10 width=20\n"
    diags = _lint(text, rule_fn=rule_exclusive_conflict)
    e006 = [d for d in diags if d.code == "E006"]
    assert len(e006) == 0, f"E006 must not fire for height/width together, got: {e006}"


def test_e006_no_false_positive_file_iges_write_analysis_frame():
    """file iges write analysis_name=run1 frame_number=5 must NOT fire E006."""
    text = 'file iges write file_name="out.igs" analysis_name=run1 frame_number=5\n'
    diags = _lint(text, rule_fn=rule_exclusive_conflict)
    e006 = [d for d in diags if d.code == "E006"]
    assert len(e006) == 0, f"E006 must not fire for analysis_name/frame_number together, got: {e006}"


def test_e006_no_false_positive_mnfxform_pl_points():
    """file mnfxform mirror pl_point_1/2/3 together must NOT fire E006."""
    text = (
        "file mnfxform mirror modal_neutral_file_name=f.mnf output_file_type=mnf "
        "output_file_name=out.mnf pl_point_1=0,0,0 pl_point_2=1,0,0 pl_point_3=0,1,0\n"
    )
    diags = _lint(text, rule_fn=rule_exclusive_conflict)
    e006 = [d for d in diags if d.code == "E006"]
    assert len(e006) == 0, f"E006 must not fire for pl_point_1/2/3 together, got: {e006}"


# E005 — exclusive attachment alternatives in geometry create shape force

def test_e005_no_false_positive_geometry_shape_force_with_joint():
    """geometry create shape force with joint_name should not fire E005 for jprim/curve args."""
    text = (
        "geometry create shape force "
        "force_name=.m.gf1 force_element_name=.m.f1 "
        "joint_name=.m.j1 applied_at_marker_name=.m.p.m1\n"
    )
    diags = _lint(text, rules=[rule_unknown_command, rule_missing_required])
    e005 = [d for d in diags if d.code == "E005"]
    assert len(e005) == 0, f"E005 must not fire when joint_name is provided, got: {e005}"


def test_e005_no_false_positive_file_parasolid_read_part_name():
    """file parasolid read with part_name should not fire E005 for fe_part_name."""
    text = (
        'file parasolid read file_name="test.x_t" model_name=.m part_name=.m.p1\n'
    )
    diags = _lint(text, rules=[rule_unknown_command, rule_missing_required])
    e005 = [d for d in diags if d.code == "E005" and "fe_part_name" in d.message]
    assert len(e005) == 0, f"E005 for fe_part_name must not fire when part_name given, got: {e005}"


def test_e005_no_false_positive_file_parasolid_read_fe_part_name():
    """file parasolid read with fe_part_name should not fire E005 for part_name."""
    text = (
        'file parasolid read file_name="test.x_t" model_name=.m fe_part_name=.m.flex1\n'
    )
    diags = _lint(text, rules=[rule_unknown_command, rule_missing_required])
    e005 = [d for d in diags if d.code == "E005" and "part_name" in d.message]
    assert len(e005) == 0, f"E005 for part_name must not fire when fe_part_name given, got: {e005}"


def test_e005_no_false_positive_file_iges_write_with_analysis():
    """file iges write with only analysis_name should not fire E005 for frame_number."""
    text = 'file iges write file_name="out.igs" analysis_name=run1\n'
    diags = _lint(text, rules=[rule_unknown_command, rule_missing_required])
    e005 = [d for d in diags if d.code == "E005" and "frame_number" in d.message]
    assert len(e005) == 0, f"E005 for frame_number must not fire when analysis_name given, got: {e005}"


# E004 — new enum values and comma-list support

def test_e004_no_false_positive_mode_result():
    """interface plot panel mode_set mode=result must NOT fire E004."""
    text = "interface plot panel mode_set mode=result\n"
    diags = _lint(text, rules=[rule_unknown_command, rule_invalid_enum_value])
    e004 = [d for d in diags if d.code == "E004"]
    assert len(e004) == 0, f"E004 must not fire for mode=result, got: {e004}"


def test_e004_no_false_positive_mode_measure():
    """interface plot panel mode_set mode=measure must NOT fire E004."""
    text = "interface plot panel mode_set mode=measure\n"
    diags = _lint(text, rules=[rule_unknown_command, rule_invalid_enum_value])
    e004 = [d for d in diags if d.code == "E004"]
    assert len(e004) == 0, f"E004 must not fire for mode=measure, got: {e004}"


def test_e004_no_false_positive_mode_object():
    """interface plot panel mode_set mode=object must NOT fire E004."""
    text = "interface plot panel mode_set mode=object\n"
    diags = _lint(text, rules=[rule_unknown_command, rule_invalid_enum_value])
    e004 = [d for d in diags if d.code == "E004"]
    assert len(e004) == 0, f"E004 must not fire for mode=object, got: {e004}"


def test_e004_no_false_positive_technique_box_behnken():
    """optimize design_of_experiments technique=box_behnken must NOT fire E004."""
    text = (
        "optimize design_of_experiments "
        "design_study_name=.ds technique=box_behnken\n"
    )
    diags = _lint(text, rules=[rule_unknown_command, rule_invalid_enum_value])
    e004 = [d for d in diags if d.code == "E004" and "technique" in d.message]
    assert len(e004) == 0, f"E004 must not fire for technique=box_behnken, got: {e004}"


def test_e004_no_false_positive_technique_casewise():
    """optimize design_of_experiments technique=casewise must NOT fire E004."""
    text = (
        "optimize design_of_experiments "
        "design_study_name=.ds technique=casewise\n"
    )
    diags = _lint(text, rules=[rule_unknown_command, rule_invalid_enum_value])
    e004 = [d for d in diags if d.code == "E004" and "technique" in d.message]
    assert len(e004) == 0, f"E004 must not fire for technique=casewise, got: {e004}"


def test_e004_no_false_positive_units_length():
    """numeric_results create values units=length must NOT fire E004."""
    text = (
        "numeric_results create values "
        "new_result_set_component_name=.m.run.x values=1,2,3 units=length\n"
    )
    diags = _lint(text, rules=[rule_unknown_command, rule_invalid_enum_value])
    e004 = [d for d in diags if d.code == "E004" and "units" in d.message]
    assert len(e004) == 0, f"E004 must not fire for units=length, got: {e004}"


def test_e004_no_false_positive_pattern_comma_separated_yn():
    """pattern=y,n,y,n must NOT fire E004 (each element is prefix of yes/no)."""
    # Find a command that uses pattern arg - use variable set with pattern
    # Use a command with pattern array arg
    text = (
        "simulation single_step_size step_size=0.01 number_of_steps=4 "
        "pattern=y,n,y,n\n"
    )
    diags = _lint(text, rules=[rule_unknown_command, rule_invalid_enum_value])
    e004 = [d for d in diags if d.code == "E004" and "pattern" in d.message]
    assert len(e004) == 0, f"E004 must not fire for pattern=y,n,y,n, got: {e004}"


def test_e004_no_false_positive_toggle_active():
    """entity attributes active=toggle must NOT fire E004."""
    text = "entity attributes entity=.m.p1 active=toggle\n"
    diags = _lint(text, rules=[rule_unknown_command, rule_invalid_enum_value])
    e004 = [d for d in diags if d.code == "E004" and "active" in d.message]
    assert len(e004) == 0, f"E004 must not fire for active=toggle, got: {e004}"


# E001 — stub commands now recognized

def test_e001_no_false_positive_mdi_modify_macro():
    """mdi modify_macro must NOT fire E001 (stub added to schema)."""
    text = 'mdi modify_macro macro_name=test commands="foo"\n'
    diags = _lint(text, rule_fn=rule_unknown_command)
    e001 = [d for d in diags if d.code == "E001"]
    assert len(e001) == 0, f"E001 must not fire for mdi modify_macro, got: {e001}"


def test_e001_no_false_positive_snapshot():
    """snapshot must NOT fire E001 (stub added to schema)."""
    text = "snapshot file=snap.png\n"
    diags = _lint(text, rule_fn=rule_unknown_command)
    e001 = [d for d in diags if d.code == "E001"]
    assert len(e001) == 0, f"E001 must not fire for snapshot, got: {e001}"


def test_e001_no_false_positive_reset():
    """reset must NOT fire E001 (stub added to schema)."""
    text = "reset\n"
    diags = _lint(text, rule_fn=rule_unknown_command)
    e001 = [d for d in diags if d.code == "E001"]
    assert len(e001) == 0, f"E001 must not fire for reset, got: {e001}"


def test_e001_no_false_positive_aview_postprocessing():
    """aview postprocessing plots create must NOT fire E001."""
    text = "aview postprocessing plots create\n"
    diags = _lint(text, rule_fn=rule_unknown_command)
    e001 = [d for d in diags if d.code == "E001"]
    assert len(e001) == 0, f"E001 must not fire for aview postprocessing plots create, got: {e001}"


def test_e001_macro_defined_command_suppressed():
    """Calling a user-defined macro (created via 'macro create') must NOT fire E001."""
    text = (
        'macro create macro_name=my_tool commands="list_info model model_name=.m"\n'
        "my_tool arg1=val1\n"
    )
    diags = _lint(text, rule_fn=rule_unknown_command)
    e001 = [d for d in diags if d.code == "E001" and "my_tool" in d.message]
    assert len(e001) == 0, f"E001 must not fire for user-defined macro call, got: {e001}"


# W201 — new type widening entries

def test_w201_no_false_positive_spdp_as_force():
    """A spring-damper (Spdp) used where Force expected must NOT fire W201."""
    assert _types_compatible("SPDP", "FORCE"), "SPDP should be compatible with FORCE"


def test_w201_no_false_positive_mforce_as_force():
    """A modal force (Mforce) used where Force expected must NOT fire W201."""
    assert _types_compatible("MFORCE", "FORCE"), "MFORCE should be compatible with FORCE"


def test_w201_no_false_positive_mea_point_as_measure():
    """A Mea_point used where Measure expected must NOT fire W201."""
    assert _types_compatible("MEA_POINT", "MEASURE"), "MEA_POINT should be compatible with MEASURE"


def test_w201_no_false_positive_gi_window_as_gi_gui():
    """A Gi_window used where Gi_gui expected must NOT fire W201."""
    assert _types_compatible("GI_WINDOW", "GI_GUI"), "GI_WINDOW should be compatible with GI_GUI"


def test_w201_no_false_positive_gi_container_as_gi_gui():
    """A Gi_container used where Gi_gui expected must NOT fire W201."""
    assert _types_compatible("GI_CONTAINER", "GI_GUI"), "GI_CONTAINER should be compatible with GI_GUI"


def test_w201_no_false_positive_plate_as_graph():
    """A Plate used where Graph expected must NOT fire W201."""
    assert _types_compatible("PLATE", "GRAPH"), "PLATE should be compatible with GRAPH"


def test_w201_no_false_positive_circle_as_graph():
    """A Circle used where Graph expected must NOT fire W201."""
    assert _types_compatible("CIRCLE", "GRAPH"), "CIRCLE should be compatible with GRAPH"


def test_w201_no_false_positive_ccurve_as_constr():
    """A Ccurve used where Constr expected must NOT fire W201."""
    assert _types_compatible("CCURVE", "CONSTR"), "CCURVE should be compatible with CONSTR"


def test_w201_no_false_positive_macro_as_all():
    """A Macro used where All expected must NOT fire W201."""
    assert _types_compatible("MACRO", "ALL"), "MACRO should be compatible with ALL"


def test_w201_no_false_positive_part_as_all():
    """A Part used where All expected must NOT fire W201."""
    assert _types_compatible("PART", "ALL"), "PART should be compatible with ALL"


def test_w201_no_false_positive_udeinst_as_all():
    """A Udeinst used where All expected must NOT fire W201."""
    assert _types_compatible("UDEINST", "ALL"), "UDEINST should be compatible with ALL"


# ---------------------------------------------------------------------------
# E001 — dot-path property assignment suppression
# ---------------------------------------------------------------------------

def test_e001_no_false_positive_dot_path_assignment():
    """Direct property assignment (.obj.prop = value) must NOT fire E001.

    Adams CMD supports a direct object-property assignment syntax where the
    line starts with a dot-qualified object path followed by '= value', e.g.:

        .plot_1.curve_2.y_history = "filter(.plot_1.curve_1.x_data)"
        .model_1.spring_1.deformation_velocity.func = "vr(.model_1.m1)"

    These are not Adams commands and must be silently ignored by rule E001.
    """
    text = '.plot_1.curve_2.y_history = "filter(.plot_1.curve_1.x_data)"\n'
    diags = _lint(text, rule_fn=rule_unknown_command)
    e001 = [d for d in diags if d.code == "E001"]
    assert len(e001) == 0, (
        f"E001 must not fire for dot-path property assignment, got: {e001}"
    )


def test_e001_no_false_positive_dot_path_func_assignment():
    """Dot-path .func= assignment must not fire E001."""
    text = '.model_1.spring_1.deformation_velocity.func=     "vr(.model_1.m1, .model_1.m2)"\n'
    diags = _lint(text, rule_fn=rule_unknown_command)
    e001 = [d for d in diags if d.code == "E001"]
    assert len(e001) == 0, (
        f"E001 must not fire for .func= assignment, got: {e001}"
    )


# ---------------------------------------------------------------------------
# E001 — stub schema commands (batch-7)
# ---------------------------------------------------------------------------

def test_e001_no_false_positive_file_temporary_settings_apply():
    """file temporary_settings apply must NOT fire E001."""
    text = "file temporary_settings apply\n"
    diags = _lint(text, rule_fn=rule_unknown_command)
    e001 = [d for d in diags if d.code == "E001"]
    assert len(e001) == 0, f"E001 must not fire for 'file temporary_settings apply': {e001}"


def test_e001_no_false_positive_file_temporary_settings_revert():
    """file temporary_settings revert must NOT fire E001."""
    text = "file temporary_settings revert\n"
    diags = _lint(text, rule_fn=rule_unknown_command)
    e001 = [d for d in diags if d.code == "E001"]
    assert len(e001) == 0, f"E001 must not fire for 'file temporary_settings revert': {e001}"


def test_e001_no_false_positive_part_modify_flexible_body_modal_content():
    """part modify flexible_body modal_content must NOT fire E001."""
    text = "part modify flexible_body modal_content part_name=.m.P1\n"
    diags = _lint(text, rule_fn=rule_unknown_command)
    e001 = [d for d in diags if d.code == "E001"]
    assert len(e001) == 0, f"E001 must not fire for 'part modify flexible_body modal_content': {e001}"


def test_e001_no_false_positive_mdi_durability_nodal_plot():
    """mdi durability nodal_plot must NOT fire E001."""
    text = "mdi durability nodal_plot\n"
    diags = _lint(text, rule_fn=rule_unknown_command)
    e001 = [d for d in diags if d.code == "E001"]
    assert len(e001) == 0, f"E001 must not fire for 'mdi durability nodal_plot': {e001}"


def test_e001_no_false_positive_mdi_vibration_modal_info_display():
    """mdi vibration modal_info_display must NOT fire E001."""
    text = "mdi vibration modal_info_display\n"
    diags = _lint(text, rule_fn=rule_unknown_command)
    e001 = [d for d in diags if d.code == "E001"]
    assert len(e001) == 0, f"E001 must not fire for 'mdi vibration modal_info_display': {e001}"


def test_e001_no_false_positive_mdi_marker_delete_unused():
    """mdi marker delete_unused must NOT fire E001."""
    text = "mdi marker delete_unused\n"
    diags = _lint(text, rule_fn=rule_unknown_command)
    e001 = [d for d in diags if d.code == "E001"]
    assert len(e001) == 0, f"E001 must not fire for 'mdi marker delete_unused': {e001}"


def test_e001_no_false_positive_mdi_flx_unv2mnf():
    """mdi flx_unv2mnf must NOT fire E001."""
    text = "mdi flx_unv2mnf\n"
    diags = _lint(text, rule_fn=rule_unknown_command)
    e001 = [d for d in diags if d.code == "E001"]
    assert len(e001) == 0, f"E001 must not fire for 'mdi flx_unv2mnf': {e001}"


def test_e001_no_false_positive_files_delete():
    """files delete must NOT fire E001."""
    text = "files delete file_name=foo.txt\n"
    diags = _lint(text, rule_fn=rule_unknown_command)
    e001 = [d for d in diags if d.code == "E001"]
    assert len(e001) == 0, f"E001 must not fire for 'files delete': {e001}"


def test_e001_no_false_positive_files_chmod():
    """files chmod must NOT fire E001."""
    text = "files chmod file_name=foo.txt\n"
    diags = _lint(text, rule_fn=rule_unknown_command)
    e001 = [d for d in diags if d.code == "E001"]
    assert len(e001) == 0, f"E001 must not fire for 'files chmod': {e001}"


def test_e001_no_false_positive_vflex_make_flex():
    """vflex make flex must NOT fire E001."""
    text = "vflex make flex part_name=.m.P1\n"
    diags = _lint(text, rule_fn=rule_unknown_command)
    e001 = [d for d in diags if d.code == "E001"]
    assert len(e001) == 0, f"E001 must not fire for 'vflex make flex': {e001}"


def test_e001_no_false_positive_vibration_actuator_create():
    """vibration actuator create must NOT fire E001."""
    text = "vibration actuator create\n"
    diags = _lint(text, rule_fn=rule_unknown_command)
    e001 = [d for d in diags if d.code == "E001"]
    assert len(e001) == 0, f"E001 must not fire for 'vibration actuator create': {e001}"


def test_e001_no_false_positive_vibration_vibration_analysis_create():
    """vibration vibration_analysis create must NOT fire E001."""
    text = "vibration vibration_analysis create\n"
    diags = _lint(text, rule_fn=rule_unknown_command)
    e001 = [d for d in diags if d.code == "E001"]
    assert len(e001) == 0, f"E001 must not fire for 'vibration vibration_analysis create': {e001}"


# ---------------------------------------------------------------------------
# Batch-6 schema changes — E005/E006 regressions
# ---------------------------------------------------------------------------

def test_e005_no_false_positive_animation_add_simulation_page_name():
    """animation add_simulation must not fire E005 for missing page_name (not required)."""
    text = "animation add_simulation new_analysis_name=.m.run1\n"
    diags = _lint(text, rules=[rule_unknown_command, rule_missing_required])
    e005 = [d for d in diags if d.code == "E005"]
    assert len(e005) == 0, (
        f"E005 must not fire for animation add_simulation (page_name is optional): {e005}"
    )


def test_e005_no_false_positive_part_create_stress_body_part_name():
    """part create stress_body must not fire E005 for missing part_name (not required)."""
    text = "part create stress_body rigid_stress_name=.m.RS1 geometry=.m.geo1\n"
    diags = _lint(text, rules=[rule_unknown_command, rule_missing_required])
    e005 = [d for d in diags if d.code == "E005"]
    assert len(e005) == 0, (
        f"E005 must not fire for part create stress_body (part_name is optional): {e005}"
    )


def test_e006_variable_create_exclusive_group():
    """variable create must fire E006 when two exclusive value args are provided."""
    text = "variable create variable_name=.m.V1 real_value=1.0 integer_value=2\n"
    diags = _lint(text, rules=[rule_unknown_command, rule_exclusive_conflict])
    e006 = [d for d in diags if d.code == "E006"]
    assert len(e006) > 0, (
        f"E006 must fire when real_value and integer_value both provided: {diags}"
    )


def test_e005_no_false_positive_variable_create_no_value():
    """variable create without any value arg must not fire E005 (value args are optional)."""
    text = "variable create variable_name=.m.V1\n"
    diags = _lint(text, rules=[rule_unknown_command, rule_missing_required])
    e005 = [d for d in diags if d.code == "E005"]
    assert len(e005) == 0, (
        f"E005 must not fire for variable create with no value args: {e005}"
    )


def test_e006_interface_data_table_set_row_exclusive_group():
    """interface data_table set row must fire E006 when range and use_row_selected are both given."""
    text = "interface data_table set row data_table_name=.m.tbl range=3 use_row_selected=yes\n"
    diags = _lint(text, rules=[rule_unknown_command, rule_exclusive_conflict])
    e006 = [d for d in diags if d.code == "E006"]
    assert len(e006) > 0, (
        f"E006 must fire when range and use_row_selected both provided: {diags}"
    )


def test_e005_no_false_positive_interface_data_table_set_row_no_range():
    """interface data_table set row must not fire E005 when range is omitted."""
    text = "interface data_table set row data_table_name=.m.tbl strings=foo\n"
    diags = _lint(text, rules=[rule_unknown_command, rule_missing_required])
    e005 = [d for d in diags if d.code == "E005"]
    assert len(e005) == 0, (
        f"E005 must not fire for interface data_table set row (range optional): {e005}"
    )


def test_e006_no_false_positive_geometry_create_curve_curve_trace():
    """geometry create curve curve_trace must NOT fire E006 (false exclusive group removed)."""
    text = (
        "geometry create curve curve_trace "
        "curve_name=.m.C1 trace_marker=.m.M1 base_marker=.m.M2\n"
    )
    diags = _lint(text, rules=[rule_unknown_command, rule_exclusive_conflict])
    e006 = [d for d in diags if d.code == "E006"]
    assert len(e006) == 0, (
        f"E006 must not fire for geometry create curve curve_trace "
        f"(trace_marker and base_marker are not exclusive): {e006}"
    )


# ---------------------------------------------------------------------------
# W201 type-hierarchy additions (batch-8) — geometry copy pattern
# ---------------------------------------------------------------------------

def test_w201_all_expected_accepts_any_type():
    """When a schema arg expects 'All', any object type must be accepted (no W201)."""
    assert _types_compatible("Box",       "All"), "Box must be compatible with All"
    assert _types_compatible("Marker",    "All"), "Marker must be compatible with All"
    assert _types_compatible("Mechanism", "All"), "Mechanism must be compatible with All"
    assert _types_compatible("Solvar",    "All"), "Solvar must be compatible with All"
    assert _types_compatible("Mea_pt2pt", "All"), "Mea_pt2pt must be compatible with All"
    assert _types_compatible("Vvar",      "All"), "Vvar must be compatible with All"
    assert _types_compatible("Torus",     "All"), "Torus must be compatible with All"
    assert _types_compatible("Ellipse",   "All"), "Ellipse must be compatible with All"
    assert _types_compatible("Group",     "All"), "Group must be compatible with All"
    assert _types_compatible("Spline",    "All"), "Spline must be compatible with All"
    assert _types_compatible("Force",     "All"), "Force must be compatible with All"


def test_w201_graph_as_specific_geometry_subtype():
    """A Graph (result of geometry copy) must be accepted where a specific geom subtype is expected."""
    assert _types_compatible("Graph", "Circle"),    "Graph must be compatible with Circle (copy pattern)"
    assert _types_compatible("Graph", "Box"),       "Graph must be compatible with Box (copy pattern)"
    assert _types_compatible("Graph", "Cylinder"),  "Graph must be compatible with Cylinder (copy pattern)"
    assert _types_compatible("Graph", "Frustum"),   "Graph must be compatible with Frustum (copy pattern)"
    assert _types_compatible("Graph", "Ellipsoid"), "Graph must be compatible with Ellipsoid (copy pattern)"
    assert _types_compatible("Graph", "Gspdp"),     "Graph must be compatible with Gspdp (copy pattern)"
    assert _types_compatible("Graph", "Arc"),       "Graph must be compatible with Arc (copy pattern)"
    assert _types_compatible("Graph", "Extrusion"), "Graph must be compatible with Extrusion (copy pattern)"
    assert _types_compatible("Graph", "Revolution"),"Graph must be compatible with Revolution (copy pattern)"
    assert _types_compatible("Graph", "Gcurve"),    "Graph must be compatible with Gcurve (copy pattern)"
    assert _types_compatible("Graph", "Gwire"),     "Graph must be compatible with Gwire (copy pattern)"
    assert _types_compatible("Graph", "Torus"),     "Graph must be compatible with Torus (copy pattern)"
    assert _types_compatible("Graph", "Sphere"),    "Graph must be compatible with Sphere (copy pattern)"
    assert _types_compatible("Graph", "Plate"),     "Graph must be compatible with Plate (copy pattern)"


def test_w201_extrusion_as_graph():
    """An Extrusion IS a Graph — no W201 when Extrusion is used where Graph is expected."""
    assert _types_compatible("Extrusion",  "Graph"), "Extrusion must be compatible with Graph"
    assert _types_compatible("Arc",        "Graph"), "Arc must be compatible with Graph"
    assert _types_compatible("Revolution", "Graph"), "Revolution must be compatible with Graph"
    assert _types_compatible("Gcurve",     "Graph"), "Gcurve must be compatible with Graph"


def test_w201_gspdp_as_graph():
    """A Gspdp (spring-damper visual) IS a Graph."""
    assert _types_compatible("Gspdp", "Graph"), "Gspdp must be compatible with Graph"


def test_w201_gwire_subtypes():
    """Outline and Gcurve are Gwire subtypes."""
    assert _types_compatible("Outline", "Gwire"), "Outline must be compatible with Gwire"
    assert _types_compatible("Gcurve",  "Gwire"), "Gcurve must be compatible with Gwire"


def test_w201_constr_as_jprim_or_ccurve():
    """A generic Constr (e.g. from constraint copy) must be accepted where Jprim/Ccurve is expected."""
    assert _types_compatible("Constr", "Jprim"),  "Constr must be compatible with Jprim (copy pattern)"
    assert _types_compatible("Constr", "Ccurve"), "Constr must be compatible with Ccurve (copy pattern)"


def test_w201_force_as_specific_force_subtypes():
    """A generic Force (e.g. from a copy command) must be accepted where Mforce/Accgrav/Beam/Bushing is expected."""
    assert _types_compatible("Force", "Mforce"),  "Force must be compatible with Mforce (copy pattern)"
    assert _types_compatible("Force", "Accgrav"), "Force must be compatible with Accgrav (copy pattern)"
    assert _types_compatible("Force", "Beam"),    "Force must be compatible with Beam (copy pattern)"
    assert _types_compatible("Force", "Bushing"), "Force must be compatible with Bushing (copy pattern)"


def test_w201_glink_as_contact_solid():
    """A Glink (link geometry) must be accepted where Contact_solid is expected."""
    assert _types_compatible("Glink", "Contact_solid"), "Glink must be compatible with Contact_solid"


def test_w201_lse_gse_as_equ():
    """Lse and Gse are Equ subtypes."""
    assert _types_compatible("Lse", "Equ"), "Lse must be compatible with Equ"
    assert _types_compatible("Gse", "Equ"), "Gse must be compatible with Equ"


def test_w201_equ_as_tfsiso():
    """A generic Equ is accepted where Tfsiso is expected (copy pattern)."""
    assert _types_compatible("Equ", "Tfsiso"), "Equ must be compatible with Tfsiso (copy pattern)"


def test_w201_var_subtypes():
    """Spline, Solvar, Array, Pinput, Poutput are all Var subtypes."""
    assert _types_compatible("Spline",  "Var"), "Spline must be compatible with Var"
    assert _types_compatible("Solvar",  "Var"), "Solvar must be compatible with Var"
    assert _types_compatible("Array",   "Var"), "Array must be compatible with Var"
    assert _types_compatible("Pinput",  "Var"), "Pinput must be compatible with Var"
    assert _types_compatible("Poutput", "Var"), "Poutput must be compatible with Var"
    assert _types_compatible("Vvar",    "Var"), "Vvar must be compatible with Var"


def test_w201_resset_as_spline_or_var():
    """A Resset (result set) is accepted where Spline or Var is expected."""
    assert _types_compatible("Resset", "Spline"), "Resset must be compatible with Spline"
    assert _types_compatible("Resset", "Var"),    "Resset must be compatible with Var"


def test_w201_pcurve_as_constr():
    """A Pcurve (point-curve constraint) is a Constr subtype."""
    assert _types_compatible("Pcurve", "Constr"), "Pcurve must be compatible with Constr"


def test_w201_accgrav_as_force():
    """Accgrav (gravity) is a Force subtype."""
    assert _types_compatible("Accgrav", "Force"), "Accgrav must be compatible with Force"


def test_w201_motion_as_adams():
    """Motion is compatible with Adams (top-level Adams object)."""
    assert _types_compatible("Motion", "Adams"), "Motion must be compatible with Adams"


def test_w201_all_actual_accepted_anywhere():
    """When actual type is 'All' (from entity copy), it must be accepted for any expected type."""
    assert _types_compatible("All", "Mforce"),  "All must be accepted where Mforce is expected (entity copy)"
    assert _types_compatible("All", "Force"),   "All must be accepted where Force is expected"
    assert _types_compatible("All", "Marker"),  "All must be accepted where Marker is expected"
    assert _types_compatible("All", "Spline"),  "All must be accepted where Spline is expected"


def test_w201_var_as_solvar():
    """A generic Var (from data_element copy) must be accepted where Solvar is expected."""
    assert _types_compatible("Var", "Solvar"), "Var must be compatible with Solvar (copy pattern)"


# ---------------------------------------------------------------------------
# E104 Python-in-CMD false positives
# ---------------------------------------------------------------------------

def test_e104_no_false_positive_python_for_loop():
    """Python 'for' loops after 'language switch_to python' must NOT fire E104."""
    text = (
        "model create model_name = MODEL_1\n"
        "language switch_to python\n"
        "import Adams\n"
        "for i in range(10):\n"
        "    pass\n"
        "Adams.switchToCmd()\n"
    )
    diags = _lint(text, rules=[rule_control_flow_balance])
    e104 = [d for d in diags if d.code == "E104"]
    assert len(e104) == 0, (
        f"E104 must not fire for Python 'for' loops in python mode: {e104}"
    )


def test_e104_no_false_positive_python_if_statement():
    """Python 'if' statements after 'language switch_to python' must NOT fire E104."""
    text = (
        "language switch_to python\n"
        "pycmd = 'x=1'\n"
        "if '':\n"
        "    pycmd += 'a'\n"
        "else:\n"
        "    pycmd += 'b'\n"
        "exec(pycmd)\n"
        "Adams.switchToCmd()\n"
    )
    diags = _lint(text, rules=[rule_control_flow_balance])
    e104 = [d for d in diags if d.code == "E104"]
    assert len(e104) == 0, (
        f"E104 must not fire for Python 'if/else' in python mode: {e104}"
    )


def test_e104_adams_control_flow_still_checked_after_python_section():
    """Adams if/for/end checking must resume after Adams.switchToCmd()."""
    text = (
        "language switch_to python\n"
        "for i in range(5):\n"
        "    pass\n"
        "Adams.switchToCmd()\n"
        "end\n"          # This 'end' is Adams CMD — should fire E104
    )
    diags = _lint(text, rules=[rule_control_flow_balance])
    e104 = [d for d in diags if d.code == "E104"]
    assert len(e104) == 1, (
        f"E104 must fire for orphan Adams 'end' after Python section: {e104}"
    )

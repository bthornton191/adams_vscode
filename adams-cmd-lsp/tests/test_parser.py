"""Tests for adams_cmd_lsp.parser module."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from adams_cmd_lsp.parser import (
    parse,
    _extract_command_key,
    _consume_argument_value,
    _consume_comma_separated_tail,
    _group_continuation_lines,
    _find_comment_start,
)


# ---------------------------------------------------------------------------
# _find_comment_start
# ---------------------------------------------------------------------------

def test_comment_start_no_comment():
    line = "marker create marker_name = .model.m1"
    assert _find_comment_start(line) == len(line)


def test_comment_start_trailing():
    line = "marker create  ! this is a comment"
    assert _find_comment_start(line) == 15


def test_comment_start_inside_string():
    line = 'title = "hello ! world"'
    assert _find_comment_start(line) == len(line)


def test_comment_start_after_string():
    line = 'title = "hello" ! comment'
    assert _find_comment_start(line) == 16


def test_comment_start_escaped_quote_in_string():
    """'!' after a backslash-escaped quote inside a string must not be a comment.

    Line: "  format=\\"#! /bin/csh -f\\"", &
    The '#!' is inside the outer double-quoted string. The \\" sequences are
    escaped quotes, not string terminators. The '!' must not be treated as a
    comment start.
    """
    line = '    "  format=\\"#! /bin/csh -f\\"", &'
    assert _find_comment_start(line) == len(line), (
        "! inside a string with escaped quotes must not be a comment start"
    )


# ---------------------------------------------------------------------------
# _consume_argument_value
# ---------------------------------------------------------------------------

def test_consume_bare_word():
    text = ".model.PART_1 rest"
    end = _consume_argument_value(text, 0)
    assert text[:end] == ".model.PART_1"


def test_consume_quoted_string():
    text = '"hello world" rest'
    end = _consume_argument_value(text, 0)
    assert text[:end] == '"hello world"'


def test_consume_quoted_string_escaped_double_quote():
    """Escaped \" inside a double-quoted string must not terminate the string."""
    text = r'"say \"hello\" now" rest'
    end = _consume_argument_value(text, 0)
    assert text[:end] == r'"say \"hello\" now"'


def test_consume_quoted_string_escaped_single_quote():
    """Escaped \' inside a single-quoted string must not terminate the string."""
    text = r"'it\'s fine' rest"
    end = _consume_argument_value(text, 0)
    assert text[:end] == r"'it\'s fine'"


def test_consume_parenthesised():
    text = "(eval(1+2)) rest"
    end = _consume_argument_value(text, 0)
    assert text[:end] == "(eval(1+2))"


def test_consume_nested_parens():
    text = "(step(time,0,0,1,100)) rest"
    end = _consume_argument_value(text, 0)
    assert text[:end] == "(step(time,0,0,1,100))"


def test_consume_unclosed_paren():
    text = "(unclosed"
    end = _consume_argument_value(text, 0)
    assert end == len(text)


def test_consume_empty():
    assert _consume_argument_value("", 0) == 0


# ---------------------------------------------------------------------------
# _consume_comma_separated_tail
# ---------------------------------------------------------------------------

def test_comma_tail_three_values():
    text = "1.0, 2.0, 3.0"
    # Consume first value first
    end = _consume_argument_value(text, 0)
    end = _consume_comma_separated_tail(text, end, 0)
    assert text[:end].strip().rstrip(",") == "1.0, 2.0, 3.0".rstrip()


def test_comma_tail_stops_at_arg_pair():
    text = "1.0, 2.0 part_name=foo"
    end = _consume_argument_value(text, 0)
    end = _consume_comma_separated_tail(text, end, 0)
    assert text[end:].strip().startswith("part_name=")


def test_comma_tail_whitespace_before_comma():
    """Values separated by spaces-then-comma (e.g. polyline coords on continuation lines).

    After joining: 'points_for_profile = 30.0, 0.0, 60.0         , 60.0, 0.0, 80.0'
    The value consumer sees '30.0,' then '0.0,' then '60.0' (no trailing comma).
    The next non-space char is ',' — must continue consuming.
    """
    text = "30.0, 0.0, 60.0         , 60.0, 0.0, 80.0"
    end = _consume_argument_value(text, 0)
    end = _consume_comma_separated_tail(text, end, 0)
    assert text[:end] == "30.0, 0.0, 60.0         , 60.0, 0.0, 80.0"


def test_comma_tail_whitespace_comma_stops_at_arg():
    """Whitespace-before-comma lookahead must stop at an arg=value token."""
    text = '60.0         angle_extent = 180.0'
    end = _consume_argument_value(text, 0)
    end = _consume_comma_separated_tail(text, end, 0)
    assert text[end:].strip().startswith("angle_extent")


def test_extract_key_geometry_shape_polyline():
    """geometry create shape revolution with comma-continuation polyline points.

    Real Adams CMD pattern — points_for_profile value spans multiple continuation
    lines, each starting with ', x, y, z'.  The command key must be just
    'geometry create shape revolution', not contaminated with coordinate data.
    """
    text = (
        'geometry create shape revolution '
        'revolution_name = .m.REV7 '
        'points_for_profile = 30.0, 0.0, 60.0'
        '         , 60.0, 0.0, 60.0'
        '         , 60.0, 0.0, 80.0'
        '         , 40.0, 0.0, 80.0 '
        'angle_extent = 180.0 '
        'number_of_sides = 20'
    )
    assert _extract_command_key(text) == "geometry create shape revolution"


def test_parse_geometry_shape_revolution_polyline():
    """Full parse of geometry create shape revolution with multi-line polyline.

    Command key must be 'geometry create shape revolution'.
    points_for_profile must contain all coordinate triplets.
    """
    text = (
        'geometry create shape revolution  &\n'
        '   revolution_name = .m.ground.REV7  &\n'
        '   adams_id = 69  &\n'
        '   points_for_profile = 30.0, 0.0, 60.0  &\n'
        '      , 60.0, 0.0, 60.0  &\n'
        '      , 60.0, 0.0, 80.0  &\n'
        '      , 40.0, 0.0, 80.0  &\n'
        '   angle_extent = 180.0  &\n'
        '   number_of_sides = 20\n'
    )
    stmts = parse(text)
    real = [s for s in stmts if not s.is_blank and not s.is_comment]
    assert len(real) == 1
    stmt = real[0]
    assert stmt.command_key == 'geometry create shape revolution', (
        f"command_key contaminated with coordinate data: {stmt.command_key!r}"
    )
    arg_names = [a.name for a in stmt.arguments]
    assert 'points_for_profile' in arg_names
    pfp = next(a for a in stmt.arguments if a.name == 'points_for_profile')
    # All continuation coordinate sets must be in the value
    assert '60.0, 0.0, 80.0' in pfp.value, (
        f"Continuation coordinates missing from points_for_profile: {pfp.value!r}"
    )


def test_parse_macro_create_commands_quoted_array():
    """macro create commands= with comma-separated quoted strings on continuation lines.

    The commands= argument takes an array of quoted Adams CMD strings.  Each
    element is a double-quoted string, and elements are separated by ' , &'
    (space-comma-continuation) across lines.  The command key must be just
    'macro create' and commands= must capture all quoted strings.
    """
    text = (
        'macro create macro=.mdi.MyMacro &\n'
        '  wrap_in_undo=no &\n'
        '  commands= &\n'
        '     "undo begin suppres=yes" , &\n'
        '     "assembly create instance &", &\n'
        '     "undo end"\n'
    )
    stmts = parse(text)
    real = [s for s in stmts if not s.is_blank and not s.is_comment]
    assert len(real) == 1
    stmt = real[0]
    assert stmt.command_key == 'macro create', (
        f"command_key contaminated: {stmt.command_key!r}"
    )
    arg_names = [a.name for a in stmt.arguments]
    assert 'commands' in arg_names
    cmd_arg = next(a for a in stmt.arguments if a.name == 'commands')
    assert '"undo end"' in cmd_arg.value, (
        f"Last quoted string missing from commands value: {cmd_arg.value!r}"
    )


# ---------------------------------------------------------------------------
# _extract_command_key
# ---------------------------------------------------------------------------

def test_extract_key_no_args():
    assert _extract_command_key("marker create") == "marker create"


def test_extract_key_with_args():
    text = "marker create marker_name=.model.MAR_1 location=0,0,0"
    assert _extract_command_key(text) == "marker create"


def test_extract_key_multiword():
    text = "part create rigid_body name_and_position part_name=.model.P1"
    assert _extract_command_key(text) == "part create rigid_body name_and_position"


def test_extract_key_quoted_value():
    text = 'model create model_name=my_model title="My Model"'
    assert _extract_command_key(text) == "model create"


def test_extract_key_paren_value():
    text = "marker create location=(eval(1+2)),0,0 marker_name=.m.MAR"
    assert _extract_command_key(text) == "marker create"


# ---------------------------------------------------------------------------
# _group_continuation_lines
# ---------------------------------------------------------------------------

def test_continuation_group_single():
    lines = ["model create model_name = my_model"]
    groups = _group_continuation_lines(lines)
    assert len(groups) == 1
    assert groups[0][0] == 0  # line_start
    assert groups[0][1] == 0  # line_end


def test_continuation_group_multi():
    lines = [
        "part create rigid_body name_and_position &",
        "    part_name = .model.PART_1 &",
        "    location = 0.0, 0.0, 0.0",
    ]
    groups = _group_continuation_lines(lines)
    assert len(groups) == 1
    g = groups[0]
    assert g[0] == 0  # line_start
    assert g[1] == 2  # line_end
    assert "part_name" in g[2]
    assert "location" in g[2]


def test_continuation_group_comment_in_continuation():
    lines = [
        "data_element modify matrix full &",
        "   ! this is a comment line in a continuation &",
        "   row_count = 5",
    ]
    # The comment line is absorbed (it ends with &, continuing the group)
    groups = _group_continuation_lines(lines)
    assert len(groups) == 1
    assert groups[0][0] == 0
    assert groups[0][1] == 2


def test_continuation_two_separate_statements():
    lines = [
        "model create model_name = my_model",
        "marker create marker_name = .my_model.MAR_1",
    ]
    groups = _group_continuation_lines(lines)
    assert len(groups) == 2


# ---------------------------------------------------------------------------
# parse() — high-level tests
# ---------------------------------------------------------------------------

def test_parse_blank_lines():
    text = "\n\n\n"
    stmts = parse(text)
    assert all(s.is_blank for s in stmts)


def test_parse_comment_only():
    text = "! This is a comment\n! Another comment"
    stmts = parse(text)
    assert all(s.is_comment for s in stmts)


def test_parse_control_flow_if():
    text = "if condition = (DB_EXISTS(.model.P1))"
    stmts = parse(text)
    assert len(stmts) == 1
    assert stmts[0].is_control_flow
    assert stmts[0].control_flow_keyword == "if"


def test_parse_control_flow_end():
    text = "end"
    stmts = parse(text)
    assert stmts[0].is_control_flow
    assert stmts[0].control_flow_keyword == "end"


def test_parse_control_flow_elseif():
    text = "elseif condition = (x > 0)"
    stmts = parse(text)
    assert stmts[0].is_control_flow
    assert stmts[0].control_flow_keyword == "elseif"


def test_parse_normal_command():
    text = "model create model_name = my_model"
    stmts = parse(text)
    assert len(stmts) == 1
    stmt = stmts[0]
    assert not stmt.is_blank
    assert not stmt.is_comment
    assert not stmt.is_control_flow
    assert stmt.command_key == "model create"
    assert len(stmt.arguments) == 1
    assert stmt.arguments[0].name == "model_name"
    assert stmt.arguments[0].value == "my_model"


def test_parse_arguments_with_spaces():
    text = "model create model_name = my_model  title = \"My Model\""
    stmts = parse(text)
    stmt = stmts[0]
    names = [a.name for a in stmt.arguments]
    assert "model_name" in names
    assert "title" in names


def test_parse_continuation_statement():
    text = (
        "part create rigid_body name_and_position &\n"
        "    part_name = .model.PART_1 &\n"
        "    location = 0.0, 0.0, 0.0\n"
    )
    stmts = [s for s in parse(text) if not s.is_blank]
    assert len(stmts) == 1
    stmt = stmts[0]
    assert "part create rigid_body name_and_position" in stmt.command_key
    arg_names = [a.name for a in stmt.arguments]
    assert "part_name" in arg_names
    assert "location" in arg_names


def test_parse_line_column_positions():
    """Argument positions should map back to correct physical lines."""
    text = (
        "marker create &\n"
        "    marker_name = .model.MAR_1\n"
    )
    stmts = [s for s in parse(text) if not s.is_blank]
    stmt = stmts[0]
    arg = next(a for a in stmt.arguments if a.name == "marker_name")
    # marker_name is on physical line 1 (0-based)
    assert arg.name_line == 1


def test_parse_variable_name_with_if_keyword():
    """'if' inside a variable name should NOT be treated as control flow."""
    text = "variable set variable_name = if_needed string = test"
    stmts = parse(text)
    assert len(stmts) == 1
    assert not stmts[0].is_control_flow
    assert stmts[0].command_key == "variable set"


def test_parse_mixed_file():
    text = (
        "! Header comment\n"
        "\n"
        "model create model_name = my_model\n"
        "if condition = (x > 0)\n"
        "    marker create marker_name = .my_model.MAR_1\n"
        "end\n"
    )
    stmts = parse(text)
    types = {
        "blank": sum(1 for s in stmts if s.is_blank),
        "comment": sum(1 for s in stmts if s.is_comment),
        "control": sum(1 for s in stmts if s.is_control_flow),
        "command": sum(1 for s in stmts if not s.is_blank and not s.is_comment and not s.is_control_flow),
    }
    assert types["blank"] >= 1
    assert types["comment"] == 1
    assert types["control"] == 2  # if + end
    assert types["command"] == 2  # model create + marker create


# ---------------------------------------------------------------------------
# Single-quoted string handling
# ---------------------------------------------------------------------------

def test_comment_start_inside_single_quoted_string():
    """'!' inside single-quoted string must NOT be treated as a comment start."""
    line = "var set var=.mdi.tmpstr str=(eval(str_print('HELLO WORLD!!')))"
    assert _find_comment_start(line) == len(line)


def test_comment_start_after_single_quoted_string():
    """'!' after a closed single-quoted string IS a comment."""
    line = "var set var=.mdi.tmpstr str='hello' ! comment"
    idx = _find_comment_start(line)
    assert line[idx] == '!'


def test_consume_single_quoted_string():
    """Single-quoted string value should be consumed in full."""
    text = "'HELLO WORLD!!' rest"
    end = _consume_argument_value(text, 0)
    assert text[:end] == "'HELLO WORLD!!'"


def test_consume_parens_with_single_quoted_string_inside():
    """Parens containing a single-quoted string with '!' are consumed fully."""
    text = "(eval(str_print('HELLO WORLD!!')))"
    end = _consume_argument_value(text, 0)
    assert text[:end] == "(eval(str_print('HELLO WORLD!!')))"


def test_parse_single_quoted_exclamation_not_comment():
    """Full parse: line with single-quoted '!!' should preserve text after the parens."""
    line = "var set var=.mdi.tmpstr str=(eval(str_print('HELLO WORLD!!')))"
    stmts = parse(line)
    assert len(stmts) == 1
    stmt = stmts[0]
    assert not stmt.is_comment
    assert not stmt.is_blank
    # The raw_text must NOT be truncated at the '!!' — closing ))) must be present
    assert stmt.raw_text.endswith(")))")


# ---------------------------------------------------------------------------
# '!' as NOT operator / '!=' inside parentheses
# ---------------------------------------------------------------------------

def test_comment_start_not_operator_inside_parens():
    """'!' as logical NOT operator inside '(...)' must NOT be treated as a comment."""
    line = "if condition=(eval(!DB_EXISTS(\".part\")))"
    assert _find_comment_start(line) == len(line)


def test_comment_start_not_equal_operator_inside_parens():
    """'!' in '!=' inside '(...)' must NOT be treated as a comment."""
    line = "if condition=(eval($oml_pitch != 0))"
    assert _find_comment_start(line) == len(line)


def test_comment_start_not_operator_inside_nested_parens():
    """'!' inside deeply nested parens is not a comment."""
    line = "if condition=((eval(\"yes\" == \"yes\") && !DB_EXISTS(\".part\")))"
    assert _find_comment_start(line) == len(line)


def test_comment_start_after_closing_paren_is_comment():
    """'!' AFTER all parens are closed IS a comment."""
    line = "if condition=(eval(DB_EXISTS(\".part\"))) ! check"
    idx = _find_comment_start(line)
    assert line[idx] == '!'
    assert line[idx:] == "! check"


def test_parse_not_operator_in_condition():
    """if condition=(eval(!DB_EXISTS(...))) should parse as a single control-flow
    statement with raw_text preserved (not truncated at '!')."""
    line = "if condition=(eval(!DB_EXISTS(\".part\")))"
    stmts = parse(line)
    assert len(stmts) == 1
    stmt = stmts[0]
    assert stmt.is_control_flow
    assert stmt.raw_text.endswith(")))")


def test_parse_not_equal_in_condition():
    """if condition=(eval($x != 0)) should parse as a single statement, not truncated."""
    line = "if condition=(eval($oml_pitch != 0))"
    stmts = parse(line)
    assert len(stmts) == 1
    stmt = stmts[0]
    assert stmt.is_control_flow
    assert "!= 0" in stmt.raw_text


def test_parse_logical_and_before_not_operator_no_false_continuation():
    """'if condition=((eval(...) && !db_exists(...)))' must NOT be treated as a
    continuation line — the '&&' after comment-stripping the '!' must not be
    mistaken for a trailing '&' continuation marker."""
    line = 'if condition=((eval("$x" == "yes") && !DB_EXISTS(".bp")))'
    next_line = "    plugin load plugin=my_plugin"
    stmts = parse(line + "\n" + next_line)
    # Must parse as two separate statements, not one merged continuation
    assert len(stmts) == 2
    assert stmts[0].is_control_flow
    assert stmts[0].line_start == 0
    assert stmts[0].line_end == 0   # must NOT absorb the next line
    assert stmts[1].line_start == 1


def test_continuation_blank_line_absorbed():
    """A '&'-only spacer line inside a continuation group must be absorbed.

    Real Adams files use lines containing only '&' (or spaces + '&') as
    placeholder spacers inside continuation blocks.  These must not break
    the group.  A truly empty line (no '&') DOES break the continuation.
    """
    text = (
        "part create rigid_body name_and_position &\n"
        "     &\n"                          # spacer line: spaces + '&'
        "  part_name = .model.PART_1\n"
    )
    stmts = parse(text)
    # All three physical lines must form ONE logical statement
    real = [s for s in stmts if not s.is_blank and not s.is_comment]
    assert len(real) == 1
    assert real[0].line_start == 0
    assert real[0].line_end == 2
    assert "part_name" in [a.name for a in real[0].arguments]


def test_continuation_multiple_blank_lines_absorbed():
    """Multiple consecutive '&'-only spacer lines inside a continuation are all absorbed."""
    text = (
        "part create rigid_body name_and_position &\n"
        "     &\n"
        "     &\n"
        "  part_name = .model.PART_1\n"
    )
    stmts = parse(text)
    real = [s for s in stmts if not s.is_blank and not s.is_comment]
    assert len(real) == 1
    assert real[0].line_start == 0
    assert real[0].line_end == 3
    assert "part_name" in [a.name for a in real[0].arguments]


def test_continuation_blank_and_comment_lines_absorbed():
    """'&'-only spacer lines and comment-only lines mixed inside a continuation are all absorbed."""
    text = (
        "part create rigid_body name_and_position &\n"
        "     &\n"
        "! This comment is inside the continuation\n"
        "  part_name = .model.PART_1\n"
    )
    stmts = parse(text)
    assert len(stmts) == 1
    assert stmts[0].line_start == 0
    assert stmts[0].line_end == 3
    assert "part_name" in [a.name for a in stmts[0].arguments]


def test_continuation_blank_line_between_two_statements():
    """A blank line that is NOT inside a continuation must still separate statements."""
    text = (
        "model create model_name = .model1\n"
        "\n"
        "model create model_name = .model2\n"
    )
    stmts = parse(text)
    # Two independent statements -- the blank line should not merge them
    real_stmts = [s for s in stmts if not s.is_blank and not s.is_comment]
    assert len(real_stmts) == 2
    assert real_stmts[0].line_start == 0
    assert real_stmts[1].line_start == 2


def test_continuation_whitespace_only_line_breaks_group():
    """A blank or whitespace-only line (no '&') inside a continuation terminates it.

    Real Adams .cmd files use blank lines (or lines with only spaces) to
    separate commands. Once no '&' is present, the continuation ends.
    """
    text = (
        "animation create animation_name = .a1 &\n"
        "   analysis_name = .sim1  &\n"
        "   \n"                           # whitespace-only line — breaks the group
        "animation create animation_name = .a2 &\n"
        "   analysis_name = .sim2\n"
    )
    stmts = parse(text)
    real = [s for s in stmts if not s.is_blank and not s.is_comment]
    assert len(real) == 2, (
        f"Expected 2 statements, got {len(real)}: "
        + ", ".join(repr(s.command_key) for s in real)
    )
    # First statement must end before the whitespace-only line
    assert real[0].line_end <= 2, f"First stmt absorbed too many lines: line_end={real[0].line_end}"
    # Second statement must start at line 3 (0-indexed)
    assert real[1].line_start == 3, f"Second stmt starts at wrong line: {real[1].line_start}"


def test_continuation_truly_blank_line_breaks_group():
    """A truly empty line (no characters) inside a continuation also terminates it.

    This matches the real Adams .cmd file pattern where a completely empty
    line between continuation-using commands separates them.
    """
    text = (
        "animation play animation_name = .a1 &\n"
        "   analysis_name = .sim1  &\n"
        "\n"                              # truly empty line — breaks the group
        "animation modify animation_name = .a1 &\n"
        "   frame_number = 100\n"
    )
    stmts = parse(text)
    real = [s for s in stmts if not s.is_blank and not s.is_comment]
    assert len(real) == 2, (
        f"Expected 2 statements, got {len(real)}: "
        + ", ".join(repr(s.command_key) for s in real)
    )
    assert real[1].line_start == 3, f"Second stmt starts at wrong line: {real[1].line_start}"


# ---------------------------------------------------------------------------
# Embedded quoted components in hierarchical names (e.g. .MODEL."Part 1")
# ---------------------------------------------------------------------------

def test_consume_embedded_quoted_in_hierarchical_name():
    """A bare-word value like .MODEL."Part 1" must be consumed in full.

    The quoted component "Part 1" contains a space, which must NOT stop the
    bare-word scanner — it should consume through the closing quote.
    """
    text = 'part_name = .SPLIT_TOOL."Part 1"'
    # position of value start (after '= ')
    val_start = text.index('.SPLIT_TOOL')
    end = _consume_argument_value(text, val_start)
    value = text[val_start:end]
    assert value == '.SPLIT_TOOL."Part 1"', f"Got: {value!r}"


def test_consume_embedded_quoted_with_suffix():
    """Quoted component followed by more path tokens: .MODEL."Part 1".cm"""
    text = 'marker_name = .SPLIT_TOOL."Part 1".cm'
    val_start = text.index('.SPLIT_TOOL')
    end = _consume_argument_value(text, val_start)
    value = text[val_start:end]
    assert value == '.SPLIT_TOOL."Part 1".cm', f"Got: {value!r}"


def test_parse_embedded_quoted_part_name_argument():
    """Full parse: part_name = .SPLIT_TOOL."Part 1" must produce correct argument value."""
    text = 'part create rigid_body name_and_position part_name = .SPLIT_TOOL."Part 1"\n'
    stmts = parse(text)
    real = [s for s in stmts if not s.is_blank and not s.is_comment]
    assert len(real) == 1, f"Expected 1 statement, got {len(real)}"
    args = {a.name: a.value for a in real[0].arguments}
    assert "part_name" in args, f"part_name missing from args: {list(args)}"
    assert args["part_name"] == '.SPLIT_TOOL."Part 1"', f"Got: {args['part_name']!r}"


def test_parse_embedded_quoted_no_spurious_unknown_command():
    """Embedded quoted name must NOT produce extra spurious statement tokens.

    Previously the parser would stop bare-word scanning at the space inside
    "Part 1", leaving '1"' as residue that became a bogus second statement.
    """
    text = 'part create rigid_body name_and_position part_name = .SPLIT_TOOL."Part 1"\n'
    stmts = parse(text)
    real = [s for s in stmts if not s.is_blank and not s.is_comment]
    # Must be exactly ONE statement — no residue parsed as a second command
    assert len(real) == 1, (
        f"Expected 1 statement but got {len(real)}: "
        + ", ".join(repr(s.command_key) for s in real)
    )


# ---------------------------------------------------------------------------
# Escaped quotes inside commands= array (E003 false-positive regression)
# ---------------------------------------------------------------------------

def test_no_duplicate_args_from_escaped_quotes_in_commands_array():
    """macro create commands= with escaped quotes must not produce E003 duplicates.

    Adams CMD files use \\\" (backslash + double-quote) to embed a literal
    double-quote inside a double-quoted string.  A string like:

        "if cond=(DB_EXISTS(\\"name\\"))"

    contains \\\" sequences.  Without proper escape handling, the quote parser
    terminates early at the first \\\" and the remainder (e.g. name\\\")))  is
    scanned as free text -- which then produces spurious arg=value matches and
    ultimately E003 (duplicate argument) false positives.
    """
    text = (
        'macro create macro=M1 &\n'
        '  commands= &\n'
        '"if cond=(DB_EXISTS(\\"name\\"))",  &\n'
        '"variable set variable=.M.V real=(1.0)",  &\n'
        '"if cond=(DB_EXISTS(\\"name2\\"))",  &\n'
        '"variable set variable=.M.V2 real=(2.0)"\n'
    )
    stmts = parse(text)
    real = [s for s in stmts if not s.is_blank and not s.is_comment]
    assert len(real) == 1, f"Expected 1 statement, got {len(real)}"

    stmt = real[0]
    arg_names = [a.name for a in stmt.arguments]

    # Only 'macro' and 'commands' should appear -- no leaked args from inside strings
    assert 'macro' in arg_names
    assert 'commands' in arg_names
    for leaked in ('cond', 'variable', 'real'):
        assert leaked not in arg_names, (
            f"Arg '{leaked}' leaked from inside quoted string content"
        )


# ---------------------------------------------------------------------------
# is_property_assignment detection
# ---------------------------------------------------------------------------

def test_parse_property_assignment_bare_name():
    """VarName=value must be flagged as is_property_assignment."""
    stmts = parse("VarName=5\n")
    real = [s for s in stmts if not s.is_blank and not s.is_comment]
    assert len(real) == 1
    assert real[0].is_property_assignment
    assert real[0].command_key == ""


def test_parse_property_assignment_spaces_around_equals():
    """VarName = value (spaces) must be flagged as is_property_assignment."""
    stmts = parse("VarName = 5\n")
    real = [s for s in stmts if not s.is_blank and not s.is_comment]
    assert len(real) == 1
    assert real[0].is_property_assignment


def test_parse_property_assignment_dot_path():
    """.model.MyVar=value must be flagged as is_property_assignment."""
    stmts = parse(".model.MyVar=5\n")
    real = [s for s in stmts if not s.is_blank and not s.is_comment]
    assert len(real) == 1
    assert real[0].is_property_assignment


def test_parse_property_assignment_dollar_macro_param():
    """$model.$name.prop=$value (macro param substitution) must be flagged."""
    stmts = parse("$model.$name.youngs_modulus=$youngs_modulus\n")
    real = [s for s in stmts if not s.is_blank and not s.is_comment]
    assert len(real) == 1
    assert real[0].is_property_assignment


def test_parse_property_assignment_object_reference():
    """VarName=.model.Part_1.Marker_1 (object reference rhs) must be flagged."""
    stmts = parse("VarName=.model.Part_1.Marker_1\n")
    real = [s for s in stmts if not s.is_blank and not s.is_comment]
    assert len(real) == 1
    assert real[0].is_property_assignment


def test_parse_property_assignment_not_fired_on_normal_command():
    """part create part_name=.m.p must NOT be flagged as is_property_assignment."""
    stmts = parse("part create part_name=.m.p\n")
    real = [s for s in stmts if not s.is_blank and not s.is_comment]
    assert len(real) == 1
    assert not real[0].is_property_assignment
    assert real[0].command_key == "part create"


def test_parse_property_assignment_not_fired_on_continuation():
    """A continuation command with arg=value must NOT be flagged as is_property_assignment."""
    text = "marker create &\n    marker_name=.m.M1\n"
    stmts = [s for s in parse(text) if not s.is_blank]
    assert len(stmts) == 1
    assert not stmts[0].is_property_assignment
    assert stmts[0].command_key == "marker create"

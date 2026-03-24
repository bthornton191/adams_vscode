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

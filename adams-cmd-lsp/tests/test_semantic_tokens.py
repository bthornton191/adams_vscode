"""Tests for semantic token support: parser command_key_tokens and server._compute_semantic_tokens."""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from adams_cmd_lsp.parser import parse, _extract_command_key_tokens

# Guard: skip server tests if pygls/lsprotocol are not installed
try:
    from pygls.lsp.server import LanguageServer  # noqa: F401
    _PYGLS_AVAILABLE = True
except ImportError:
    _PYGLS_AVAILABLE = False

if _PYGLS_AVAILABLE:
    from adams_cmd_lsp import server as srv
    from adams_cmd_lsp.schema import Schema
    from adams_cmd_lsp.macros import MacroRegistry, MacroDefinition


# ---------------------------------------------------------------------------
# _extract_command_key_tokens
# ---------------------------------------------------------------------------

def test_extract_tokens_single_word():
    offsets = [(0, 0, 0)]
    tokens = _extract_command_key_tokens("pause", offsets)
    assert tokens == [("pause", 0, 0)]


def test_extract_tokens_multi_word():
    text = "part create rigid_body"
    offsets = [(i, 0, i) for i in range(len(text))]
    tokens = _extract_command_key_tokens(text, offsets)
    assert tokens == [("part", 0, 0), ("create", 0, 5), ("rigid_body", 0, 12)]


def test_extract_tokens_skips_arg_value_pairs():
    text = "part create rigid_body part_name=.model.P1 loc=0,0,0"
    offsets = [(i, 0, i) for i in range(len(text))]
    tokens = _extract_command_key_tokens(text, offsets)
    assert tokens == [("part", 0, 0), ("create", 0, 5), ("rigid_body", 0, 12)]


def test_extract_tokens_leading_whitespace_skipped():
    text = "  part create"
    offsets = [(i, 0, i) for i in range(len(text))]
    tokens = _extract_command_key_tokens(text, offsets)
    assert tokens == [("part", 0, 2), ("create", 0, 7)]


def test_extract_tokens_empty_text():
    tokens = _extract_command_key_tokens("", [])
    assert tokens == []


def test_extract_tokens_only_arg_value():
    # Unlike _extract_command_key which would return the raw text as command key,
    # _extract_command_key_tokens correctly recognises the arg=value pattern at
    # position 0 and returns no command tokens.  This is intentional — command
    # key tokens should never start with an arg=value pair.
    text = "name=foo"
    offsets = [(i, 0, i) for i in range(len(text))]
    tokens = _extract_command_key_tokens(text, offsets)
    assert tokens == []


def test_extract_tokens_command_with_quoted_value():
    text = 'macro create macro_name=mymac user_entered_command="cdm wear"'
    offsets = [(i, 0, i) for i in range(len(text))]
    tokens = _extract_command_key_tokens(text, offsets)
    assert tokens == [("macro", 0, 0), ("create", 0, 6)]


# ---------------------------------------------------------------------------
# Statement.command_key_tokens populated by parse()
# ---------------------------------------------------------------------------

def test_parse_normal_command_has_tokens():
    stmts = parse("part create rigid_body part_name=.model.p1\n")
    cmd_stmt = [s for s in stmts if not s.is_comment and not s.is_blank][0]
    token_words = [t[0] for t in cmd_stmt.command_key_tokens]
    assert token_words == ["part", "create", "rigid_body"]


def test_parse_comment_has_no_tokens():
    stmts = parse("! this is a comment\n")
    assert stmts[0].is_comment
    assert stmts[0].command_key_tokens == []


def test_parse_blank_has_no_tokens():
    stmts = parse("\n")
    assert stmts[0].is_blank
    assert stmts[0].command_key_tokens == []


def test_parse_control_flow_has_tokens():
    stmts = parse("if condition(1)\n")
    assert stmts[0].is_control_flow
    assert stmts[0].command_key_tokens[0][0] == "if"


def test_parse_token_positions_are_correct():
    stmts = parse("model create model_name=my_model\n")
    cmd_stmt = [s for s in stmts if not s.is_comment and not s.is_blank][0]
    assert ("model", 0, 0) in cmd_stmt.command_key_tokens
    assert ("create", 0, 6) in cmd_stmt.command_key_tokens


def test_parse_continuation_line_tokens():
    """Command key tokens spanning a continuation line should have correct positions."""
    stmts = parse("cdm &\n  wear model=.model\n")
    cmd_stmt = [s for s in stmts if not s.is_comment and not s.is_blank][0]
    token_words = [t[0] for t in cmd_stmt.command_key_tokens]
    assert "cdm" in token_words
    assert "wear" in token_words
    # "cdm" should be on line 0, "wear" on line 1
    cdm_tok = [t for t in cmd_stmt.command_key_tokens if t[0] == "cdm"][0]
    wear_tok = [t for t in cmd_stmt.command_key_tokens if t[0] == "wear"][0]
    assert cdm_tok[1] == 0  # line 0
    assert wear_tok[1] == 1  # line 1
    assert wear_tok[2] == 2  # col 2 (after leading spaces)


# ---------------------------------------------------------------------------
# _compute_semantic_tokens (server-level)
# ---------------------------------------------------------------------------

@pytest.fixture()
def _setup_server():
    """Load schema and reset macro registry before/after each server test."""
    srv._schema = Schema.load()
    srv._macro_registry = None
    yield
    srv._schema = None
    srv._macro_registry = None


@pytest.mark.skipif(not _PYGLS_AVAILABLE, reason="pygls / lsprotocol not installed")
@pytest.mark.usefixtures("_setup_server")
def test_compute_tokens_builtin_command_emits_tokens():
    """Built-in commands should produce keyword + parameter semantic tokens."""
    data = srv._compute_semantic_tokens(
        "model create model_name=my_model\n",
        "file:///test.cmd",
    )
    # 3 tokens: "model" (keyword), "create" (keyword), "model_name" (parameter)
    assert len(data) == 15
    tokens = [(data[i], data[i+1], data[i+2], data[i+3], data[i+4])
              for i in range(0, len(data), 5)]
    assert tokens[0] == (0, 0, 5, srv._TOKEN_TYPE_KEYWORD, 0)   # "model"
    assert tokens[1] == (0, 6, 6, srv._TOKEN_TYPE_KEYWORD, 0)   # "create"
    assert tokens[2] == (0, 7, 10, srv._TOKEN_TYPE_PARAMETER, 0)  # "model_name"


@pytest.mark.skipif(not _PYGLS_AVAILABLE, reason="pygls / lsprotocol not installed")
@pytest.mark.usefixtures("_setup_server")
def test_compute_tokens_builtin_abbreviated_command():
    """Abbreviated built-in command should be resolved and emit keyword tokens."""
    data = srv._compute_semantic_tokens(
        "mod cre model_name=m1\n",
        "file:///test.cmd",
    )
    # "mod" and "cre" should both get keyword tokens, "model_name" a parameter token
    assert len(data) == 15
    tokens = [(data[i], data[i+1], data[i+2], data[i+3], data[i+4])
              for i in range(0, len(data), 5)]
    keyword_tokens = [t for t in tokens if t[3] == srv._TOKEN_TYPE_KEYWORD]
    assert len(keyword_tokens) == 2
    assert keyword_tokens[0][:3] == (0, 0, 3)  # "mod"
    assert keyword_tokens[1][:3] == (0, 4, 3)  # "cre"


@pytest.mark.skipif(not _PYGLS_AVAILABLE, reason="pygls / lsprotocol not installed")
@pytest.mark.usefixtures("_setup_server")
def test_compute_tokens_builtin_invalid_arg_not_highlighted():
    """Invalid argument names on a built-in command should NOT get a parameter token."""
    data = srv._compute_semantic_tokens(
        "model create bogus_arg=foo\n",
        "file:///test.cmd",
    )
    tokens = [(data[i], data[i+1], data[i+2], data[i+3], data[i+4])
              for i in range(0, len(data), 5)]
    keyword_tokens = [t for t in tokens if t[3] == srv._TOKEN_TYPE_KEYWORD]
    parameter_tokens = [t for t in tokens if t[3] == srv._TOKEN_TYPE_PARAMETER]
    assert len(keyword_tokens) == 2  # "model" and "create"
    assert len(parameter_tokens) == 0  # "bogus_arg" not valid


@pytest.mark.skipif(not _PYGLS_AVAILABLE, reason="pygls / lsprotocol not installed")
@pytest.mark.usefixtures("_setup_server")
def test_compute_tokens_builtin_abbreviated_arg_highlighted():
    """Abbreviated valid argument name on built-in command should get a parameter token."""
    # "mod" is a valid prefix for "model_name" on "model create"
    data = srv._compute_semantic_tokens(
        "model create mod=m1\n",
        "file:///test.cmd",
    )
    tokens = [(data[i], data[i+1], data[i+2], data[i+3], data[i+4])
              for i in range(0, len(data), 5)]
    parameter_tokens = [t for t in tokens if t[3] == srv._TOKEN_TYPE_PARAMETER]
    assert len(parameter_tokens) == 1
    # "mod" comes after "create" (col 6) on the same line, so delta_col = 13 - 6 = 7
    assert parameter_tokens[0][1] == 7

@pytest.mark.skipif(not _PYGLS_AVAILABLE, reason="pygls / lsprotocol not installed")
@pytest.mark.usefixtures("_setup_server")
def test_compute_tokens_unknown_command_no_registry():
    """Unknown commands with no macro registry should produce no tokens."""
    data = srv._compute_semantic_tokens(
        "cdm wear model=.model\n",
        "file:///test.cmd",
    )
    assert data == []


@pytest.mark.skipif(not _PYGLS_AVAILABLE, reason="pygls / lsprotocol not installed")
@pytest.mark.usefixtures("_setup_server")
def test_compute_tokens_registry_macro_emits_tokens():
    """A workspace macro in the registry should emit keyword + parameter tokens."""
    registry = MacroRegistry()
    registry.register(MacroDefinition(
        command="cdm wear",
        parameters={"model": None},
        source_file="/fake/tool.mac",
        line=0,
    ))
    srv._macro_registry = registry

    data = srv._compute_semantic_tokens(
        "cdm wear model=.model\n",
        "file:///test.cmd",
    )
    # 3 tokens × 5 ints each: "cdm" (keyword), "wear" (keyword), "model" (parameter)
    assert len(data) == 15
    tokens = [(data[i], data[i+1], data[i+2], data[i+3], data[i+4])
              for i in range(0, len(data), 5)]
    assert tokens[0] == (0, 0, 3, srv._TOKEN_TYPE_KEYWORD, 0)
    assert tokens[1] == (0, 4, 4, srv._TOKEN_TYPE_KEYWORD, 0)
    assert tokens[2] == (0, 5, 5, srv._TOKEN_TYPE_PARAMETER, 0)


@pytest.mark.skipif(not _PYGLS_AVAILABLE, reason="pygls / lsprotocol not installed")
@pytest.mark.usefixtures("_setup_server")
def test_compute_tokens_inline_macro_emits_tokens():
    """A macro defined by 'macro create' in the same file should emit tokens."""
    srv._macro_registry = MacroRegistry()

    text = (
        'macro create macro_name=mymac user_entered_command="my_command"\n'
        "my_command arg1=val1\n"
    )
    data = srv._compute_semantic_tokens(text, "file:///test.cmd")
    assert len(data) > 0
    tokens = [(data[i], data[i+1], data[i+2], data[i+3], data[i+4])
              for i in range(0, len(data), 5)]
    keyword_tokens = [t for t in tokens if t[3] == srv._TOKEN_TYPE_KEYWORD]
    assert len(keyword_tokens) >= 1
    # "my_command" keyword should appear after the line-0 'macro create' tokens
    # (delta_line > 0 means the token is on a new line relative to the previous token)
    line1_keyword_tokens = [t for t in keyword_tokens if t[0] > 0]
    assert len(line1_keyword_tokens) >= 1


@pytest.mark.skipif(not _PYGLS_AVAILABLE, reason="pygls / lsprotocol not installed")
@pytest.mark.usefixtures("_setup_server")
def test_compute_tokens_comment_and_blank_no_tokens():
    """Comments and blank lines should not produce any semantic tokens."""
    srv._macro_registry = MacroRegistry()
    data = srv._compute_semantic_tokens(
        "! this is a comment\n\n",
        "file:///test.cmd",
    )
    assert data == []


@pytest.mark.skipif(not _PYGLS_AVAILABLE, reason="pygls / lsprotocol not installed")
@pytest.mark.usefixtures("_setup_server")
def test_compute_tokens_no_schema_returns_empty():
    """If no schema is loaded, return empty."""
    srv._schema = None
    data = srv._compute_semantic_tokens("cdm wear model=.m\n", "file:///test.cmd")
    assert data == []


@pytest.mark.skipif(not _PYGLS_AVAILABLE, reason="pygls / lsprotocol not installed")
@pytest.mark.usefixtures("_setup_server")
def test_compute_tokens_dot_path_assignment_no_tokens():
    """Dot-path property assignments should not produce tokens."""
    srv._macro_registry = MacroRegistry()
    data = srv._compute_semantic_tokens(
        '.model_1.spring_1.func = "vr(1,2)"\n',
        "file:///test.cmd",
    )
    assert data == []


@pytest.mark.skipif(not _PYGLS_AVAILABLE, reason="pygls / lsprotocol not installed")
@pytest.mark.usefixtures("_setup_server")
def test_compute_tokens_control_flow_no_tokens():
    """Control flow statements should not produce tokens."""
    srv._macro_registry = MacroRegistry()
    data = srv._compute_semantic_tokens(
        "if condition(1)\nend\n",
        "file:///test.cmd",
    )
    assert data == []


@pytest.mark.skipif(not _PYGLS_AVAILABLE, reason="pygls / lsprotocol not installed")
@pytest.mark.usefixtures("_setup_server")
def test_compute_tokens_abbreviated_macro_not_highlighted():
    """An abbreviated macro command should NOT produce semantic tokens.

    MacroRegistry uses exact matching, so 'cdm wea' should not match 'cdm wear'.
    """
    registry = MacroRegistry()
    registry.register(MacroDefinition(
        command="cdm wear",
        parameters={"model": None},
        source_file="/fake/tool.mac",
        line=0,
    ))
    srv._macro_registry = registry
    data = srv._compute_semantic_tokens("cdm wea model=.m\n", "file:///test.cmd")
    assert data == []


@pytest.mark.skipif(not _PYGLS_AVAILABLE, reason="pygls / lsprotocol not installed")
@pytest.mark.usefixtures("_setup_server")
def test_compute_tokens_multiple_macro_invocations():
    """Multiple macro invocations across lines should produce correct delta encoding."""
    registry = MacroRegistry()
    registry.register(MacroDefinition(
        command="cdm wear", parameters={}, source_file="/fake/tool.mac", line=0,
    ))
    registry.register(MacroDefinition(
        command="cdm create", parameters={}, source_file="/fake/tool.mac", line=5,
    ))
    srv._macro_registry = registry

    text = "cdm wear model=.m\nmodel create model_name=m1\ncdm create part=.p\n"
    data = srv._compute_semantic_tokens(text, "file:///test.cmd")
    tokens = [(data[i], data[i+1], data[i+2], data[i+3], data[i+4])
              for i in range(0, len(data), 5)]
    # Line 0: "cdm" keyword, "wear" keyword, "model" parameter
    # Line 1: built-in "model create" — now also emits tokens (model, create, model_name)
    # Line 2: "cdm" keyword, "create" keyword, "part" parameter
    keyword_tokens = [t for t in tokens if t[3] == srv._TOKEN_TYPE_KEYWORD]
    assert len(keyword_tokens) == 6  # cdm, wear, model, create, cdm, create
    parameter_tokens = [t for t in tokens if t[3] == srv._TOKEN_TYPE_PARAMETER]
    assert len(parameter_tokens) == 3  # model, model_name, part


@pytest.mark.skipif(not _PYGLS_AVAILABLE, reason="pygls / lsprotocol not installed")
@pytest.mark.usefixtures("_setup_server")
def test_compute_tokens_continuation_line_macro():
    """A macro invocation spanning continuation lines should have correct positions."""
    registry = MacroRegistry()
    registry.register(MacroDefinition(
        command="cdm wear", parameters={}, source_file="/fake/tool.mac", line=0,
    ))
    srv._macro_registry = registry

    text = "cdm &\n  wear model=.model\n"
    data = srv._compute_semantic_tokens(text, "file:///test.cmd")
    assert len(data) > 0
    tokens = [(data[i], data[i+1], data[i+2], data[i+3], data[i+4])
              for i in range(0, len(data), 5)]
    keyword_tokens = [t for t in tokens if t[3] == srv._TOKEN_TYPE_KEYWORD]
    assert len(keyword_tokens) == 2
    # "cdm" at line 0, col 0
    assert keyword_tokens[0][:3] == (0, 0, 3)
    # "wear" at line 1, col 2
    assert keyword_tokens[1][:3] == (1, 2, 4)


@pytest.mark.skipif(not _PYGLS_AVAILABLE, reason="pygls / lsprotocol not installed")
@pytest.mark.usefixtures("_setup_server")
def test_compute_tokens_mixed_builtin_and_macro():
    """A file with both a built-in command and a macro invocation should emit
    tokens for both with correct delta encoding."""
    registry = MacroRegistry()
    registry.register(MacroDefinition(
        command="cdm wear", parameters={"model": None}, source_file="/fake/tool.mac", line=0,
    ))
    srv._macro_registry = registry

    text = "model create model_name=m1\ncdm wear model=.model\n"
    data = srv._compute_semantic_tokens(text, "file:///test.cmd")
    tokens = [(data[i], data[i+1], data[i+2], data[i+3], data[i+4])
              for i in range(0, len(data), 5)]
    keyword_tokens = [t for t in tokens if t[3] == srv._TOKEN_TYPE_KEYWORD]
    parameter_tokens = [t for t in tokens if t[3] == srv._TOKEN_TYPE_PARAMETER]
    # Line 0: "model" keyword, "create" keyword, "model_name" parameter
    # Line 1: "cdm" keyword, "wear" keyword, "model" parameter
    assert len(keyword_tokens) == 4
    assert len(parameter_tokens) == 2
    # "cdm" on line 1 should have delta_line=1 from the last token on line 0
    cdm_token = next(t for t in tokens if t[3] == srv._TOKEN_TYPE_KEYWORD and t[2] == 3)
    assert cdm_token[0] == 1  # delta_line from previous token on line 0

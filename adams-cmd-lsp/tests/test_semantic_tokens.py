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


def test_parse_control_flow_has_no_tokens():
    stmts = parse("if condition(1)\n")
    assert stmts[0].is_control_flow
    assert stmts[0].command_key_tokens == []


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
def test_compute_tokens_builtin_command_no_tokens():
    """Built-in commands should produce no semantic tokens."""
    data = srv._compute_semantic_tokens(
        "model create model_name=my_model\n",
        "file:///test.cmd",
    )
    assert data == []


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
    # "my_command" should be on line 1 (delta-line 1 from start)
    assert keyword_tokens[0][0] == 1


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
    # Line 1: built-in "model create" — skipped
    # Line 2: "cdm" keyword, "create" keyword, "part" parameter
    keyword_tokens = [t for t in tokens if t[3] == srv._TOKEN_TYPE_KEYWORD]
    assert len(keyword_tokens) == 4  # cdm, wear, cdm, create
    # The third keyword ("cdm" on line 2) should have delta_line=2 from line 0
    assert keyword_tokens[2][0] == 2


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

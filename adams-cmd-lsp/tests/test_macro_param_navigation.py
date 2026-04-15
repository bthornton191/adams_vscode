"""Tests for macro parameter definition ↔ reference navigation helpers.

Covers:
  _find_macro_param_defs_in_text    — pure function, no LSP server required
  _find_macro_param_def_at_position — pure function, no LSP server required
  goto_definition (integration)     — cursor on $param reference or !$param definition
  find_references (integration)     — cursor on either position
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

# Guard: skip entire module if pygls/lsprotocol are not installed
try:
    from pygls.lsp.server import LanguageServer  # noqa: F401
    from lsprotocol import types
    _PYGLS_AVAILABLE = True
except ImportError:
    _PYGLS_AVAILABLE = False

pytestmark = pytest.mark.skipif(not _PYGLS_AVAILABLE, reason="pygls not installed")

import adams_cmd_lsp.server as srv
from adams_cmd_lsp.server import (
    _find_macro_param_defs_in_text,
    _find_macro_param_def_at_position,
)
from adams_cmd_lsp.schema import Schema


# ---------------------------------------------------------------------------
# Shared helper
# ---------------------------------------------------------------------------

def _make_mock_doc(text, uri):
    """Return a mock server object for monkeypatching srv.server."""
    import types as python_types
    doc = python_types.SimpleNamespace(source=text, uri=uri)
    workspace = python_types.SimpleNamespace(
        get_text_document=lambda u: doc,
        folders={},
    )
    return python_types.SimpleNamespace(workspace=workspace)


# ---------------------------------------------------------------------------
# _find_macro_param_defs_in_text — unit tests
# ---------------------------------------------------------------------------

def test_find_defs_basic():
    """Single bare parameter definition is found at the correct position."""
    text = "!$part_name:t=part:c=1\n"
    defs = _find_macro_param_defs_in_text(text)
    assert "$part_name" in defs
    line, col_start, col_end = defs["$part_name"]
    assert line == 0
    assert text.splitlines()[0][col_start:col_end] == "$part_name"


def test_find_defs_multiple_params():
    """Multiple parameter definitions are all returned."""
    text = (
        "!$part_name:t=part:c=1\n"
        "!$scale:t=real:d=1.0\n"
        "!$label:t=string:d=Label\n"
    )
    defs = _find_macro_param_defs_in_text(text)
    assert set(defs.keys()) == {"$part_name", "$scale", "$label"}


def test_find_defs_stops_at_end_of_parameters():
    """Parameters after !END_OF_PARAMETERS are not included."""
    text = (
        "!$before:t=real\n"
        "!END_OF_PARAMETERS\n"
        "!$after:t=real\n"
    )
    defs = _find_macro_param_defs_in_text(text)
    assert "$before" in defs
    assert "$after" not in defs


def test_find_defs_excludes_self():
    """$_self is not returned — it is the macro namespace, not a parameter."""
    text = "!$_self:t=string\n"
    defs = _find_macro_param_defs_in_text(text)
    assert "$_self" not in defs


def test_find_defs_quoted_form():
    """Quoted form !$'name:qualifiers' is parsed correctly."""
    text = "!$'my_param:t=real:d=0.0'\n"
    defs = _find_macro_param_defs_in_text(text)
    assert "$my_param" in defs
    line, col_start, col_end = defs["$my_param"]
    assert line == 0
    # Quoted form spans $'name (dollar, single-quote, then the name characters)
    assert text.splitlines()[0][col_start:col_end] == "$'my_param"


def test_find_defs_keys_are_lowercase():
    """Dict keys are always lowercase even if the source uses mixed case."""
    text = "!$PartName:t=part\n"
    defs = _find_macro_param_defs_in_text(text)
    assert "$partname" in defs
    assert "$PartName" not in defs


def test_find_defs_no_qualifiers():
    """Bare !$name without any qualifiers is found."""
    text = "!$simple\n"
    defs = _find_macro_param_defs_in_text(text)
    assert "$simple" in defs


def test_find_defs_leading_whitespace_on_line():
    """Leading whitespace before ! is handled via strip inside the function."""
    text = "  !$param:t=real\n"
    defs = _find_macro_param_defs_in_text(text)
    assert "$param" in defs
    # col_start should point to the '$' in the original line
    _, col_start, col_end = defs["$param"]
    original = "  !$param:t=real"
    assert original[col_start:col_end] == "$param"


def test_find_defs_empty_text():
    """Empty text returns empty dict."""
    assert _find_macro_param_defs_in_text("") == {}


def test_find_defs_non_param_comment_ignored():
    """Regular comments that don't match !$name are not included."""
    text = (
        "! This is a regular comment\n"
        "! Author: me\n"
        "!$real_param:t=real\n"
    )
    defs = _find_macro_param_defs_in_text(text)
    assert set(defs.keys()) == {"$real_param"}


def test_find_defs_column_span_correct():
    """col_start and col_end exactly span the $name token (no qualifiers)."""
    text = "!$iterations:t=integer:d=10\n"
    defs = _find_macro_param_defs_in_text(text)
    assert "$iterations" in defs
    _, col_start, col_end = defs["$iterations"]
    line_text = text.splitlines()[0]
    assert line_text[col_start:col_end] == "$iterations"


# ---------------------------------------------------------------------------
# _find_macro_param_def_at_position — unit tests
# ---------------------------------------------------------------------------

def test_def_at_position_cursor_on_dollar():
    """Cursor on the '$' of !$param returns the param info."""
    text = "!$part_name:t=part\n"
    dollar_col = text.index("$")
    result = _find_macro_param_def_at_position(text, 0, dollar_col)
    assert result is not None
    token, line, col_start, col_end = result
    assert token.lower() == "$part_name"
    assert line == 0
    assert col_start == dollar_col


def test_def_at_position_cursor_middle_of_name():
    """Cursor in the middle of the param name returns the param info."""
    text = "!$part_name:t=part\n"
    col = text.index("part_name") + 4  # middle of "part_name"
    result = _find_macro_param_def_at_position(text, 0, col)
    assert result is not None
    token = result[0]
    assert token.lower() == "$part_name"


def test_def_at_position_cursor_on_exclamation():
    """Cursor on the leading '!' (before '$') returns None."""
    text = "!$part_name:t=part\n"
    bang_col = text.index("!")
    result = _find_macro_param_def_at_position(text, 0, bang_col)
    assert result is None


def test_def_at_position_cursor_on_qualifier():
    """Cursor on ':t=part' qualifier suffix returns None."""
    text = "!$part_name:t=part\n"
    col = text.index(":t=")  # start of qualifiers
    result = _find_macro_param_def_at_position(text, 0, col)
    assert result is None


def test_def_at_position_regular_comment_returns_none():
    """A plain comment line (no $name pattern) returns None."""
    text = "! This is a comment\n"
    result = _find_macro_param_def_at_position(text, 0, 5)
    assert result is None


def test_def_at_position_end_of_parameters_returns_none():
    """!END_OF_PARAMETERS line is not treated as a parameter definition."""
    text = "!END_OF_PARAMETERS\n"
    result = _find_macro_param_def_at_position(text, 0, 1)
    assert result is None


def test_def_at_position_self_excluded():
    """!$_self is not a parameter definition — returns None."""
    text = "!$_self:t=string\n"
    col = text.index("$")
    result = _find_macro_param_def_at_position(text, 0, col)
    assert result is None


def test_def_at_position_wrong_line():
    """Line index beyond text returns None."""
    text = "!$param:t=real\n"
    result = _find_macro_param_def_at_position(text, 99, 0)
    assert result is None


def test_def_at_position_second_line():
    """Correctly identifies a param definition on a later line."""
    text = (
        "!USER_ENTERED_COMMAND mylib mymacro\n"
        "!$scale:t=real:d=1.0\n"
    )
    dollar_col = text.splitlines()[1].index("$")
    result = _find_macro_param_def_at_position(text, 1, dollar_col)
    assert result is not None
    token, line, col_start, _ = result
    assert token.lower() == "$scale"
    assert line == 1


# ---------------------------------------------------------------------------
# goto_definition integration tests — macro parameters
# ---------------------------------------------------------------------------

_MACRO_TEXT = """\
!USER_ENTERED_COMMAND mylib my_macro
!$part_name:t=part:c=1
!$scale:t=real:d=1.0
!END_OF_PARAMETERS

variable set variable_name=$_self.model integer_value=1

marker modify &
    marker_name = (eval($part_name // ".cm")) &
    location = (eval({0, $scale, 0}))
"""


def test_goto_definition_param_reference_jumps_to_definition(monkeypatch):
    """Ctrl+Click on $part_name in body navigates to its !$part_name definition."""
    uri = "file:///test.mac"
    monkeypatch.setattr(srv, "server", _make_mock_doc(_MACRO_TEXT, uri))
    srv._schema = Schema.load()
    srv._macro_registry = None
    srv._doc_cache.pop(uri, None)

    # Find $part_name on a body line (a continuation line, not a !comment)
    lines = _MACRO_TEXT.splitlines()
    target_line = next(
        i for i, l in enumerate(lines)
        if "$part_name" in l and not l.strip().startswith("!")
    )
    col = lines[target_line].index("$part_name")

    params = types.DefinitionParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=target_line, character=col + 3),
    )
    result = srv.goto_definition(params)
    assert result is not None and len(result) == 1, f"Expected 1 LocationLink, got: {result}"
    link = result[0]
    # Target should be the !$part_name definition line (line 1)
    def_line = next(i for i, l in enumerate(lines) if l.strip().startswith("!$part_name"))
    assert link.target_range.start.line == def_line, (
        f"Expected target line {def_line} (!$part_name definition), "
        f"got line {link.target_range.start.line}"
    )


def test_goto_definition_from_definition_site_returns_references(monkeypatch):
    """Ctrl+Click on !$scale definition returns all $scale body references."""
    uri = "file:///test.mac"
    monkeypatch.setattr(srv, "server", _make_mock_doc(_MACRO_TEXT, uri))
    srv._schema = Schema.load()
    srv._macro_registry = None
    srv._doc_cache.pop(uri, None)

    lines = _MACRO_TEXT.splitlines()
    def_line = next(i for i, l in enumerate(lines) if l.strip().startswith("!$scale"))
    col = lines[def_line].index("$scale")

    params = types.DefinitionParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=def_line, character=col + 1),
    )
    result = srv.goto_definition(params)
    assert result is not None and len(result) >= 1, f"Expected references, got: {result}"

    # The target lines should include the $scale usage in the body (not the definition itself)
    target_lines = {link.target_range.start.line for link in result}
    body_line = next(i for i, l in enumerate(lines) if "$scale" in l and "!" not in l)
    assert body_line in target_lines, f"Expected body reference on line {body_line}, got {target_lines}"
    # Definition line should NOT be in results (it's excluded)
    assert def_line not in target_lines, "Definition line should be excluded from inverse navigation"


def test_goto_definition_self_not_treated_as_param(monkeypatch):
    """$_self references are not navigated as macro parameters."""
    uri = "file:///test.mac"
    text = (
        "!USER_ENTERED_COMMAND mylib m\n"
        "!$_self:t=string\n"  # should be ignored (excluded)
        "!END_OF_PARAMETERS\n"
        "variable set variable_name=$_self.model integer_value=1\n"
    )
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._macro_registry = None
    srv._doc_cache.pop(uri, None)

    lines = text.splitlines()
    self_line = next(i for i, l in enumerate(lines) if "$_self.model" in l)
    col = lines[self_line].index("$_self.model")

    params = types.DefinitionParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=self_line, character=col + 1),
    )
    result = srv.goto_definition(params)
    # $variable navigation should pick this up via variable set, not macro param defs
    # The !$_self: line should have no effect on navigation
    if result is not None:
        for link in result:
            # Must not point to the !$_self line (line 1)
            assert link.target_range.start.line != 1, \
                "$_self navigation must not target the !$_self definition"


def test_goto_definition_undefined_param_returns_none(monkeypatch):
    """$undeclared in a macro body where no definition exists returns None."""
    uri = "file:///test.mac"
    text = (
        "!USER_ENTERED_COMMAND mylib m\n"
        "!END_OF_PARAMETERS\n"
        "\n"
        "marker modify marker_name=(eval($undeclared // \".cm\"))\n"
    )
    monkeypatch.setattr(srv, "server", _make_mock_doc(text, uri))
    srv._schema = Schema.load()
    srv._macro_registry = None
    srv._doc_cache.pop(uri, None)

    lines = text.splitlines()
    ref_line = next(i for i, l in enumerate(lines) if "$undeclared" in l)
    col = lines[ref_line].index("$undeclared")

    params = types.DefinitionParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=ref_line, character=col + 3),
    )
    result = srv.goto_definition(params)
    assert result is None


# ---------------------------------------------------------------------------
# find_references integration tests — macro parameters
# ---------------------------------------------------------------------------

def test_find_references_from_param_reference_returns_all(monkeypatch):
    """Shift+F12 on $scale body reference returns all occurrences."""
    uri = "file:///test.mac"
    monkeypatch.setattr(srv, "server", _make_mock_doc(_MACRO_TEXT, uri))
    srv._schema = Schema.load()
    srv._macro_registry = None
    srv._doc_cache.pop(uri, None)

    lines = _MACRO_TEXT.splitlines()
    ref_line = next(i for i, l in enumerate(lines) if "$scale" in l and "!" not in l)
    col = lines[ref_line].index("$scale")

    params = types.ReferenceParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=ref_line, character=col + 1),
        context=types.ReferenceContext(include_declaration=True),
    )
    result = srv.find_references(params)
    assert result is not None and len(result) >= 1
    result_lines = [loc.range.start.line for loc in result]

    # With include_declaration=True, the definition line should be included
    def_line = next(i for i, l in enumerate(lines) if l.strip().startswith("!$scale"))
    assert def_line in result_lines, f"Expected definition line {def_line} in results"
    assert ref_line in result_lines, f"Expected reference line {ref_line} in results"


def test_find_references_from_param_reference_exclude_declaration(monkeypatch):
    """Shift+F12 on $scale with include_declaration=False omits the def line."""
    uri = "file:///test.mac"
    monkeypatch.setattr(srv, "server", _make_mock_doc(_MACRO_TEXT, uri))
    srv._schema = Schema.load()
    srv._macro_registry = None
    srv._doc_cache.pop(uri, None)

    lines = _MACRO_TEXT.splitlines()
    ref_line = next(i for i, l in enumerate(lines) if "$scale" in l and "!" not in l)
    col = lines[ref_line].index("$scale")

    params = types.ReferenceParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=ref_line, character=col + 1),
        context=types.ReferenceContext(include_declaration=False),
    )
    result = srv.find_references(params)
    result_lines = [loc.range.start.line for loc in result]

    def_line = next(i for i, l in enumerate(lines) if l.strip().startswith("!$scale"))
    assert def_line not in result_lines, "Definition line must be excluded when include_declaration=False"


def test_find_references_from_definition_site(monkeypatch):
    """Shift+F12 on !$part_name definition returns all body references."""
    uri = "file:///test.mac"
    monkeypatch.setattr(srv, "server", _make_mock_doc(_MACRO_TEXT, uri))
    srv._schema = Schema.load()
    srv._macro_registry = None
    srv._doc_cache.pop(uri, None)

    lines = _MACRO_TEXT.splitlines()
    def_line = next(i for i, l in enumerate(lines) if l.strip().startswith("!$part_name"))
    col = lines[def_line].index("$part_name")

    params = types.ReferenceParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=def_line, character=col + 1),
        context=types.ReferenceContext(include_declaration=False),
    )
    result = srv.find_references(params)
    assert result is not None
    result_lines = [loc.range.start.line for loc in result]

    # Body reference line should be present
    body_line = next(i for i, l in enumerate(lines) if "$part_name" in l and "!" not in l)
    assert body_line in result_lines, f"Expected body reference on line {body_line}, got {result_lines}"
    # Definition itself excluded since include_declaration=False
    assert def_line not in result_lines


def test_find_references_from_definition_include_declaration(monkeypatch):
    """Shift+F12 on !$part_name with include_declaration=True includes the def line."""
    uri = "file:///test.mac"
    monkeypatch.setattr(srv, "server", _make_mock_doc(_MACRO_TEXT, uri))
    srv._schema = Schema.load()
    srv._macro_registry = None
    srv._doc_cache.pop(uri, None)

    lines = _MACRO_TEXT.splitlines()
    def_line = next(i for i, l in enumerate(lines) if l.strip().startswith("!$part_name"))
    col = lines[def_line].index("$part_name")

    params = types.ReferenceParams(
        text_document=types.TextDocumentIdentifier(uri=uri),
        position=types.Position(line=def_line, character=col + 1),
        context=types.ReferenceContext(include_declaration=True),
    )
    result = srv.find_references(params)
    result_lines = [loc.range.start.line for loc in result]
    assert def_line in result_lines, "Definition line must appear when include_declaration=True"

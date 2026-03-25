"""Tests for adams_cmd_lsp.symbols module."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from adams_cmd_lsp.symbols import SymbolTable, build_symbol_table
from adams_cmd_lsp.parser import parse
from adams_cmd_lsp.schema import Schema


# ---------------------------------------------------------------------------
# SymbolTable unit tests
# ---------------------------------------------------------------------------

def test_symbol_table_register_and_lookup():
    table = SymbolTable()
    table.register(".model.PART_1", "Part", 0)
    sym = table.lookup(".model.PART_1")
    assert sym is not None
    assert sym.name == ".model.PART_1"
    assert sym.object_type == "Part"
    assert sym.line == 0


def test_symbol_table_lookup_case_insensitive():
    table = SymbolTable()
    table.register(".Model.Part_1", "Part", 5)
    assert table.lookup(".model.part_1") is not None
    assert table.lookup(".MODEL.PART_1") is not None


def test_symbol_table_has():
    table = SymbolTable()
    table.register(".model.marker_1", "Marker", 2)
    assert table.has(".model.marker_1")
    assert table.has(".MODEL.MARKER_1")
    assert not table.has(".model.nonexistent")


def test_symbol_table_lookup_missing_returns_none():
    table = SymbolTable()
    assert table.lookup(".model.doesnt_exist") is None


def test_symbol_table_overwrite():
    """Registering the same name twice overwrites the first entry."""
    table = SymbolTable()
    table.register(".model.part", "Part", 1)
    table.register(".model.part", "Part", 99)
    sym = table.lookup(".model.part")
    assert sym.line == 99


# ---------------------------------------------------------------------------
# build_symbol_table integration tests
# ---------------------------------------------------------------------------

def test_build_symbol_table_model_create():
    """model create registers the model name."""
    schema = Schema.load()
    stmts = parse("model create model_name = my_model")
    table = build_symbol_table(stmts, schema)
    assert table.has("my_model")
    sym = table.lookup("my_model")
    assert sym.object_type in ("Mechanism", "mechanism", "MECHANISM", "MODEL")


def test_build_symbol_table_marker_create():
    """marker create registers marker_name."""
    schema = Schema.load()
    stmts = parse("marker create marker_name = .model_1.PART_1.MAR_1 location = 0,0,0")
    table = build_symbol_table(stmts, schema)
    assert table.has(".model_1.PART_1.MAR_1")


def test_build_symbol_table_multiple_creates():
    """Multiple create statements populate the table."""
    schema = Schema.load()
    text = (
        "model create model_name = my_model\n"
        "part create rigid_body name_and_position part_name = my_model.PART_1\n"
    )
    stmts = parse(text)
    table = build_symbol_table(stmts, schema)
    assert table.has("my_model")
    assert table.has("my_model.PART_1")


def test_build_symbol_table_skips_comments_and_blanks():
    """Comments and blank lines produce no user symbols (only builtins)."""
    schema = Schema.load()
    stmts = parse("! just a comment\n\n")
    table = build_symbol_table(stmts, schema)
    # The table should contain only pre-populated builtins (ground, colors, views, etc.)
    # — no user-defined symbols.  The builtins dict is non-empty.
    assert not table.has("my_model"), "No user symbols should be created from a comment"
    assert not table.has(".model.PART_1"), "No user symbols should be created from a comment"
    # Builtins must still be present
    assert table.has("ground"), "ground builtin must always be present"


def test_build_symbol_table_skips_unknown_commands():
    """Unknown commands (no schema entry) produce no symbols."""
    schema = Schema.load()
    stmts = parse("not_a_real_command object_name = foo")
    table = build_symbol_table(stmts, schema)
    assert not table.has("foo")


def test_build_symbol_table_set_does_not_create():
    """A modify/set command does not create a new symbol."""
    schema = Schema.load()
    # variable set modifies an existing variable; it uses MDBWD (modify) not NDBWD (new)
    stmts = parse("variable set variable_name = .model.v1 real_value = 1.0")
    table = build_symbol_table(stmts, schema)
    # variable_name arg is MDBWD_VVAR (existing), not new_object type
    assert not table.has(".model.v1")


# ---------------------------------------------------------------------------
# Symbol table normalization — leading dot
# ---------------------------------------------------------------------------

def test_symbol_table_normalize_leading_dot_on_register():
    """Registering a name without a leading dot must be findable WITH a leading dot.

    In Adams, 'model' and '.model' refer to the same database path. The symbol
    table must normalize both forms to '.name' on register and lookup.
    """
    table = SymbolTable()
    table.register("model", "MECHANISM", 0)
    assert table.has(".model"), "Symbol registered as 'model' must be found as '.model'"
    assert table.has("model"), "Symbol registered as 'model' must still be found as 'model'"


def test_symbol_table_normalize_leading_dot_on_lookup():
    """Looking up a name without a leading dot must find an entry registered WITH a leading dot."""
    table = SymbolTable()
    table.register(".model", "MECHANISM", 0)
    assert table.has("model"), "Symbol registered as '.model' must be found as 'model'"
    assert table.has(".model"), "Symbol registered as '.model' must still be found as '.model'"


def test_symbol_table_normalize_lookup_returns_symbol():
    """lookup() with and without leading dot both return the same Symbol."""
    table = SymbolTable()
    table.register("model", "MECHANISM", 5)
    sym_with = table.lookup(".model")
    sym_without = table.lookup("model")
    assert sym_with is not None
    assert sym_without is not None
    assert sym_with.line == 5
    assert sym_without.line == 5


def test_build_symbol_table_model_name_normalized():
    """Full integration: 'model create model_name = model' → table.has('.model') is True."""
    schema = Schema.load()
    stmts = parse("model create model_name = model")
    table = build_symbol_table(stmts, schema)
    assert table.has(".model"), "Model 'model' (no dot) must be findable as '.model'"
    assert table.has("model"), "Model 'model' must still be findable as 'model'"


# ---------------------------------------------------------------------------
# Dynamic prefix — eval expression support
# ---------------------------------------------------------------------------

def test_symbol_table_register_dynamic_prefix():
    """register_dynamic_prefix stores a prefix; has_dynamic_prefix_match returns True."""
    table = SymbolTable()
    table.register_dynamic_prefix(".model.part_")
    assert table.has_dynamic_prefix_match(".model.part_1")
    assert table.has_dynamic_prefix_match(".model.part_1.cm")
    assert table.has_dynamic_prefix_match(".model.part_99.marker")


def test_symbol_table_dynamic_prefix_case_insensitive():
    """Dynamic prefix matching is case-insensitive."""
    table = SymbolTable()
    table.register_dynamic_prefix(".Model.Part_")
    assert table.has_dynamic_prefix_match(".model.part_1")
    assert table.has_dynamic_prefix_match(".MODEL.PART_1.CM")


def test_symbol_table_dynamic_prefix_no_match_for_unrelated_name():
    """A reference with a different root does not match the dynamic prefix."""
    table = SymbolTable()
    table.register_dynamic_prefix(".model.part_")
    assert not table.has_dynamic_prefix_match(".model.other_1")
    assert not table.has_dynamic_prefix_match(".other_model.part_1")


def test_symbol_table_no_dynamic_prefixes_returns_false():
    """has_dynamic_prefix_match returns False when no prefixes are registered."""
    table = SymbolTable()
    assert not table.has_dynamic_prefix_match(".model.part_1")


def test_build_symbol_table_eval_new_object_registers_dynamic_prefix():
    """marker_name = (eval(...)) must register the leading literal as a dynamic prefix."""
    schema = Schema.load()
    text = (
        'marker create &\n'
        '    marker_name = (eval(".model.mass_" // RTOI(i) // ".cm")) &\n'
        '    location    = 0.0, 0.0, 0.0\n'
    )
    stmts = parse(text)
    table = build_symbol_table(stmts, schema)
    # The eval expression prefix ".model.mass_" must be registered
    assert table.has_dynamic_prefix_match(".model.mass_1.cm"), (
        "Dynamic prefix '.model.mass_' should match '.model.mass_1.cm'"
    )
    assert table.has_dynamic_prefix_match(".model.mass_42"), (
        "Dynamic prefix '.model.mass_' should match any suffix"
    )
    # Plain symbol registration must NOT be contaminated
    assert not table.has(".model.mass_1.cm"), (
        "Eval expression must not be registered as a plain symbol"
    )


def test_build_symbol_table_plain_new_object_still_registers_symbol():
    """Non-eval new_object args are still registered as plain symbols (no regression)."""
    schema = Schema.load()
    stmts = parse("marker create marker_name = .model.PART_1.MAR_1 location = 0,0,0")
    table = build_symbol_table(stmts, schema)
    assert table.has(".model.PART_1.MAR_1"), "Plain name must still register as a symbol"

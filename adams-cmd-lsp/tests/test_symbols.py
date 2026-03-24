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
    """Comments and blank lines produce no symbols."""
    schema = Schema.load()
    stmts = parse("! just a comment\n\n")
    table = build_symbol_table(stmts, schema)
    assert table.symbols == {}


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

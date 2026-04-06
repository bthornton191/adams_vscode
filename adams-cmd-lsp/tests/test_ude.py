"""Tests for adams_cmd_lsp.ude module."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from adams_cmd_lsp.ude import (
    UdeParameter,
    UdeDefinition,
    UdeRegistry,
    _extract_leaf_name,
    _split_comma_values,
    parse_ude_definitions,
    parse_ude_file,
)
from adams_cmd_lsp.schema import Schema
from adams_cmd_lsp.parser import parse

_schema = Schema.load()


# ---------------------------------------------------------------------------
# _extract_leaf_name
# ---------------------------------------------------------------------------

def test_extract_leaf_dollar_path():
    assert _extract_leaf_name("$model.damprat") == "damprat"


def test_extract_leaf_dot_path():
    assert _extract_leaf_name(".model.damprat") == "damprat"


def test_extract_leaf_bare_name():
    assert _extract_leaf_name("damprat") == "damprat"


def test_extract_leaf_eval_skipped():
    assert _extract_leaf_name("(eval($model.damprat))") is None


def test_extract_leaf_empty():
    assert _extract_leaf_name("") is None


def test_extract_leaf_quoted():
    # quotes are stripped before splitting
    assert _extract_leaf_name('"$model.od"') == "od"


# ---------------------------------------------------------------------------
# _split_comma_values
# ---------------------------------------------------------------------------

def test_split_simple():
    assert _split_comma_values("a, b, c") == ["a", "b", "c"]


def test_split_parens_preserved():
    result = _split_comma_values("(eval(a, b)), c")
    assert len(result) == 2
    assert result[0] == "(eval(a, b))"
    assert result[1] == "c"


def test_split_quoted_commas():
    result = _split_comma_values('"hello, world", b')
    assert len(result) == 2
    assert result[0] == '"hello, world"'
    assert result[1] == "b"


def test_split_empty():
    assert _split_comma_values("") == []


# ---------------------------------------------------------------------------
# parse_ude_definitions — ude create definition
# ---------------------------------------------------------------------------

def test_parse_ude_create_definition_basic():
    """A basic ude create definition should extract definition name and all parameter categories."""
    text = (
        "ude create definition "
        "definition_name=.lib.my_ude "
        "parameters=$model.damprat, $model.stiffness "
        "input_parameters=$model.ref_mkr "
        "output_parameters=$model.height, $model.n_elements\n"
    )
    stmts = parse(text)
    defs = parse_ude_definitions(stmts, _schema)
    assert len(defs) == 1
    d = defs[0]
    assert d.definition_name == ".lib.my_ude"
    assert "damprat" in d.parameters
    assert "stiffness" in d.parameters
    assert d.parameters["damprat"].category == "parameter"
    assert "ref_mkr" in d.parameters
    assert d.parameters["ref_mkr"].category == "input"
    assert "height" in d.parameters
    assert d.parameters["height"].category == "output"
    assert "n_elements" in d.parameters
    assert d.parameters["n_elements"].category == "output"


def test_parse_ude_create_definition_no_params():
    text = "ude create definition definition_name=.lib.empty_ude\n"
    stmts = parse(text)
    defs = parse_ude_definitions(stmts, _schema)
    assert len(defs) == 1
    assert len(defs[0].parameters) == 0


def test_parse_ude_create_definition_eval_params_skipped():
    """Parameters that are eval() expressions should be skipped."""
    text = (
        "ude create definition "
        "definition_name=.lib.my_ude "
        "parameters=(eval($_self.parts)), $model.damprat\n"
    )
    stmts = parse(text)
    defs = parse_ude_definitions(stmts, _schema)
    assert len(defs) == 1
    assert "damprat" in defs[0].parameters
    assert len(defs[0].parameters) == 1


def test_parse_ude_create_definition_continuation():
    """ude create definition with continuation lines should parse all parameters."""
    text = (
        "ude create definition &\n"
        "   definition_name = .lib.flex_comp &\n"
        "   parameters = $model.damprat, &\n"
        "                $model.od, &\n"
        "                $model.elevation &\n"
        "   output_parameters = $model.height\n"
    )
    stmts = parse(text)
    defs = parse_ude_definitions(stmts, _schema)
    assert len(defs) == 1
    d = defs[0]
    assert d.definition_name == ".lib.flex_comp"
    assert "damprat" in d.parameters
    assert "od" in d.parameters
    assert "elevation" in d.parameters
    assert "height" in d.parameters
    assert d.parameters["height"].category == "output"


# ---------------------------------------------------------------------------
# parse_ude_definitions — ude copy
# ---------------------------------------------------------------------------

def test_parse_ude_copy_inherits_params():
    """ude copy should inherit all parameters from the source definition."""
    text = (
        "ude create definition "
        "definition_name=.lib.my_ude "
        "parameters=$model.damprat, $model.stiffness\n"
        "ude copy "
        "definition_name=.lib.my_ude "
        "new_definition_name=.model.my_copy\n"
    )
    stmts = parse(text)
    defs = parse_ude_definitions(stmts, _schema)
    assert len(defs) == 2
    copy = defs[1]
    assert copy.definition_name == ".model.my_copy"
    assert "damprat" in copy.parameters
    assert "stiffness" in copy.parameters


def test_parse_ude_copy_unknown_source():
    """ude copy of an unknown source should still register with empty params."""
    text = (
        "ude copy "
        "definition_name=.lib.unknown "
        "new_definition_name=.model.my_copy\n"
    )
    stmts = parse(text)
    defs = parse_ude_definitions(stmts, _schema)
    assert len(defs) == 1
    assert defs[0].definition_name == ".model.my_copy"
    assert len(defs[0].parameters) == 0


# ---------------------------------------------------------------------------
# parse_ude_definitions — ude modify definition
# ---------------------------------------------------------------------------

def test_parse_ude_modify_rename_only():
    """Rename via new_definition_name should update the definition name."""
    text = (
        "ude create definition "
        "definition_name=.lib.old_name "
        "parameters=$model.damprat\n"
        "ude modify definition "
        "definition_name=.lib.old_name "
        "new_definition_name=.lib.new_name\n"
    )
    stmts = parse(text)
    defs = parse_ude_definitions(stmts, _schema)
    assert len(defs) == 1
    assert defs[0].definition_name == ".lib.new_name"
    assert "damprat" in defs[0].parameters


def test_parse_ude_modify_replace_parameters():
    """Modifying parameters= should replace the parameter category entirely."""
    text = (
        "ude create definition "
        "definition_name=.lib.my_ude "
        "parameters=$model.old_param\n"
        "ude modify definition "
        "definition_name=.lib.my_ude "
        "parameters=$model.new_param_a, $model.new_param_b\n"
    )
    stmts = parse(text)
    defs = parse_ude_definitions(stmts, _schema)
    assert len(defs) == 1
    d = defs[0]
    assert "old_param" not in d.parameters
    assert "new_param_a" in d.parameters
    assert "new_param_b" in d.parameters


def test_parse_ude_modify_partial_replace():
    """Modifying only output_parameters= should leave parameters untouched."""
    text = (
        "ude create definition "
        "definition_name=.lib.my_ude "
        "parameters=$model.stiffness "
        "output_parameters=$model.old_out\n"
        "ude modify definition "
        "definition_name=.lib.my_ude "
        "output_parameters=$model.new_out\n"
    )
    stmts = parse(text)
    defs = parse_ude_definitions(stmts, _schema)
    assert len(defs) == 1
    d = defs[0]
    # parameters category untouched
    assert "stiffness" in d.parameters
    assert d.parameters["stiffness"].category == "parameter"
    # output_parameters replaced
    assert "old_out" not in d.parameters
    assert "new_out" in d.parameters
    assert d.parameters["new_out"].category == "output"


def test_parse_ude_modify_unknown_def_noop():
    """ude modify definition for an unknown name should not crash and be a no-op."""
    text = (
        "ude modify definition "
        "definition_name=.lib.nonexistent "
        "parameters=$model.x\n"
    )
    stmts = parse(text)
    defs = parse_ude_definitions(stmts, _schema)
    assert defs == []


# ---------------------------------------------------------------------------
# UdeRegistry
# ---------------------------------------------------------------------------

def test_registry_register_and_lookup():
    reg = UdeRegistry()
    d = UdeDefinition(
        definition_name=".lib.my_ude",
        parameters={"damprat": UdeParameter(name="damprat")},
    )
    reg.register(d)
    assert len(reg) == 1
    assert reg.lookup(".lib.my_ude") is d


def test_registry_lookup_by_leaf():
    reg = UdeRegistry()
    d = UdeDefinition(definition_name=".lib.my_ude")
    reg.register(d)
    assert reg.lookup("my_ude") is d


def test_registry_lookup_case_insensitive():
    reg = UdeRegistry()
    d = UdeDefinition(definition_name=".Lib.My_UDE")
    reg.register(d)
    assert reg.lookup(".lib.my_ude") is d
    assert reg.lookup("My_UDE") is d


def test_registry_unregister_by_file():
    reg = UdeRegistry()
    d = UdeDefinition(definition_name=".lib.my_ude", source_file="/test/file.cmd")
    reg.register(d)
    assert len(reg) == 1
    reg.unregister_by_file("/test/file.cmd")
    assert len(reg) == 0
    assert reg.lookup(".lib.my_ude") is None


def test_registry_lookup_missing():
    reg = UdeRegistry()
    assert reg.lookup("nonexistent") is None


# ---------------------------------------------------------------------------
# Symbol table integration — assembly create instance
# ---------------------------------------------------------------------------

def test_ude_instance_registers_no_i202():
    """assembly create instance for a known UDE should not fire I202 for the instance."""
    from adams_cmd_lsp.linter import lint_text

    reg = UdeRegistry()
    reg.register(UdeDefinition(
        definition_name=".lib.my_ude",
        parameters={
            "damprat": UdeParameter(name="damprat", category="parameter"),
            "height":  UdeParameter(name="height",  category="output"),
        },
    ))

    text = (
        "assembly create instance "
        "definition_name=.lib.my_ude "
        "instance_name=.model.my_inst\n"
    )
    diags = lint_text(text, ude_registry=reg)
    i202 = [d for d in diags if d.code == "I202"]
    assert len(i202) == 0, f"Unexpected I202: {i202}"


def test_ude_instance_child_symbol_resolvable():
    """build_symbol_table should register child symbols for UDE instance parameters."""
    from adams_cmd_lsp.symbols import build_symbol_table

    reg = UdeRegistry()
    reg.register(UdeDefinition(
        definition_name=".lib.my_ude",
        parameters={
            "damprat": UdeParameter(name="damprat"),
            "height":  UdeParameter(name="height"),
        },
    ))

    text = (
        "assembly create instance "
        "definition_name=.lib.my_ude "
        "instance_name=.model.my_inst\n"
    )
    stmts = parse(text)
    for s in stmts:
        if not s.is_comment and not s.is_blank and not s.is_control_flow:
            tokens = s.command_key.split()
            resolved, _ = _schema.resolve_command_key(tokens)
            if resolved:
                s.resolved_command_key = resolved

    table = build_symbol_table(stmts, _schema, ude_registry=reg)
    assert table.has(".model.my_inst"), "Instance should be registered"
    assert table.has(".model.my_inst.damprat"), "Child param 'damprat' should be registered"
    assert table.has(".model.my_inst.height"),  "Child param 'height' should be registered"

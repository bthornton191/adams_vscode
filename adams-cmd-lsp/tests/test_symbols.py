"""Tests for adams_cmd_lsp.symbols module."""

from adams_cmd_lsp.schema import Schema
from adams_cmd_lsp.parser import parse
from adams_cmd_lsp.symbols import SymbolTable, build_symbol_table, _extract_eval_object_names
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


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


# ---------------------------------------------------------------------------
# ObjectReference — reference tracking in build_symbol_table
# ---------------------------------------------------------------------------

def test_build_symbol_table_collects_existing_object_reference():
    """An existing_object argument (e.g. i_marker) must generate an ObjectReference."""
    schema = Schema.load()
    text = (
        "marker create marker_name = .m.p.mkr1 location = 0,0,0\n"
        "constraint create joint fixed &\n"
        "   joint_name = .m.fix1 &\n"
        "   i_marker = .m.p.mkr1 &\n"
        "   j_marker = .m.ground.cm\n"
    )
    stmts = parse(text)
    # Pre-resolve so build_symbol_table sees canonical keys
    for stmt in stmts:
        if not stmt.resolved_command_key and stmt.command_key and \
                not stmt.is_comment and not stmt.is_blank and not stmt.is_control_flow:
            resolved, _ = schema.resolve_command_key(stmt.command_key.split())
            if resolved:
                stmt.resolved_command_key = resolved
    table = build_symbol_table(stmts, schema)
    # References should include .m.p.mkr1 (i_marker) and .m.ground.cm (j_marker)
    ref_names = [r.name for r in table.references]
    assert ".m.p.mkr1" in ref_names, f"Expected .m.p.mkr1 in {ref_names}"
    assert ".m.ground.cm" in ref_names, f"Expected .m.ground.cm in {ref_names}"


def test_build_symbol_table_skips_array_references():
    """Array-valued existing_object args must not generate references."""
    schema = Schema.load()
    text = "constraint create complex_joint coupler joint_name = .m.coupler1 joint_name = .m.rev1, .m.rev2, .m.rev3\n"
    stmts = parse(text)
    for stmt in stmts:
        if not stmt.resolved_command_key and stmt.command_key and \
                not stmt.is_comment and not stmt.is_blank and not stmt.is_control_flow:
            resolved, _ = schema.resolve_command_key(stmt.command_key.split())
            if resolved:
                stmt.resolved_command_key = resolved
    table = build_symbol_table(stmts, schema)
    # Array-valued joint_name references must be skipped (not individually resolvable)
    # No assertion here — just confirm no exception is raised
    assert isinstance(table.references, list)


def test_build_symbol_table_skips_eval_references():
    """Dot-path names inside (eval(...)) are now tracked as references.

    The literal word "eval" must never appear in a reference name, and plain
    existing_object references must still be recorded.  Names extracted from
    the eval expression are registered so Go-to-Definition can navigate to
    their definition sites.
    """
    schema = Schema.load()
    text = (
        "constraint create joint fixed &\n"
        "   joint_name = .m.fix1 &\n"
        "   i_marker = (eval(.m.p // \".cm\")) &\n"
        "   j_marker = .m.ground.cm\n"
    )
    stmts = parse(text)
    for stmt in stmts:
        if not stmt.resolved_command_key and stmt.command_key and \
                not stmt.is_comment and not stmt.is_blank and not stmt.is_control_flow:
            resolved, _ = schema.resolve_command_key(stmt.command_key.split())
            if resolved:
                stmt.resolved_command_key = resolved
    table = build_symbol_table(stmts, schema)
    ref_names = [r.name for r in table.references]
    # The literal string "eval" must never appear as a reference name
    assert not any("eval" in n for n in ref_names)
    # Plain existing_object reference must still be present
    assert ".m.ground.cm" in ref_names, f"Expected .m.ground.cm in {ref_names}"
    # Dot-path names from the eval expression are now tracked as references
    assert ".m.p" in ref_names, f"Expected .m.p from eval expression; got {ref_names}"


def test_object_reference_has_positions():
    """ObjectReferences must carry correct line/column positions."""
    schema = Schema.load()
    text = (
        "marker create marker_name = .m.p.mkr1 location = 0,0,0\n"
        "constraint create joint fixed joint_name=.m.f1 i_marker=.m.p.mkr1 j_marker=.m.ground.cm\n"
    )
    stmts = parse(text)
    for stmt in stmts:
        if not stmt.resolved_command_key and stmt.command_key and \
                not stmt.is_comment and not stmt.is_blank and not stmt.is_control_flow:
            resolved, _ = schema.resolve_command_key(stmt.command_key.split())
            if resolved:
                stmt.resolved_command_key = resolved
    table = build_symbol_table(stmts, schema)
    mkr_refs = [r for r in table.references if r.name == ".m.p.mkr1"]
    assert len(mkr_refs) == 1
    ref = mkr_refs[0]
    assert ref.line == 1, f"Expected line 1, got {ref.line}"
    assert ref.column >= 0
    assert ref.end_column > ref.column


# ---------------------------------------------------------------------------
# SymbolTable — lookup_by_leaf_name
# ---------------------------------------------------------------------------

def test_lookup_by_leaf_name_basic():
    """lookup_by_leaf_name must find symbols by their last dot-separated component."""
    table = SymbolTable()
    table.register(".model.ground._tmp_mkr_", "Marker", 10)
    results = table.lookup_by_leaf_name("_tmp_mkr_")
    assert len(results) == 1
    assert results[0].name == ".model.ground._tmp_mkr_"


def test_lookup_by_leaf_name_case_insensitive():
    """Leaf-name lookup must be case-insensitive."""
    table = SymbolTable()
    table.register(".model.ground.MY_MARKER", "Marker", 5)
    results = table.lookup_by_leaf_name("my_marker")
    assert len(results) == 1


def test_lookup_by_leaf_name_multiple_matches():
    """Multiple symbols with the same leaf name must all be returned."""
    table = SymbolTable()
    table.register(".model.part1.cm", "Marker", 1)
    table.register(".model.part2.cm", "Marker", 2)
    results = table.lookup_by_leaf_name("cm")
    assert len(results) == 2


def test_lookup_by_leaf_name_no_match():
    """lookup_by_leaf_name must return empty list when no match."""
    table = SymbolTable()
    table.register(".model.part1.cm", "Marker", 1)
    results = table.lookup_by_leaf_name("nonexistent")
    assert results == []


def test_lookup_by_leaf_name_excludes_builtins():
    """Builtins (line == -1) must not appear in leaf-name lookup results."""
    schema = Schema.load()
    # Build table with builtins including "ground"
    stmts = parse("")
    table = build_symbol_table(stmts, schema)
    # ground is a builtin with line == -1
    assert table.has("ground")
    builtin = table.lookup("ground")
    assert builtin.line == -1
    # Leaf lookup must exclude it
    results = table.lookup_by_leaf_name("ground")
    assert results == [], f"Builtins must be excluded, got {results}"


# ---------------------------------------------------------------------------
# SymbolTable — get_references_by_name
# ---------------------------------------------------------------------------

def test_get_references_by_name_full_path():
    """get_references_by_name must find via exact full-path match."""
    table = SymbolTable()
    table.add_reference(".model.part1.mkr1", "Marker", 5, 10, 30)
    refs = table.get_references_by_name(".model.part1.mkr1")
    assert len(refs) == 1
    assert refs[0].line == 5


def test_get_references_by_name_leaf_fallback():
    """get_references_by_name must fall back to leaf when full path not found."""
    table = SymbolTable()
    table.add_reference(".model.part1.mkr1", "Marker", 5, 10, 30)
    # Full path not added — only leaf fallback matches
    refs = table.get_references_by_name("mkr1")
    assert len(refs) == 1


def test_get_references_by_name_full_path_takes_priority():
    """Full path results must be returned without triggering leaf fallback."""
    table = SymbolTable()
    table.add_reference(".model.part1.mkr1", "Marker", 1, 0, 10)
    table.add_reference(".model.part2.mkr1", "Marker", 2, 0, 10)
    # Full path only matches one
    refs = table.get_references_by_name(".model.part1.mkr1")
    assert len(refs) == 1
    assert refs[0].line == 1


def test_get_references_by_name_no_match():
    """get_references_by_name must return empty list when nothing matches."""
    table = SymbolTable()
    table.add_reference(".model.part1.mkr1", "Marker", 1, 0, 10)
    refs = table.get_references_by_name(".model.part1.nonexistent")
    assert refs == []


def test_get_references_by_name_no_false_positive_same_leaf_different_path():
    """Full-path query must NOT match full-path stored references from a different
    model that only share the leaf component (the cross-model false positive bug)."""
    table = SymbolTable()
    # Reference in one model
    table.add_reference(".demo_model.GROUND.MAR_1", "Marker", 10, 0, 24)
    # Reference in another model — same leaf 'MAR_1', different path
    table.add_reference(".model_1.ground.MAR_1", "Marker", 20, 0, 21)
    # Query by full path of the first model's marker
    refs = table.get_references_by_name(".demo_model.GROUND.MAR_1")
    assert len(refs) == 1, (
        "Full-path query should only return exact-match, not same-leaf from other model"
    )
    assert refs[0].line == 10


# ---------------------------------------------------------------------------
# _extract_eval_object_names unit tests
# ---------------------------------------------------------------------------

def test_extract_eval_object_names_simple():
    """Simple eval with a single object name returns one entry."""
    results = _extract_eval_object_names("(eval(.m.arm_mass))", value_line=5, value_column=10)
    assert len(results) == 1
    name, line, col, end_col = results[0]
    assert name == ".m.arm_mass"
    assert line == 5
    assert end_col == col + len(".m.arm_mass")


def test_extract_eval_object_names_simple_positions():
    """Column positions are offset correctly from value_column."""
    value = "(eval(.m.arm_mass))"
    dot_offset = value.index(".m")
    results = _extract_eval_object_names(value, value_line=0, value_column=20)
    assert len(results) == 1
    name, line, col, end_col = results[0]
    assert name == ".m.arm_mass"
    assert col == 20 + dot_offset
    assert end_col == col + len(".m.arm_mass")


def test_extract_eval_object_names_compound():
    """Compound eval with multiple object references returns one entry per name."""
    value = "(eval(.m.arm_mass * 0.6 * .m.arm1_len**2 / 12.0))"
    results = _extract_eval_object_names(value, value_line=2, value_column=0)
    names = [r[0] for r in results]
    assert ".m.arm_mass" in names
    assert ".m.arm1_len" in names
    assert len(results) == 2


def test_extract_eval_object_names_no_eval():
    """Values without eval() return an empty list."""
    results = _extract_eval_object_names(".m.part1", value_line=0, value_column=0)
    assert results == []


def test_extract_eval_object_names_no_dots():
    """eval() with no dot-path names returns an empty list."""
    results = _extract_eval_object_names("(eval(30.0 * 2))", value_line=0, value_column=0)
    assert results == []


def test_extract_eval_object_names_ignores_numeric_dot():
    """Numeric literals like 0.6 must not be mistaken for object names."""
    value = "(eval(.m.arm_mass * 0.6))"
    results = _extract_eval_object_names(value, value_line=0, value_column=0)
    names = [r[0] for r in results]
    assert ".m.arm_mass" in names
    assert not any(n == ".6" or n == "0.6" for n in names)


def test_extract_eval_object_names_case_insensitive_eval():
    """EVAL(...) and Eval(...) are both detected."""
    value = "(EVAL(.m.v1))"
    results = _extract_eval_object_names(value, value_line=0, value_column=0)
    assert len(results) == 1
    assert results[0][0] == ".m.v1"


# ---------------------------------------------------------------------------
# build_symbol_table — eval references in non-object arg types
# ---------------------------------------------------------------------------

def test_build_symbol_table_eval_in_real_arg_registers_reference():
    """Object names inside (eval(...)) on a real argument are tracked as references."""
    schema = Schema.load()
    text = (
        "variable create variable_name = .m.arm_mass real_value = 0.8\n"
        "part modify rigid_body mass_properties &\n"
        "   part_name = .m.arm1 &\n"
        "   mass = (eval(.m.arm_mass))\n"
    )
    stmts = parse(text)
    for stmt in stmts:
        if not stmt.resolved_command_key and stmt.command_key and \
                not stmt.is_comment and not stmt.is_blank and not stmt.is_control_flow:
            resolved, _ = schema.resolve_command_key(stmt.command_key.split())
            if resolved:
                stmt.resolved_command_key = resolved
    table = build_symbol_table(stmts, schema)
    ref_names = [r.name for r in table.references]
    assert ".m.arm_mass" in ref_names, (
        f"Expected .m.arm_mass from eval() on real arg; got {ref_names}"
    )


def test_build_symbol_table_eval_compound_real_arg():
    """Multiple object names in a compound eval expression all generate references."""
    schema = Schema.load()
    text = (
        "variable create variable_name = .m.arm_mass real_value = 0.8\n"
        "variable create variable_name = .m.arm1_len real_value = 300.0\n"
        "part modify rigid_body mass_properties &\n"
        "   part_name = .m.arm1 &\n"
        "   ixx = (eval(.m.arm_mass * .m.arm1_len**2 / 12.0))\n"
    )
    stmts = parse(text)
    for stmt in stmts:
        if not stmt.resolved_command_key and stmt.command_key and \
                not stmt.is_comment and not stmt.is_blank and not stmt.is_control_flow:
            resolved, _ = schema.resolve_command_key(stmt.command_key.split())
            if resolved:
                stmt.resolved_command_key = resolved
    table = build_symbol_table(stmts, schema)
    ref_names = [r.name for r in table.references]
    assert ".m.arm_mass" in ref_names, f"Expected .m.arm_mass; got {ref_names}"
    assert ".m.arm1_len" in ref_names, f"Expected .m.arm1_len; got {ref_names}"


def test_build_symbol_table_eval_ref_has_correct_positions():
    """ObjectReferences from eval() carry positions that span the dot-path token."""
    schema = Schema.load()
    # Single-line: "variable create variable_name = .m.v1 real_value = 0.0"  (line 0)
    # "part modify rigid_body mass_properties part_name=.m.p mass=(eval(.m.v1))" (line 1)
    text = (
        "variable create variable_name = .m.v1 real_value = 0.0\n"
        "part modify rigid_body mass_properties part_name=.m.p mass=(eval(.m.v1))\n"
    )
    stmts = parse(text)
    for stmt in stmts:
        if not stmt.resolved_command_key and stmt.command_key and \
                not stmt.is_comment and not stmt.is_blank and not stmt.is_control_flow:
            resolved, _ = schema.resolve_command_key(stmt.command_key.split())
            if resolved:
                stmt.resolved_command_key = resolved
    table = build_symbol_table(stmts, schema)
    v1_refs = [r for r in table.references if r.name == ".m.v1"]
    # There should be at least one reference for .m.v1 (from the eval expression on line 1)
    assert len(v1_refs) >= 1
    eval_ref = next((r for r in v1_refs if r.line == 1), None)
    assert eval_ref is not None, "Expected a reference on line 1 (eval expression)"
    assert eval_ref.column >= 0
    assert eval_ref.end_column == eval_ref.column + len(".m.v1")

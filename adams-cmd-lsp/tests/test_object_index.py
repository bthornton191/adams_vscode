"""Tests for adams_cmd_lsp.object_index module."""

from adams_cmd_lsp.schema import Schema
from adams_cmd_lsp.object_index import (
    IndexedDefinition, IndexedReference, ObjectIndex, index_file_objects,
)
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# ---------------------------------------------------------------------------
# ObjectIndex — definitions
# ---------------------------------------------------------------------------

def test_object_index_update_and_get_definitions():
    """update_file must store definitions; get_definitions must return them."""
    idx = ObjectIndex()
    defs = [
        IndexedDefinition(name=".model.PART_1", object_type="Part", line=0, source_file="/a.cmd"),
        IndexedDefinition(name=".model.PART_1.CM", object_type="Marker", line=1, source_file="/a.cmd"),
    ]
    idx.update_file("/a.cmd", defs, [])
    results = idx.get_definitions(".model.PART_1")
    assert len(results) == 1
    assert results[0].object_type == "Part"


def test_object_index_get_definitions_leaf_fallback():
    """get_definitions must fall back to leaf name when full path not found."""
    idx = ObjectIndex()
    defs = [IndexedDefinition(name=".model.PART_1.CM", object_type="Marker", line=0, source_file="/a.cmd")]
    idx.update_file("/a.cmd", defs, [])
    results = idx.get_definitions("CM")
    assert len(results) == 1


def test_object_index_get_definitions_full_path_priority():
    """Full-path match must be returned without triggering leaf fallback."""
    idx = ObjectIndex()
    defs = [
        IndexedDefinition(name=".model.PART_1.CM", object_type="Marker", line=0, source_file="/a.cmd"),
        IndexedDefinition(name=".model.PART_2.CM", object_type="Marker", line=1, source_file="/a.cmd"),
    ]
    idx.update_file("/a.cmd", defs, [])
    results = idx.get_definitions(".model.PART_1.CM")
    assert len(results) == 1
    assert results[0].line == 0


def test_object_index_get_definitions_case_insensitive():
    """Lookups must be case-insensitive."""
    idx = ObjectIndex()
    defs = [IndexedDefinition(name=".Model.Part_1", object_type="Part", line=3, source_file="/a.cmd")]
    idx.update_file("/a.cmd", defs, [])
    results = idx.get_definitions(".model.part_1")
    assert len(results) == 1


def test_object_index_remove_file_clears_entries():
    """remove_file must remove all definitions and references for the file."""
    idx = ObjectIndex()
    defs = [IndexedDefinition(name=".model.P1", object_type="Part", line=0, source_file="/a.cmd")]
    refs = [IndexedReference(name=".model.P1", object_type="Part", line=5, column=10, end_column=20, source_file="/a.cmd")]
    idx.update_file("/a.cmd", defs, refs)
    idx.remove_file("/a.cmd")
    assert idx.get_definitions(".model.P1") == []
    assert idx.get_references(".model.P1") == []


def test_object_index_update_file_replaces_stale_entries():
    """Calling update_file twice for the same path must replace previous entries."""
    idx = ObjectIndex()
    defs1 = [IndexedDefinition(name=".model.OLD", object_type="Part", line=0, source_file="/a.cmd")]
    defs2 = [IndexedDefinition(name=".model.NEW", object_type="Part", line=0, source_file="/a.cmd")]
    idx.update_file("/a.cmd", defs1, [])
    idx.update_file("/a.cmd", defs2, [])
    assert idx.get_definitions(".model.OLD") == []
    assert len(idx.get_definitions(".model.NEW")) == 1


def test_object_index_no_duplicate_leaf_entries_after_update():
    """After a second update_file the leaf index must not accumulate duplicates."""
    idx = ObjectIndex()
    defs = [IndexedDefinition(name=".model.P1.CM", object_type="Marker", line=0, source_file="/a.cmd")]
    idx.update_file("/a.cmd", defs, [])
    idx.update_file("/a.cmd", defs, [])
    results = idx.get_definitions("CM")
    assert len(results) == 1, f"Expected 1, got {len(results)}"


# ---------------------------------------------------------------------------
# ObjectIndex — references
# ---------------------------------------------------------------------------

def test_object_index_get_references():
    """get_references must return stored references."""
    idx = ObjectIndex()
    refs = [
        IndexedReference(name=".model.P1.CM", object_type="Marker", line=3, column=12, end_column=25, source_file="/b.cmd"),
    ]
    idx.update_file("/b.cmd", [], refs)
    results = idx.get_references(".model.P1.CM")
    assert len(results) == 1
    assert results[0].line == 3


def test_object_index_references_leaf_fallback():
    """get_references must fall back to leaf when full path not found."""
    idx = ObjectIndex()
    refs = [IndexedReference(name=".model.P1.CM", object_type="Marker", line=0, column=0, end_column=5, source_file="/b.cmd")]
    idx.update_file("/b.cmd", [], refs)
    results = idx.get_references("CM")
    assert len(results) == 1


def test_object_index_no_false_positive_same_leaf_different_path():
    """A full-path reference to one model must NOT match a full-path reference in
    another model that only shares the leaf name (e.g. MAR_1 in two models)."""
    idx = ObjectIndex()
    # Reference in model_a (.demo_model.GROUND.MAR_1)
    idx.update_file("/model_a.cmd", [], [
        IndexedReference(name=".demo_model.GROUND.MAR_1", object_type="Marker",
                         line=0, column=0, end_column=22, source_file="/model_a.cmd"),
    ])
    # Reference in model_b (.model_1.ground.MAR_1) — different model, same leaf
    idx.update_file("/model_b.cmd", [], [
        IndexedReference(name=".model_1.ground.MAR_1", object_type="Marker",
                         line=5, column=0, end_column=21, source_file="/model_b.cmd"),
    ])
    # Query by full path — must NOT return model_b's reference
    results = idx.get_references(".demo_model.GROUND.MAR_1")
    assert len(results) == 1
    assert results[0].source_file == "/model_a.cmd"


def test_object_index_no_false_positive_same_leaf_definitions():
    """A full-path definition query must NOT match definitions from a different
    model that only shares the leaf name."""
    idx = ObjectIndex()
    idx.update_file("/model_a.cmd", [
        IndexedDefinition(name=".demo_model.GROUND.MAR_1", object_type="Marker",
                          line=0, source_file="/model_a.cmd"),
    ], [])
    idx.update_file("/model_b.cmd", [
        IndexedDefinition(name=".model_1.ground.MAR_1", object_type="Marker",
                          line=0, source_file="/model_b.cmd"),
    ], [])
    results = idx.get_definitions(".demo_model.GROUND.MAR_1")
    assert len(results) == 1
    assert results[0].source_file == "/model_a.cmd"


def test_object_index_leaf_query_still_matches_full_path():
    """A leaf-only query like 'MAR_1' must still match full-path entries."""
    idx = ObjectIndex()
    idx.update_file("/a.cmd", [], [
        IndexedReference(name=".model.GROUND.MAR_1", object_type="Marker",
                         line=0, column=0, end_column=20, source_file="/a.cmd"),
    ])
    results = idx.get_references("MAR_1")
    assert len(results) == 1


def test_object_index_cross_file_definitions():
    """Definitions from multiple files must all be returned."""
    idx = ObjectIndex()
    idx.update_file("/a.cmd", [
        IndexedDefinition(name=".model.P1", object_type="Part", line=0, source_file="/a.cmd"),
    ], [])
    idx.update_file("/b.cmd", [
        IndexedDefinition(name=".model.P1", object_type="Part", line=0, source_file="/b.cmd"),
    ], [])
    results = idx.get_definitions(".model.P1")
    assert len(results) == 2
    source_files = {r.source_file for r in results}
    assert "/a.cmd" in source_files
    assert "/b.cmd" in source_files


# ---------------------------------------------------------------------------
# index_file_objects — integration
# ---------------------------------------------------------------------------

def test_index_file_objects_definitions():
    """index_file_objects must extract new_object definitions."""
    schema = Schema.load()
    text = (
        "model create model_name = my_model\n"
        "part create rigid_body name_and_position part_name = my_model.PART_1\n"
        "marker create marker_name = my_model.PART_1.CM location = 0,0,0\n"
    )
    defs, refs = index_file_objects(text, schema, source_file="/test.cmd")
    def_names = [d.name for d in defs]
    assert ".my_model" in def_names or "my_model" in [d.name.lstrip('.') for d in defs]
    part_defs = [d for d in defs if d.name.lower().rsplit('.', 1)[-1] == 'part_1']
    assert len(part_defs) == 1
    marker_defs = [d for d in defs if "CM" in d.name]
    assert len(marker_defs) == 1


def test_index_file_objects_references():
    """index_file_objects must extract existing_object references."""
    schema = Schema.load()
    text = (
        "marker create marker_name = .m.p.mkr1 location = 0,0,0\n"
        "constraint create joint fixed &\n"
        "   joint_name = .m.fix1 &\n"
        "   i_marker = .m.p.mkr1 &\n"
        "   j_marker = .m.ground.cm\n"
    )
    defs, refs = index_file_objects(text, schema, source_file="/test.cmd")
    ref_names = [r.name for r in refs]
    assert ".m.p.mkr1" in ref_names, f"i_marker ref not found: {ref_names}"
    assert ".m.ground.cm" in ref_names


def test_index_file_objects_excludes_builtins():
    """index_file_objects must not include builtin symbols (line == -1) in definitions."""
    schema = Schema.load()
    text = "model create model_name = my_model\n"
    defs, _ = index_file_objects(text, schema, source_file="/test.cmd")
    # No builtin (ground, colors, etc.) must appear
    builtin_names = ["ground", "Black", "White", "front", "back"]
    for name in builtin_names:
        assert not any(d.name.lower().lstrip('.') == name.lower() for d in defs), \
            f"Builtin '{name}' must not appear in definitions"


def test_index_file_objects_source_file_attached():
    """All returned items must carry the source_file path."""
    schema = Schema.load()
    text = (
        "marker create marker_name = .m.p.mkr1 location = 0,0,0\n"
        "constraint create joint fixed joint_name=.m.f1 i_marker=.m.p.mkr1 j_marker=.m.ground.cm\n"
    )
    defs, refs = index_file_objects(text, schema, source_file="/my/file.cmd")
    assert all(d.source_file == "/my/file.cmd" for d in defs)
    assert all(r.source_file == "/my/file.cmd" for r in refs)


def test_index_file_objects_empty_text():
    """Empty text must return empty lists without raising."""
    schema = Schema.load()
    defs, refs = index_file_objects("", schema, source_file="/test.cmd")
    assert defs == []
    assert refs == []


def test_index_file_objects_no_schema_commands():
    """Text with no recognized commands must produce no definitions."""
    schema = Schema.load()
    text = "! just a comment\n\nnot_a_real_command foo=bar\n"
    defs, refs = index_file_objects(text, schema, source_file="/test.cmd")
    # Unknown commands don't produce definitions
    assert defs == []


# ---------------------------------------------------------------------------
# ObjectIndex — mtime helpers
# ---------------------------------------------------------------------------

def test_object_index_needs_refresh_new_path():
    """Unindexed path must need refresh."""
    idx = ObjectIndex()
    assert idx.needs_refresh("/new/file.cmd")


def test_object_index_needs_refresh_after_record(tmp_path):
    """Path must not need refresh immediately after record_mtime."""
    idx = ObjectIndex()
    f = tmp_path / "a.cmd"
    f.write_text("", encoding="utf-8")
    path = str(f)
    idx.record_mtime(path)
    assert not idx.needs_refresh(path)


# ---------------------------------------------------------------------------
# ObjectIndex — stats
# ---------------------------------------------------------------------------

def test_object_index_total_definitions():
    """total_definitions must count all stored definition entries."""
    idx = ObjectIndex()
    idx.update_file("/a.cmd", [
        IndexedDefinition(name=".m.P1", object_type="Part", line=0, source_file="/a.cmd"),
        IndexedDefinition(name=".m.P2", object_type="Part", line=1, source_file="/a.cmd"),
    ], [])
    assert idx.total_definitions() == 2


def test_object_index_total_references():
    """total_references must count all stored reference entries."""
    idx = ObjectIndex()
    idx.update_file("/a.cmd", [], [
        IndexedReference(name=".m.P1", object_type="Part", line=3, column=0, end_column=5, source_file="/a.cmd"),
    ])
    assert idx.total_references() == 1

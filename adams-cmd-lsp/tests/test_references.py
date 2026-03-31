"""Tests for adams_cmd_lsp.references module.

Pure unit tests — no Adams View, no LSP server.
Covers MacroIndex (CRUD + reverse index) and index_file_text().
"""

from adams_cmd_lsp.schema import Schema
from adams_cmd_lsp.references import MacroIndex, MacroReference, index_file_text
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# Load the real schema once (bundled command_schema.json)
_SCHEMA = Schema.load()


# ---------------------------------------------------------------------------
# MacroReference dataclass
# ---------------------------------------------------------------------------

def test_macro_reference_fields():
    ref = MacroReference(command_key="cdm wear", line=5, column=0, end_column=8)
    assert ref.command_key == "cdm wear"
    assert ref.line == 5
    assert ref.column == 0
    assert ref.end_column == 8


# ---------------------------------------------------------------------------
# MacroIndex — update_file and get_file_refs
# ---------------------------------------------------------------------------

def test_macro_index_update_and_get_file_refs():
    idx = MacroIndex()
    ref = MacroReference(command_key="cdm wear", line=0, column=0, end_column=8)
    idx.update_file("/a/file.cmd", [ref])
    assert idx.get_file_refs("/a/file.cmd") == [ref]


def test_macro_index_update_replaces_previous_refs():
    idx = MacroIndex()
    r1 = MacroReference(command_key="cdm wear", line=0, column=0, end_column=8)
    r2 = MacroReference(command_key="cdm wear", line=10, column=0, end_column=8)
    idx.update_file("/a/file.cmd", [r1])
    idx.update_file("/a/file.cmd", [r2])
    assert idx.get_file_refs("/a/file.cmd") == [r2]


def test_macro_index_empty_refs():
    idx = MacroIndex()
    assert idx.get_file_refs("/nonexistent.cmd") == []


# ---------------------------------------------------------------------------
# MacroIndex — get_references (reverse lookup)
# ---------------------------------------------------------------------------

def test_macro_index_get_references_single_file():
    idx = MacroIndex()
    ref = MacroReference(command_key="cdm wear", line=3, column=0, end_column=8)
    idx.update_file("/proj/use.cmd", [ref])
    results = idx.get_references("cdm wear")
    assert len(results) == 1
    path, r = results[0]
    assert path == "/proj/use.cmd"
    assert r.line == 3


def test_macro_index_get_references_multiple_files():
    idx = MacroIndex()
    r1 = MacroReference(command_key="cdm wear", line=1, column=0, end_column=8)
    r2 = MacroReference(command_key="cdm wear", line=5, column=0, end_column=8)
    idx.update_file("/a.cmd", [r1])
    idx.update_file("/b.cmd", [r2])
    results = idx.get_references("cdm wear")
    assert len(results) == 2
    paths = {p for p, _ in results}
    assert "/a.cmd" in paths
    assert "/b.cmd" in paths


def test_macro_index_get_references_unknown_command():
    idx = MacroIndex()
    assert idx.get_references("nonexistent command") == []


def test_macro_index_get_references_case_insensitive():
    idx = MacroIndex()
    ref = MacroReference(command_key="cdm wear", line=0, column=0, end_column=8)
    idx.update_file("/f.cmd", [ref])
    assert len(idx.get_references("CDM WEAR")) == 1
    assert len(idx.get_references("Cdm Wear")) == 1


# ---------------------------------------------------------------------------
# MacroIndex — remove_file
# ---------------------------------------------------------------------------

def test_macro_index_remove_file():
    idx = MacroIndex()
    ref = MacroReference(command_key="cdm wear", line=0, column=0, end_column=8)
    idx.update_file("/a.cmd", [ref])
    idx.remove_file("/a.cmd")
    assert idx.get_file_refs("/a.cmd") == []
    assert idx.get_references("cdm wear") == []


def test_macro_index_remove_file_cleans_reverse_index():
    idx = MacroIndex()
    r1 = MacroReference(command_key="cdm wear", line=0, column=0, end_column=8)
    r2 = MacroReference(command_key="cdm wear", line=1, column=0, end_column=8)
    idx.update_file("/a.cmd", [r1])
    idx.update_file("/b.cmd", [r2])
    idx.remove_file("/a.cmd")
    results = idx.get_references("cdm wear")
    assert len(results) == 1
    assert results[0][0] == "/b.cmd"


def test_macro_index_remove_file_that_was_last_reference_removes_command_entry():
    idx = MacroIndex()
    ref = MacroReference(command_key="cdm wear", line=0, column=0, end_column=8)
    idx.update_file("/a.cmd", [ref])
    idx.remove_file("/a.cmd")
    # The command key should no longer appear in the reverse index
    assert "cdm wear" not in idx._files_by_command


# ---------------------------------------------------------------------------
# MacroIndex — counters
# ---------------------------------------------------------------------------

def test_macro_index_total_references():
    idx = MacroIndex()
    refs = [
        MacroReference(command_key="cdm wear", line=i, column=0, end_column=8)
        for i in range(3)
    ]
    idx.update_file("/a.cmd", refs)
    assert idx.total_references() == 3


def test_macro_index_command_count():
    idx = MacroIndex()
    idx.update_file("/a.cmd", [MacroReference("cmd one", 0, 0, 7)])
    idx.update_file("/b.cmd", [MacroReference("cmd two", 0, 0, 7)])
    idx.update_file("/c.cmd", [MacroReference("cmd one", 1, 0, 7)])
    assert idx.command_count() == 2


# ---------------------------------------------------------------------------
# MacroIndex — mtime tracking
# ---------------------------------------------------------------------------

def test_macro_index_needs_refresh_for_unknown_path():
    idx = MacroIndex()
    assert idx.needs_refresh("/no/such/file.cmd") is True


def test_macro_index_needs_refresh_after_record_mtime(tmp_path):
    idx = MacroIndex()
    f = tmp_path / "test.cmd"
    f.write_text("model create model_name=m\n")
    path = str(f)
    assert idx.needs_refresh(path) is True
    idx.record_mtime(path)
    assert idx.needs_refresh(path) is False


# ---------------------------------------------------------------------------
# index_file_text — pure function
# ---------------------------------------------------------------------------

def test_index_file_text_skips_builtin_commands():
    text = "model create model_name=my_model\n"
    refs = index_file_text(text, _SCHEMA)
    # "model create" is a built-in — should NOT appear in the index
    cmds = [r.command_key for r in refs]
    assert "model create" not in cmds


def test_index_file_text_captures_unresolved_command():
    text = "cdm wear part_name=my_part\n"
    refs = index_file_text(text, _SCHEMA)
    assert len(refs) == 1
    assert refs[0].command_key == "cdm wear"
    assert refs[0].line == 0


def test_index_file_text_skips_comments():
    text = "! this is a comment\n"
    refs = index_file_text(text, _SCHEMA)
    assert refs == []


def test_index_file_text_skips_blank_lines():
    text = "\n   \n\t\n"
    refs = index_file_text(text, _SCHEMA)
    assert refs == []


def test_index_file_text_skips_control_flow():
    text = "if (condition == 1)\nend\n"
    refs = index_file_text(text, _SCHEMA)
    # control-flow tokens should NOT be indexed
    cmds = [r.command_key for r in refs]
    assert "if" not in cmds
    assert "end" not in cmds


def test_index_file_text_multiple_unresolved():
    text = "cdm wear part_name=p1\nmy custom macro arg=val\n"
    refs = index_file_text(text, _SCHEMA)
    assert len(refs) == 2
    keys = {r.command_key for r in refs}
    assert "cdm wear" in keys
    assert "my custom macro" in keys


def test_index_file_text_mixed_builtin_and_macro():
    text = (
        "model create model_name=m1\n"
        "cdm wear part_name=p1\n"
        "part create rigid_body name_and_position part_name=p1\n"
    )
    refs = index_file_text(text, _SCHEMA)
    # Only the unresolved "cdm wear" should appear
    assert len(refs) == 1
    assert refs[0].command_key == "cdm wear"


def test_index_file_text_command_position():
    text = "cdm wear part_name=p1\n"
    refs = index_file_text(text, _SCHEMA)
    assert refs[0].line == 0
    assert refs[0].column == 0
    assert refs[0].end_column == len("cdm wear")


def test_index_file_text_continuation_line_position():
    # Continuation lines are joined — the line_start should be the first line
    text = "cdm wear &\n    part_name=p1\n"
    refs = index_file_text(text, _SCHEMA)
    assert len(refs) == 1
    assert refs[0].line == 0   # first physical line of the statement

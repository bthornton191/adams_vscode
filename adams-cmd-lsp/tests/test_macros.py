"""Tests for adams_cmd_lsp.macros — macro parser, registry, and scanner."""

from adams_cmd_lsp.schema import Schema as _Schema
from adams_cmd_lsp.parser import parse as _parse_stmts
from adams_cmd_lsp.macros import extract_macros_from_statements
from adams_cmd_lsp.macros import _parse_qualifiers
import os
from pathlib import Path

import pytest

from adams_cmd_lsp.macros import (
    MacroDefinition,
    MacroParameter,
    MacroRegistry,
    DEFAULT_MACRO_PATTERNS,
    parse_macro_file,
    scan_macro_globs,
    scan_macro_files,
    scan_macro_paths,  # legacy alias — still tested for backward compat
    resolve_macro_argument_name,
    _compute_min_prefixes,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _mac(text, source="test.mac"):
    return parse_macro_file(text, source_file=source)


# ---------------------------------------------------------------------------
# parse_macro_file — basic header detection
# ---------------------------------------------------------------------------

def test_no_user_entered_command_returns_none():
    text = "! just a comment\npart create rigid_body\n"
    assert _mac(text) is None


def test_user_entered_command_basic():
    text = "!USER_ENTERED_COMMAND cdm wear\n"
    m = _mac(text)
    assert m is not None
    assert m.command == "cdm wear"


def test_user_entered_command_case_insensitive():
    text = "!user_entered_command CDM Wear\n"
    m = _mac(text)
    assert m is not None
    assert m.command == "cdm wear"


def test_user_entered_command_with_leading_space():
    text = "  !  USER_ENTERED_COMMAND  my tool  \n"
    m = _mac(text)
    assert m is not None
    assert m.command == "my tool"


def test_source_file_stored():
    text = "!USER_ENTERED_COMMAND cdm wear\n"
    m = _mac(text, source="/path/to/wear/main.mac")
    assert m.source_file == "/path/to/wear/main.mac"


def test_command_line_stored():
    text = "! preamble\n!USER_ENTERED_COMMAND cdm wear\n"
    m = _mac(text)
    assert m.line == 1


# ---------------------------------------------------------------------------
# parse_macro_file — parameter parsing
# ---------------------------------------------------------------------------

def test_parameter_with_all_qualifiers():
    text = (
        "!USER_ENTERED_COMMAND cdm wear\n"
        "!$iterations:t=integer:ge=1:d=3\n"
    )
    m = _mac(text)
    p = m.parameters["iterations"]
    assert p.type_str == "integer"
    assert p.constraints["ge"] == "1"
    assert p.default == "3"


def test_parameter_no_qualifiers():
    """!$name with no qualifiers is valid — defaults to string with no default."""
    text = (
        "!USER_ENTERED_COMMAND cdm tool\n"
        "!$name\n"
    )
    m = _mac(text)
    assert "name" in m.parameters
    p = m.parameters["name"]
    assert p.type_str is None
    assert p.default is None


def test_parameter_type_only():
    text = (
        "!USER_ENTERED_COMMAND cdm tool\n"
        "!$model:t=model\n"
    )
    m = _mac(text)
    assert m.parameters["model"].type_str == "model"


def test_parameter_list_type():
    text = (
        "!USER_ENTERED_COMMAND cdm tool\n"
        "!$output:t=list(yes,no):d=yes\n"
    )
    m = _mac(text)
    p = m.parameters["output"]
    assert p.type_str == "list(yes,no)"
    assert p.default == "yes"


def test_parameter_range_qualifiers():
    text = (
        "!USER_ENTERED_COMMAND cdm tool\n"
        "!$NSpokes:T=INTEGER:GE=3:LE=8:D=3\n"
    )
    m = _mac(text)
    p = m.parameters["nspokes"]
    assert p.type_str == "integer"
    assert p.constraints["ge"] == "3"
    assert p.constraints["le"] == "8"
    assert p.default == "3"


def test_parameter_count_qualifier():
    text = (
        "!USER_ENTERED_COMMAND cdm tool\n"
        "!$sim_scripts:t=simulation_script:c=0\n"
    )
    m = _mac(text)
    p = m.parameters["sim_scripts"]
    assert p.count == "0"


def test_parameter_updated_default():
    text = (
        "!USER_ENTERED_COMMAND cdm tool\n"
        "!$size:t=real:ud=1.0\n"
    )
    m = _mac(text)
    p = m.parameters["size"]
    assert p.updated_default == "1.0"


def test_multiple_parameters():
    text = (
        "!USER_ENTERED_COMMAND cdm wear\n"
        "!$model:t=model\n"
        "!$iterations:t=integer:ge=1:d=1\n"
        "!$scale_factor:t=real:d=1\n"
    )
    m = _mac(text)
    assert set(m.parameters.keys()) == {"model", "iterations", "scale_factor"}


def test_parameter_case_insensitive_name():
    """Parameter names are case-insensitive — stored lower-cased."""
    text = (
        "!USER_ENTERED_COMMAND cdm tool\n"
        "!$MyParam:t=real\n"
    )
    m = _mac(text)
    assert "myparam" in m.parameters


# ---------------------------------------------------------------------------
# parse_macro_file — single-quote syntax
# ---------------------------------------------------------------------------

def test_parameter_quoted_name_no_qualifiers():
    text = (
        "!USER_ENTERED_COMMAND cdm tool\n"
        "!$'part'\n"
    )
    m = _mac(text)
    assert "part" in m.parameters


def test_parameter_quoted_name_with_qualifiers():
    text = (
        "!USER_ENTERED_COMMAND cdm tool\n"
        "!$'size:t=real:d=1.0'\n"
    )
    m = _mac(text)
    p = m.parameters["size"]
    assert p.type_str == "real"
    assert p.default == "1.0"


def test_inline_quoted_param_adjacent_text():
    """$'part'_1 should define param 'part', not 'part_1'."""
    text = (
        "!USER_ENTERED_COMMAND cdm tool\n"
        "marker create marker_name=$'part'_1\n"
    )
    m = _mac(text)
    assert "part" in m.parameters
    assert "part_1" not in m.parameters


# ---------------------------------------------------------------------------
# parse_macro_file — END_OF_PARAMETERS behaviour
# ---------------------------------------------------------------------------

def test_end_of_parameters_stops_scanning():
    """Parameters defined AFTER !END_OF_PARAMETERS are NOT collected."""
    text = (
        "!USER_ENTERED_COMMAND cdm tool\n"
        "!$before:t=real\n"
        "!END_OF_PARAMETERS\n"
        "!$after:t=real\n"
    )
    m = _mac(text)
    assert "before" in m.parameters
    assert "after" not in m.parameters


def test_no_end_of_parameters_scans_entire_file():
    """Without !END_OF_PARAMETERS the whole file is scanned."""
    text = (
        "!USER_ENTERED_COMMAND cdm tool\n"
        "part create rigid_body part_name=$mypart\n"
        "marker create marker_name=$mymarker\n"
    )
    m = _mac(text)
    assert "mypart" in m.parameters
    assert "mymarker" in m.parameters


def test_first_occurrence_wins():
    """First occurrence of $name defines it; later occurrences add nothing."""
    text = (
        "!USER_ENTERED_COMMAND cdm tool\n"
        "!$x:t=real:d=0\n"
        "!$x:t=integer:d=99\n"   # second definition — should be ignored
    )
    m = _mac(text)
    p = m.parameters["x"]
    assert p.type_str == "real"
    assert p.default == "0"


def test_self_not_collected():
    """$_self is the macro's own database path, not a user parameter."""
    text = (
        "!USER_ENTERED_COMMAND cdm tool\n"
        "var set var=$_self.tmp int=1\n"
    )
    m = _mac(text)
    assert "_self" not in m.parameters


# ---------------------------------------------------------------------------
# MacroRegistry
# ---------------------------------------------------------------------------

def test_registry_register_and_lookup():
    reg = MacroRegistry()
    macro = MacroDefinition(command="cdm wear", parameters={})
    reg.register(macro)
    assert reg.has_command("cdm wear")
    assert reg.lookup_command("cdm wear") is macro


def test_registry_lookup_case_insensitive():
    reg = MacroRegistry()
    reg.register(MacroDefinition(command="cdm wear", parameters={}))
    assert reg.has_command("CDM WEAR")
    assert reg.lookup_command("CDM Wear") is not None


def test_registry_lookup_missing_returns_none():
    reg = MacroRegistry()
    assert reg.lookup_command("unknown cmd") is None
    assert not reg.has_command("unknown cmd")


def test_registry_later_registration_wins():
    reg = MacroRegistry()
    m1 = MacroDefinition(command="cdm tool", parameters={}, source_file="first.mac")
    m2 = MacroDefinition(command="cdm tool", parameters={}, source_file="second.mac")
    reg.register(m1)
    reg.register(m2)
    assert reg.lookup_command("cdm tool").source_file == "second.mac"


def test_registry_multi_word_command():
    reg = MacroRegistry()
    reg.register(MacroDefinition(command="cdm rotating_assembly main", parameters={}))
    assert reg.has_command("cdm rotating_assembly main")
    assert not reg.has_command("cdm rotating_assembly")


def test_registry_get_parameters():
    params = {"x": MacroParameter(name="x", type_str="real")}
    reg = MacroRegistry()
    reg.register(MacroDefinition(command="cdm tool", parameters=params))
    assert reg.get_parameters("cdm tool") == params
    assert reg.get_parameters("other") is None


def test_registry_len():
    reg = MacroRegistry()
    reg.register(MacroDefinition(command="cdm a", parameters={}))
    reg.register(MacroDefinition(command="cdm b", parameters={}))
    assert len(reg) == 2


# ---------------------------------------------------------------------------
# scan_directory / scan_macro_paths
# ---------------------------------------------------------------------------

def test_registry_items():
    """items() exposes (command_key, MacroDefinition) pairs."""
    reg = MacroRegistry()
    m1 = MacroDefinition(command="cdm a", parameters={})
    m2 = MacroDefinition(command="cdm b", parameters={})
    reg.register(m1)
    reg.register(m2)
    found = dict(reg.items())
    assert "cdm a" in found
    assert "cdm b" in found
    assert found["cdm a"] is m1


def test_registry_needs_refresh_new_file(tmp_path):
    """A path not yet in the cache always needs refresh."""
    reg = MacroRegistry()
    p = tmp_path / "never_seen.mac"
    p.write_text("", encoding="utf-8")
    assert reg.needs_refresh(str(p)) is True


def test_registry_needs_refresh_after_record(tmp_path):
    """After recording mtime, needs_refresh returns False for unchanged file."""
    reg = MacroRegistry()
    p = tmp_path / "tool.mac"
    p.write_text("!USER_ENTERED_COMMAND cdm tool\n", encoding="utf-8")
    reg._record_mtime(str(p))
    assert reg.needs_refresh(str(p)) is False


def test_registry_needs_refresh_after_modification(tmp_path):
    """After file modification, needs_refresh returns True."""
    import time
    reg = MacroRegistry()
    p = tmp_path / "tool.mac"
    p.write_text("!USER_ENTERED_COMMAND cdm tool\n", encoding="utf-8")
    reg._record_mtime(str(p))
    # Bump mtime
    time.sleep(0.05)
    p.write_text("!USER_ENTERED_COMMAND cdm tool\nchanged\n", encoding="utf-8")
    assert reg.needs_refresh(str(p)) is True


# ---------------------------------------------------------------------------
# scan_macro_globs
# ---------------------------------------------------------------------------

def test_scan_macro_globs_finds_mac_files(tmp_path):
    """Default pattern finds .mac files recursively."""
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "tool.mac").write_text("!USER_ENTERED_COMMAND cdm tool\n", encoding="utf-8")
    (tmp_path / "root.mac").write_text("!USER_ENTERED_COMMAND cdm root\n", encoding="utf-8")

    found = scan_macro_globs(str(tmp_path))
    names = {p.name for p in found}
    assert "tool.mac" in names
    assert "root.mac" in names


def test_scan_macro_globs_non_recursive_pattern(tmp_path):
    """A non-recursive pattern like 'macros/*' should not recurse."""
    macros = tmp_path / "macros"
    macros.mkdir()
    deep = macros / "sub"
    deep.mkdir()
    (macros / "top.mac").write_text("!USER_ENTERED_COMMAND top\n", encoding="utf-8")
    (deep / "nested.mac").write_text("!USER_ENTERED_COMMAND nested\n", encoding="utf-8")

    found = scan_macro_globs(str(tmp_path), patterns=["macros/*.mac"])
    names = {p.name for p in found}
    assert "top.mac" in names
    assert "nested.mac" not in names


def test_scan_macro_globs_custom_extension(tmp_path):
    """Custom glob pattern can target any extension."""
    (tmp_path / "tool.cmd").write_text("!USER_ENTERED_COMMAND my tool\n", encoding="utf-8")
    (tmp_path / "other.mac").write_text("!USER_ENTERED_COMMAND cdm wear\n", encoding="utf-8")

    found = scan_macro_globs(str(tmp_path), patterns=["**/*.cmd"])
    names = {p.name for p in found}
    assert "tool.cmd" in names
    assert "other.mac" not in names


def test_scan_macro_globs_skips_default_ignored_dirs(tmp_path):
    """Files inside .git, node_modules, etc. are automatically excluded."""
    for ignore_dir in [".git", "node_modules", "__pycache__", "build"]:
        d = tmp_path / ignore_dir
        d.mkdir()
        (d / "tool.mac").write_text("!USER_ENTERED_COMMAND auto\n", encoding="utf-8")
    (tmp_path / "real.mac").write_text("!USER_ENTERED_COMMAND real\n", encoding="utf-8")

    found = scan_macro_globs(str(tmp_path))
    names = {p.name for p in found}
    assert "real.mac" in names
    assert "tool.mac" not in names


def test_scan_macro_globs_user_ignore_patterns(tmp_path):
    """User-supplied ignore patterns are applied on top of default ignores."""
    gen = tmp_path / "generated"
    gen.mkdir()
    (gen / "auto.mac").write_text("!USER_ENTERED_COMMAND auto cmd\n", encoding="utf-8")
    (tmp_path / "manual.mac").write_text("!USER_ENTERED_COMMAND manual cmd\n", encoding="utf-8")

    found = scan_macro_globs(str(tmp_path), ignore_patterns=["generated/**"])
    names = {p.name for p in found}
    assert "manual.mac" in names
    assert "auto.mac" not in names


def test_scan_macro_globs_nonexistent_root():
    """Nonexistent root returns empty list without error."""
    assert scan_macro_globs("/nonexistent/path/xyz") == []


def test_scan_macro_globs_deduplicates(tmp_path):
    """A file matched by multiple patterns appears only once."""
    (tmp_path / "tool.mac").write_text("!USER_ENTERED_COMMAND cdm tool\n", encoding="utf-8")

    found = scan_macro_globs(str(tmp_path), patterns=["**/*.mac", "*.mac"])
    assert len(found) == 1


# ---------------------------------------------------------------------------
# scan_macro_files
# ---------------------------------------------------------------------------

def test_scan_macro_files_finds_mac_files(tmp_path):
    """scan_macro_files populates registry from .mac files."""
    (tmp_path / "wear.mac").write_text(
        "!USER_ENTERED_COMMAND cdm wear\n!$model:t=model\n", encoding="utf-8"
    )

    reg = scan_macro_files([str(tmp_path)])
    assert reg.has_command("cdm wear")


def test_scan_macro_files_ignores_files_without_command(tmp_path):
    """Files without !USER_ENTERED_COMMAND don't add to registry."""
    (tmp_path / "plain.mac").write_text(
        "! no command here\n", encoding="utf-8"
    )

    reg = scan_macro_files([str(tmp_path)])
    assert len(reg) == 0


def test_scan_macro_files_incremental_skips_unchanged(tmp_path):
    """Incremental scan skips files whose mtime hasn't changed."""
    mac = tmp_path / "tool.mac"
    mac.write_text("!USER_ENTERED_COMMAND cdm tool\n", encoding="utf-8")

    reg = scan_macro_files([str(tmp_path)])
    assert reg.has_command("cdm tool")

    # Overwrite content without changing mtime (simulate by recording mtime)
    # Second scan should skip the file since mtime is recorded
    read_count = [0]
    original_read = Path.read_text

    def counting_read(self, *args, **kwargs):
        read_count[0] += 1
        return original_read(self, *args, **kwargs)

    import unittest.mock as mock
    with mock.patch.object(Path, "read_text", counting_read):
        scan_macro_files([str(tmp_path)], registry=reg)

    assert read_count[0] == 0  # File not re-read because mtime unchanged


def test_scan_macro_files_nonexistent_root():
    """Nonexistent root is silently skipped."""
    reg = scan_macro_files(["/no/such/path"])
    assert len(reg) == 0


# ---------------------------------------------------------------------------
# scan_macro_paths (legacy alias)
# ---------------------------------------------------------------------------

def test_scan_directory_finds_mac_files(tmp_path):
    """Legacy: scan_macro_paths finds .mac files recursively."""
    (tmp_path / "wear.mac").write_text(
        "!USER_ENTERED_COMMAND cdm wear\n!$model:t=model\n", encoding="utf-8"
    )

    reg = scan_macro_paths([str(tmp_path)])
    assert reg.has_command("cdm wear")


def test_scan_directory_ignores_files_without_command(tmp_path):
    (tmp_path / "plain.mac").write_text("! no USER_ENTERED_COMMAND here\n", encoding="utf-8")
    reg = scan_macro_paths([str(tmp_path)])
    assert len(reg) == 0


def test_scan_directory_custom_extensions(tmp_path):
    """Legacy: extensions arg is accepted but ignored; use glob patterns."""
    (tmp_path / "tool.cmd").write_text("!USER_ENTERED_COMMAND my tool\n", encoding="utf-8")
    (tmp_path / "wear.mac").write_text("!USER_ENTERED_COMMAND cdm wear\n", encoding="utf-8")

    # With default patterns (*.mac) only wear.mac should be found
    reg = scan_macro_paths([str(tmp_path)])
    assert reg.has_command("cdm wear")
    # extensions kwarg is accepted (compat) but has no effect in new scanner
    reg2 = scan_macro_paths([str(tmp_path)], extensions=[".cmd"])
    assert isinstance(reg2, MacroRegistry)


def test_scan_directory_ignore_patterns(tmp_path):
    sub = tmp_path / "generated"
    sub.mkdir()
    (sub / "auto.mac").write_text("!USER_ENTERED_COMMAND auto cmd\n", encoding="utf-8")
    (tmp_path / "manual.mac").write_text("!USER_ENTERED_COMMAND manual cmd\n", encoding="utf-8")

    reg = scan_macro_paths([str(tmp_path)], ignore_patterns=["generated/**"])
    assert reg.has_command("manual cmd")
    assert not reg.has_command("auto cmd")


def test_scan_directory_recursive(tmp_path):
    sub = tmp_path / "sub" / "deep"
    sub.mkdir(parents=True)
    (sub / "deep.mac").write_text("!USER_ENTERED_COMMAND deep cmd\n", encoding="utf-8")

    reg = scan_macro_paths([str(tmp_path)])
    assert reg.has_command("deep cmd")


def test_scan_macro_paths_skips_nonexistent():
    reg = scan_macro_paths(["/nonexistent/path/xyz"])
    assert len(reg) == 0


def test_scan_macro_paths_populates_registry(tmp_path):
    (tmp_path / "a.mac").write_text("!USER_ENTERED_COMMAND cdm a\n", encoding="utf-8")
    (tmp_path / "b.mac").write_text("!USER_ENTERED_COMMAND cdm b\n", encoding="utf-8")

    reg = scan_macro_paths([str(tmp_path)])
    assert reg.has_command("cdm a")
    assert reg.has_command("cdm b")


# ---------------------------------------------------------------------------
# _parse_qualifiers — isolated unit tests
# ---------------------------------------------------------------------------


def test_parse_qualifiers_empty_string():
    """Empty qualifier string returns a MacroParameter with all defaults."""
    p = _parse_qualifiers("")
    assert p.type_str is None
    assert p.default is None
    assert p.constraints == {}
    assert p.count is None


def test_parse_qualifiers_unknown_key_ignored():
    """Unknown qualifier keys are silently ignored — no error."""
    p = _parse_qualifiers(":t=real:x=unknown_key:d=1.0")
    assert p.type_str == "real"
    assert p.default == "1.0"


def test_parse_qualifiers_missing_equals_ignored():
    """A qualifier segment without '=' is silently skipped."""
    p = _parse_qualifiers(":justtext:t=integer")
    assert p.type_str == "integer"


def test_parse_qualifiers_duplicate_key_last_wins():
    """When the same qualifier key appears twice, the last value wins."""
    p = _parse_qualifiers(":d=1:d=2")
    assert p.default == "2"


# ---------------------------------------------------------------------------
# extract_macros_from_statements — unit tests
# ---------------------------------------------------------------------------


_SCHEMA = _Schema.load()


def test_extract_macro_create_with_user_entered_command():
    """macro create with user_entered_command extracts that as the callable command."""
    stmts = _parse_stmts('macro create macro_name=foo user_entered_command="cdm tool"\n')
    macros = extract_macros_from_statements(stmts, _SCHEMA)
    assert len(macros) == 1
    assert macros[0].command == "cdm tool"


def test_extract_macro_read_with_user_entered_command():
    """macro read with user_entered_command extracts that as the callable command."""
    stmts = _parse_stmts(
        'macro read file_name="foo.mac" macro_name=bar user_entered_command="my cmd"\n'
    )
    macros = extract_macros_from_statements(stmts, _SCHEMA)
    assert len(macros) == 1
    assert macros[0].command == "my cmd"


def test_extract_fallback_to_macro_name():
    """When user_entered_command is absent, macro_name becomes the command."""
    stmts = _parse_stmts("macro create macro_name=mytool\n")
    macros = extract_macros_from_statements(stmts, _SCHEMA)
    assert len(macros) == 1
    assert macros[0].command == "mytool"


def test_extract_empty_macro_name_skipped():
    """If neither user_entered_command nor macro_name is present, the stmt is skipped."""
    stmts = _parse_stmts("macro create\n")
    macros = extract_macros_from_statements(stmts, _SCHEMA)
    assert len(macros) == 0


def test_extract_schema_none():
    """schema=None branch must not raise and must still fall back to macro_name."""
    stmts = _parse_stmts("macro create macro_name=notool\n")
    macros = extract_macros_from_statements(stmts, schema=None)
    assert len(macros) == 1
    assert macros[0].command == "notool"


def test_extract_multiple_macros():
    """Multiple macro create/read statements each produce one MacroDefinition."""
    text = (
        'macro create macro_name=a user_entered_command="cmd a"\n'
        'macro create macro_name=b user_entered_command="cmd b"\n'
        'macro read   macro_name=c user_entered_command="cmd c"\n'
    )
    stmts = _parse_stmts(text)
    macros = extract_macros_from_statements(stmts, _SCHEMA)
    commands = [m.command for m in macros]
    assert "cmd a" in commands
    assert "cmd b" in commands
    assert "cmd c" in commands


def test_extract_skips_comments_blanks_and_control_flow():
    """Comments, blank lines, and control-flow statements are skipped."""
    text = (
        "! this is a comment\n"
        "\n"
        "if condition=(1)\n"
        'macro create macro_name=real_one user_entered_command="real cmd"\n'
        "end\n"
    )
    stmts = _parse_stmts(text)
    macros = extract_macros_from_statements(stmts, _SCHEMA)
    assert len(macros) == 1
    assert macros[0].command == "real cmd"


# ---------------------------------------------------------------------------
# scan_macro_files — incremental re-parse on modified file
# ---------------------------------------------------------------------------

def test_scan_macro_files_incremental_reparses_modified(tmp_path):
    """A file whose mtime changes should be re-parsed in the second scan."""
    import time
    mac = tmp_path / "tool.mac"
    mac.write_text("!USER_ENTERED_COMMAND cdm tool\n", encoding="utf-8")

    reg = scan_macro_files([str(tmp_path)])
    assert reg.has_command("cdm tool")

    # Wait a tiny bit and rewrite the file with a different command
    time.sleep(0.05)
    mac.write_text("!USER_ENTERED_COMMAND cdm wear\n", encoding="utf-8")

    # Incremental scan should detect the changed mtime and re-parse
    reg2 = scan_macro_files([str(tmp_path)], registry=reg)
    assert reg2.has_command("cdm wear")


# ---------------------------------------------------------------------------
# scan_macro_globs — multiple patterns
# ---------------------------------------------------------------------------

def test_scan_macro_globs_multiple_patterns(tmp_path):
    """Two patterns in one call find both matching file types."""
    special = tmp_path / "special"
    special.mkdir()
    (tmp_path / "a.mac").write_text("!USER_ENTERED_COMMAND cdm a\n", encoding="utf-8")
    (special / "b.cmd").write_text("!USER_ENTERED_COMMAND cdm b\n", encoding="utf-8")

    found = scan_macro_globs(str(tmp_path), patterns=["**/*.mac", "special/*.cmd"])
    names = {p.name for p in found}
    assert "a.mac" in names
    assert "b.cmd" in names


# ---------------------------------------------------------------------------
# MacroRegistry — needs_refresh for deleted file
# ---------------------------------------------------------------------------

def test_registry_needs_refresh_deleted_file(tmp_path):
    """After recording mtime for a file that is then deleted, needs_refresh returns True."""
    reg = MacroRegistry()
    p = tmp_path / "gone.mac"
    p.write_text("!USER_ENTERED_COMMAND cdm gone\n", encoding="utf-8")
    reg._record_mtime(str(p))
    assert reg.needs_refresh(str(p)) is False

    # Now delete the file
    p.unlink()
    assert reg.needs_refresh(str(p)) is True


# ---------------------------------------------------------------------------
# scan_macro_files — multiple root directories (G8)
# ---------------------------------------------------------------------------

def test_scan_macro_files_multi_root(tmp_path):
    """scan_macro_files with two root directories should populate macros from both."""
    root1 = tmp_path / "workspace1"
    root2 = tmp_path / "workspace2"
    root1.mkdir()
    root2.mkdir()

    (root1 / "tool_a.mac").write_text(
        "!USER_ENTERED_COMMAND cdm tool_a\n", encoding="utf-8"
    )
    (root2 / "tool_b.mac").write_text(
        "!USER_ENTERED_COMMAND cdm tool_b\n", encoding="utf-8"
    )

    reg = scan_macro_files([str(root1), str(root2)])
    assert reg.has_command("cdm tool_a"), "Macro from first root should be registered"
    assert reg.has_command("cdm tool_b"), "Macro from second root should be registered"


# ---------------------------------------------------------------------------
# _compute_min_prefixes
# ---------------------------------------------------------------------------

def test_compute_min_prefixes_single_name():
    """A single name has min_prefix of 1."""
    assert _compute_min_prefixes(["model_name"]) == {"model_name": 1}


def test_compute_min_prefixes_disjoint_names():
    """Names with different first letters each get min_prefix of 1."""
    result = _compute_min_prefixes(["alpha", "beta", "gamma"])
    assert result == {"alpha": 1, "beta": 1, "gamma": 1}


def test_compute_min_prefixes_shared_prefix():
    """Names sharing a common prefix require enough chars to be unambiguous."""
    result = _compute_min_prefixes(["model", "mass"])
    # 'm' is ambiguous; 'mo' uniquely identifies 'model'; 'ma' uniquely identifies 'mass'
    assert result["model"] == 2
    assert result["mass"] == 2


def test_compute_min_prefixes_one_is_prefix_of_another():
    """When one name is a prefix of another, the shorter gets its full length as min_prefix."""
    result = _compute_min_prefixes(["model", "model_name"])
    # "model" shares every prefix with "model_name" up to the full word,
    # so it falls through to the else clause: min_prefix = len("model") = 5.
    # "model_name" diverges at position 6 ("model_" is unique), so min_prefix = 6.
    assert result["model"] == 5
    assert result["model_name"] == 6


def test_compute_min_prefixes_case_insensitive():
    """Prefix computation is case-insensitive."""
    result = _compute_min_prefixes(["Model", "Mass"])
    # 'Mo' vs 'Ma' — still 2 each
    assert result["Model"] == 2
    assert result["Mass"] == 2


# ---------------------------------------------------------------------------
# resolve_macro_argument_name
# ---------------------------------------------------------------------------

def _make_macro_def(command, param_names):
    """Build a MacroDefinition with simple parameters keyed by lower-case name."""
    params = {n.lower(): MacroParameter(name=n.lower()) for n in param_names}
    return MacroDefinition(command=command, parameters=params)


def test_resolve_exact_match():
    """Exact argument name (case-insensitive) resolves correctly."""
    macro = _make_macro_def("cdm tool", ["model_name", "iterations"])
    assert resolve_macro_argument_name(macro, "model_name") == "model_name"
    assert resolve_macro_argument_name(macro, "MODEL_NAME") == "model_name"
    assert resolve_macro_argument_name(macro, "Iterations") == "iterations"


def test_resolve_exact_wins_over_prefix():
    """When a param named 'mod' exists alongside 'model', 'mod' resolves exactly."""
    macro = _make_macro_def("cdm tool", ["mod", "model"])
    assert resolve_macro_argument_name(macro, "mod") == "mod"


def test_resolve_unambiguous_prefix():
    """An unambiguous prefix resolves to the matching parameter."""
    macro = _make_macro_def("cdm tool", ["model_name", "iterations"])
    assert resolve_macro_argument_name(macro, "mod") == "model_name"
    assert resolve_macro_argument_name(macro, "iter") == "iterations"


def test_resolve_ambiguous_prefix_returns_none():
    """An ambiguous prefix returns None."""
    macro = _make_macro_def("cdm tool", ["model", "mode"])
    assert resolve_macro_argument_name(macro, "mod") is None
    assert resolve_macro_argument_name(macro, "mo") is None


def test_resolve_too_short_prefix_returns_none():
    """A prefix shorter than min_prefix returns None."""
    macro = _make_macro_def("cdm tool", ["model_name", "mass"])
    # 'm' is below min_prefix for both
    assert resolve_macro_argument_name(macro, "m") is None


def test_resolve_unknown_name_returns_none():
    """A completely unknown argument name returns None."""
    macro = _make_macro_def("cdm tool", ["model_name"])
    assert resolve_macro_argument_name(macro, "typo") is None


def test_resolve_empty_params_returns_none():
    """A macro with no declared parameters always returns None."""
    macro = _make_macro_def("cdm tool", [])
    assert resolve_macro_argument_name(macro, "anything") is None


def test_resolve_single_param_any_prefix():
    """With only one parameter, any non-empty prefix resolves."""
    macro = _make_macro_def("cdm tool", ["model_name"])
    assert resolve_macro_argument_name(macro, "m") == "model_name"
    assert resolve_macro_argument_name(macro, "mod") == "model_name"
    assert resolve_macro_argument_name(macro, "model_name") == "model_name"


def test_resolve_case_insensitive_prefix():
    """Prefix matching is case-insensitive."""
    macro = _make_macro_def("cdm tool", ["model_name", "iterations"])
    assert resolve_macro_argument_name(macro, "MOD") == "model_name"
    assert resolve_macro_argument_name(macro, "ITER") == "iterations"

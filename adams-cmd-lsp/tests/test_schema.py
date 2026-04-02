"""Tests for adams_cmd_lsp.schema module."""

from adams_cmd_lsp.schema import Schema
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def _make_schema(commands=None, command_tree=None):
    """Build a minimal Schema for testing."""
    return Schema({
        "commands": commands or {},
        "command_tree": command_tree or {"children": {}},
    })


# ---------------------------------------------------------------------------
# Schema loading
# ---------------------------------------------------------------------------

def test_schema_load_default():
    """Default schema loads without error and has commands."""
    schema = Schema.load()
    assert schema.has_command("model create")
    assert schema.has_command("marker create")


def test_schema_has_command_false():
    schema = Schema.load()
    assert not schema.has_command("not a real command xyz")


# ---------------------------------------------------------------------------
# Command lookups
# ---------------------------------------------------------------------------

def test_get_command_returns_dict():
    schema = Schema.load()
    cmd = schema.get_command("model create")
    assert isinstance(cmd, dict)
    assert "args" in cmd


def test_get_args_returns_dict():
    schema = Schema.load()
    args = schema.get_args("model create")
    assert isinstance(args, dict)
    assert "model_name" in args


def test_get_arg_required():
    schema = Schema.load()
    arg = schema.get_arg("model create", "model_name")
    assert arg is not None
    assert arg.get("required") is True


def test_get_arg_unknown_returns_none():
    schema = Schema.load()
    assert schema.get_arg("model create", "nonexistent_arg") is None


def test_get_exclusive_groups():
    schema = Schema.load()
    groups = schema.get_exclusive_groups("marker create")
    assert isinstance(groups, list)
    # marker create has at least 2 exclusive groups (orientation group etc.)
    assert len(groups) >= 2


def test_get_exclusive_groups_empty():
    schema = Schema.load()
    # model create has no exclusive groups
    groups = schema.get_exclusive_groups("model create")
    assert groups == []


# ---------------------------------------------------------------------------
# resolve_command_key — exact match
# ---------------------------------------------------------------------------

def test_resolve_exact_match():
    schema = Schema.load()
    key, err = schema.resolve_command_key(["model", "create"])
    assert key == "model create"
    assert err is None


def test_resolve_unknown_command():
    schema = Schema.load()
    key, err = schema.resolve_command_key(["notacommand"])
    assert key is None
    assert err is not None


# ---------------------------------------------------------------------------
# resolve_command_key — abbreviation
# ---------------------------------------------------------------------------

def test_resolve_abbreviated_mar_cre():
    schema = Schema.load()
    key, err = schema.resolve_command_key(["mar", "cre"])
    assert key == "marker create"
    assert err is None


def test_resolve_abbreviated_mod_cre():
    schema = Schema.load()
    key, err = schema.resolve_command_key(["mod", "cre"])
    assert key == "model create"
    assert err is None


def test_resolve_abbreviated_case_insensitive():
    schema = Schema.load()
    key, err = schema.resolve_command_key(["MAR", "CRE"])
    assert key == "marker create"
    assert err is None


def test_resolve_ambiguous_prefix():
    """A prefix that matches multiple siblings should fail."""
    schema = Schema.load()
    # "m" alone should be ambiguous (model, marker, mass, material, ...)
    key, err = schema.resolve_command_key(["m"])
    assert key is None


def test_resolve_too_short_prefix():
    """Prefix shorter than min_prefix should fail."""
    # Build a minimal schema where min_prefix is 3 for "model" and "marker"
    tree = {
        "children": {
            "model": {"min_prefix": 3, "children": {
                "create": {"min_prefix": 1, "is_leaf": True, "children": {}},
            }},
            "marker": {"min_prefix": 3, "children": {
                "create": {"min_prefix": 1, "is_leaf": True, "children": {}},
            }},
        }
    }
    commands = {
        "model create": {"args": {}, "exclusive_groups": []},
        "marker create": {"args": {}, "exclusive_groups": []},
    }
    schema = _make_schema(commands, tree)
    # "mo" has 2 chars < min_prefix of 3 → should fail to resolve
    key, err = schema.resolve_command_key(["mo", "cre"])
    assert key is None, f"Expected None but got {key!r}"
    assert err == 0  # first token is the problem
    # "mod" (3 chars == min_prefix=3) correctly resolves "model"
    key2, err2 = schema.resolve_command_key(["mod", "cre"])
    assert key2 == "model create"
    assert err2 is None
    # With real schema: "mod cre" should also resolve
    real = Schema.load()
    key3, err3 = real.resolve_command_key(["mod", "cre"])
    assert key3 == "model create"


# ---------------------------------------------------------------------------
# resolve_argument_name — exact and abbreviated
# ---------------------------------------------------------------------------

def test_resolve_arg_exact():
    schema = Schema.load()
    result = schema.resolve_argument_name("model create", "model_name")
    assert result == "model_name"


def test_resolve_arg_abbreviated():
    schema = Schema.load()
    # "model_n" should resolve to "model_name" (unique prefix)
    result = schema.resolve_argument_name("model create", "model_n")
    assert result == "model_name"


def test_resolve_arg_case_insensitive():
    schema = Schema.load()
    result = schema.resolve_argument_name("model create", "MODEL_NAME")
    assert result == "model_name"


def test_resolve_arg_unknown():
    schema = Schema.load()
    result = schema.resolve_argument_name("model create", "not_a_real_arg")
    assert result is None


def test_resolve_arg_wrong_command():
    schema = Schema.load()
    # part_name is not an argument for model create
    result = schema.resolve_argument_name("model create", "part_name")
    assert result is None


# ---------------------------------------------------------------------------
# command_server — schema entries
# ---------------------------------------------------------------------------

def test_has_command_command_server_show():
    schema = Schema.load()
    assert schema.has_command("command_server show")


def test_has_command_command_server_start():
    schema = Schema.load()
    assert schema.has_command("command_server start")


def test_has_command_command_server_stop():
    schema = Schema.load()
    assert schema.has_command("command_server stop")


def test_resolve_command_server_exact():
    schema = Schema.load()
    key, err = schema.resolve_command_key(["command_server", "start"])
    assert key == "command_server start"
    assert err is None


def test_resolve_command_server_abbreviated():
    schema = Schema.load()
    key, err = schema.resolve_command_key(["com", "sta"])
    assert key == "command_server start"
    assert err is None

    key2, err2 = schema.resolve_command_key(["com", "sto"])
    assert key2 == "command_server stop"
    assert err2 is None

    key3, err3 = schema.resolve_command_key(["com", "sh"])
    assert key3 == "command_server show"
    assert err3 is None

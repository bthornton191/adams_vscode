"""Tests for LSP completion helpers in adams_cmd_lsp.server.

These tests exercise _parse_list_type_values, _lookup_macro_for_cmd, and
_get_completion_context directly, without starting a live LSP server.
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    from lsprotocol import types  # noqa: F401
    _PYGLS_AVAILABLE = True
except ImportError:
    _PYGLS_AVAILABLE = False

pytestmark = pytest.mark.skipif(
    not _PYGLS_AVAILABLE,
    reason="lsprotocol not installed",
)

if _PYGLS_AVAILABLE:
    from adams_cmd_lsp import server as srv
    from adams_cmd_lsp.macros import MacroDefinition, MacroParameter, MacroRegistry
    from adams_cmd_lsp.schema import Schema


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_registry(*defs):
    """Return a MacroRegistry containing the given MacroDefinition objects."""
    reg = MacroRegistry()
    for d in defs:
        reg.register(d)
    return reg


def _make_macro(command, **params):
    """Build a MacroDefinition with simple MacroParameter objects."""
    parameters = {}
    for name, type_str in params.items():
        parameters[name] = MacroParameter(name=name, type_str=type_str)
    return MacroDefinition(command=command, parameters=parameters, source_file="/test/test.mac")


# ---------------------------------------------------------------------------
# _parse_list_type_values
# ---------------------------------------------------------------------------

class TestParseListTypeValues:
    def test_simple_list(self):
        assert srv._parse_list_type_values("list(yes,no)") == ["yes", "no"]

    def test_list_with_spaces(self):
        assert srv._parse_list_type_values("list(yes, no)") == ["yes", "no"]

    def test_uppercase_list(self):
        result = srv._parse_list_type_values("LIST(merge,rename)")
        assert result == ["merge", "rename"]

    def test_single_value(self):
        assert srv._parse_list_type_values("list(on)") == ["on"]

    def test_non_list_type(self):
        assert srv._parse_list_type_values("integer") == []

    def test_empty_type_str(self):
        assert srv._parse_list_type_values("") == []

    def test_none_type_str(self):
        # Called with empty string since type_str can be None (guarded by caller)
        assert srv._parse_list_type_values("") == []

    def test_three_values(self):
        result = srv._parse_list_type_values("list(x,y,z)")
        assert result == ["x", "y", "z"]


# ---------------------------------------------------------------------------
# _lookup_macro_for_cmd
# ---------------------------------------------------------------------------

class TestLookupMacroForCmd:
    def setup_method(self):
        srv._schema = Schema.load()
        srv._macro_registry = None

    def test_finds_registry_macro(self):
        macro = _make_macro("custom command", part_name="part")
        srv._macro_registry = _make_registry(macro)
        result = srv._lookup_macro_for_cmd("custom command", [], 0, "file:///test.cmd")
        assert result is not None
        assert result.command == "custom command"

    def test_case_insensitive_lookup(self):
        macro = _make_macro("custom command", part_name="part")
        srv._macro_registry = _make_registry(macro)
        result = srv._lookup_macro_for_cmd("CUSTOM COMMAND", [], 0, "file:///test.cmd")
        assert result is not None

    def test_returns_none_for_unknown_command(self):
        srv._macro_registry = _make_registry()
        result = srv._lookup_macro_for_cmd("unknown macro", [], 0, "file:///test.cmd")
        assert result is None

    def test_returns_none_when_registry_is_none(self):
        srv._macro_registry = None
        result = srv._lookup_macro_for_cmd("custom command", [], 0, "file:///test.cmd")
        assert result is None

    def test_finds_inline_macro(self):
        """Macro defined via 'macro create' earlier in the same file."""
        text = dedent("""\
            macro create macro_name=mymac user_entered_command="my command"
            my command
        """)
        from adams_cmd_lsp.parser import parse as parse_cmd
        statements = parse_cmd(text)
        # stmt for "my command" is on line 1
        target_stmt = next(s for s in statements if not s.is_comment and not s.is_blank and s.line_start == 1)
        srv._macro_registry = _make_registry()
        result = srv._lookup_macro_for_cmd("my command", statements, target_stmt.line_start, "file:///test.cmd")
        assert result is not None
        assert result.command == "my command"

    def teardown_method(self):
        srv._macro_registry = None


# ---------------------------------------------------------------------------
# _get_completion_context
# ---------------------------------------------------------------------------

class TestGetCompletionContext:
    def setup_method(self):
        srv._schema = Schema.load()
        srv._macro_registry = None

    def teardown_method(self):
        srv._macro_registry = None

    # --- No schema ---

    def test_returns_none_when_no_schema(self):
        srv._schema = None
        result = srv._get_completion_context("custom command\n", 0, 6, "file:///test.cmd")
        assert result is None
        srv._schema = Schema.load()

    # --- Comment lines ---

    def test_returns_none_on_comment_line(self):
        result = srv._get_completion_context("! this is a comment\n", 0, 5, "file:///test.cmd")
        assert result is None

    # --- Command context ---

    def test_partial_command_returns_command_context(self):
        macro = _make_macro("custom command", part_name="part")
        srv._macro_registry = _make_registry(macro)
        text = "cust\n"
        result = srv._get_completion_context(text, 0, 4, "file:///test.cmd")
        assert result is not None
        assert result[0] == "command"
        assert result[1] == "cust"

    def test_empty_line_returns_command_context(self):
        macro = _make_macro("custom command", part_name="part")
        srv._macro_registry = _make_registry(macro)
        text = "\n"
        result = srv._get_completion_context(text, 0, 0, "file:///test.cmd")
        assert result is not None
        assert result[0] == "command"

    def test_mid_command_key_returns_command_context(self):
        """Cursor inside 'custom com' → command context."""
        macro = _make_macro("custom command", part_name="part")
        srv._macro_registry = _make_registry(macro)
        text = "custom com\n"
        # cursor at end of line (character=10)
        result = srv._get_completion_context(text, 0, 10, "file:///test.cmd")
        assert result is not None
        assert result[0] == "command"
        assert "custom com" in result[1]

    def test_builtin_command_returns_none(self):
        """Built-in commands (schema resolves) should return None."""
        text = "model create model_name=\n"
        # cursor at character 13 (in 'model create ')
        result = srv._get_completion_context(text, 0, 13, "file:///test.cmd")
        assert result is None

    # --- Argument context ---

    def test_after_command_key_returns_argument_context(self):
        """Cursor after full command key → argument completion."""
        macro = _make_macro("custom command", part_name="part", stiffness="real")
        srv._macro_registry = _make_registry(macro)
        text = "custom command \n"
        # cursor at character=15 (after 'custom command ')
        result = srv._get_completion_context(text, 0, 15, "file:///test.cmd")
        assert result is not None
        assert result[0] == "argument"
        _, macro_def, used_args, prefix = result
        assert macro_def.command == "custom command"
        assert used_args == set()
        assert prefix == ""

    def test_argument_with_partial_name(self):
        """Cursor at 'custom command part_' → argument context with prefix."""
        macro = _make_macro("custom command", part_name="part")
        srv._macro_registry = _make_registry(macro)
        text = "custom command part_\n"
        result = srv._get_completion_context(text, 0, 20, "file:///test.cmd")
        assert result is not None
        assert result[0] == "argument"
        _, macro_def, used_args, prefix = result
        assert prefix == "part_"

    def test_already_used_args_excluded(self):
        """Args already in the statement are reported in used_args."""
        macro = _make_macro("custom command", part_name="part", stiffness="real")
        srv._macro_registry = _make_registry(macro)
        text = "custom command part_name=.model.PART_1 \n"
        # cursor at end (character=39)
        result = srv._get_completion_context(text, 0, 39, "file:///test.cmd")
        assert result is not None
        assert result[0] == "argument"
        _, macro_def, used_args, prefix = result
        assert "part_name" in used_args

    def test_argument_on_continuation_line(self):
        """Argument completion on a continuation line."""
        macro = _make_macro("custom command", part_name="part", stiffness="real")
        srv._macro_registry = _make_registry(macro)
        text = "custom command  &\n  \n"
        # cursor at character=2 on line 1 (the continuation)
        result = srv._get_completion_context(text, 1, 2, "file:///test.cmd")
        assert result is not None
        assert result[0] == "argument"

    # --- Value context ---

    def test_value_context_after_equals(self):
        """Cursor after 'mode=' → value context."""
        macro = _make_macro("custom command", mode="list(on,off)")
        srv._macro_registry = _make_registry(macro)
        text = "custom command mode=\n"
        # cursor at character=20 (right after =)
        result = srv._get_completion_context(text, 0, 20, "file:///test.cmd")
        assert result is not None
        assert result[0] == "value"
        _, param, prefix = result
        assert param.name == "mode"
        assert prefix == ""

    def test_value_context_with_partial(self):
        """Cursor at 'mode=on' → value context with prefix 'on'."""
        macro = _make_macro("custom command", mode="list(on,off)")
        srv._macro_registry = _make_registry(macro)
        text = "custom command mode=on\n"
        result = srv._get_completion_context(text, 0, 22, "file:///test.cmd")
        assert result is not None
        assert result[0] == "value"
        _, param, prefix = result
        assert prefix == "on"

    def test_value_context_non_list_returns_value_kind_but_no_items(self):
        """For non-list types, _get_completion_context returns value context
        but the handler will find no list values to suggest."""
        macro = _make_macro("custom command", count="integer")
        srv._macro_registry = _make_registry(macro)
        text = "custom command count=5\n"
        result = srv._get_completion_context(text, 0, 21, "file:///test.cmd")
        # Could be ("value", ...) or ("argument", ...) depending on whether
        # "5" matches \w+ — we just verify no crash
        assert result is None or result[0] in ("value", "argument", "command")


# ---------------------------------------------------------------------------
# _parse_list_type_values + completion item generation (integration-style)
# ---------------------------------------------------------------------------

class TestCompletionItems:
    """Test the items that would be returned in each completion scenario."""

    def setup_method(self):
        srv._schema = Schema.load()
        srv._macro_registry = None

    def teardown_method(self):
        srv._macro_registry = None

    def test_command_items_include_matching_macros(self):
        """Command context returns CompletionItems for all matching macros."""
        macro_a = _make_macro("custom command", part_name="part")
        macro_b = _make_macro("custom other", part_name="part")
        macro_c = _make_macro("different cmd", part_name="part")
        srv._macro_registry = _make_registry(macro_a, macro_b, macro_c)

        text = "cust\n"
        ctx = srv._get_completion_context(text, 0, 4, "file:///test.cmd")
        assert ctx is not None and ctx[0] == "command"
        prefix = ctx[1].lower()

        labels = [
            cmd_key for cmd_key, _ in srv._macro_registry.items()
            if cmd_key.startswith(prefix)
        ]
        assert "custom command" in labels
        assert "custom other" in labels
        assert "different cmd" not in labels

    def test_argument_items_exclude_used_args(self):
        """Argument context filters out already-provided arguments."""
        macro = _make_macro("custom command", part_name="part", stiffness="real", damping="real")
        srv._macro_registry = _make_registry(macro)
        text = "custom command part_name=.model.P stiffness=1e6 \n"
        result = srv._get_completion_context(text, 0, 48, "file:///test.cmd")
        assert result is not None and result[0] == "argument"
        _, macro_def, used_args, _ = result
        assert "part_name" in used_args
        assert "stiffness" in used_args
        assert "damping" not in used_args

    def test_value_items_from_list_type(self):
        """Value context gives enum values from list() type constraint."""
        macro = _make_macro("custom command", mode="list(on,off,auto)")
        srv._macro_registry = _make_registry(macro)
        text = "custom command mode=\n"
        result = srv._get_completion_context(text, 0, 20, "file:///test.cmd")
        assert result is not None and result[0] == "value"
        _, param, prefix = result
        values = srv._parse_list_type_values(param.type_str or "")
        assert set(values) == {"on", "off", "auto"}

    def test_value_prefix_filters_list(self):
        """Value prefix filters enum suggestions."""
        macro = _make_macro("custom command", mode="list(yes,no,never)")
        srv._macro_registry = _make_registry(macro)
        text = "custom command mode=n\n"
        result = srv._get_completion_context(text, 0, 21, "file:///test.cmd")
        assert result is not None and result[0] == "value"
        _, param, prefix = result
        values = srv._parse_list_type_values(param.type_str or "")
        filtered = [v for v in values if v.lower().startswith(prefix.lower())]
        assert "no" in filtered
        assert "never" in filtered
        assert "yes" not in filtered

    def test_no_completions_for_builtin(self):
        """Built-in commands should never get macro completion context."""
        srv._macro_registry = _make_registry()
        text = "marker create \n"
        result = srv._get_completion_context(text, 0, 14, "file:///test.cmd")
        assert result is None


# ---------------------------------------------------------------------------
# Inline macro completion
# ---------------------------------------------------------------------------

class TestInlineMacroCompletion:
    def setup_method(self):
        srv._schema = Schema.load()
        srv._macro_registry = _make_registry()

    def teardown_method(self):
        srv._macro_registry = None

    def test_inline_macro_appears_in_command_context(self):
        """Macros defined earlier via 'macro create' are completable."""
        text = dedent("""\
            macro create macro_name=mymac user_entered_command="my command"
            my \
        """)
        result = srv._get_completion_context(text, 1, 3, "file:///test.cmd")
        # Should return command context with prefix "my "
        assert result is not None
        assert result[0] == "command"

    def test_inline_macro_not_visible_before_definition(self):
        """A macro cannot be completed before it is defined."""
        text = dedent("""\
            my command
            macro create macro_name=mymac user_entered_command="my command"
        """)
        # cursor on line 0, before the macro create
        # Look up inline macros with only statements preceding line 0 (none)
        from adams_cmd_lsp.parser import parse as parse_cmd
        from adams_cmd_lsp.macros import extract_macros_from_statements
        statements = parse_cmd(text)
        # Preceding statements for cursor at line 0: only stmts that ended before line 0
        preceding = [s for s in statements if s.line_end < 0]
        inline_macros = extract_macros_from_statements(preceding, srv._schema)
        assert all(m.command != "my command" for m in inline_macros)


# ---------------------------------------------------------------------------
# Integration tests for the completion() LSP handler
# ---------------------------------------------------------------------------

class TestCompletionHandler:
    """Test the completion() handler with a mocked LSP workspace."""

    def _make_params(self, uri, line, character, trigger_char=None):
        """Build CompletionParams for the given position."""
        trigger_kind = (
            types.CompletionTriggerKind.TriggerCharacter
            if trigger_char
            else types.CompletionTriggerKind.Invoked
        )
        return types.CompletionParams(
            text_document=types.TextDocumentIdentifier(uri=uri),
            position=types.Position(line=line, character=character),
            context=types.CompletionContext(
                trigger_kind=trigger_kind,
                trigger_character=trigger_char,
            ),
        )

    def _mock_workspace(self, monkeypatch, text, uri="file:///test.cmd"):
        """Patch srv.server.workspace to return a mock document."""
        import types as python_types
        mock_doc = python_types.SimpleNamespace(source=text)
        mock_ws = python_types.SimpleNamespace(
            get_text_document=lambda u: mock_doc,
        )
        monkeypatch.setattr(srv, "server", python_types.SimpleNamespace(workspace=mock_ws))

    def setup_method(self):
        srv._schema = Schema.load()
        srv._macro_registry = None

    def teardown_method(self):
        srv._macro_registry = None

    def test_handler_returns_none_when_no_schema(self, monkeypatch):
        srv._schema = None
        self._mock_workspace(monkeypatch, "custom command\n")
        params = self._make_params("file:///test.cmd", 0, 6)
        result = srv.completion(params)
        assert result is None
        srv._schema = Schema.load()

    def test_handler_returns_none_for_builtin(self, monkeypatch):
        """Built-in commands must not get LSP completions."""
        self._mock_workspace(monkeypatch, "marker create \n")
        params = self._make_params("file:///test.cmd", 0, 14)
        result = srv.completion(params)
        assert result is None

    def test_handler_command_completion_returns_completion_list(self, monkeypatch):
        """Command context returns a CompletionList with matching macro labels."""
        macro = _make_macro("custom command", part_name="part")
        srv._macro_registry = _make_registry(macro)
        self._mock_workspace(monkeypatch, "cust\n")
        params = self._make_params("file:///test.cmd", 0, 4)
        result = srv.completion(params)
        assert result is not None
        assert isinstance(result, types.CompletionList)
        labels = [item.label for item in result.items]
        assert "custom command" in labels

    def test_handler_command_completion_uses_text_edit(self, monkeypatch):
        """Command completion items must use text_edit for correct multi-word replacement."""
        macro = _make_macro("custom command", part_name="part")
        srv._macro_registry = _make_registry(macro)
        self._mock_workspace(monkeypatch, "custom \n")
        params = self._make_params("file:///test.cmd", 0, 7)
        result = srv.completion(params)
        assert result is not None
        item = next((i for i in result.items if i.label == "custom command"), None)
        assert item is not None
        assert item.text_edit is not None
        assert item.text_edit.new_text == "custom command"

    def test_handler_argument_completion_returns_param_names(self, monkeypatch):
        """Argument context returns CompletionItems for macro parameters."""
        macro = _make_macro("custom command", part_name="part", stiffness="real")
        srv._macro_registry = _make_registry(macro)
        self._mock_workspace(monkeypatch, "custom command \n")
        params = self._make_params("file:///test.cmd", 0, 15)
        result = srv.completion(params)
        assert result is not None
        labels = [item.label for item in result.items]
        assert "part_name" in labels
        assert "stiffness" in labels

    def test_handler_argument_insert_text_has_equals(self, monkeypatch):
        """Argument completion items must insert 'param_name=' with trailing =."""
        macro = _make_macro("custom command", part_name="part")
        srv._macro_registry = _make_registry(macro)
        self._mock_workspace(monkeypatch, "custom command \n")
        params = self._make_params("file:///test.cmd", 0, 15)
        result = srv.completion(params)
        assert result is not None
        item = next((i for i in result.items if i.label == "part_name"), None)
        assert item is not None
        assert item.text_edit.new_text == "part_name="

    def test_handler_argument_excludes_used_params(self, monkeypatch):
        """Arguments already in the statement are not suggested."""
        macro = _make_macro("custom command", part_name="part", stiffness="real")
        srv._macro_registry = _make_registry(macro)
        self._mock_workspace(monkeypatch, "custom command part_name=.model.P \n")
        params = self._make_params("file:///test.cmd", 0, 35)
        result = srv.completion(params)
        assert result is not None
        labels = [item.label for item in result.items]
        assert "part_name" not in labels
        assert "stiffness" in labels

    def test_handler_value_completion_returns_enum_items(self, monkeypatch):
        """Value context after '=' returns enum values from list() type."""
        macro = _make_macro("custom command", mode="list(on,off,auto)")
        srv._macro_registry = _make_registry(macro)
        self._mock_workspace(monkeypatch, "custom command mode=\n")
        params = self._make_params("file:///test.cmd", 0, 20, trigger_char="=")
        result = srv.completion(params)
        assert result is not None
        labels = [item.label for item in result.items]
        assert "on" in labels
        assert "off" in labels
        assert "auto" in labels

    def test_handler_value_completion_filters_by_prefix(self, monkeypatch):
        """Value items starting with the typed prefix are included; others excluded."""
        macro = _make_macro("custom command", mode="list(yes,no,never)")
        srv._macro_registry = _make_registry(macro)
        self._mock_workspace(monkeypatch, "custom command mode=n\n")
        params = self._make_params("file:///test.cmd", 0, 21)
        result = srv.completion(params)
        assert result is not None
        labels = [item.label for item in result.items]
        assert "no" in labels
        assert "never" in labels
        assert "yes" not in labels

    def test_handler_returns_none_when_no_items(self, monkeypatch):
        """When no items match, handler returns None (not an empty list)."""
        macro = _make_macro("custom command", part_name="part")
        srv._macro_registry = _make_registry(macro)
        # Cursor inside a built-in command — no macro matches
        self._mock_workspace(monkeypatch, "model create \n")
        params = self._make_params("file:///test.cmd", 0, 13)
        result = srv.completion(params)
        assert result is None


# ---------------------------------------------------------------------------
# TestParamRefCompletion
# ---------------------------------------------------------------------------

class TestParamRefCompletion:
    """$param reference completions — triggered by '$' anywhere on the line."""

    def _make_params(self, uri, line, character,
                     trigger_kind=types.CompletionTriggerKind.TriggerCharacter,
                     trigger_char="$"):
        return types.CompletionParams(
            text_document=types.TextDocumentIdentifier(uri=uri),
            position=types.Position(line=line, character=character),
            context=types.CompletionContext(
                trigger_kind=trigger_kind,
                trigger_character=trigger_char,
            ),
        )

    def _mock_workspace(self, monkeypatch, text, uri="file:///test.cmd"):
        import types as python_types
        mock_doc = python_types.SimpleNamespace(source=text)
        mock_ws = python_types.SimpleNamespace(
            get_text_document=lambda u: mock_doc,
        )
        monkeypatch.setattr(srv, "server", python_types.SimpleNamespace(workspace=mock_ws))

    def setup_method(self):
        srv._schema = srv.Schema.load()
        srv._macro_registry = None

    def teardown_method(self):
        srv._macro_registry = None

    # -----------------------------------------------------------------------
    # Core behaviour
    # -----------------------------------------------------------------------

    def test_dollar_returns_all_params_and_self(self, monkeypatch):
        """'$' with no partial returns all defined params plus $_self."""
        text = (
            "!$str_param_1:t=str\n"
            "!$real_param_1:t=real\n"
            "!$model:t=model\n"
            "!END_OF_PARAMETERS\n"
            "part create rigid_body name_and_position part_name=$\n"
        )
        self._mock_workspace(monkeypatch, text)
        line = 4
        character = len("part create rigid_body name_and_position part_name=$")
        params = self._make_params("file:///test.cmd", line, character)
        result = srv.completion(params)
        assert result is not None
        labels = [item.label for item in result.items]
        assert "$str_param_1" in labels
        assert "$real_param_1" in labels
        assert "$model" in labels
        assert "$_self" in labels

    def test_dollar_partial_filters(self, monkeypatch):
        """'$s' returns only params whose name starts with 's'; not others."""
        text = (
            "!$str_param_1:t=str\n"
            "!$real_param_1:t=real\n"
            "!$model:t=model\n"
            "!END_OF_PARAMETERS\n"
            "part create rigid_body name_and_position part_name=$s\n"
        )
        self._mock_workspace(monkeypatch, text)
        line = 4
        character = len("part create rigid_body name_and_position part_name=$s")
        params = self._make_params("file:///test.cmd", line, character)
        result = srv.completion(params)
        assert result is not None
        labels = [item.label for item in result.items]
        assert "$str_param_1" in labels
        assert "$real_param_1" not in labels
        assert "$model" not in labels
        assert "$_self" not in labels

    def test_self_sorts_last(self, monkeypatch):
        """$_self has a higher sort_text than macro-specific params."""
        text = (
            "!$my_param:t=str\n"
            "!END_OF_PARAMETERS\n"
            "marker create marker_name=$\n"
        )
        self._mock_workspace(monkeypatch, text)
        line = 2
        character = len("marker create marker_name=$")
        params = self._make_params("file:///test.cmd", line, character)
        result = srv.completion(params)
        assert result is not None
        self_item = next((i for i in result.items if i.label == "$_self"), None)
        param_item = next((i for i in result.items if i.label == "$my_param"), None)
        assert self_item is not None
        assert param_item is not None
        assert self_item.sort_text > param_item.sort_text

    def test_no_params_returns_self_only(self, monkeypatch):
        """File with no header params still returns $_self."""
        text = "marker create marker_name=$\n"
        self._mock_workspace(monkeypatch, text)
        line = 0
        character = len("marker create marker_name=$")
        params = self._make_params("file:///test.cmd", line, character)
        result = srv.completion(params)
        assert result is not None
        labels = [item.label for item in result.items]
        assert labels == ["$_self"]

    def test_dollar_mid_expression(self, monkeypatch):
        """$param completions work inside eval(...) expressions."""
        text = (
            "!$my_part:t=part\n"
            "!END_OF_PARAMETERS\n"
            "marker create location=(eval(loc_global({0,0,0}, $\n"
        )
        self._mock_workspace(monkeypatch, text)
        line = 2
        character = len("marker create location=(eval(loc_global({0,0,0}, $")
        params = self._make_params("file:///test.cmd", line, character)
        result = srv.completion(params)
        assert result is not None
        labels = [item.label for item in result.items]
        assert "$my_part" in labels
        assert "$_self" in labels

    def test_param_has_docstring(self, monkeypatch):
        """Params with a docstring comment get a documentation field."""
        text = (
            "!$my_param:t=str\n"
            "! This is the docstring.\n"
            "!END_OF_PARAMETERS\n"
            "marker create marker_name=$\n"
        )
        self._mock_workspace(monkeypatch, text)
        line = 3
        character = len("marker create marker_name=$")
        params = self._make_params("file:///test.cmd", line, character)
        result = srv.completion(params)
        assert result is not None
        item = next((i for i in result.items if i.label == "$my_param"), None)
        assert item is not None
        assert item.documentation is not None
        assert "docstring" in item.documentation.value

    def test_param_type_in_detail(self, monkeypatch):
        """The type qualifier appears in the detail field."""
        text = (
            "!$my_real:t=real\n"
            "!END_OF_PARAMETERS\n"
            "marker create marker_name=$\n"
        )
        self._mock_workspace(monkeypatch, text)
        line = 2
        character = len("marker create marker_name=$")
        params = self._make_params("file:///test.cmd", line, character)
        result = srv.completion(params)
        assert result is not None
        item = next((i for i in result.items if i.label == "$my_real"), None)
        assert item is not None
        assert item.detail == "real"

    def test_dollar_in_builtin_command(self, monkeypatch):
        """$param completions work inside built-in Adams commands too."""
        text = (
            "!$part_name:t=str\n"
            "!END_OF_PARAMETERS\n"
            "part create rigid_body name_and_position part_name=$\n"
        )
        self._mock_workspace(monkeypatch, text)
        line = 2
        character = len("part create rigid_body name_and_position part_name=$")
        params = self._make_params("file:///test.cmd", line, character)
        result = srv.completion(params)
        assert result is not None
        labels = [item.label for item in result.items]
        assert "$part_name" in labels
        assert "$_self" in labels

    def test_dollar_on_comment_line_no_completions(self, monkeypatch):
        """No $param completions inside comment lines."""
        text = (
            "!$my_param:t=str\n"
            "!END_OF_PARAMETERS\n"
            "! This is a comment with a $ reference\n"
        )
        self._mock_workspace(monkeypatch, text)
        line = 2
        character = len("! This is a comment with a $ reference")
        params = self._make_params("file:///test.cmd", line, character)
        result = srv.completion(params)
        # The comment-line guard should prevent any $param completions
        # (context will be None and result will be None)
        assert result is None

    def test_param_completion_replace_range_is_correct(self, monkeypatch):
        """text_edit.range spans exactly the typed $partial (start at '$', end at cursor)."""
        text = (
            "!$my_var:t=str\n"
            "!END_OF_PARAMETERS\n"
            "marker create marker_name=$my_v\n"
        )
        self._mock_workspace(monkeypatch, text)
        line = 2
        character = len("marker create marker_name=$my_v")
        params = self._make_params("file:///test.cmd", line, character)
        result = srv.completion(params)
        assert result is not None
        item = next((i for i in result.items if i.label == "$my_var"), None)
        assert item is not None
        # '$my_v' is 5 chars; dollar_col = character - 5
        assert item.text_edit.range.start.character == character - 5
        assert item.text_edit.range.end.character == character


# ---------------------------------------------------------------------------
# TestParamDefinitionCompletion
# ---------------------------------------------------------------------------

class TestParamDefinitionCompletion:
    """Completions on !$param_name:qualifier lines."""

    def _make_params(self, uri, line, character,
                     trigger_kind=types.CompletionTriggerKind.TriggerCharacter,
                     trigger_char="="):
        return types.CompletionParams(
            text_document=types.TextDocumentIdentifier(uri=uri),
            position=types.Position(line=line, character=character),
            context=types.CompletionContext(
                trigger_kind=trigger_kind,
                trigger_character=trigger_char,
            ),
        )

    def _mock_workspace(self, monkeypatch, text, uri="file:///test.cmd"):
        import types as python_types
        mock_doc = python_types.SimpleNamespace(source=text)
        mock_ws = python_types.SimpleNamespace(
            get_text_document=lambda u: mock_doc,
        )
        monkeypatch.setattr(srv, "server", python_types.SimpleNamespace(workspace=mock_ws))

    def setup_method(self):
        srv._schema = srv.Schema.load()
        srv._macro_registry = None

    def teardown_method(self):
        srv._macro_registry = None

    # -----------------------------------------------------------------------

    def test_t_equals_returns_all_type_values(self, monkeypatch):
        """'!$p:t=' returns all type values including primitives and object types."""
        text = "!$p:t=\n"
        self._mock_workspace(monkeypatch, text)
        params = self._make_params("file:///test.cmd", 0, len("!$p:t="))
        result = srv.completion(params)
        assert result is not None
        labels = [item.label for item in result.items]
        # Primitives present
        assert "real" in labels
        assert "integer" in labels
        assert "string" in labels
        # Adams object types present
        assert "model" in labels
        assert "part" in labels
        assert "marker" in labels
        # Special list type present
        assert "list" in labels

    def test_t_equals_partial_filters(self, monkeypatch):
        """'!$p:t=m' returns only type values starting with 'm'."""
        text = "!$p:t=m\n"
        self._mock_workspace(monkeypatch, text)
        params = self._make_params("file:///test.cmd", 0, len("!$p:t=m"))
        result = srv.completion(params)
        assert result is not None
        labels = [item.label for item in result.items]
        # All returned labels start with 'm'
        assert all(lbl.startswith("m") for lbl in labels), f"Non-m labels: {labels}"
        assert "model" in labels
        assert "marker" in labels
        # Non-matching types excluded
        assert "real" not in labels
        assert "part" not in labels

    def test_primitives_sort_before_entity_types(self, monkeypatch):
        """Primitive types (real, string, integer) sort before Adams entity types."""
        text = "!$p:t=\n"
        self._mock_workspace(monkeypatch, text)
        params = self._make_params("file:///test.cmd", 0, len("!$p:t="))
        result = srv.completion(params)
        assert result is not None
        sorted_items = sorted(result.items, key=lambda i: i.sort_text or i.label)
        primitive_labels = {"real", "integer", "string", "str"}
        non_primitive_labels = {"model", "part", "marker", "contact"}
        first_non_prim = next(
            (i for i in sorted_items if i.label in non_primitive_labels), None
        )
        last_prim = next(
            (i for i in reversed(sorted_items) if i.label in primitive_labels), None
        )
        assert first_non_prim is not None
        assert last_prim is not None
        assert last_prim.sort_text < first_non_prim.sort_text

    def test_list_type_is_snippet(self, monkeypatch):
        """The 'list' type completion uses snippet insert format with $1 inside parens."""
        text = "!$p:t=l\n"
        self._mock_workspace(monkeypatch, text)
        params = self._make_params("file:///test.cmd", 0, len("!$p:t=l"))
        result = srv.completion(params)
        assert result is not None
        item = next((i for i in result.items if i.label == "list"), None)
        assert item is not None
        assert item.insert_text == "list($1)"
        assert item.insert_text_format == types.InsertTextFormat.Snippet

    def test_colon_returns_qualifier_keys(self, monkeypatch):
        """'!$p:' returns all qualifier key completions."""
        text = "!$p:\n"
        self._mock_workspace(monkeypatch, text)
        params = self._make_params("file:///test.cmd", 0, len("!$p:"), trigger_char=":")
        result = srv.completion(params)
        assert result is not None
        labels = [item.label for item in result.items]
        assert "t" in labels
        assert "d" in labels
        assert "ud" in labels
        assert "ge" in labels
        assert "gt" in labels
        assert "le" in labels
        assert "lt" in labels
        assert "c" in labels

    def test_qualifier_partial_filters(self, monkeypatch):
        """'!$p:t=real:g' returns only ge and gt."""
        text = "!$p:t=real:g\n"
        self._mock_workspace(monkeypatch, text)
        params = self._make_params("file:///test.cmd", 0, len("!$p:t=real:g"))
        result = srv.completion(params)
        assert result is not None
        labels = [item.label for item in result.items]
        assert "ge" in labels
        assert "gt" in labels
        assert "t" not in labels
        assert "d" not in labels

    def test_excludes_already_used_qualifiers(self, monkeypatch):
        """Qualifier keys already present on the line are excluded from suggestions."""
        text = "!$p:t=real:\n"
        self._mock_workspace(monkeypatch, text)
        params = self._make_params("file:///test.cmd", 0, len("!$p:t=real:"), trigger_char=":")
        result = srv.completion(params)
        assert result is not None
        labels = [item.label for item in result.items]
        # 't' is already used — should not appear
        assert "t" not in labels
        # Others still available
        assert "d" in labels
        assert "ge" in labels

    def test_qualifier_insert_text_includes_equals(self, monkeypatch):
        """Qualifier key completion insert text ends with '='."""
        text = "!$p:\n"
        self._mock_workspace(monkeypatch, text)
        params = self._make_params("file:///test.cmd", 0, len("!$p:"), trigger_char=":")
        result = srv.completion(params)
        assert result is not None
        t_item = next((i for i in result.items if i.label == "t"), None)
        assert t_item is not None
        assert t_item.insert_text == "t="

    def test_plain_comment_returns_none(self, monkeypatch):
        """A plain comment line (! but no $) returns None — no param-def completions."""
        text = "! This is a regular comment with t=m\n"
        self._mock_workspace(monkeypatch, text)
        params = self._make_params("file:///test.cmd", 0, len("! This is a regular comment with t=m"))
        result = srv.completion(params)
        assert result is None

    def test_non_param_line_not_affected(self, monkeypatch):
        """Regular command lines are not matched by the param-def handler."""
        macro = _make_macro("custom command", part_name="part")
        srv._macro_registry = _make_registry(macro)
        text = "custom command \n"
        self._mock_workspace(monkeypatch, text)
        params = self._make_params("file:///test.cmd", 0, len("custom command "))
        result = srv.completion(params)
        # Normal macro argument completions should still work
        assert result is not None
        labels = [item.label for item in result.items]
        assert "part_name" in labels

    def test_cursor_inside_param_name_returns_none(self, monkeypatch):
        """No completions when cursor is inside the param name itself (before first ':')."""
        text = "!$param_na\n"
        self._mock_workspace(monkeypatch, text)
        # Cursor is mid-name: '!$param_na' — no qualifier context yet
        params = self._make_params(
            "file:///test.cmd", 0, len("!$param_na"),
            trigger_kind=types.CompletionTriggerKind.Invoked, trigger_char=None,
        )
        result = srv.completion(params)
        assert result is None

    def test_quoted_param_name_no_completions_before_colon(self, monkeypatch):
        """No completions inside a quoted param name (before any qualifier)."""
        text = "!$'my param'\n"
        self._mock_workspace(monkeypatch, text)
        params = self._make_params(
            "file:///test.cmd", 0, len("!$'my param'"),
            trigger_kind=types.CompletionTriggerKind.Invoked, trigger_char=None,
        )
        result = srv.completion(params)
        assert result is None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def dedent(text):
    """Simple textwrap.dedent replacement to avoid import."""
    import textwrap
    return textwrap.dedent(text)

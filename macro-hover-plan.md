# Plan: Macro Hover Documentation via LSP

## TL;DR
Add `textDocument/hover` to the Adams CMD LSP server so that hovering a macro command invocation (e.g. `cdm qual set_158`) shows the description extracted from the macro's `! DESCRIPTION:` header line. Requires extending `MacroDefinition` with a `description` field, parsing it from macro headers, and implementing the LSP hover handler.

## Decisions
- **Invocations only** — hover triggers on macro command usage, not the definition-site `!USER_ENTERED_COMMAND` line
- **LSP server** handles macro hover; JS hover provider unchanged (continues handling built-in commands/functions)
- **Description only** — show the description text, not parameter tables or source links
- **Single-line description** — the `! DESCRIPTION:` convention is single-line per the snippet template; empty descriptions treated as None

## Recent Codebase Changes (post-plan)
Since this plan was written, several commits have landed on the current branch (`dev_lsp_linked_object_refs`) that affect the implementation context. **None conflict with the plan**, but the implementation should be aware of:

- **`_doc_cache` pattern** — `server.py` now caches `(statements, symbol_table)` per document. The hover handler can use `_get_doc_cache()` to access pre-parsed statements rather than re-parsing.
- **Expanded `goto_definition` / `find_references`** — these handlers now try multiple strategies in order (macros → Adams objects → $variables). The new hover handler should follow the same pattern: try macro hover first, return `None` if no match (letting the JS provider handle built-in commands).
- **`_refresh_macro_file()` now returns `bool`** — indicates whether the file matched a macro pattern. Not relevant for hover, but good to know for test patterns.
- **New module `object_index.py`** — provides `ObjectIndex` for cross-file Adams object navigation. Not needed for macro hover, but shows the pattern for new index modules.
- **New imports** in `server.py`: `SymbolTable`, `build_symbol_table`, `ObjectIndex`, `index_file_objects`, `_resolve_command_keys`, `re`.

## Steps

### Phase 1: Parse description from macro headers (Python)

1. **Add `description` field to `MacroDefinition`** in `adams-cmd-lsp/adams_cmd_lsp/macros.py`
   - Add `description: Optional[str] = None` to the dataclass (after `line`)
   - This is non-breaking — existing callers don't need changes

2. **Extract description in `parse_macro_file()`** in `adams-cmd-lsp/adams_cmd_lsp/macros.py`
   - After finding `!USER_ENTERED_COMMAND`, scan subsequent lines for `! DESCRIPTION:` pattern
   - Regex: `^\s*!\s*DESCRIPTION:\s*(.*)$` (case-insensitive)
   - Stop scanning at `!END_OF_PARAMETERS` or the first non-comment line (whichever comes first)
   - If the captured text is blank/whitespace, store `None`
   - Only extract description lines between `!USER_ENTERED_COMMAND` and `!END_OF_PARAMETERS` (the header block)

3. **Add tests for description parsing** in `adams-cmd-lsp/tests/test_macros.py`
   - Test: description is extracted from standard header
   - Test: empty `! DESCRIPTION:` results in `None`
   - Test: missing `! DESCRIPTION:` line results in `None`
   - Test: description with leading/trailing whitespace is stripped

### Phase 2: LSP hover handler (Python)

4. **Implement `textDocument/hover`** in `adams-cmd-lsp/adams_cmd_lsp/server.py`
   - Register `@server.feature(types.TEXT_DOCUMENT_HOVER)` handler
   - Use `_get_command_key_at_position()` to resolve the macro under the cursor (same helper used by `goto_definition`)
   - If result origin is `"registry"` or `"inline"`:
     - Build markdown: `**{command_key}**\n\n{description}` (if description exists)
     - If no description, just show `**{command_key}**` (macro name, so user knows it resolved)
     - Return `types.Hover(contents=types.MarkupContent(kind=types.MarkupKind.Markdown, value=md))`
   - If result origin is `"definition_site"` or `None` → return `None` (no hover)
   - Set the hover range to the `origin_range` returned by `_get_command_key_at_position()` so the full command key highlights on hover
   - **Note**: Unlike `goto_definition`, the hover handler does NOT need to fall through to object/variable navigation — it only handles macros. The JS hover provider handles built-in commands/functions independently.

5. **Add tests for hover handler** in `adams-cmd-lsp/tests/test_server.py`
   - Test: hover on macro invocation returns description markdown
   - Test: hover on macro with no description returns command key only
   - Test: hover on built-in command returns None (defers to JS provider)
   - Test: hover on non-command line returns None
   - Test: hover on definition_site returns None (per scope decision)

### Phase 3: Verification

6. **Run `pytest adams-cmd-lsp`** to confirm all new + existing tests pass
7. **Manual test**: open a `.cmd` file that invokes a macro, hover the macro command, confirm hover appears with description

## Relevant Files

| File | Change |
|------|--------|
| `adams-cmd-lsp/adams_cmd_lsp/macros.py` | Add `description` field to `MacroDefinition`; extract it in `parse_macro_file()` |
| `adams-cmd-lsp/adams_cmd_lsp/server.py` | Add `@server.feature(types.TEXT_DOCUMENT_HOVER)` handler; reuse `_get_command_key_at_position()` |
| `adams-cmd-lsp/tests/test_macros.py` | Description parsing tests |
| `adams-cmd-lsp/tests/test_server.py` | Hover handler tests |

**Not modified** (verified unchanged since plan was written):
- `adams-cmd-lsp/adams_cmd_lsp/macros.py` — no recent commits touched this file
- `adams-cmd-lsp/tests/test_macros.py` — no recent commits touched this file

## Verification Checklist
1. `cd adams-cmd-lsp && python -m pytest --tb=short -q` — all tests pass
2. Run "Bundle LSP Dependencies" task to update `bundled/libs/`
3. Reload VS Code, open a `.cmd` file that invokes a known macro, hover the macro command → hover popup with description appears
4. Hover a built-in command (e.g. `marker create`) → existing JS hover still works (no regression)
5. Hover a macro with empty `! DESCRIPTION:` → hover shows just the command name

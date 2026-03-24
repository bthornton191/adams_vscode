---
name: adams-cmd-lsp-builder
description: "Build, modify, test, and debug the Adams CMD Language Server (LSP) and CLI linter Python package. Use when: implementing parser, schema, rules, linter, CLI, or LSP server code in adams-cmd-lsp/; writing or running pytest tests; generating command_schema.json; wiring the LSP client into the VS Code extension. Covers pygls 2.x patterns, the parser port from JS, lint rule signatures, schema format, and testing conventions."
---

# Adams CMD LSP Builder

Condensed reference for implementing the `adams-cmd-lsp` Python package. The full design document is `adams-cmd-lsp-plan.md` in the repo root — consult it for detailed algorithms, edge cases, and rationale.

## Package Layout

```
adams-cmd-lsp/                         Python package root
  pyproject.toml                       setuptools config + entry points
  adams_cmd_lsp/
    __init__.py
    __main__.py                        python -m adams_cmd_lsp -> starts LSP
    parser.py                          Tokenize .cmd text -> Statement objects
    schema.py                          Load & query command_schema.json
    rules.py                           All lint rules (E001..I202)
    symbols.py                         Single-file symbol table
    linter.py                          Orchestrator: parse -> symbols -> rules
    diagnostics.py                     Diagnostic dataclass + Severity enum
    server.py                          pygls LSP server (~200-300 lines)
    cli.py                             adams-cmd-lint CLI entry point
    data/
      command_schema.json              Generated schema (committed to repo)
  tests/
    test_parser.py
    test_schema.py
    test_rules.py
    test_symbols.py
    test_linter.py
    test_cli.py
    test_server.py
    fixtures/                          Test .cmd files

scripts/
  generate_command_schema.py           One-time schema generator (reads commands.exp)
```

## Key Conventions

### Python version & dependencies
- Python 3.9+ (guaranteed by VS Code extension's `extensionDependencies` on `ms-python.python`)
- Runtime: `pygls>=2.0`, `lsprotocol`
- Dev: `pytest`

### Proprietary data protection
- `commands.exp`, `language.src`, `commands.more` are closed-source Adams files — NEVER commit them
- `command_schema.json` is derived work — review carefully before first commit
- The schema generator should print a reminder about reviewing before commit

### Testing
- Pure unit tests, NO Adams View required
- Run with: `cd adams-cmd-lsp && pytest`
- Use `tests/fixtures/` for test CMD files
- Can also reference `test/files/*.cmd` from the parent repo for integration-level checks

## pygls 2.x API Patterns

pygls 2.x has a different API from 1.x. Always use these imports:

```python
from pygls.lsp.server import LanguageServer    # NOT from pygls.server
from lsprotocol import types                    # NOT from pygls.lsp.types

server = LanguageServer("adams-cmd-lsp", "v0.1.0")

@server.feature(types.TEXT_DOCUMENT_DID_OPEN)
def did_open(params: types.DidOpenTextDocumentParams):
    doc = params.text_document
    # lint doc.text, publish diagnostics
    
@server.feature(types.TEXT_DOCUMENT_DID_CHANGE)
def did_change(params: types.DidChangeTextDocumentParams):
    doc = server.workspace.get_text_document(params.text_document.uri)
    # lint doc.source

@server.feature(types.TEXT_DOCUMENT_DID_CLOSE)  
def did_close(params: types.DidCloseTextDocumentParams):
    server.publish_diagnostics(params.text_document.uri, [])

@server.feature(types.TEXT_DOCUMENT_DID_SAVE)
def did_save(params: types.DidSaveTextDocumentParams):
    doc = server.workspace.get_text_document(params.text_document.uri)
    # lint doc.source
```

Transport: stdio by default, `--tcp` flag for debugging.

## Core Data Structures

### Diagnostic (diagnostics.py)
```python
class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

@dataclass
class Diagnostic:
    line: int           # 0-based
    column: int         # 0-based
    end_line: int       # 0-based
    end_column: int     # 0-based
    code: str           # "E001", "W005", etc.
    message: str
    severity: Severity
```

### Statement (parser.py)
```python
@dataclass
class Argument:
    name: str
    value: str
    name_line: int
    name_column: int
    value_line: int
    value_column: int

@dataclass
class Statement:
    command_key: str                # as written (lowercase)
    resolved_command_key: str       # canonical form after abbreviation resolution, or None
    arguments: list[Argument]
    line_start: int                 # 0-based
    line_end: int                   # 0-based, inclusive
    raw_text: str
    is_comment: bool
    is_blank: bool
    is_control_flow: bool
    control_flow_keyword: str       # "if", "else", "end", "for", "while", or None
```

## Parser Overview

The parser is a port from `src/cmd_completion_provider.ts.js`. Key functions to port:

1. **`group_continuation_lines(lines)`** — Join lines ending with `&`, tracking original line/column positions
2. **`extract_command_key(text)`** — Strip all `arg=value` pairs to isolate the command key (port of `strip_argument_pairs`)
3. **`consume_argument_value(text, start)`** — Consume quoted strings, parenthesized expressions (with nesting), or bare words
4. **`consume_comma_separated_tail(text, i, value_start)`** — Continue consuming comma-separated values after initial value
5. **`extract_arguments(text, line_offsets)`** — Extract all `arg=value` pairs with line/column positions

Critical detail: when continuation lines are joined, maintain a mapping from character positions in the joined string back to original (line, column) for accurate diagnostic positions.

Control flow keywords (`if`, `else`, `end`, `for`, `while`) are NOT Adams commands — they are built-in and should NOT be validated against the command schema. Only the FIRST token determines control flow; `variable set variable_name = if_needed` is not control flow.

## Schema Format (command_schema.json)

Two top-level keys:

```json
{
  "commands": {
    "marker create": {
      "args": {
        "marker_name": {
          "required": true,
          "type": "new_object",
          "object_type": "Marker",
          "db_type": "NDBWD_MARKER",
          "min_prefix": 2
        },
        "adams_id": {
          "required": false,
          "type": "adams_id",
          "min_prefix": 1
        }
      },
      "exclusive_groups": [
        {"group": 1, "members": ["node_id", "preserve_location"]}
      ]
    }
  },
  "command_tree": {
    "children": {
      "marker": {
        "min_prefix": 3,
        "children": {
          "create": {"min_prefix": 1, "is_leaf": true}
        }
      }
    }
  }
}
```

### Abbreviation matching
Adams uses shortest unique prefix matching (case-insensitive). `min_prefix` is pre-computed during schema generation. At lint time:
- Exact match always takes priority
- Prefix must be >= `min_prefix` chars and unambiguous among siblings
- Applied to both command tokens (via `command_tree`) and argument names (via per-arg `min_prefix`)

### Type classification
| Token pattern | Schema type | Notes |
|---|---|---|
| `NDBWD_X` / `NDB_X` | `new_object` | Creates new object; auto-names if omitted |
| `DB_X` | `existing_object` | References existing object |
| `INT` | `integer` | |
| `REAL`, `LENGTH`, `MASS`, etc. | `real` (with `unit`) | Physical quantities |
| `LOCATION` | `location` | x,y,z |
| `ORIENTATION` | `orientation` | angle triplet |
| `BOOLEAN`, `ON_OFF`, etc. | `boolean` | |
| `STRING`, `FILE` | `string` | |
| `FUNCTION` | `function` | Adams expression |
| `ADAMS_ID` | `adams_id` | Auto-assigned integer |

## Lint Rules

Each rule is a function: `rule_xxx(statements, schema, symbols) -> list[Diagnostic]`

| Code | Severity | What it checks |
|---|---|---|
| E001 | Error | Unknown command (even after abbreviation expansion) |
| E002 | Error | Invalid argument name for this command |
| E003 | Error | Duplicate argument (same canonical name twice) |
| E004 | Error | Invalid enum value |
| E005 | Error | Missing truly required argument (not auto-generated) |
| W005 | Warning | Object name (`NDBWD_*`) omitted — auto-generated but explicit preferred |
| I006 | Info | Manual `adams_id` assignment — auto-assign is best practice |
| E006 | Warning | Mutual exclusion conflict (two exclusive args provided) |
| E101 | Error | Unbalanced parentheses |
| E102 | Error | Unclosed quote |
| E103 | Error | Orphan continuation line |
| E104 | Error | Unbalanced if/end, else without if, etc. |
| W201 | Warning | Type mismatch (wrong object type for argument) |
| I202 | Info | Unresolved reference (not found in file) |

### E005/W005 nuances
- `ADAMS_ID` type args omitted: **no diagnostic** (omission is preferred)
- `NDBWD_*`/`NDB_*` type args omitted: **W005 warning** (auto-generated name, but explicit is better)
- All other required args omitted: **E005 error**
- **Exclusive group suppression:** If a required arg belongs to a mutual exclusion group and another member is provided, suppress the missing-required diagnostic entirely

### I006 nuance
- Fires when user **provides** `adams_id`, not when they omit it
- Omitting `adams_id` produces no diagnostic at all

## Linter Orchestrator (linter.py)

```python
def lint_text(text, schema=None, min_severity=None):
    schema = schema or Schema.load()
    statements = parse(text)
    symbols = build_symbol_table(statements, schema)
    diagnostics = []
    for rule in ALL_RULES:
        diagnostics.extend(rule(statements, schema, symbols))
    # Filter by severity, sort by (line, column)
    return sorted(diagnostics, key=lambda d: (d.line, d.column))
```

## CLI (cli.py)

```
adams-cmd-lint <files> [--format text|json|gcc] [--severity error|warning|info] [--schema PATH]
```

Exit codes: 0 = clean, 1 = issues found, 2 = usage error

## Schema Generation (scripts/generate_command_schema.py)

Reads from two sources:
1. **Primary:** `commands.exp` — fully expanded commands with flattened keys, types, `*` required markers, defaults
2. **Secondary:** `language.src` — only for `{...}` mutual exclusion groups

Also merges:
- `argument_options.json` — enum values for arguments
- Validates against `structured.json` — cross-reference coverage

### commands.exp format
```
 model create
   model_name=NDBWD_MECHANISM*
   comments=STRING(0)
   title=STRING
   view_name=DB_VIEW(0)=DYN_DB
   fit_to_view=BOOLEAN=yes
 model modify
   ...
```
- Command key lines: 1 leading space + text
- Argument lines: 3+ spaces indent, `name=TYPE`, `name=TYPE*` (required), `name=TYPE=default`
- `TYPE(0)` = array, `TYPE(n,m)` = n-to-m values, `TYPE(GT,lo,LT,hi)` = range constraint

## VS Code Integration

### LSP Client (src/cmd_lsp_client.ts.js)
- Plain JavaScript, CommonJS, `.ts.js` extension
- Dependency injection: `output_channel`, `reporter`
- Uses `vscode-languageclient/node` to start the Python LSP via stdio
- Respects `msc-adams.linter.enabled` setting
- Python path: `msc-adams.linter.pythonPath` > `python.defaultInterpreterPath` > `"python"`

### Extension wiring (src/extension.ts.js)
```javascript
const { cmd_lsp_client } = require("./cmd_lsp_client.ts.js");
// Inside activate():
const lsp = cmd_lsp_client(output_channel, reporter);
lsp.start(context);
```

### package.json additions
- Dependency: `"vscode-languageclient": "^9.0.1"`
- Settings: `msc-adams.linter.enabled`, `msc-adams.linter.pythonPath`, `msc-adams.linter.severity`, `msc-adams.linter.semanticAnalysis`

## VS Code Extension Test Conventions
- Tests for the LSP client go in `test/cmd_lsp_client.test.js`
- Must NOT require Adams View — follow the pure unit test pattern from `cmd_completion_provider.test.js`
- Use Mocha `suite()` / `test()` (not `describe()` / `it()`)
- Test: module exports, setting respect, graceful failure when Python LSP not installed

## Implementation Phases

1. **Phase 0:** Schema generation (`scripts/generate_command_schema.py`)
2. **Phase 1:** Core library (diagnostics, parser, schema, symbols, rules, linter)
3. **Phase 2:** CLI linter (`cli.py`)
4. **Phase 3:** LSP server (`server.py`)
5. **Phase 4:** VS Code integration (`cmd_lsp_client.ts.js` + extension wiring)
6. **Phase 5:** Testing (all `test_*.py` files + `cmd_lsp_client.test.js`)

Implement sequentially — each phase builds on the previous. The full plan has detailed pseudocode for every module.

## Common Pitfalls

- **pygls version:** Always use 2.x imports (`from pygls.lsp.server import LanguageServer`). 1.x imports will fail.
- **Abbreviation matching:** Without this, every abbreviated command gets flagged as E001, making the linter unusable. This is a core feature, not optional.
- **`commands.exp` never committed:** It's a closed-source Adams file. Only the generated `command_schema.json` is committed.
- **Continuation line positions:** When joining `&` lines, the character-to-line/column mapping must be maintained for accurate diagnostic positions.
- **Control flow is not in schema:** `if`/`else`/`end`/`for`/`while` are built-in, not Adams commands. Don't validate them against the command schema.
- **Exclusive group suppression:** Required args in mutual exclusion groups must not be flagged as missing when a sibling member is provided.

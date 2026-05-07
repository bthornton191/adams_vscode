# Adams CMD Language Server — Implementation Plan

## Purpose of This Document

This is the original design document for the Adams CMD Language Server (LSP) and CLI linter. **All phases (0–5) are fully implemented.** The package has 139 passing tests.

> **Note:** This document was written before implementation and served as the blueprint. Some details have diverged from the original plan during implementation — notably the `pyproject.toml` build-backend, `bundled/tool/lsp_server.py` entry point, and single-quoted string handling in the parser. These differences are noted inline with `[UPDATED]` markers. For the current working reference, see `.agents/skills/adams-cmd-lsp-builder/SKILL.md`.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture](#2-architecture)
3. [The Adams CMD Language](#3-the-adams-cmd-language)
4. [Data Sources & Formats](#4-data-sources--formats)
5. [Phase 0: Schema Generation](#5-phase-0-schema-generation)
6. [Phase 1: Core Library](#6-phase-1-core-library)
7. [Phase 2: CLI Linter](#7-phase-2-cli-linter)
8. [Phase 3: LSP Server](#8-phase-3-lsp-server)
9. [Phase 4: VS Code Integration](#9-phase-4-vs-code-integration)
10. [Phase 5: Testing](#10-phase-5-testing)
11. [Verification Checklist](#11-verification-checklist)
12. [Design Decisions & Rationale](#12-design-decisions--rationale)
13. [Future Considerations](#13-future-considerations)

---

## 1. Project Overview

### What

Build a Python package (`adams-cmd-lsp`) that provides:
1. **An LSP server** for real-time diagnostics (squiggly underlines) in any LSP-capable editor (VS Code, Claude Code, Neovim, Zed, OpenCode, etc.)
2. **A CLI linter** (`adams-cmd-lint`) for batch checking from the command line, CI pipelines, and non-LSP agent harnesses

Both share the same core library — the CLI and LSP are thin wrappers around the same parser, schema, and rule engine.

### Why

- AI coding agents (Claude Code, OpenCode, etc.) writing Adams CMD files currently get no feedback about mistakes until runtime in Adams View
- The existing VS Code extension has completions and hover but **zero diagnostics** — no `DiagnosticCollection`, no `createDiagnostic`, no `DiagnosticSeverity` usage anywhere
- The LSP protocol makes diagnostics available to ALL editors, not just VS Code

### Where It Lives

Start as a subdirectory `adams-cmd-lsp/` inside the existing `adams_vscode` repo. Extract to its own repo when stable.

### Prerequisites

- Python 3.9+ (the VS Code extension already requires `ms-python.python` as an `extensionDependency`)
- `pygls>=2.0` and `lsprotocol` for the LSP server
- Access to `commands.exp` (and optionally `language.src`) from the Adams source tree (for one-time schema generation only — the generated schema is committed to the repo)

### Proprietary Data Protection

> **CRITICAL: `commands.exp` and `language.src` are from the closed-source Adams
> repository. They must NEVER be committed to this open-source repo.**

- `commands.exp`, `language.src`, `commands.more` — these are proprietary Adams
  source files located in `../hexagon/Adams/source/`. They are only read by the
  schema generator script at development time. They must not be copied into this
  repo, committed to git, or included in any published package.
- `command_schema.json` — the generated schema is a derived work containing
  command names, argument names, types, and structural metadata. This is likely
  safe to commit (similar to how `structured.json` and `argument_options.json`
  are already committed), but **must be reviewed carefully before the first
  commit** to ensure it does not contain proprietary information beyond what is
  already publicly documented.
- Add `commands.exp`, `language.src`, and `commands.more` to `.gitignore` as a
  safety net in case they are accidentally copied into the repo.
- The schema generator script should print a reminder: "Review
  command_schema.json before committing — do not commit proprietary data."

---

## 2. Architecture

### Directory Structure

```
adams_vscode/                              (existing repo root)
├── adams-cmd-lsp/                         (NEW — Python package subdirectory)
│   ├── pyproject.toml                     (package config with entry points)
│   ├── adams_cmd_lsp/                     (Python package)
│   │   ├── __init__.py
│   │   ├── __main__.py                    (python -m adams_cmd_lsp entry point → starts LSP server)
│   │   ├── parser.py                      (tokenize .cmd text → Statement objects)
│   │   ├── schema.py                      (load & query command_schema.json)
│   │   ├── rules.py                       (all lint rules: structural, syntax, semantic)
│   │   ├── symbols.py                     (single-file symbol table for semantic checks)
│   │   ├── linter.py                      (orchestrator: parse → symbols → rules → Diagnostics)
│   │   ├── diagnostics.py                 (Diagnostic dataclass)
│   │   ├── server.py                      (pygls LSP server wrapper, ~200-300 lines)
│   │   ├── cli.py                         (adams-cmd-lint CLI entry point)
│   │   └── data/
│   │       └── command_schema.json        (generated from commands.exp + language.src, checked into repo — review before committing)
│   └── tests/
│       ├── test_parser.py
│       ├── test_schema.py
│       ├── test_rules.py
│       ├── test_symbols.py
│       ├── test_linter.py
│       ├── test_cli.py
│       ├── test_server.py
│       └── fixtures/                      (test .cmd files)
│
├── scripts/
│   └── generate_command_schema.py         (NEW — parse commands.exp + language.src → command_schema.json)
│
├── bundled/                               (NEW — Python runtime dependencies)
│   ├── tool/
│   │   └── lsp_server.py                  (NEW — bootstraps sys.path, runs adams_cmd_lsp.server.main())
│   └── libs/                              (gitignored — populated by `npm run bundle-lsp`)
│
├── src/
│   ├── cmd_lsp_client.ts.js               (NEW — VS Code LSP client wrapper)
│   ├── extension.ts.js                    (MODIFY — wire in LSP client)
│   ├── cmd_completion_provider.ts.js      (UNCHANGED — existing completions)
│   ├── cmd_hover_provider.ts.js           (UNCHANGED — existing hover)
│   └── ...
│
├── package.json                           (MODIFY — add vscode-languageclient dep, settings)
└── ...
```

### Data Flow

```
commands.exp (Adams source, external — primary)
language.src (Adams source, external — exclusive groups only)
      │
      ▼  [one-time, scripts/generate_command_schema.py]
command_schema.json (committed to repo)
      │  Contains: commands, args, types, required flags,
      │  exclusive groups, abbreviation prefixes, command tree
      │
      ▼  [loaded at startup by both LSP and CLI]
┌─────────────────────────────────────┐
│         Core Library (Python)        │
│  parser.py → symbols.py → rules.py  │
│            linter.py                 │
└────────────┬────────────┬───────────┘
             │            │
      ┌──────┘            └──────┐
      ▼                          ▼
  server.py                   cli.py
  (LSP, stdio)            (adams-cmd-lint)
      │
      ▼
  cmd_lsp_client.ts.js
  (VS Code extension)
```

---

## 3. The Adams CMD Language

### Overview

Adams CMD is the command language for MSC Adams View, a multi-body dynamics simulation tool. It's used to create models, define parts, markers, forces, constraints, and run analyses.

### Syntax Rules

**Commands are multi-word keywords followed by argument=value pairs:**
```
part create rigid_body name_and_position  &
    part_name = .model.PART_1  &
    adams_id = 1  &
    location = 0.0, 0.0, 0.0
```

**Key syntax elements:**
- `&` at end of line = continuation (command spans multiple lines)
- `!` to end of line = comment
- Arguments are `name=value` or `name = value` (whitespace around `=` is allowed)
- Values can be:
  - Bare words: `part_name=my_part`
  - Quoted strings: `title="My Model"`
  - Parenthesized expressions: `location=(eval(1+2)), 0, 0`
  - Comma-separated lists: `values=1.0, 2.0, 3.0`
  - Nested parentheses: `function=step(time, 0, 0, 1, 100)`
- Object names use dot-separated paths: `.model.PART_1.MARKER_1`
- Variables use `$` prefix: `$my_variable`
- `eval()` wraps runtime expressions
- Control flow: `if`/`else`/`end`, `for`/`end`, `while`/`end`, `variable` commands

**Example valid CMD file:**
```cmd
! Create a simple model
model create model_name=my_model

part create rigid_body name_and_position  &
    part_name = .my_model.PART_1  &
    location = 0.0, 0.0, 0.0

marker create  &
    marker_name = .my_model.PART_1.MARKER_1  &
    location = 1.0, 0.0, 0.0

! Conditional logic
if condition = (DB_EXISTS(".my_model.PART_2"))
    variable set variable_name = found string = "yes"
else
    variable set variable_name = found string = "no"
end
```

**Example CMD with errors:**
```cmd
xyz create marker_name = .model.MAR1     ! "xyz" is not a valid command (no abbreviation match)
part create rigid_body name_and_position &
    part_name = .model.PART1 &
    part_name = .model.PART2             ! duplicate argument
    location = (eval(abs()))             ! unbalanced parentheses: ()))
```

---

## 4. Data Sources & Formats

### 4.1. `language.src` — Master Command DSL (External, Secondary)

**Location:** `../hexagon/Adams/source/aview/src/cmd_language/language.src`

This is the master command definition file for Adams View, ~15,500 lines of a custom DSL (Domain-Specific Language). It defines every command, every argument, types, required/optional flags, mutual exclusion groups, and defaults. This file is **NOT** part of the adams_vscode repo — it lives in the Adams source tree.

**Role in schema generation:** `language.src` is used ONLY to extract mutual exclusion groups (`{...}` blocks), which are not preserved in `commands.exp`. All other schema data (command keys, argument names, types, required flags, defaults) comes from `commands.exp`.

### 4.1b. `commands.exp` — Fully Expanded Commands (External, Primary)

**Location:** `../hexagon/Adams/source/aview/src/cmd_language/commands.exp`

~11,189 lines. Based on the file name and contents, this appears to be the expanded/preprocessed output of `language.src` — all macros are inlined, dispatch trees are flattened, and `?suffix` hints are stripped. (This inference is from examining the file's structure, not from running `lang_to_tables.exe`.) Each command key appears on a line starting with one space, followed by indented argument definitions with `name=TYPE`, `name=TYPE*` (required), or `name=TYPE=default`.

**This is the primary input for schema generation** because:
- No macro expansion needed — everything is already inlined
- No dispatch tree walking needed — command keys are already flattened
- `*` required markers are preserved
- Types and defaults are preserved
- `?suffix` hints are already stripped (clean argument names)

**What it lacks:** Mutual exclusion groups (`{...}` blocks) — these must come from `language.src`.

### 4.1c. `commands.more` — Tree-Indented Hierarchy (External, Reference Only)

**Location:** `../hexagon/Adams/source/aview/src/cmd_language/commands.more`

~9,480 lines. Shows command hierarchy in a tree-indented format with argument types. Useful as a human-readable reference but not used for schema generation — it lacks `*` required markers and default values.

#### DSL Syntax Reference

> **Note:** This reference documents the full `language.src` DSL for understanding
> the source material. However, the schema generator only parses `language.src`
> for `{...}` mutual exclusion blocks. All other data (command keys, arguments,
> types, required flags, defaults) is extracted from `commands.exp`, which has
> these already expanded and flattened.

| Syntax | Meaning | Example |
|--------|---------|---------|
| `#name ... ;` | Macro definition (semicolon-terminated) | `#model_create ... ;` |
| `@name` | Macro reference (expanded inline) | `@ADAMS_ID_CREATE` |
| `<func_name>` | C handler function | `<cmd_model_create>` |
| `arg=TYPE*` | **Required** argument | `model_name=NDBWD_MECHANISM*` |
| `arg=TYPE` | **Optional** argument (no default) | `comments=STRING(0)` |
| `arg=TYPE=default` | **Optional** with default value | `fit_to_view=BOOLEAN=yes` |
| `TYPE(0)` | Array: 0 or more values | `comments=STRING(0)` |
| `TYPE(n,m)` | Exactly n to m values | `along_axis_orientation=LOCATION(1,2)` |
| `TYPE(GT,low,LT,high)` | Value range constraint | `INT(GT,0,UNLIMITED,0)` |
| `NDBWD_X` / `NDB_X` | Creates a **new** database object of type X | `NDBWD_MARKER` |
| `DB_X` | References an **existing** database object | `DB_MARKER` |
| `{...}` | Mutually exclusive group (nested `{}` for sub-groups) | See examples below |
| `[...\|...]` | Select-one alternative groups | Used for command dispatch |
| `?suffix` | Help file suffix hint — **strip for linting** | `marker_name?cre=...` → arg name is `marker_name` |
| `:M` | Menu-only (no command line) — skip for linting | `:M preprocessing @preprocessing;` |
| `:D` | Debug-only — skip for linting | |
| `:N` | No menu/panel field | |
| `:V` | No vvar button | |
| `:X` | No marker button | |
| `:E` | Expert mode panel field | |
| `:F` | Add FUNCTION OVERVIEW button | |
| `:L` | Add LOAD button | |

#### Concrete Examples from language.src

**Simple command (model create):**
```
#model_create
  <cmd_model_create>
  model_name?cre=NDBWD_MECHANISM*
  comments=STRING(0)
  title?mod=STRING
  view_name?mo=DB_VIEW(0)=DYN_DB
  fit_to_view=BOOLEAN=yes;
```

Parsing this:
- Handler: `cmd_model_create`
- `model_name?cre=NDBWD_MECHANISM*` → arg name `model_name` (strip `?cre`), type `new_object`, object_type `MECHANISM` (strip `NDBWD_` prefix), **required** (has `*`)
- `comments=STRING(0)` → arg name `comments`, type `string`, array (has `(0)`), optional
- `title?mod=STRING` → arg name `title`, type `string`, optional
- `view_name?mo=DB_VIEW(0)=DYN_DB` → arg name `view_name`, type `existing_object`, object_type `VIEW`, array, default `DYN_DB`, optional
- `fit_to_view=BOOLEAN=yes` → arg name `fit_to_view`, type `boolean`, default `yes`, optional

**Command with mutual exclusion (marker create):**
```
#marker_create
  <cmd_marker_create>
  marker_name?cre=NDBWD_MARKER*
  @ADAMS_ID_CREATE
  comments=STRING(0)
  location?cs=LOCATION
  {node_id=INT(0)
   preserve_location=TRUE_ONLY
  }
  {orientation?cs=ORIENTATION=0,0,0
   along_axis_orientation=LOCATION(1,2)
   in_plane_orientation=LOCATION(2,3)
   natural_coordinates_relative_orientation=ORIENTATION}
  curve_name=DB_ACURVE
  reference_marker_name=DB_MARKER
  {{TANGENT
    velocity=VELOCITY
   }
   {VECTOR
    vx=VELOCITY
    vy=VELOCITY
    vz=VELOCITY
  }}
  relative_to=DB_RFRAME=DYN_CS
  offset=LOCATION;
```

Parsing this:
- `marker_name?cre=NDBWD_MARKER*` → required, new_object Marker
- `@ADAMS_ID_CREATE` → expands to `adams_id=ADAMS_ID` (optional) — this macro is NOT defined in language.src, it's built into `lang_to_tables.exe`
- First `{...}` block → exclusive group 1: `node_id` and `preserve_location` are mutually exclusive
- Second `{...}` block → exclusive group 2: `orientation`, `along_axis_orientation`, `in_plane_orientation`, and `natural_coordinates_relative_orientation` are mutually exclusive
- Third `{{...}{...}}` → nested exclusive group 3: TANGENT group (`velocity`) vs VECTOR group (`vx`, `vy`, `vz`). The ALL-CAPS words `TANGENT` and `VECTOR` are labels for user-facing menus, not arguments — they have no `=` sign.

**Command with constrained integers:**
```
#model_attributes
  <cmd_model_attributes>
  model_name?mod=DB_MECHANISM(0)=DYN_DB
  {scale_of_icons=REAL(GT,0,UNLIMITED,0)
   size_of_icons=LENGTH(GE,0,UNLIMITED,0)}
  visibility?tog=ON_OFF_WITH_TOGGLE
  name_visibility=ON_OFF_WITH_TOGGLE
  transparency=INT(GT,-1,LT,101)
  lod=INT(GE,1,LE,100)
  color?nc=DB_COLOR
  entity_scope=COLOR_SCOPE;
```

Constraint syntax: `TYPE(bound_type, bound_val, bound_type, bound_val)` where:
- `GT` = greater than, `GE` = greater than or equal
- `LT` = less than, `LE` = less than or equal
- `UNLIMITED` = no bound on that side
- Example: `INT(GT,-1,LT,101)` means integer in range (-1, 101) exclusive = 0 to 100

#### Built-in Macros (Not in language.src — Reference Only)

> **Note:** Since the schema generator uses `commands.exp` (which has all macros
> already expanded), these built-in macros do NOT need to be hardcoded in the
> generator. This section is retained as reference material for understanding the
> `language.src` DSL.

These macros are referenced with `@` in language.src but their definitions are built into the `lang_to_tables.exe` preprocessor:

| Macro | Expands To | Source |
|-------|-----------|--------|
| `@ADAMS_ID_CREATE` | `adams_id=ADAMS_ID` (optional) | Verified from `commands.more` output |
| `@ADAMS_ID_MODIFY` | `adams_id=ADAMS_ID` (optional) | Verified from `commands.more` output |
| `@list_info_file` | `write_to_terminal=ON_OFF` + `file_name=FILE` | Verified from `commands.more` output |
| `@ANGLE` | `angle=ANGLE` (likely) | Inferred; verify against `commands.more` |

If parsing `language.src` for exclusive groups and encountering an unknown macro reference `@FOO`:
1. It can be safely ignored — the exclusive group parser only needs `{` `}` blocks and argument names within them
2. All argument data comes from `commands.exp`, not from macro expansion

#### Command Hierarchy / Dispatch

At the top level, language.src uses `[...|...]` blocks for dispatching to sub-macros:

```
#model [  create?mod        @model_create     |
       :L modify?mod        @model_modify     |
          delete?mod        @model_delete     |
          ...               ];
```

This defines the tree: `model` → `create` dispatches to `#model_create`, `model` → `modify` dispatches to `#model_modify`, etc.

The flattened command key is built by concatenating the hierarchy: `model create`, `model modify`, `model delete`, etc. The `?mod`, `?del`, `?cre` suffixes on keywords are help hints — strip them.

#### The `?suffix` Pattern

Both argument names AND keyword names can have `?suffix` appended:
- `marker_name?cre=NDBWD_MARKER*` → argument name is `marker_name` (strip `?cre`)
- `create?mod` → keyword is `create` (strip `?mod`)

The `?suffix` is a help file naming hint: `create?mod` means the help file is `create_mod.help`. The schema generator must strip everything from `?` to `=` (for args) or `?` to whitespace/end (for keywords).

### 4.2. `structured.json` — Existing Command→Arguments Map

**Location:** `resources/adams_view_commands/structured.json` (in this repo)

~10,000 lines. Maps each command key to an array of valid argument names.

```json
{
  "part create rigid_body name_and_position": [
    "part_name", "ground_part", "adams_id", "comments", "location",
    "orientation", "relative_to", "vm", "wm", "vx", "vy", "vz",
    "wx", "wy", "wz", "exact_coordinates", "ip_xx", "ip_yy", ...
  ],
  "model create": ["model_name", "type", "comments"],
  ...
}
```

**~550+ command keys.** Use this to **cross-reference and validate** the generated schema — every command in structured.json should appear in command_schema.json, and vice versa.

### 4.3. `argument_options.json` — Enum Values

**Location:** `resources/adams_view_commands/argument_options.json` (in this repo)

~10,000 lines. For arguments that accept enumerated values, maps command → argument → valid values.

```json
{
  "animation create": {
    "configuration": ["model_input", "equilibrium", "contact", "forward", "backward"],
    "static_frames": ["yes", "no"],
    "show_time_decay": ["yes", "no"]
  },
  "model merge": {
    "duplicate_parts": ["merge", "omit", "rename", "error"]
  },
  ...
}
```

**Important:** Merge these enum values into `command_schema.json` during schema generation. The schema should have `"enum_values": [...]` on arguments that have enum options. These values come from the `LUP_TABLE` lookups in the Adams parser, and the existing `argument_options.json` captures them already.

### 4.4. `command_docs/` — Markdown Documentation

**Location:** `resources/adams_view_commands/command_docs/` (in this repo)

~996 markdown files, one per command. Filename uses underscores: `part_create_rigid_body_name_and_position.md`. Contains parameter tables, descriptions, and examples.

**NOT the source of truth for required/optional** — these docs have inconsistent marking. They're useful for hover documentation but should NOT be parsed for schema data.

### 4.5. `parse_types.h` — Adams Parser C Definitions (External Reference)

**Location:** `C:\Users\ben.thornton\code\hexagon\Adams\source\aview\src\cmd_parser\parse_types.h`

This file is a reference for understanding type systems and constraint types. You don't need to parse it — it just explains the semantics. Key definitions:

**P_TYPE enum (40+ argument types):**
- Scalars: `PAR_T_INT`, `PAR_T_REAL`, `PAR_T_STRING`, `PAR_T_ENT`
- Database: `PAR_T_IN_DBASE` (existing object), `PAR_T_NOT_IN_DBASE` (new object), `PAR_T_MAY_BE_IN_DBASE`
- Physical: `PAR_T_ANGLE`, `PAR_T_MASS`, `PAR_T_LENGTH`, `PAR_T_TIME`, `PAR_T_FORCE`, `PAR_T_VELOCITY`, `PAR_T_ACCELERATION`, `PAR_T_ANGULAR_VEL`, `PAR_T_ANGULAR_ACCEL`, `PAR_T_STIFFNESS`, `PAR_T_DAMPING`, `PAR_T_TORQUE`, `PAR_T_PRESSURE`
- Geometry: `PAR_T_POINT`, `PAR_T_ORIENT`, `PAR_T_SCREEN_COORDS`
- Enums: `PAR_T_IN_TABLE`, `PAR_T_NOT_IN_TABLE`
- Special: `PAR_T_FUNCTION`, `PAR_T_ADAMS_ID`

**PAR_DEF_TYPE enum:**
- `PAR_D_OPTIONAL` — can be omitted
- `PAR_D_REQUIRED` — must be provided (maps to `*` in language.src)
- `PAR_D_CONSTANT` — has constant default
- `PAR_D_UPDATE` — default can be overridden
- `PAR_D_DYNAMIC` — default computed at runtime

**VAL_RANGE struct:**
```c
typedef struct {
    double upper;        // Upper bound value
    double lower;        // Lower bound value
    BOUND_TYPE upper_type; // GT, GE, LT, LE, or UNLIMITED
    BOUND_TYPE lower_type;
} VAL_RANGE;
```

---

## 5. Phase 0: Schema Generation

### Goal

Parse `commands.exp` → produce `command_schema.json` that captures the full richness of command definitions, including argument types, required flags, defaults, and minimum abbreviation prefixes for both commands and arguments.

### Why `commands.exp` Instead of `language.src`

Three data files exist in the Adams source tree (`../hexagon/Adams/source/aview/src/cmd_language/`):

| File | Lines | Contents | Pros | Cons |
|------|-------|----------|------|------|
| `language.src` | 15,568 | Master DSL (Domain-Specific Language) with macros, dispatch trees, mutual exclusion groups | Has `{...}` exclusion groups | Requires full DSL parser with macro expansion |
| `commands.exp` | 11,189 | Fully expanded output: flattened command keys, `*` required markers, `=default` values, clean arg names | Already expanded — no macro/dispatch parsing needed; has types and required markers | Does NOT have mutual exclusion groups |
| `commands.more` | 9,480 | Tree-indented hierarchy with types | Shows hierarchy | No `*` markers, no defaults |

**`commands.exp` is the primary input** because it's already fully expanded — all macros are inlined, dispatch trees are flattened, and `?suffix` hints are stripped. This eliminates the need for a complex DSL parser with macro expansion, dispatch tree walking, and recursion depth limits.

**`language.src` is a secondary input** used ONLY to extract mutual exclusion groups (`{...}` blocks), which `commands.exp` does not preserve.

### Data Files

- **Primary:** `../hexagon/Adams/source/aview/src/cmd_language/commands.exp`
- **Secondary:** `../hexagon/Adams/source/aview/src/cmd_language/language.src` (for exclusive groups only)
- **Merge:** `resources/adams_view_commands/argument_options.json` (enum values)
- **Validate:** `resources/adams_view_commands/structured.json` (cross-reference)

### File: `scripts/generate_command_schema.py`

This is a standalone script the developer runs once (or whenever `commands.exp` changes). It reads the data files and outputs JSON.

**Usage:**
```
python scripts/generate_command_schema.py \
    --input "../hexagon/Adams/source/aview/src/cmd_language/commands.exp" \
    --language-src "../hexagon/Adams/source/aview/src/cmd_language/language.src" \
    --arg-options "resources/adams_view_commands/argument_options.json" \
    --output "adams-cmd-lsp/adams_cmd_lsp/data/command_schema.json" \
    --validate "resources/adams_view_commands/structured.json"
```

### `commands.exp` Format

Each command starts with its flattened key on a line beginning with a space, followed by indented argument definitions:

```
 model create
   model_name=NDBWD_MECHANISM*
   comments=STRING(0)
   title=STRING
   view_name=DB_VIEW(0)=DYN_DB
   fit_to_view=BOOLEAN=yes
 model modify
   model_name=DB_MECHANISM(0)=DYN_DB
   comments=STRING(0)
   ...
```

Key format rules:
- Command key lines start with exactly one leading space
- Argument lines are indented further (3+ spaces)
- Argument format: `name=TYPE`, `name=TYPE*` (required), `name=TYPE=default`
- `TYPE(0)` = array, `TYPE(n,m)` = n-to-m values, `TYPE(GT,lo,LT,hi)` = range constraint
- `NDBWD_X` / `NDB_X` = new object, `DB_X` = existing object
- `?suffix` patterns are already stripped in `commands.exp` (unlike `language.src`)

### Parsing Algorithm

#### Step 1: Parse `commands.exp`

```python
def parse_commands_exp(text):
    """Parse commands.exp into a dict of command_key → {args: {...}}."""
    commands = {}
    current_cmd = None

    for line in text.splitlines():
        if not line.strip():
            continue

        # Command key line: starts with exactly 1 space, then non-space
        if line.startswith(' ') and not line.startswith('   ') and line.strip():
            current_cmd = line.strip().lower()
            commands[current_cmd] = {"args": {}}
            continue

        # Argument line: indented further, has name=TYPE pattern
        if current_cmd and '=' in line:
            arg_text = line.strip()
            name, type_spec = parse_argument_line(arg_text)
            if name:
                commands[current_cmd]["args"][name] = type_spec

    return commands
```

#### Step 2: Parse Each Argument Line

```python
def parse_argument_line(text):
    """Parse 'name=TYPE*', 'name=TYPE=default', 'name=TYPE(0)', etc.

    Returns (name, spec_dict) or (None, None) for unparseable lines.
    """
    # Split on first '='
    eq_pos = text.index('=')
    name = text[:eq_pos].strip()

    # Strip ?suffix from name if present (should already be stripped in .exp, but be safe)
    if '?' in name:
        name = name[:name.index('?')]

    remainder = text[eq_pos + 1:]

    # Check for required marker (trailing *)
    required = remainder.rstrip().endswith('*')
    if required:
        remainder = remainder.rstrip()[:-1]

    # Check for default value (second = after type)
    default = None
    type_part = remainder
    # Need careful parsing: TYPE=default vs TYPE(n,m)=default
    # Find the type token boundary, then check for =default after it
    type_token, array_spec, range_spec, default = parse_type_and_modifiers(type_part)

    spec = classify_type(type_token)
    spec["required"] = required

    if array_spec is not None:
        spec["array"] = True
        if array_spec.get("min") is not None:
            spec["min_values"] = array_spec["min"]
        if array_spec.get("max") is not None:
            spec["max_values"] = array_spec["max"]

    if range_spec:
        spec["range"] = range_spec

    if default is not None:
        spec["default"] = default

    return name, spec
```

**Type classification helper** (used by `parse_argument_line`):

```python
def classify_type(type_token):
    """Classify a type token from commands.exp into a schema type."""
    if type_token.startswith("NDBWD_") or type_token.startswith("NDB_"):
        prefix = "NDBWD_" if type_token.startswith("NDBWD_") else "NDB_"
        return {"type": "new_object", "object_type": type_token[len(prefix):], "db_type": type_token}
    elif type_token.startswith("DB_"):
        return {"type": "existing_object", "object_type": type_token[3:], "db_type": type_token}
    elif type_token == "INT":
        return {"type": "integer"}
    elif type_token in ("REAL", "LENGTH", "MASS", "TIME", "FORCE", "VELOCITY",
                        "ACCELERATION", "ANGULAR_VEL", "ANGULAR_ACCEL",
                        "STIFFNESS", "DAMPING", "TORQUE", "PRESSURE",
                        "INERTIA", "DENSITY", "AREA", "VOLUME"):
        return {"type": "real", "unit": type_token.lower()}
    elif type_token == "LOCATION":
        return {"type": "location"}
    elif type_token == "ORIENTATION":
        return {"type": "orientation"}
    elif type_token in ("BOOLEAN", "ON_OFF", "ON_OFF_WITH_TOGGLE", "TRUE_ONLY"):
        return {"type": "boolean"}
    elif type_token in ("STRING", "FILE"):
        return {"type": "string"}
    elif type_token == "FUNCTION":
        return {"type": "function"}
    elif type_token == "ADAMS_ID":
        return {"type": "adams_id"}
    elif type_token == "ANGLE":
        return {"type": "real", "unit": "angle"}
    else:
        # Unknown type — store raw for debugging
        return {"type": "unknown", "raw_type": type_token}
```

#### Step 3: Extract Exclusive Groups from `language.src`

Parse `language.src` ONLY for `{...}` mutual exclusion blocks. This is a targeted extraction — we don't need to parse macros, dispatch trees, or expand `@references`. We just need to:

1. Find each macro definition (`#name ... ;`)
2. Within each macro body, scan for `{...}` blocks
3. Extract the argument names inside each block (lines matching `name=...`)
4. Map the macro name back to the flattened command key

```python
def extract_exclusive_groups(language_src_text, command_keys):
    """Extract {mutual exclusion} groups from language.src.

    Returns dict of command_key → list of {"group": N, "members": [...]}
    """
    # Parse macro bodies from language.src
    macros = parse_macro_bodies(language_src_text)

    groups_by_cmd = {}
    for macro_name, body in macros.items():
        # Map macro name to command key (e.g., "marker_create" → "marker create")
        cmd_key = macro_name_to_command_key(macro_name, command_keys)
        if not cmd_key:
            continue

        groups = parse_exclusion_blocks(body)
        if groups:
            groups_by_cmd[cmd_key] = groups

    return groups_by_cmd
```

The `parse_exclusion_blocks` function scans for `{` ... `}` blocks, extracts argument names (lines with `=`), and assigns incrementing group IDs. Nested `{{...}{...}}` creates sub-groups. ALL-CAPS words without `=` are menu labels and should be ignored.

#### Step 4: Compute Minimum Abbreviation Prefixes

Adams uses **shortest unique prefix matching** at runtime. Given siblings `["marker", "mass", "material"]`, the minimum prefixes are `"mar"`, `"mas"`, `"mat"` — each must be long enough to be unambiguous among its siblings.

This computation must happen at two levels:
1. **Command keyword level:** Each token in the command hierarchy has siblings (e.g., under `part create`, the sub-keywords `rigid_body`, `rigid_body_mass_properties`, etc.)
2. **Argument name level:** Each argument within a command has siblings (all other argument names for the same command)

```python
def compute_min_prefixes(names):
    """Compute the minimum unique prefix for each name among its siblings.

    Args:
        names: list of sibling names (case-insensitive comparison)

    Returns:
        dict of name → min_prefix_length

    Algorithm:
        For each name, find the shortest prefix that uniquely identifies it
        among all siblings. An exact match always takes priority over prefix
        match (handled at match time, not here).
    """
    lower_names = [n.lower() for n in names]
    result = {}

    for i, name in enumerate(lower_names):
        # Start with prefix length 1, increase until unique
        for prefix_len in range(1, len(name) + 1):
            prefix = name[:prefix_len]
            # Count how many siblings share this prefix
            matches = sum(1 for j, other in enumerate(lower_names)
                         if j != i and other.startswith(prefix))
            if matches == 0:
                result[names[i]] = prefix_len
                break
        else:
            # Full name required (no shorter prefix is unique)
            result[names[i]] = len(name)

    return result
```

The computed minimum prefix lengths are stored in the schema:
- For commands: a `"min_prefix"` field per keyword token in a separate `"command_tree"` section
- For arguments: a `"min_prefix"` field on each argument definition

#### Step 5: Build the Command Tree for Abbreviation Matching

In addition to the flat command→args map, build a hierarchical command tree that enables prefix matching during linting:

```python
def build_command_tree(command_keys):
    """Build a hierarchical tree from flat command keys.

    Input: ["model create", "model modify", "model delete", "marker create", ...]
    Output: {
        "children": {
            "model": {"min_prefix": 3, "children": {
                "create": {"min_prefix": 1, "children": {}, "is_leaf": True},
                "modify": {"min_prefix": 1, "children": {}, "is_leaf": True},
                ...
            }},
            "marker": {"min_prefix": 3, "children": {...}},
            ...
        }
    }

    At each level, compute min_prefix among siblings using compute_min_prefixes().
    """
    tree = {"children": {}}

    for key in command_keys:
        tokens = key.split()
        node = tree
        for token in tokens:
            if token not in node["children"]:
                node["children"][token] = {"children": {}}
            node = node["children"][token]
        node["is_leaf"] = True

    # Now compute min_prefix at each level
    def annotate_prefixes(node):
        if node["children"]:
            siblings = list(node["children"].keys())
            prefixes = compute_min_prefixes(siblings)
            for name, min_len in prefixes.items():
                node["children"][name]["min_prefix"] = min_len
            for child in node["children"].values():
                annotate_prefixes(child)

    annotate_prefixes(tree)
    return tree
```

#### Step 6: Merge Enum Values

Load `argument_options.json` and merge valid enum values into the schema:
```python
for cmd_key, arg_opts in arg_options.items():
    if cmd_key in schema:
        for arg_name, values in arg_opts.items():
            if arg_name in schema[cmd_key]["args"]:
                schema[cmd_key]["args"][arg_name]["enum_values"] = values
```

#### Step 7: Compute Argument Abbreviation Prefixes

For each command, compute minimum unique prefixes across all argument names:
```python
for cmd_key, cmd_data in schema.items():
    arg_names = list(cmd_data["args"].keys())
    if arg_names:
        prefixes = compute_min_prefixes(arg_names)
        for arg_name, min_len in prefixes.items():
            cmd_data["args"][arg_name]["min_prefix"] = min_len
```

#### Step 8: Validate Against structured.json

Load `structured.json` and check coverage:
```python
for cmd_key in structured_commands:
    if cmd_key not in schema:
        print(f"WARNING: {cmd_key} in structured.json but not in generated schema")
    else:
        for arg in structured_commands[cmd_key]:
            if arg not in schema[cmd_key]["args"]:
                print(f"WARNING: {cmd_key}.{arg} in structured.json but not in schema")
```

Also check the reverse — schema commands not in structured.json (may be debug-only or menu-only commands that were correctly skipped).

### Output: `command_schema.json` Format

```json
{
  "commands": {
    "model create": {
      "args": {
        "model_name": {
          "required": true,
          "type": "new_object",
          "object_type": "Mechanism",
          "db_type": "NDBWD_MECHANISM",
          "min_prefix": 1
        },
        "comments": {
          "required": false,
          "type": "string",
          "array": true,
          "min_prefix": 1
        },
        "title": {
          "required": false,
          "type": "string",
          "min_prefix": 1
        },
        "view_name": {
          "required": false,
          "type": "existing_object",
          "object_type": "View",
          "db_type": "DB_VIEW",
          "array": true,
          "default": "DYN_DB",
          "min_prefix": 1
        },
        "fit_to_view": {
          "required": false,
          "type": "boolean",
          "default": "yes",
          "min_prefix": 1
        }
      },
      "exclusive_groups": []
    },
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
        },
        "orientation": {
          "required": false,
          "type": "orientation",
          "default": "0,0,0",
          "min_prefix": 2
        },
        "offset": {
          "required": false,
          "type": "location",
          "min_prefix": 2
        }
      },
      "exclusive_groups": [
        {"group": 1, "members": ["node_id", "preserve_location"]},
        {"group": 2, "members": ["orientation", "along_axis_orientation", "in_plane_orientation", "natural_coordinates_relative_orientation"]},
        {"group": 3, "members": ["velocity", "vx"]}
      ]
    }
  },
  "command_tree": {
    "children": {
      "model": {
        "min_prefix": 3,
        "children": {
          "create": {"min_prefix": 1, "is_leaf": true},
          "modify": {"min_prefix": 1, "is_leaf": true},
          "delete": {"min_prefix": 1, "is_leaf": true}
        }
      },
      "marker": {
        "min_prefix": 3,
        "children": {
          "create": {"min_prefix": 1, "is_leaf": true},
          "modify": {"min_prefix": 1, "is_leaf": true}
        }
      }
    }
  }
}
```

---

## 6. Phase 1: Core Library

### 6.1. Project Scaffold

**File: `adams-cmd-lsp/pyproject.toml`**

> [UPDATED] The build-backend below has been corrected from the original plan.
> The original specified `setuptools.backends._legacy:_Backend`, which does not
> exist. The correct value is `setuptools.build_meta`. Additionally,
> `[tool.setuptools.package-data]` is required to include `data/*.json` in the
> installed package.

```toml
[build-system]
requires = ["setuptools>=64"]
build-backend = "setuptools.build_meta"

[project]
name = "adams-cmd-lsp"
version = "0.1.0"
description = "LSP server and CLI linter for MSC Adams CMD language"
requires-python = ">=3.9"
dependencies = ["pygls>=2.0", "lsprotocol"]

[project.optional-dependencies]
dev = ["pytest"]

[project.scripts]
adams-cmd-lint = "adams_cmd_lsp.cli:main"
adams-cmd-lsp = "adams_cmd_lsp.server:main"

[tool.setuptools.package-data]
adams_cmd_lsp = ["data/*.json"]
```

### 6.2. Diagnostics (`diagnostics.py`)

```python
from dataclasses import dataclass
from enum import Enum

class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

@dataclass
class Diagnostic:
    line: int           # 0-based line number
    column: int         # 0-based column
    end_line: int       # 0-based end line
    end_column: int     # 0-based end column
    code: str           # e.g. "E001", "W005"
    message: str        # human-readable message
    severity: Severity
```

### 6.3. Parser (`parser.py`)

This module tokenizes raw `.cmd` text into a list of `Statement` objects. It must be ported from the JavaScript parsing functions in `src/cmd_completion_provider.ts.js`.

#### Data Structures

```python
from dataclasses import dataclass, field

@dataclass
class Argument:
    name: str           # e.g. "marker_name"
    value: str          # e.g. ".model.PART_1.MAR_1" (raw text, not interpreted)
    name_line: int      # 0-based line of the argument name
    name_column: int    # 0-based column of the argument name
    value_line: int     # 0-based line of the value start
    value_column: int   # 0-based column of the value start

@dataclass
class Statement:
    command_key: str            # e.g. "marker create" (normalized, lowercase, as written by user)
    resolved_command_key: str   # canonical form after abbreviation resolution (e.g. "mar cre" → "marker create"), or None if unresolvable
    arguments: list[Argument]   # parsed arg=value pairs
    line_start: int             # 0-based first line of this statement
    line_end: int               # 0-based last line (inclusive)
    raw_text: str               # full raw text including continuations
    is_comment: bool            # True if the entire line is a comment
    is_blank: bool              # True if the line is blank
    is_control_flow: bool       # True for if/else/end/for/while
    control_flow_keyword: str   # "if", "else", "end", "for", "while", or None
```

#### Parsing Algorithm

**Top-level: `parse(text: str) -> list[Statement]`**

1. Split text into lines
2. Group continuation lines: walk forward, joining lines ending with `&` (stripping the `&` and optional trailing comment)
3. For each logical statement (may span multiple physical lines):
   a. Skip blank lines → emit `Statement(is_blank=True)`
   b. Skip comment-only lines (first non-whitespace is `!`) → emit `Statement(is_comment=True)`
   c. Check for control flow: first word is `if`/`else`/`end`/`for`/`while` → emit with `is_control_flow=True`

> **Concern D — Control Flow Edge Cases:** The control flow detection must handle:
> - `if condition = (expr)` — the `if` keyword followed by `condition=` argument
> - `end` alone on a line — closes the nearest `if`/`for`/`while` block
> - `else` alone on a line — flips the nearest `if` block
> - `for variable_name = ... to ... by ...` — loop with arguments
> - `while condition = (expr)` — loop with condition
> - Nested `if`/`for`/`while` blocks — maintain a stack for E104
> - `if`/`for`/`while` are NOT Adams commands in the schema — they're built-in
>   control flow keywords and should NOT be validated against the command schema
> - A common pitfall: `variable set variable_name = if_needed ...` — the `if`
>   here is part of a variable name, not a control flow keyword. Only treat the
>   FIRST token as a control flow keyword.
   d. Otherwise, parse as command+arguments

**Continuation line joining:**

> **Concern B — Line/Column Tracking:** When continuation lines are joined with
> `&`, the parser must maintain a mapping from character positions in the joined
> string back to the original (line, column) in the source file. This is critical
> for accurate diagnostic positions. The approach:
> 1. Build a `line_offsets` array: for each character position in the joined
>    string, record which physical line and column it maps to
> 2. When `&` and the newline are stripped, the gap in positions must be tracked
>    so subsequent characters map to the correct physical line
> 3. The `char_to_line_col(pos, line_offsets)` helper (used in argument
>    extraction) must use this mapping
> 4. Edge case: inline comments after `&` (e.g., `value & ! comment`) — the
>    comment is stripped, but the `&` position on the physical line must be
>    correctly tracked

```python
def group_continuation_lines(lines):
    """Group lines connected by & into logical statements.
    Returns list of (line_start, line_end, joined_text) tuples."""
    groups = []
    i = 0
    while i < len(lines):
        start = i
        parts = []
        while i < len(lines):
            line = lines[i]
            # Check if line ends with & (with optional trailing comment)
            match = re.match(r'^(.*?)&[ \t]*(!.*)?$', line)
            if match:
                parts.append(match.group(1).rstrip())
                i += 1
            else:
                parts.append(line)
                i += 1
                break
        groups.append((start, i - 1, " ".join(parts)))
    return groups
```

**Command key extraction (port of `strip_argument_pairs`):**

This is the trickiest part. The command key is everything that's NOT an `arg=value` pair.

```python
def extract_command_key(text):
    """Strip all arg=value pairs from text to isolate the command key.

    Port of strip_argument_pairs() from cmd_completion_provider.ts.js.

    Example: "part create rigid_body name_and_position part_name=.model.P1 location=0,0,0"
           → "part create rigid_body name_and_position"
    """
    result = ""
    i = 0
    while i < len(text):
        if text[i].isspace():
            ws_start = i
            while i < len(text) and text[i].isspace():
                i += 1
            # Check if next chars form word=
            m = re.match(r'(\w+\s*=\s*)', text[i:])
            if m:
                value_start = i + len(m.group(0))
                i = consume_argument_value(text, value_start)
                i = consume_comma_separated_tail(text, i, value_start)
            else:
                result += text[ws_start:i]
        else:
            result += text[i]
            i += 1
    return result.strip()
```

**Value consumption (port of `consume_argument_value`):**

> [UPDATED] The implementation also handles single-quoted strings (`'...'`), which
> the original plan omitted. Adams CMD uses single-quoted strings in contexts like
> `FUNCTION='...'` that can contain `!` characters (which are otherwise comment
> delimiters). The parser's `_find_comment_start()`, `_consume_argument_value()`,
> and `rule_unbalanced_parens()` all track single-quoted string boundaries to
> avoid false positives.

```python
def consume_argument_value(text, start):
    """Consume a single argument value starting at position start.

    Handles:
    - Quoted strings: "..." and '...'
    - Parenthesized expressions: (...) with nesting
    - Bare words: sequences of non-whitespace chars
    """
    if start >= len(text):
        return start

    ch = text[start]

    # Quoted string
    if ch == '"':
        i = start + 1
        while i < len(text) and text[i] != '"':
            i += 1
        return i + 1 if i < len(text) else i

    # Parenthesized expression (with nesting)
    if ch == '(':
        depth = 0
        i = start
        while i < len(text):
            if text[i] == '(':
                depth += 1
            elif text[i] == ')':
                depth -= 1
                if depth == 0:
                    return i + 1
            i += 1
        return i  # unclosed paren

    # Bare word
    i = start
    while i < len(text) and not text[i].isspace():
        i += 1
    return i
```

**Comma-separated tail (port of `consume_comma_separated_tail`):**
```python
def consume_comma_separated_tail(text, i, value_start):
    """After consuming a value, continue consuming comma-separated values.

    Handles: stiffness=1e6, 1e6, 1e6
    """
    while True:
        has_trailing_comma = i > value_start and text[i - 1] == ','
        has_following_comma = i < len(text) and text[i] == ','

        if has_trailing_comma or has_following_comma:
            next_pos = i
            if has_following_comma:
                next_pos += 1
            while next_pos < len(text) and text[next_pos].isspace():
                next_pos += 1

            if next_pos >= len(text):
                break
            # Stop if next token looks like a new arg=value pair
            if re.match(r'^\w+\s*=', text[next_pos:]):
                break

            i = consume_argument_value(text, next_pos)
        else:
            break
    return i
```

**Argument extraction (new — not in the JS code):**
```python
def extract_arguments(text, line_offsets):
    """Extract all arg=value pairs from statement text.

    Returns list of Argument objects with line/column positions.
    line_offsets maps character positions to (line, column) tuples.
    """
    arguments = []
    i = 0
    while i < len(text):
        # Look for word= pattern
        m = re.match(r'(\w+)\s*=\s*', text[i:])
        if m and (i == 0 or text[i-1].isspace()):
            name = m.group(1)
            name_pos = i
            value_start = i + len(m.group(0))
            value_end = consume_argument_value(text, value_start)
            value_end = consume_comma_separated_tail(text, value_end, value_start)
            value = text[value_start:value_end].strip()

            name_line, name_col = char_to_line_col(name_pos, line_offsets)
            val_line, val_col = char_to_line_col(value_start, line_offsets)

            arguments.append(Argument(
                name=name,
                value=value,
                name_line=name_line,
                name_column=name_col,
                value_line=val_line,
                value_column=val_col,
            ))
            i = value_end
        else:
            i += 1
    return arguments
```

### 6.4. Schema (`schema.py`)

```python
import json
from pathlib import Path

_DEFAULT_SCHEMA_PATH = Path(__file__).parent / "data" / "command_schema.json"

class Schema:
    def __init__(self, data):
        self._commands = data["commands"]
        self._tree = data.get("command_tree", {})

    @classmethod
    def load(cls, path=None):
        path = path or _DEFAULT_SCHEMA_PATH
        with open(path) as f:
            return cls(json.load(f))

    def has_command(self, key):
        return key in self._commands

    def get_command(self, key):
        return self._commands.get(key)

    def get_args(self, key):
        cmd = self._commands.get(key)
        return cmd["args"] if cmd else None

    def get_arg(self, cmd_key, arg_name):
        cmd = self._commands.get(cmd_key)
        if cmd:
            return cmd["args"].get(arg_name)
        return None

    def commands(self):
        return self._commands.keys()

    def get_exclusive_groups(self, cmd_key):
        cmd = self._commands.get(cmd_key)
        return cmd.get("exclusive_groups", []) if cmd else []

    def resolve_command_key(self, tokens):
        """Resolve a list of (possibly abbreviated) command tokens to a canonical key.

        Uses the command_tree to match abbreviated prefixes against siblings.
        Returns (canonical_key, error_token_index) — error_token_index is None
        on success, or the index of the first unresolvable token on failure.

        Matching rules (per Adams runtime behavior):
        - Case-insensitive
        - Exact match takes priority over prefix match
        - Prefix must be at least min_prefix chars long
        - Prefix must be unambiguous (match exactly one sibling)
        """
        node = self._tree
        resolved = []

        for i, token in enumerate(tokens):
            children = node.get("children", {})
            if not children:
                return None, i

            match = self._match_token(token, children)
            if match is None:
                return None, i

            resolved.append(match)
            node = children[match]

        key = " ".join(resolved)
        if key in self._commands:
            return key, None
        # Partial command (intermediate node, not a leaf)
        return None, len(tokens) - 1

    def _match_token(self, token, children):
        """Match a single token against sibling children.

        Returns the canonical name on match, None on failure.
        """
        token_lower = token.lower()

        # Exact match takes priority
        for name in children:
            if name.lower() == token_lower:
                return name

        # Prefix match — must be unambiguous
        matches = []
        for name, node_data in children.items():
            min_prefix = node_data.get("min_prefix", len(name))
            if (len(token_lower) >= min_prefix and
                    name.lower().startswith(token_lower)):
                matches.append(name)

        if len(matches) == 1:
            return matches[0]

        return None  # 0 matches or ambiguous

    def resolve_argument_name(self, cmd_key, arg_name):
        """Resolve a (possibly abbreviated) argument name to its canonical form.

        Returns canonical name on match, None on failure.
        """
        cmd = self._commands.get(cmd_key)
        if not cmd:
            return None

        args = cmd["args"]
        arg_lower = arg_name.lower()

        # Exact match first
        for name in args:
            if name.lower() == arg_lower:
                return name

        # Prefix match
        matches = []
        for name, arg_def in args.items():
            min_prefix = arg_def.get("min_prefix", len(name))
            if (len(arg_lower) >= min_prefix and
                    name.lower().startswith(arg_lower)):
                matches.append(name)

        if len(matches) == 1:
            return matches[0]

        return None
```

### 6.5. Symbol Table (`symbols.py`)

Single-file semantic analysis. Walk parsed statements top-to-bottom and track which objects have been created.

```python
@dataclass
class Symbol:
    name: str           # full object path, e.g. ".model.PART_1"
    object_type: str    # e.g. "Marker", "Part", "Model"
    line: int           # line where created (0-based)

class SymbolTable:
    def __init__(self):
        self.symbols = {}  # name → Symbol

    def register(self, name, object_type, line):
        self.symbols[name.lower()] = Symbol(name, object_type, line)

    def lookup(self, name):
        return self.symbols.get(name.lower())

    def has(self, name):
        return name.lower() in self.symbols


def build_symbol_table(statements, schema):
    """Walk statements and collect created objects."""
    table = SymbolTable()
    for stmt in statements:
        if stmt.is_comment or stmt.is_blank or stmt.is_control_flow:
            continue
        cmd_key = stmt.resolved_command_key or stmt.command_key
        cmd = schema.get_command(cmd_key)
        if not cmd:
            continue
        for arg in stmt.arguments:
            # Resolve abbreviated argument names
            canonical = schema.resolve_argument_name(cmd_key, arg.name)
            arg_def = cmd["args"].get(canonical or arg.name)
            if arg_def and arg_def.get("type") == "new_object":
                table.register(arg.value, arg_def.get("object_type", "unknown"), arg.name_line)
    return table
```

### 6.6. Lint Rules (`rules.py`)

Each rule is a function that takes `(statements, schema, symbols)` and returns a list of `Diagnostic` objects.

#### Rule Table

| Code | Name | Severity | Description | Data Source |
|------|------|----------|-------------|-------------|
| **E001** | Unknown command | Error | Command key doesn't match any known command (even after abbreviation expansion) | `command_schema.json` (command_tree) |
| **E002** | Invalid argument | Error | Argument name not valid for this command (even after abbreviation expansion) | `command_schema.json` (args + min_prefix) |
| **E003** | Duplicate argument | Error | Same argument name (or abbreviation resolving to same canonical name) appears twice in one statement | Statement parsing + abbreviation resolution |
| **E004** | Invalid enum value | Error | Argument value not in the allowed enum list | `command_schema.json` (enum_values) |
| **E005** | Missing required argument | Error | A required argument (marked `*`) is missing, AND it is not an auto-generated name, auto-assigned ID, or a member of a mutual exclusion group where another member is provided | `command_schema.json` (required flag + exclusive_groups) |
| **W005** | Object name omitted | Warning | A required `NDBWD_*`/`NDB_*` argument is omitted — Adams auto-generates a name, but explicit names are strongly encouraged | `command_schema.json` |
| **I006** | Manual Adams ID assignment | Info | The user explicitly assigned an `adams_id` — Adams auto-assigns IDs and manual assignment is discouraged | `command_schema.json` |
| **E006** | Mutual exclusion conflict | Warning | Two or more mutually exclusive arguments are both provided | `command_schema.json` (exclusive_groups) |
| **E101** | Unbalanced parentheses | Error | More opens than closes, or vice versa | Syntax scan |
| **E102** | Unclosed quote | Error | A double-quoted string is not closed | Syntax scan |
| **E103** | Orphan continuation line | Error | A continuation `&` appears but the previous line doesn't continue | Continuation context |
| **E104** | Unbalanced if/end | Error | `if` without `end`, `else` without `if`, `end` without `if` | Control flow tracking |
| **W201** | Type mismatch | Warning | An `existing_object` argument receives an object of the wrong type (e.g., passing a geometry where a marker is expected) | Symbol table |
| **I202** | Unresolved reference | Info | An `existing_object` argument references a name not found in the file (may come from an external file or be computed at runtime) | Symbol table |

#### Rule Implementation Details

**E001 — Unknown command (with abbreviation support):**
```python
def rule_unknown_command(statements, schema, symbols):
    diagnostics = []
    for stmt in statements:
        if stmt.is_comment or stmt.is_blank or stmt.is_control_flow:
            continue
        if not stmt.command_key:
            continue

        # First try exact match
        if schema.has_command(stmt.command_key):
            continue

        # Then try abbreviation resolution via command tree
        tokens = stmt.command_key.split()
        resolved_key, error_index = schema.resolve_command_key(tokens)

        if resolved_key:
            # Successfully resolved — update the statement's canonical key
            # for downstream rules to use
            stmt.resolved_command_key = resolved_key
            continue

        # Failed to resolve — report error at the problematic token
        diagnostics.append(Diagnostic(
            line=stmt.line_start,
            column=0,
            end_line=stmt.line_start,
            end_column=len(stmt.command_key),
            code="E001",
            message=f"Unknown command: '{stmt.command_key}'",
            severity=Severity.ERROR,
        ))
    return diagnostics
```

> **Implementation note:** The parser should attempt abbreviation resolution
> during parsing and store the result in `stmt.resolved_command_key`. Rules
> downstream of E001 should use `stmt.resolved_command_key or stmt.command_key`
> to access the canonical command key. This avoids re-resolving in every rule.

**E005/W005 — Missing required argument (two-tier, with exclusive group suppression):**

This is the most nuanced rule. The `*` flag in language.src means "required," but:

1. Some "required" arguments are auto-generated by Adams:
   - **`NDBWD_*` / `NDB_*` type args** (new object names): Adams auto-generates a name like `PART_1`, `MARKER_2` if omitted. Missing these is legal but poor practice → **W005 (warning)**
   - **`ADAMS_ID` type args**: Adams auto-assigns integer IDs if omitted. This is the **preferred** behavior — manual ID assignment is discouraged → **no diagnostic when omitted**
   - **All other required args**: Truly required, omission causes a runtime error → **E005 (error)**

2. **Exclusive group suppression (Concern C):** If a required argument belongs to a mutual exclusion group and ANY other member of the same group is provided, suppress the missing-required diagnostic entirely. Example: if `orientation` and `along_axis_orientation` are mutually exclusive and the user provides `along_axis_orientation`, do NOT flag `orientation` as missing even if it's marked required.

```python
def rule_missing_required(statements, schema, symbols):
    diagnostics = []
    for stmt in statements:
        if stmt.is_comment or stmt.is_blank or stmt.is_control_flow:
            continue
        cmd_key = getattr(stmt, 'resolved_command_key', None) or stmt.command_key
        cmd = schema.get_command(cmd_key)
        if not cmd:
            continue

        provided = set()
        for arg in stmt.arguments:
            # Resolve abbreviated argument names
            canonical = schema.resolve_argument_name(cmd_key, arg.name)
            if canonical:
                provided.add(canonical)
            else:
                provided.add(arg.name)

        # Build a set of args that are "covered" by exclusive group membership
        groups = schema.get_exclusive_groups(cmd_key)
        covered_by_group = set()
        for group in groups:
            members = group["members"]
            used = [m for m in members if m in provided]
            if used:
                # Some member of this group is provided — all other members
                # are implicitly satisfied (mutually exclusive = pick one)
                covered_by_group.update(members)

        for arg_name, arg_def in cmd["args"].items():
            if not arg_def.get("required"):
                continue
            if arg_name in provided:
                continue
            if arg_name in covered_by_group:
                continue  # Suppressed: another member of exclusive group is provided

            # Determine severity based on type
            arg_type = arg_def.get("type", "")
            db_type = arg_def.get("db_type", "")

            if arg_type == "adams_id" or db_type == "ADAMS_ID":
                continue  # Omitting adams_id is the preferred behavior — no diagnostic
            elif db_type.startswith("NDBWD_") or db_type.startswith("NDB_"):
                code, severity = "W005", Severity.WARNING
                message = f"Object name '{arg_name}' omitted (auto-generated). Explicit names are recommended."
            else:
                code, severity = "E005", Severity.ERROR
                message = f"Missing required argument: '{arg_name}'"

            diagnostics.append(Diagnostic(
                line=stmt.line_start,
                column=0,
                end_line=stmt.line_start,
                end_column=len(stmt.command_key),
                code=code,
                message=message,
                severity=severity,
            ))
    return diagnostics
```

**I006 — Manual Adams ID assignment:**
```python
def rule_manual_adams_id(statements, schema, symbols):
    """Flag when a user manually assigns an adams_id.

    Best practice is to let Adams auto-assign IDs. Manual assignment
    can cause ID conflicts and maintenance headaches.
    """
    diagnostics = []
    for stmt in statements:
        if stmt.is_comment or stmt.is_blank or stmt.is_control_flow:
            continue
        cmd_key = getattr(stmt, 'resolved_command_key', None) or stmt.command_key
        cmd = schema.get_command(cmd_key)
        if not cmd:
            continue

        for arg in stmt.arguments:
            canonical = schema.resolve_argument_name(cmd_key, arg.name)
            arg_name = canonical or arg.name
            arg_def = cmd["args"].get(arg_name)
            if arg_def and (arg_def.get("type") == "adams_id" or
                            arg_def.get("db_type") == "ADAMS_ID"):
                diagnostics.append(Diagnostic(
                    line=arg.name_line,
                    column=arg.name_column,
                    end_line=arg.value_line,
                    end_column=arg.value_column + len(arg.value),
                    code="I006",
                    message=f"Manual Adams ID assignment — consider letting Adams auto-assign",
                    severity=Severity.INFO,
                ))
    return diagnostics
```

**E006 — Mutual exclusion conflict:**
```python
def rule_exclusive_conflict(statements, schema, symbols):
    diagnostics = []
    for stmt in statements:
        if stmt.is_comment or stmt.is_blank or stmt.is_control_flow:
            continue
        groups = schema.get_exclusive_groups(stmt.command_key)
        provided = {arg.name for arg in stmt.arguments}

        for group in groups:
            members = group["members"]
            used = [m for m in members if m in provided]
            if len(used) > 1:
                # Find the second occurrence to put the diagnostic on
                for arg in stmt.arguments:
                    if arg.name == used[1]:
                        diagnostics.append(Diagnostic(
                            line=arg.name_line,
                            column=arg.name_column,
                            end_line=arg.name_line,
                            end_column=arg.name_column + len(arg.name),
                            code="E006",
                            message=f"'{arg.name}' conflicts with '{used[0]}' (mutually exclusive)",
                            severity=Severity.WARNING,
                        ))
    return diagnostics
```

**E101 — Unbalanced parentheses:**

> [UPDATED] The implementation also tracks single-quoted strings (`'...'`) in
> addition to double-quoted strings. Parentheses inside single-quoted strings
> (e.g., `FUNCTION='step(time,0,0,1,100)'`) are correctly ignored by the paren
> depth counter.

```python
def rule_unbalanced_parens(statements, schema, symbols):
    diagnostics = []
    for stmt in statements:
        if stmt.is_comment or stmt.is_blank:
            continue
        depth = 0
        in_string = False
        for i, ch in enumerate(stmt.raw_text):
            if ch == '"':
                in_string = not in_string
            elif not in_string:
                if ch == '(':
                    depth += 1
                elif ch == ')':
                    depth -= 1
                    if depth < 0:
                        line, col = char_to_line_col(i, stmt)
                        diagnostics.append(Diagnostic(
                            line=line, column=col,
                            end_line=line, end_column=col + 1,
                            code="E101",
                            message="Unexpected closing parenthesis ')'",
                            severity=Severity.ERROR,
                        ))
                        depth = 0  # reset to continue scanning
        if depth > 0:
            diagnostics.append(Diagnostic(
                line=stmt.line_end, column=0,
                end_line=stmt.line_end, end_column=0,
                code="E101",
                message=f"Unbalanced parentheses: {depth} unclosed '('",
                severity=Severity.ERROR,
            ))
    return diagnostics
```

**W201 — Type mismatch (semantic):**
```python
def rule_type_mismatch(statements, schema, symbols):
    diagnostics = []
    for stmt in statements:
        if stmt.is_comment or stmt.is_blank or stmt.is_control_flow:
            continue
        cmd = schema.get_command(stmt.command_key)
        if not cmd:
            continue
        for arg in stmt.arguments:
            arg_def = cmd["args"].get(arg.name)
            if not arg_def or arg_def.get("type") != "existing_object":
                continue
            expected_type = arg_def.get("object_type")
            if not expected_type:
                continue

            # Skip values with runtime expressions
            if "$" in arg.value or "eval(" in arg.value.lower():
                continue

            symbol = symbols.lookup(arg.value)
            if symbol and symbol.object_type.upper() != expected_type.upper():
                diagnostics.append(Diagnostic(
                    line=arg.value_line,
                    column=arg.value_column,
                    end_line=arg.value_line,
                    end_column=arg.value_column + len(arg.value),
                    code="W201",
                    message=f"Type mismatch: '{arg.value}' is a {symbol.object_type}, expected {expected_type}",
                    severity=Severity.WARNING,
                ))
            elif not symbol and "$" not in arg.value:
                diagnostics.append(Diagnostic(
                    line=arg.value_line,
                    column=arg.value_column,
                    end_line=arg.value_line,
                    end_column=arg.value_column + len(arg.value),
                    code="I202",
                    message=f"Unresolved reference: '{arg.value}'",
                    severity=Severity.INFO,
                ))
    return diagnostics
```

### 6.7. Linter Orchestrator (`linter.py`)

```python
from .parser import parse
from .schema import Schema
from .symbols import build_symbol_table
from .rules import ALL_RULES

def lint_text(text, schema=None, min_severity=None):
    """Lint a CMD text string and return sorted diagnostics.

    Args:
        text: The raw .cmd file content
        schema: Schema object (loads default if None)
        min_severity: Minimum severity to include (None = all)

    Returns:
        list[Diagnostic] sorted by (line, column)
    """
    schema = schema or Schema.load()
    statements = parse(text)
    symbols = build_symbol_table(statements, schema)

    diagnostics = []
    for rule in ALL_RULES:
        diagnostics.extend(rule(statements, schema, symbols))

    if min_severity:
        severity_order = {"error": 0, "warning": 1, "info": 2}
        threshold = severity_order.get(min_severity.lower(), 2)
        diagnostics = [d for d in diagnostics
                       if severity_order.get(d.severity.value, 2) <= threshold]

    return sorted(diagnostics, key=lambda d: (d.line, d.column))
```

---

## 7. Phase 2: CLI Linter

### File: `adams_cmd_lsp/cli.py`

**Usage:**
```
adams-cmd-lint <file1.cmd> [file2.cmd ...] [options]

Options:
  --format text|json|gcc    Output format (default: text)
  --severity error|warning|info  Minimum severity (default: info)
  --schema PATH             Path to command_schema.json (default: bundled)
```

**Exit codes:**
- `0` — no issues found
- `1` — issues found
- `2` — usage error (bad arguments, file not found)

**Output formats:**

*text (human-readable):*
```
test.cmd:1:1: E001 Unknown command: 'mar'
test.cmd:4:5: E003 Duplicate argument: 'part_name'
test.cmd:5:30: E101 Unbalanced parentheses: unexpected ')'

2 errors, 0 warnings, 0 info
```

*json (for agent consumption):*
```json
{
  "file": "test.cmd",
  "diagnostics": [
    {
      "line": 1,
      "column": 1,
      "end_line": 1,
      "end_column": 4,
      "code": "E001",
      "message": "Unknown command: 'mar'",
      "severity": "error"
    }
  ],
  "summary": {"errors": 1, "warnings": 0, "info": 0}
}
```

*gcc (editor-compatible):*
```
test.cmd:1:1: error: Unknown command: 'mar' [E001]
test.cmd:4:5: error: Duplicate argument: 'part_name' [E003]
```

### Implementation

```python
import argparse
import json
import sys
from pathlib import Path
from .linter import lint_text
from .schema import Schema

def main():
    parser = argparse.ArgumentParser(
        prog="adams-cmd-lint",
        description="Lint Adams CMD files"
    )
    parser.add_argument("files", nargs="+", help="CMD files to lint")
    parser.add_argument("--format", choices=["text", "json", "gcc"],
                        default="text", help="Output format")
    parser.add_argument("--severity", choices=["error", "warning", "info"],
                        default="info", help="Minimum severity to report")
    parser.add_argument("--schema", help="Path to command_schema.json")

    args = parser.parse_args()

    schema = Schema.load(args.schema) if args.schema else Schema.load()

    exit_code = 0
    for filepath in args.files:
        path = Path(filepath)
        if not path.exists():
            print(f"Error: file not found: {filepath}", file=sys.stderr)
            sys.exit(2)

        text = path.read_text(encoding="utf-8", errors="replace")
        diagnostics = lint_text(text, schema=schema, min_severity=args.severity)

        if diagnostics:
            exit_code = 1

        if args.format == "json":
            output_json(filepath, diagnostics)
        elif args.format == "gcc":
            output_gcc(filepath, diagnostics)
        else:
            output_text(filepath, diagnostics)

    sys.exit(exit_code)
```

---

## 8. Phase 3: LSP Server

### File: `adams_cmd_lsp/server.py`

~200-300 lines using `pygls`.

### LSP Capabilities

| Capability | Implementation |
|-----------|---------------|
| `textDocument/didOpen` | Full lint of opened document |
| `textDocument/didChange` | Debounced re-lint (500ms) |
| `textDocument/didClose` | Clear diagnostics for document |
| `textDocument/didSave` | Full re-lint |

### Key Implementation Details

- **Transport:** stdio (default), `--tcp` flag for debugging
- **Schema loading:** Load `command_schema.json` ONCE at startup, keep in memory
- **Per-document state:** Parsed statements + symbol table, rebuilt on every change
- **Debouncing:** Use `pygls` built-in or simple timer to debounce `didChange` events (500ms)
- **Diagnostic publishing:** Convert `Diagnostic` dataclass → LSP `Diagnostic` protocol objects

### Implementation Skeleton

```python
from pygls.lsp.server import LanguageServer
from lsprotocol import types

from .linter import lint_text
from .schema import Schema
from .diagnostics import Severity

server = LanguageServer("adams-cmd-lsp", "v0.1.0")
schema = None  # loaded in main()

SEVERITY_MAP = {
    Severity.ERROR: types.DiagnosticSeverity.Error,
    Severity.WARNING: types.DiagnosticSeverity.Warning,
    Severity.INFO: types.DiagnosticSeverity.Information,
}

def to_lsp_diagnostic(d):
    return types.Diagnostic(
        range=types.Range(
            start=types.Position(line=d.line, character=d.column),
            end=types.Position(line=d.end_line, character=d.end_column),
        ),
        message=d.message,
        source="adams-cmd-lint",
        code=d.code,
        severity=SEVERITY_MAP.get(d.severity, types.DiagnosticSeverity.Information),
    )

def validate_document(uri, text):
    diagnostics = lint_text(text, schema=schema)
    lsp_diags = [to_lsp_diagnostic(d) for d in diagnostics]
    server.publish_diagnostics(uri, lsp_diags)

@server.feature(types.TEXT_DOCUMENT_DID_OPEN)
def did_open(params: types.DidOpenTextDocumentParams):
    doc = params.text_document
    validate_document(doc.uri, doc.text)

@server.feature(types.TEXT_DOCUMENT_DID_CHANGE)
def did_change(params: types.DidChangeTextDocumentParams):
    doc = server.workspace.get_text_document(params.text_document.uri)
    # pygls debouncing or manual timer here
    validate_document(params.text_document.uri, doc.source)

@server.feature(types.TEXT_DOCUMENT_DID_CLOSE)
def did_close(params: types.DidCloseTextDocumentParams):
    server.publish_diagnostics(params.text_document.uri, [])

@server.feature(types.TEXT_DOCUMENT_DID_SAVE)
def did_save(params: types.DidSaveTextDocumentParams):
    doc = server.workspace.get_text_document(params.text_document.uri)
    validate_document(params.text_document.uri, doc.source)

def main():
    import argparse
    global schema

    parser = argparse.ArgumentParser()
    parser.add_argument("--tcp", action="store_true", help="Use TCP transport for debugging")
    parser.add_argument("--port", type=int, default=2087, help="TCP port (with --tcp)")
    parser.add_argument("--schema", help="Path to command_schema.json")
    args = parser.parse_args()

    schema = Schema.load(args.schema) if args.schema else Schema.load()

    if args.tcp:
        server.start_tcp("localhost", args.port)
    else:
        server.start_io()
```

### `__main__.py`

```python
"""Allow running the LSP server via `python -m adams_cmd_lsp`."""
from .server import main

main()
```

### Using with Different Editors

**Claude Code / other MCP-aware agents:**
Configure `.mcp.json` or equivalent to point to `adams-cmd-lint` CLI, or use LSP directly if the agent supports it.

**Neovim:**
```lua
vim.lsp.start({
    name = "adams-cmd-lsp",
    cmd = { "adams-cmd-lsp" },
    filetypes = { "adams_cmd" },
})
```

**VS Code:** See Phase 4 below.

---

## 9. Phase 4: VS Code Integration

### 9.1. LSP Client (`src/cmd_lsp_client.ts.js`)

This is a new JavaScript file in the existing VS Code extension that starts and manages the Python LSP server.

**Important:** This file must follow the existing codebase conventions:
- Plain JavaScript with CommonJS (`require` / `exports`)
- `.ts.js` file extension
- Dependency injection (pass `output_channel`, `reporter`)
- `const vscode = require("vscode")` inside function bodies

```javascript
/**
 * Creates and manages the Adams CMD LSP client.
 *
 * @param {vscode.OutputChannel} output_channel
 * @param {object|null} reporter
 * @returns {{ start: Function, stop: Function }}
 */
function cmd_lsp_client(output_channel, reporter) {
    const vscode = require("vscode");
    const { LanguageClient, TransportKind } = require("vscode-languageclient/node");

    let client = null;

    function start(context) {
        const config = vscode.workspace.getConfiguration("msc-adams");
        if (!config.get("linter.enabled")) {
            return;
        }

        // Find Python interpreter
        const python_path = config.get("linter.pythonPath")
            || vscode.workspace.getConfiguration("python").get("defaultInterpreterPath")
            || "python";

        const server_options = {
            command: python_path,
            args: ["-m", "adams_cmd_lsp"],
            transport: TransportKind.stdio,
        };

        const client_options = {
            documentSelector: [{ scheme: "file", language: "adams_cmd" }],
            outputChannel: output_channel,
        };

        client = new LanguageClient(
            "adams-cmd-lsp",
            "Adams CMD Language Server",
            server_options,
            client_options,
        );

        client.start().then(function () {
            output_channel.appendLine("Adams CMD Language Server started");
            if (reporter) {
                reporter.sendTelemetryEvent("lsp_started");
            }
        }, function (err) {
            output_channel.appendLine("Failed to start Adams CMD Language Server: " + err.message);
            // Don't block activation on LSP failure
        });

        context.subscriptions.push(client);
    }

    function stop() {
        if (client) {
            return client.stop();
        }
    }

    return { start: start, stop: stop };
}

exports.cmd_lsp_client = cmd_lsp_client;
```

### 9.2. Extension Wiring (`src/extension.ts.js`)

Add to the `activate()` function, after existing provider registrations:

```javascript
// At the top, add the require:
const { cmd_lsp_client } = require("./cmd_lsp_client.ts.js");

// Inside activate(), after the existing completion/hover/link registrations:

// ---------------------------------------------------------------------------
// LSP Client (Adams CMD Linter)
// ---------------------------------------------------------------------------
const lsp = cmd_lsp_client(output_channel, reporter);
lsp.start(context);
```

### 9.3. Package.json Changes

**Add dependency:**
```json
"dependencies": {
    "@vscode/extension-telemetry": "^0.9.7",
    "temp": "^0.9.4",
    "vscode-languageclient": "^9.0.1"
}
```

**Add configuration settings:**
```json
"contributes": {
    "configuration": {
        "properties": {
            "msc-adams.linter.enabled": {
                "type": "boolean",
                "default": true,
                "description": "Enable Adams CMD linter (requires adams-cmd-lsp Python package)"
            },
            "msc-adams.linter.pythonPath": {
                "type": "string",
                "default": "",
                "description": "Path to Python interpreter for the linter. Leave empty to use the default Python interpreter."
            },
            "msc-adams.linter.severity": {
                "type": "string",
                "enum": ["error", "warning", "info"],
                "default": "info",
                "description": "Minimum severity level to report"
            },
            "msc-adams.linter.semanticAnalysis": {
                "type": "boolean",
                "default": true,
                "description": "Enable semantic analysis (type mismatch detection, unresolved references)"
            }
        }
    }
}
```

---

## 10. Phase 5: Testing

### Python Tests (`adams-cmd-lsp/tests/`)

**`test_parser.py`:**
- Test continuation line joining (`&`)
- Test command key extraction (port the exact test cases from `cmd_completion_provider.test.js`)
- Test argument extraction with various value types (bare, quoted, parenthesized, comma-separated)
- Test handling of comments in continuation lines
- Test blank lines and comment-only lines
- Test control flow detection

**`test_schema.py`:**
- Test schema loading (new JSON structure with `commands` and `command_tree`)
- Test command lookup
- Test argument lookup
- Test exclusive group retrieval
- Test `resolve_command_key` with exact match, valid abbreviation, ambiguous abbreviation, too-short prefix
- Test `resolve_argument_name` with exact match, valid abbreviation, ambiguous abbreviation
- Test case-insensitivity of resolution

**`test_rules.py` (one test suite per rule):**
- E001: unknown command, known command, empty line, **abbreviated command that resolves**, **ambiguous abbreviation that fails**
- E002: valid arg, invalid arg, arg for wrong command, **abbreviated argument that resolves**, **ambiguous argument abbreviation**
- E003: duplicate arg, unique args, **two different abbreviations resolving to same canonical arg**
- E004: valid enum value, invalid enum value, arg without enum constraint
- E005/W005: required arg missing (both tiers), required arg present, optional arg missing, **required arg missing but exclusive group member provided (suppressed)**, **adams_id omitted (no diagnostic)**
- I006: adams_id manually assigned (flagged), adams_id omitted (no diagnostic)
- E006: mutual exclusion conflict, no conflict, only one of group provided
- E101: balanced parens, unbalanced open, unbalanced close, nested, in strings
- E102: unclosed quote, closed quote, no quotes
- E104: balanced if/end, if without end, end without if, nested if/end, **for without end**, **nested if inside for**
- W201: correct type, wrong type, unknown reference, runtime expression (skip)
- I202: unresolved reference, resolved reference

**`test_linter.py`:**
- Integration test: lint a complete valid file → 0 diagnostics
- Integration test: lint `test/files/test.cmd` → expected diagnostics

**`test_cli.py`:**
- Test text output format
- Test JSON output format
- Test gcc output format
- Test exit codes
- Test file not found

**`test_server.py`:**
- Test LSP protocol: didOpen → publishes diagnostics
- Test LSP protocol: didClose → clears diagnostics

### Test Fixtures

Copy or symlink relevant test files from the existing repo:
- `test/files/test.cmd` — has intentional errors (good for testing)
- `test/files/create_model.cmd` — simple valid file
- `test/files/test_measures_final.cmd` — large valid file (no false positives test)

### VS Code Extension Tests

Add a new test file `test/cmd_lsp_client.test.js` following the existing Mocha `suite()/test()` pattern.

**These tests must NOT require Adams View.** Follow the pure unit test pattern from `cmd_completion_provider.test.js` — use mock documents, mock reporters, in-memory data, and synchronous tests. 9 of 12 existing test files already work without Adams View; these new tests should too.

Test cases:
- Test that the LSP client module exports correctly
- Test that it respects the `msc-adams.linter.enabled` setting
- Test that the client gracefully handles the Python LSP server not being installed
- Test that `pythonPath` configuration is correctly resolved

---

## 11. Verification Checklist

1. **Schema generation:**
   ```
   python scripts/generate_command_schema.py --input /path/to/commands.exp --language-src /path/to/language.src
   ```
   → produces `command_schema.json` with `commands` and `command_tree` sections

2. **Schema coverage:** Compare against `structured.json` — every command in structured.json should be in the schema (and vice versa, minus debug/menu-only commands)

3. **Abbreviation prefixes:** Verify that `min_prefix` values in the schema are correct for a sample of commands:
   - `model` vs `marker` vs `mass` — should require at least 3 chars each
   - `create` vs `copy` under the same parent — `cr` and `co` should suffice
   - Argument prefixes within a command should be similarly validated

4. **Spot-check 20 commands:** Verify required/optional matches the `*` markers in commands.exp for these commands:
   - `model create`, `model modify`, `model delete`, `model merge`
   - `marker create`, `marker modify`, `marker delete`
   - `part create rigid_body name_and_position`
   - `geometry create point`, `geometry create circle`
   - `constraint create joint revolute`
   - `force create single_component_force`
   - `analysis create`
   - `data_element create spline`
   - `variable set`, `variable create`
   - `simulation single_run transient`

5. **Abbreviation resolution works:**
   ```
   adams-cmd-lint test_file_with_abbreviations.cmd
   ```
   → `mar cre` resolves to `marker create`, `part_n` resolves to `part_name`, no false E001/E002

6. **CLI works:**
   ```
   pip install -e ./adams-cmd-lsp
   adams-cmd-lint test/files/test.cmd
   ```
   → expected diagnostics output

7. **Tests pass:**
   ```
   cd adams-cmd-lsp && pytest
   ```
   → all pass

8. **CLI JSON format:**
   ```
   adams-cmd-lint test/files/test.cmd --format json
   ```
   → valid JSON

9. **No false positives on valid file:**
   ```
   adams-cmd-lint test/files/test_measures_final.cmd
   ```
   → 0 errors (or only info-level)

10. **Exclusive group suppression:** A command with mutually exclusive args where one is provided and the other is marked required → no E005 for the missing one

11. **LSP works in VS Code:**
    - Open a `.cmd` file
    - See diagnostics (squiggly underlines) on known errors
    - Hover shows diagnostic message
    - Changing `msc-adams.linter.enabled` to `false` disables diagnostics

12. **LSP works standalone:**
    ```
    echo '{"jsonrpc":"2.0","method":"initialize","id":1,"params":{}}' | adams-cmd-lsp
    ```
    → responds with LSP initialize response

---

## 12. Design Decisions & Rationale

### 1. `commands.exp` is the primary source, `language.src` is secondary
`commands.exp` is the fully expanded output of the `lang_to_tables.exe` preprocessor — all macros are inlined, dispatch trees are flattened, `?suffix` hints are stripped, and each argument has its type, required flag (`*`), and default value on a single parseable line. This eliminates the need for a complex DSL parser with macro expansion, dispatch tree walking, recursion depth limits, and hardcoded built-in macro tables. `language.src` is only needed for mutual exclusion groups (`{...}` blocks), which `commands.exp` does not preserve.

### 2. Abbreviation support is a core feature, not a future item
Adams users routinely abbreviate commands and arguments (e.g., `mar cre` for `marker create`, `part_n` for `part_name`). Adams matches using shortest unique prefix — no minimum prefix lengths are stored, they're computed dynamically from sibling sets. The linter pre-computes minimum unique prefixes during schema generation and stores them in `command_schema.json`. At lint time, `Schema.resolve_command_key()` and `Schema.resolve_argument_name()` handle prefix matching. Without this, every abbreviated command in every CMD file would be flagged as E001, making the linter unusable.

### 3. LSP for all editors, including VS Code
Python is guaranteed available because the VS Code extension already declares `extensionDependencies` on `ms-python.python`. Using LSP means the same server works in Claude Code, Neovim, Zed, and any LSP-capable editor without code changes.

### 4. CLI AND LSP from the same core
Agents that don't support LSP can still use `adams-cmd-lint` as a command-line tool. CI pipelines can run it as a pre-commit check. The cost of maintaining two thin wrappers around the same library is minimal.

### 5. Schema generated once, checked in
The schema generator reads `commands.exp` and `language.src` (which live in the Adams *source tree*, not this repo). A developer runs the script once, reviews the output, and commits `command_schema.json`. This means the linter works without access to the Adams source tree — it just needs the committed JSON file.

### 6. Subdirectory first, own repo later
Keeping `adams-cmd-lsp/` inside `adams_vscode/` simplifies development — shared test fixtures, easy cross-referencing with existing data files, single PR for the full feature. Extract to its own repo when stable to enable independent versioning and PyPI publication.

### 7. Single-file semantic analysis only
Cross-file analysis (e.g., `model create` in one file, `part create` referencing it in another) would require a workspace-level index. For now, references to objects not defined in the same file are info-level (`I202`), not errors. This avoids false positives from common patterns like separate model/macro files.

### 8. Existing JS providers stay
The completion provider and hover provider in the VS Code extension continue to work as-is. They can be migrated to the LSP server later (Phase 6+) to make completions available in all editors, but that's not part of this initial plan.

### 9. Two-tier severity for "required" arguments, plus advisory on manual IDs
Adams auto-generates object names (`NDBWD_*`/`NDB_*`) and auto-assigns IDs (`ADAMS_ID`) even though language.src marks them with `*` (required). We use two severity levels for missing-required, plus an advisory:
- **Error (E005):** truly required, omission causes runtime failure
- **Warning (W005):** auto-generated name, works but explicit names are best practice
- **Info (I006):** manual Adams ID assignment detected — best practice is to let Adams auto-assign IDs, so we flag when the user *does* provide one rather than when they omit it

---

## 13. Future Considerations

These are NOT part of the initial implementation. Documenting them for awareness only.

1. **Completions/hover migration to LSP** — Port the JS completion/hover providers to Python so all editors get completions, not just VS Code.

2. **Code actions / auto-fix** — E004 (invalid enum value) → suggest valid alternatives. E005 (missing required arg) → insert template.

3. **Per-project config** — Expose rule severity overrides and file exclusions through VS Code's settings UI (`msc-adams.linter.*` settings), so users can configure the linter without needing to know TOML or create extra config files. A `.adams-cmd-lint.toml` could be supported later for CI/editor-agnostic use.

4. **Auto-update schema** — CI job that regenerates `command_schema.json` when `commands.exp` changes upstream.

5. **Cross-file analysis** — Workspace-level symbol index for resolving references across files.

6. **Value-level validation** — E.g., checking that `LOCATION` arguments have exactly 3 comma-separated values, or that `BOOLEAN` arguments are `yes`/`no`.

---

## Appendix A: Existing JavaScript Parsing Code (Port Reference)

The following is the complete source of `src/cmd_completion_provider.ts.js` — the parsing functions in this file must be ported to Python for the parser module. The key functions are documented inline.

```javascript
// Full source: src/cmd_completion_provider.ts.js
// See the file in the repo for the complete 280-line implementation.
// Key functions to port:
//
// get_full_command_context(document, position)
//   - Walks backward through & continuation lines
//   - Concatenates them into a single string
//   - Returns the full command text up to cursor position
//
// strip_argument_pairs(text)
//   - Removes all arg=value pairs from text
//   - Returns the bare command key
//   - Handles quoted strings, parenthesized expressions, comma-separated values
//
// consume_argument_value(text, start)
//   - Consumes a single value starting at position
//   - Three modes: quoted string ("..."), parenthesized ((...)) with nesting, bare word
//   - Returns the position after the consumed value
//
// consume_comma_separated_tail(text, i, value_start)
//   - After consuming a value, looks for trailing/following comma
//   - Continues consuming comma-separated values (e.g., stiffness=1e6, 1e6, 1e6)
//   - Stops when it hits a new arg= pair or end of text
//
// get_indent_level(line, indent_type)
//   - Counts leading indent characters
//   - Used for completion item indentation (not needed in linter)
```

## Appendix B: Test CMD Files with Expected Diagnostics

### `test/files/test.cmd` — Expected Diagnostics

This file has several intentional issues. Expected diagnostics:

| Line | Code | Severity | Message |
|------|------|----------|---------|
| ~51 | — | — | `mar create` is an abbreviation that resolves to `marker create` — NOT an error (abbreviation support handles this) |
| ~57 | E101 | Error | Unbalanced parentheses in `(eval(abs())))` |
| ~53 | E101 | Error | Unbalanced condition expression |

(Exact line numbers depend on the parser's handling of continuation lines. These are approximate. The `mar create` case is a key validation that abbreviation support works correctly.)

### `test/files/create_model.cmd` — Expected: Minimal Diagnostics

This is a mostly-valid file. May have some W005/I005 info-level messages for missing names/IDs, but no hard errors.

### `test/files/test_measures_final.cmd` — Expected: Zero Errors

This is a large, valid CMD file. The linter should produce zero errors and zero warnings. Any diagnostics here are false positives that need investigation.

## Appendix C: Adams CMD Type Token Reference

Complete mapping of type tokens found in `language.src` to schema types:

| language.src Token | Schema Type | Notes |
|-------------------|-------------|-------|
| `INT` | `integer` | |
| `REAL` | `real` | |
| `STRING` | `string` | |
| `FILE` | `string` | file path |
| `BOOLEAN` | `boolean` | yes/no |
| `ON_OFF` | `boolean` | on/off |
| `ON_OFF_WITH_TOGGLE` | `boolean` | on/off/toggle |
| `TRUE_ONLY` | `boolean` | can only be set, not cleared |
| `FUNCTION` | `function` | Adams expression |
| `ADAMS_ID` | `adams_id` | auto-assigned integer ID |
| `LOCATION` | `location` | x,y,z coordinates |
| `ORIENTATION` | `orientation` | angle triplet |
| `ANGLE` | `real` (unit: angle) | |
| `LENGTH` | `real` (unit: length) | |
| `MASS` | `real` (unit: mass) | |
| `TIME` | `real` (unit: time) | |
| `FORCE` | `real` (unit: force) | |
| `VELOCITY` | `real` (unit: velocity) | |
| `ACCELERATION` | `real` (unit: acceleration) | |
| `ANGULAR_VEL` | `real` (unit: angular_vel) | |
| `ANGULAR_ACCEL` | `real` (unit: angular_accel) | |
| `STIFFNESS` | `real` (unit: stiffness) | |
| `DAMPING` | `real` (unit: damping) | |
| `TORQUE` | `real` (unit: torque) | |
| `PRESSURE` | `real` (unit: pressure) | |
| `INERTIA` | `real` (unit: inertia) | |
| `DENSITY` | `real` (unit: density) | |
| `AREA` | `real` (unit: area) | |
| `VOLUME` | `real` (unit: volume) | |
| `NDBWD_*` | `new_object` | creates new object, auto-generated name if omitted |
| `NDB_*` | `new_object` | creates new object (without default), auto-generated name |
| `DB_*` | `existing_object` | references existing object |
| `*_ACTION` | `unknown` | enum type (e.g., `DUPL_PART_ACTION`) — values from argument_options.json |
| `DB_COLOR` | `existing_object` (color) | |
| `COLOR_SCOPE` | `unknown` | enum type |
| `MDB_GROUP` | `existing_object` (group) | |

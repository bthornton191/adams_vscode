# Changelog

- [Changelog](#changelog)
  - [1.14.0 (April 16th 2026)](#1140-april-16th-2026)
  - [1.13.1 (April 15th 2026)](#1131-april-15th-2026)
  - [1.13.0 (April 8th 2026)](#1130-april-8th-2026)
  - [1.12.2 (April 8th 2026)](#1122-april-8th-2026)
  - [1.12.1 (April 6th 2026)](#1121-april-6th-2026)
  - [1.12.0 (April 6th 2026)](#1120-april-6th-2026)
  - [1.11.1 (April 6th 2026)](#1111-april-6th-2026)
  - [1.11.0 (April 3rd 2026)](#1110-april-3rd-2026)
  - [1.10.4 (April 2nd 2026)](#1104-april-2nd-2026)
  - [1.10.3 (April 2nd 2026)](#1103-april-2nd-2026)
  - [1.10.2 (April 2nd 2026)](#1102-april-2nd-2026)
  - [1.10.1 (April 2nd 2026)](#1101-april-2nd-2026)
  - [1.10.0 (April 2nd 2026)](#1100-april-2nd-2026)
  - [1.9.7 (April 1st 2026)](#197-april-1st-2026)
  - [1.9.6 (April 1st 2026)](#196-april-1st-2026)
  - [1.9.5 (April 1st 2026)](#195-april-1st-2026)
  - [1.9.4 (April 1st 2026)](#194-april-1st-2026)
  - [1.9.3 (April 1st 2026)](#193-april-1st-2026)
  - [1.9.2 (April 1st 2026)](#192-april-1st-2026)
  - [1.9.1 (March 31st 2026)](#191-march-31st-2026)
  - [1.9.0 (March 31st 2026)](#190-march-31st-2026)
  - [1.8.0 (March 31st 2026)](#180-march-31st-2026)
  - [1.7.4 (March 30th 2026)](#174-march-30th-2026)
  - [1.7.3 (March 30th 2026)](#173-march-30th-2026)
  - [1.7.0 (March 30th 2026)](#170-march-30th-2026)
  - [1.5.1 (March 20th 2026)](#151-march-20th-2026)
  - [1.5.0 (March 19th 2026)](#150-march-19th-2026)
  - [1.4.0 (March 18th 2026)](#140-march-18th-2026)
  - [1.3.1 (October 22nd 2025)](#131-october-22nd-2025)
  - [1.2.2 (July 14th 2025)](#122-july-14th-2025)
  - [1.2.0 (April 30th 2025)](#120-april-30th-2025)
  - [1.1.0 (April 28th 2025)](#110-april-28th-2025)
  - [1.0.0 (September 16th 2024)](#100-september-16th-2024)
  - [0.4.12 (September 3rd 2024)](#0412-september-3rd-2024)
    - [Documentation](#documentation)
  - [0.4.11 (September 3rd 2024)](#0411-september-3rd-2024)
    - [Documentation](#documentation-1)
  - [0.4.9 (September 3rd 2024)](#049-september-3rd-2024)
    - [Bug Fixes](#bug-fixes)
  - [0.4.7 (July 9th 2024)](#047-july-9th-2024)
    - [Bug Fixes](#bug-fixes-1)
  - [0.4.6 (July 8th 2024)](#046-july-8th-2024)
    - [Bug Fixes](#bug-fixes-2)
    - [**Improved** Run In Adams](#improved-run-in-adams)
    - [**Added** a warning when debugging Adams View versions \>= 2023](#added-a-warning-when-debugging-adams-view-versions--2023)
    - [Miscellaneous](#miscellaneous)
    - [Development](#development)
  - [0.4.2 (December 6th 2023)](#042-december-6th-2023)
    - [Intellisense support for Adams View Python Interface](#intellisense-support-for-adams-view-python-interface)
      - [**Fixed**: Fixed a bug preventing python intellisense from working properly](#fixed-fixed-a-bug-preventing-python-intellisense-from-working-properly)
  - [0.4.1 (December 1st 2023)](#041-december-1st-2023)
    - [Run in Adams View](#run-in-adams-view)
      - [**Added**: Run selection in Adams View](#added-run-selection-in-adams-view)
      - [**Added**: Run File in Adams View](#added-run-file-in-adams-view)
  - [0.3.0 (September 1st 2023)](#030-september-1st-2023)
    - [Syntax Highlighting](#syntax-highlighting)
    - [Snippets](#snippets)
    - [Improvements to the Adams View Python stub files](#improvements-to-the-adams-view-python-stub-files)
    - [Improvements to Debugger](#improvements-to-debugger)

## 1.14.0 (April 16th 2026)

- **Added** Macro parameter docstrings: place a comment line immediately after a `!$param` definition to document it (e.g. `! The part to analyse`). Docstrings are shown in hover tooltips.
- **Improved** Macro hover now shows a full **Parameters** section listing each parameter's type, default value, and docstring.
- **Added** Hovering an argument name at a macro invocation site shows that specific parameter's type, default, and docstring. Abbreviated argument names are resolved.
- **Improved** Macro Header snippet now includes a parameter placeholder with a docstring comment to demonstrate the convention.

## 1.13.1 (April 15th 2026)

- **Added** Autocomplete and hover documentation support for all `list_info` command variants (`list_info marker`, `list_info part`, `list_info model`, `list_info constraint`, `list_info force`, `list_info geometry`, and 38 others).

## 1.13.0 (April 8th 2026)

- **Improved** Telemetry instrumentation across all extension features. Completion events now include match count, completion type, and trigger kind. Hover events now track miss rate and abbreviation resolution. New events for LSP lifecycle (`lsp_disabled`, `lsp_start_failed`, `lsp_restarted`, `lsp_python_path_resolved`), MCP server registration, and document link detection. Activation event replaced with structured flags instead of a raw config dump. Error paths in debug attachment and resource loading are now instrumented with categorized error types.
- **Fixed** `msc-adams.runInAdams.substituteSelf` config setting was cached at extension startup; it is now read at call time so changes take effect without restarting VS Code.

## 1.12.2 (April 8th 2026)

- **Fixed** Diagnostic underlines now start at the actual indent column (previously started at column 0).
- **Fixed** Suppress noisy LSP warnings and prevent overlapping language server restarts.

## 1.12.1 (April 6th 2026)

- **Improved** On language server startup, discovered UDE definitions are now listed in the output panel alongside the existing macro scan summary.

## 1.12.0 (April 6th 2026)

- **Added** UDE (User-Defined Element) definition scanner. When `msc-adams.linter.scanWorkspaceMacros` is enabled, the linter now scans workspace CMD files for `ude create definition`, `ude copy`, and `ude modify definition` commands. UDE instance child parameters (e.g. `my_ude_instance.damprat`) are registered as known symbols, eliminating false I202/E001 errors on those references.
- **Added** Two new settings: `msc-adams.linter.udePaths` (glob patterns for UDE definition files, default `["**/*.cmd"]`) and `msc-adams.linter.udeIgnorePaths` (patterns to exclude).

## 1.11.1 (April 6th 2026)

- **Fixed** Linter no longer fires false E001 errors for Adams CMD shorthand variable/property assignment syntax (`VarName=value`, `.model.Var=value`, `$model.$name.prop=$val`). The parser now classifies these as `is_property_assignment` statements and skips command-key validation for them.

## 1.11.0 (April 3rd 2026)

- **Added** Hover documentation for macro command invocations in `.cmd` files. Hovering over a macro command now shows its name as a heading and the help string from `!HELP_STRING` (or legacy `!DESCRIPTION`) in the macro file header, or from the `help_string=` argument of an inline `macro create` statement. Multi-line descriptions are rendered as separate paragraphs.
- **Added** `ObjectIndex` for workspace-level object definitions and references. Go-to-definition and find-references now resolve Adams object names (parts, markers, joints, etc.) across the workspace.
- **Fixed** `$variable` navigation correctness — variable references in expressions are now resolved correctly.

## 1.10.4 (April 2nd 2026)

- **Fixed** Adams CMD linter macro registry now updates when `.mac` files are edited, saved, created, or deleted outside the editor — no extension restart required.
- **Fixed** "Ignoring notification for unknown method 'workspace/didChangeConfiguration'" and cancel notification log spam eliminated; linter server now properly handles VS Code settings change notifications.
- **Improved** Changing `msc-adams.linter.macroPaths`, `macroIgnorePaths`, `scanWorkspaceMacros`, or `pythonPath` in settings automatically restarts the language server with the new configuration and fresh file watchers.
- **Fixed** Changing a macro file's `!USER_ENTERED_COMMAND` and saving no longer leaves the old command registered in the macro index.

## 1.10.3 (April 2nd 2026)

- **Fixed** Hover abbreviation resolution now works in production — extension loads `command_schema.json` from bundled libs when the source package is excluded from the installed extension.

## 1.10.2 (April 2nd 2026)

- **Added** Hover documentation for Adams View commands (e.g. hovering over `variable set` shows argument details and documentation).
- **Added** Hover now works with abbreviated command names — `var set` resolves to `variable set`, `mar cre` to `marker create`, etc.
- **Fixed** Hover no longer shows Adams design function docs when the cursor is on a command keyword that happens to share a name (e.g. `view center` no longer triggers the `CENTER()` function doc).
- **Fixed** Hover inside an inline `!` comment correctly returns nothing.

## 1.10.1 (April 2nd 2026)

- **Fixed** Linter no longer emits false-positive I202 for `type_filter` / `type=` arguments (e.g. `type_filter=constraint`, `type_filter=spring`). These take Adams entity type name strings, not object references. An E004 is now emitted instead when the type name is unrecognized.
- **Fixed** Linter no longer emits false-positive I202 for built-in Adams color names that were missing from the symbol table (e.g. `DkGreen`, `Blue_Gray`, `LtBlue`). The full color list from Adams is now registered.
- **Fixed** Linter no longer emits false-positive E001 for `mdi toolbar display` — the command is now in the schema with args `toolbar`, `state` (`on`/`off`), and `top` (`yes`/`no`/`same`).

## 1.10.0 (April 2nd 2026)

- **Added** Hover documentation for Adams View commands in `.cmd` files. Hovering over a command keyword now shows its description, syntax, and argument details sourced from Adams documentation.
- **Added** `command_server` (show/start/stop) commands to the linter schema and documentation.
- **Fixed** Escape quotes in string literals for proper tokenization.
- **Fixed** MCP server now runs workspace macro scan in a background thread to prevent startup hang.

## 1.9.7 (April 1st 2026)

- **Improved** Semantic token highlighting now covers all recognised built-in
  commands (not just user-defined macros). Command key words are highlighted as
  keywords and valid (including abbreviated) argument names are highlighted as
  parameters. Invalid argument names receive no semantic token so they remain
  visually distinct. Abbreviated commands are resolved to their canonical form
  before highlighting. Setting `"semanticHighlighting": true` on the CMD grammar
  ensures VS Code prefers semantic tokens over the static TextMate fallback once
  the LSP server has started.

## 1.9.6 (April 1st 2026)

- **Fixed** Syntax highlighting incorrectly coloured code between `//` string-concatenation operators as a string. Single-quoted strings inside double-quoted strings (and vice versa) no longer open a nested string scope, preventing highlight bleed onto subsequent tokens and lines.

## 1.9.5 (April 1st 2026)

- **Fixed** LSP server crash on startup (`AttributeError: 'SemanticTokensOptions' object
  has no attribute 'token_types'`). The semantic tokens feature registration now passes
  the `SemanticTokensLegend` directly to `@server.feature()` rather than wrapping it in
  `SemanticTokensOptions` — pygls constructs `SemanticTokensOptions` internally.

## 1.9.4 (April 1st 2026)

- **Added** Semantic token highlighting for user-defined macro commands. When
  `msc-adams.linter.scanWorkspaceMacros` is enabled, macro invocations in `.cmd`
  and `.mac` files are now syntax-highlighted using the same colours as built-in
  Adams commands. Command-key tokens receive the `command.command` colour and
  argument names receive the `command.argument` colour.

## 1.9.3 (April 1st 2026)

- **Fixed** Adams CMD Lint MCP server failing to start due to `pydantic_core._pydantic_core`
  C-extension version mismatch. Replaced FastMCP with a pure Python stdlib JSON-RPC 2.0
  implementation — no external `mcp`, `pydantic`, or `pydantic_core` packages are required.

## 1.9.2 (April 1st 2026)

- **Added** `adams_quit_view` MCP tool — saves the current Adams View session to a
  timestamped `.bin` file in the OS temp directory, then shuts down the Adams
  View process via `quit confirmation=no`. Returns the path to the saved file.
- **Added** `adams_restart_view` MCP tool — saves the session, shuts down Adams
  View, waits for the process to fully exit, then relaunches Adams View in the
  same working directory with the Command Server running. Returns the bin file
  path and Command Server port.

## 1.9.1 (March 31st 2026)

- **Fixed** MCP server crash on startup (`ModuleNotFoundError: pydantic_core._pydantic_core`)
  caused by `mcp`/`pydantic_core` being bundled as compiled C extensions. `mcp[cli]` is now an
  optional dependency and must be installed in the user's Python environment.
- **Fixed** Ctrl+hover on multi-word macro commands (e.g. `cdm rn trim`) now underlines the
  entire command key instead of only the word under the cursor.
- **Fixed** Go-to-definition underline range was offset for indented macro invocations.

## 1.9.0 (March 31st 2026)

- **Added** Adams CMD Lint MCP Server — exposes `adams_lint_cmd_text`, `adams_lint_cmd_file`, and
  `adams_lookup_command` as MCP tools so Copilot agents can lint CMD text, lint CMD files, and look
  up command arguments and exclusive groups without Adams View running.

## 1.8.0 (March 31st 2026)

- **Added** Go-to-definition for macro invocations — Ctrl+Click a macro call to jump to its
  `.mac` file or inline `macro create` statement.
- **Added** Find-all-references for macros — right-click a macro definition or invocation to
  find all workspace-wide usages.
- **Added** Persistent macro invocation index for fast cross-file reference queries in large
  workspaces, with incremental updates on file open/save.

## 1.7.4 (March 30th 2026)

- **Fixed** CMD linter false-positive E002 ("Invalid argument") for abbreviated parameter
  names on user-defined macro calls. Adams allows argument names to be shortened to their
  shortest unambiguous prefix (e.g. `mod` for `model_name`); the linter now applies the
  same prefix-matching logic it uses for built-in Adams commands.

## 1.7.3 (March 30th 2026)

- **Fixed** CMD linter E001 "unknown command" hint suggesting `scanWorkspaceMacros` was not
  shown when macro scanning is disabled. The server always created an internal `MacroRegistry`
  instance, which suppressed the hint; the linter now receives `null` when scanning is off.
- **Added** logging to the Adams CMD LSP output panel listing all macro files discovered
  during workspace scan on startup.
- **Added** `wait_for_completion` parameter to the `adams_load_file` MCP tool. When set to
  `false`, the command is sent to Adams View and the tool returns immediately without waiting
  for execution to finish. Use `adams_check_connection` to poll until Adams View is ready
  again. Useful for scripts that run long simulations.
- **Improved** default Adams View command timeout from 10 seconds to 30 seconds.

## 1.7.0 (March 30th 2026)

- **Added** workspace macro scanning: the CMD linter now discovers user-defined macro files in the
  workspace and suppresses false "unknown command" errors for those macros.
- **Added** four new linter settings:
  - `msc-adams.linter.scanWorkspaceMacros` — enable workspace-wide macro file scanning
  - `msc-adams.linter.macroPaths` — glob patterns for macro file discovery (default: `["**/*.mac"]`)
  - `msc-adams.linter.macroIgnorePaths` — glob patterns to exclude from scanning
  - `msc-adams.linter.showMacroHint` — show a hint in E001 messages suggesting macro scanning
- **Added** user-defined macro argument validation (rule E002) — flags arguments passed to a macro
  that are not declared in its parameter list.
- **Fixed** LSP server crash when workspace macro scanning fails during initialization.

## 1.5.1 (March 20th 2026)

- **Fixed** CMD autocomplete for arguments with parenthesized, quoted, and comma-separated values.
- **Fixed** missing `point_name` in argument syntax definitions.

## 1.5.0 (March 19th 2026)

- **Improved** Adams CMD autocomplete with several enhancements:
  - Arguments already used in the current command are no longer suggested again.
  - Multi-line commands using the `&` continuation character are now fully supported — used arguments on previous continuation lines are also filtered out.
  - Argument value completions are now shown for arguments that have a fixed set of allowed values (e.g. `type=`, `friction_enabled=`). When the cursor is after `arg=`, only the valid values are shown.
  - Command and argument documentation from the Adams View help is now shown in the completion detail panel.

## 1.4.0 (March 18th 2026)

- **Added** documentation for all remaining design-time functions from the Adams View Function Builder reference.
- **Fixed** nested and backslash-escaped quotes in CMD string grammar ([Issue 11](https://github.com/bthornton191/adams_vscode/issues/11)).
- **Improved** security: replaced `exec()` with `execFile()`, added reporter null guards.
- **Added** comprehensive test coverage for 6 previously untested modules.
- **Added** copilot instructions for extension development.

## 1.3.1 (October 22nd 2025)

- **Added** configuration option for Adams View connection port.
- **Improved** type hints in `SystemElement` stubs.

## 1.2.2 (July 14th 2025)

- **Fixed** parameter matching in `format_adams_cmd` to ignore single quotes.
- **Improved** type annotations in `Adams.pyi` and `Settings.pyi`.

## 1.2.0 (April 30th 2025)

- **Added** functionality to manage Adams site-packages in Python configuration:
  - Implemented `add_adams_site_packages` to add Adams site-packages to `python.analysis.extraPaths` and `python.autoComplete.extraPaths`.
  - Registered command to load Adams site-packages when configuration changes.

## 1.1.0 (April 28th 2025)

- **Updated** the extension icon to use the old *(original?)* adams logo. This was partly just for
   fun, but also so I don't have to keep updating the icon every time Hexagon changes the logo

- **Added** intellisense support for the following design functions:
    * `file_minus_ext`
    * `str_split`

- **Added** intellisense support for the following cmd commands:
    * `doe_matrix`

- **Improved** intellisense documentation and typing in the following adamspy modules:
    * `Adams`
    * `Contact`
    * `DataElement`
    * `Defaults`
    * `EntityTypes`
    * `Force`
    * `Manager`
    * `Marker`
    * `Object`
    * `Part`


## 1.0.0 (September 16th 2024)
- Official Version 1.0.0 Release. No new features or bug fixes. This release is to mark the extension as stable and ready for production use.

## 0.4.12 (September 3rd 2024)
### Documentation
- **Fixed** a typo in the readme.

## 0.4.11 (September 3rd 2024)
### Documentation
- **Added** A note to the readme about debugging in Adams Car. [More Info](https://github.com/bthornton191/adams_vscode/issues/9#issuecomment-2332435544)
  

## 0.4.9 (September 3rd 2024)
### Bug Fixes
- **Fixed** A bug causing python type hints to only partially work in python 3.10 and higher.

## 0.4.7 (July 9th 2024)
### Bug Fixes
- **Fixed** minor bug preventing the debugger from attaching to Adams View when the command window is selected in Adams View

## 0.4.6 (July 8th 2024)

### Bug Fixes
- **Fixed** syntax highliging issue when a string argument contains an equals sign on a continuation line ([Issue 3](https://github.com/bthornton191/adams_vscode/issues/3))

### **Improved** Run In Adams
- You can now set `msc-adams.runInAdams.substituteSelf` to an existing OR non-existent library 
  (e.g. ".vscode") and the extension will automatically create an empty library by that name replace 
  all occurances of `$_self` with the library name when running the file or selection in Adams View.
  This closes [Issue 4](https://github.com/bthornton191/adams_vscode/issues/4).


### **Added** a warning when debugging Adams View versions >= 2023
A reminder that you may need to import the threading module before attaching the debugger. [More Info](https://github.com/bthornton191/adams_vscode/issues/6#issuecomment-2192053891)

### Miscellaneous
- **Added** clickable links in model and log files
- **Added** a configuration option called `msc-adams.runInAdams.autoLoadAdamspyStubs` allowing users
  to prevent the extension from automatically loading the Adams View Python stubs. This is useful if
  you have your own stubs.

- **Improved** intellisense documentation and typing in the following adamspy modules:
    * Analysis
    * Constraint
    * Contact
    * DataElement
    * DBAccess
    * Force
    * Group
    * Manager
    * Marker
    * Measure
    * Model
    * Part
    * Sensor
    * Simulation
    * SystemElement
    * UDE

- **Added** intellisense support for the following design functions:
    * `dm`
    * `dot`
    * `dx`
    * `dy`
    * `dz`
    * `eig_di`
    * `eig_dr`
    * `eig_vi`
    * `eig_vr`
    * `elementmd`
    * `execute_view_command`
    * `exp`
    * `expr_exists`
    * `expr_reference`
    * `expr_references`
    * `expr_string`
    * `top_spots`
    * `unique` copy
    * `unique_file_name`
    * `unique_full_name`
    * `unique_id`
    * `unique_name_in_hierarchy`
    * `uniquemd`
    * `units_conversion_factor`
    * `units_string`
    * `unwrap`
    * `val`
    * `valat`
    * `vali`
  
### Development
- **Added** a test suite

## 0.4.2 (December 6th 2023)

### Intellisense support for Adams View Python Interface
#### **Fixed**: Fixed a bug preventing python intellisense from working properly


## 0.4.1 (December 1st 2023)

### Run in Adams View

#### **Added**: Run selection in Adams View

This works for both CMD and Python files
![Run CMD Selection in Adams View](https://github.com/bthornton191/adams_vscode/raw/HEAD/doc/run_selection_in_adams.gif)

#### **Added**: Run File in Adams View
This works for both CMD and Python files
![Run CMD File in Adams View](https://github.com/bthornton191/adams_vscode/raw/HEAD/doc/run_file_in_adams.gif)

> [!NOTE]
> For python files, the button is located within the existing python run button stack.
> ![button to run python file in adams](https://github.com/bthornton191/adams_vscode/raw/HEAD/doc/run_python_file_in_adams.png)

## 0.3.0 (September 1st 2023)
### Syntax Highlighting
- **Added**: Syntax highlighting for aview.log files
- **Added**: Syntax highlighting for .msg files

### Snippets
- **Added**: Integer For Loop
  
  ![int_for_loop_snippet](https://github.com/bthornton191/adams_vscode/raw/HEAD/doc/int_for_loop_snippet.gif)

- **Added**: Request
  
  ![request_snippet](https://github.com/bthornton191/adams_vscode/raw/HEAD/doc/req_snippet.gif)

### Improvements to the Adams View Python stub files
Improved type hints and doc strings.

### Improvements to Debugger
Added a **msc-adams.debugOptions** setting allowing options to be passed to the debugger when
attaching to Adams View. Example:
```json
    "msc-adams.debugOptions": {
    
        "justMyCode": false,
        "subProcess": true,
        "logToFile": true
    },
```

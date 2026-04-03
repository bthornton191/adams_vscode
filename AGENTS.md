# MSC Adams VS Code Extension — Agent Instructions

## Overview
This is a VS Code extension for MSC Adams multi-body dynamics simulation software. It provides syntax highlighting, autocomplete, hover documentation, and Adams View process integration (run selection, debugging, launching Adams).

## Language & Module System
- All source files in `src/` are **plain JavaScript** using **CommonJS** (`require` / `exports.functionName`). The `.ts.js` extension is a project convention — do NOT treat them as TypeScript files and do NOT introduce TypeScript syntax, type annotations, or `import`/`export` statements.
- Always use `require()` and `exports.functionName = functionName` throughout `src/` and `test/`.

## Async Patterns
- The codebase uses **callback-based async** (Node.js socket callbacks, `done_callback` parameters). Do not introduce `async`/`await` or convert callbacks to Promises in source files.
- Tests wrap existing callbacks in `new Promise((resolve) => ...)` for compatibility with Mocha's async support — this is intentional and acceptable in `test/` only.

## Adding a Feature
1. Create a new file in `src/` that exports a single factory function: `exports.myFeature = myFeature`.
2. Wire it into `src/extension.ts.js` inside `activate()`.
3. Register any new VS Code command in `package.json` (`contributes.commands`, `contributes.menus`, and if needed, `contributes.keybindings`).
4. Add a corresponding test file in `test/` following the Mocha `suite()` / `test()` pattern.

## Code Patterns
- **Dependency injection**: pass `reporter` (telemetry), `output_channel`, and other dependencies as function parameters — never import them globally. Telemetry is always optional; never let reporting errors block execution.
- **Dynamic `vscode` require**: `const vscode = require("vscode")` inside functions (not at module top level) to honor extension reloads where needed — follow the existing pattern.
- **Configuration access**: use `vscode.workspace.getConfiguration("msc-adams").get(...)` — always read at call time (not cached at startup) so VS Code setting changes are honored without restart.

## Testing
- Tests are Mocha integration tests and require a running Adams View process. The global setup in `test/global_fixture.cjs` launches Adams before tests run.
- Use `suite()` / `test()` (not `describe()` / `it()`).
- Use `test/utils.js` helpers (`waitForAdamsConnection`, socket helpers) rather than reimplementing connection logic.
- Place test working files under `test/working_directory/`.
- **Preferred way to run tests**: Use VS Code's built-in Test Explorer (the beaker icon). This runs tests through the full extension host with Adams available, and results are visible both in the Test Explorer UI and via the `test_failure` tool (which Copilot can query to read results automatically).
- **Copilot test workflow**: After making changes, use `runTests` with specific test file paths to trigger a VS Code test run and get immediate pass/fail results. Use `test_failure` to read detailed failure info. Iterate until all tests pass. This is the **required** workflow — do not use the terminal to run tests.

## Resources
- `resources/adams_design_functions/*.md` — documentation for Adams functions, one file per function. These can be edited manually when documentation needs updating.
- `resources/adams_view_commands/` — Adams command definitions (`structured.json`, `unstructured.json`). Loaded at activation.
- `resources/adamspy/*.pyi` — Python type stubs for the Adams View Python API. Enables Python intellisense.

## Build & Publish
- Build: `vsce package -o adams_vscode.vsix --pre-release` (task: *Build Locally*)
- Publish: VS Code Marketplace via `vsce publish`; Open VSX via `npx ovsx publish`
- Versioning follows semver; update `CHANGELOG.md` with every meaningful change.

## Adams CMD LSP (Python Package)
The `adams-cmd-lsp/` subdirectory contains a fully implemented Python package that provides an LSP server, CLI linter, and MCP server for Adams CMD files. This is a separate codebase from the VS Code extension JS code.

- **Language:** Python 3.9+, standard library + `pygls>=2.0` + `lsprotocol` + `mcp[cli]>=1.0`
- **Build backend:** `setuptools.build_meta` (in `pyproject.toml`). Requires `[tool.setuptools.package-data]` for `data/*.json`.
- **Package layout:** `adams-cmd-lsp/adams_cmd_lsp/` (source), `adams-cmd-lsp/tests/` (tests)
- **Entry points:** `adams-cmd-lsp` (LSP server), `adams-cmd-lint` (CLI linter), `adams-cmd-mcp` (MCP server), `python -m adams_cmd_lsp` (LSP server)
- **Schema:** `adams-cmd-lsp/adams_cmd_lsp/data/command_schema.json` — generated once from Adams source files via `scripts/generate_command_schema.py`, committed to repo
- **Tests:** `cd adams-cmd-lsp && pytest` — pure unit tests, no Adams View required
- **Integration:** The VS Code extension starts the LSP server via `src/cmd_lsp_client.ts.js` using `vscode-languageclient`. The actual Python entry point is `bundled/tool/lsp_server.py`, which bootstraps `sys.path` to include `bundled/libs/` and then runs `adams_cmd_lsp.server.main()`.
- **Bundling:** Run `npm run bundle-lsp` (or the VS Code task *Bundle LSP Dependencies*) to pip-install the package into `bundled/libs/`. This must be done after any Python source changes. The `bundled/libs/` directory is gitignored.
- **Implementation plan:** See `adams-cmd-lsp-plan.md` for the original design document with parsing algorithms, rule definitions, and schema format

## Adams CMD Lint MCP Server
The `adams_cmd_lsp.mcp_server` module exposes Adams CMD linting and schema lookup as MCP tools that Copilot agents can call directly — without needing Adams View running or a `.cmd` file open in the editor.

- **Module:** `adams-cmd-lsp/adams_cmd_lsp/mcp_server.py` — FastMCP server with 3 tools
- **Bootstrap wrapper:** `bundled/tool/mcp_server.py` — bootstraps `sys.path` then calls `adams_cmd_lsp.mcp_server.main()` (same pattern as `lsp_server.py`)
- **Auto-registered:** `src/mcp_server_provider.ts.js` registers it as a `McpStdioServerDefinition` alongside the Adams View MCP server. Agents see it automatically when the extension is active and `msc-adams.linter.enabled` is `true`.
- **Transport:** stdio. Started and managed by VS Code; one process per session.
- **Macro registry:** Built at startup from the same settings keys as the LSP client (`msc-adams.linter.scanWorkspaceMacros`, `msc-adams.linter.macroPaths`, `msc-adams.linter.macroIgnorePaths`). Cached for the server's lifetime.

### Available Tools

| Tool | Description |
|------|-------------|
| `adams_lint_cmd_text` | Lint a string of raw CMD text. Returns JSON diagnostics array. |
| `adams_lint_cmd_file` | Lint a `.cmd` file by absolute path. Returns JSON diagnostics + file path. |
| `adams_lookup_command` | Look up a command's arguments, types, and exclusive groups. Resolves Adams abbreviations. |

### Agent configuration
To grant an agent access to these tools, include `'Adams CMD Linter/*'` in its `tools:` frontmatter list:
```yaml
tools: [..., 'Adams CMD Linter/*']
```

### Tests
`cd adams-cmd-lsp && pytest tests/test_mcp_server.py` — 20 pure unit tests, no Adams View required.

## Recommendations
These are areas worth paying attention to when writing or reviewing code — not hard rules, but patterns that have caused bugs or are easy to get wrong in this codebase.

- **Reporter null guard**: `reporter` defaults to `null`, so consider guarding calls with `if (reporter)` before calling `reporter.sendTelemetryEvent()` or `reporter.sendTelemetryErrorEvent()`.
- **`child_process.exec()` vs `execFile()`**: prefer `execFile(file, args)` when launching external processes with user-controlled or file-system-derived values, since `exec()` spawns a shell and is more vulnerable to injection.
- **`getWordRangeAtPosition()` can return `undefined`**: this happens when the cursor is at whitespace, so null-check before calling `.getText()`.
- **Config `.get()` can return `null`**: when reading array settings (e.g. `python.analysis.extraPaths`), guard before calling array methods.
- **Array comparison**: `===` / `!==` on arrays compares references, not values — use `.join()` or element-by-element comparison instead.
- **Activation-time errors**: `fs.readdirSync()`, `fs.readFileSync()`, and `JSON.parse()` on resource files can throw if the file is missing or corrupted. A try-catch here prevents crashing activation.
- **Provider disposables**: hover, completion, and link providers return a disposable — pushing it to `context.subscriptions` ensures proper cleanup on deactivation.
- **Require paths**: use the full `.ts.js` extension in `require()` calls (e.g. `require("./aview.ts.js")`); the short `.ts` form may not resolve correctly.

## Completion Protocol

After completing a feature or bug fix, follow this protocol before declaring the task done:

1. **Run tests** and confirm they pass for all changed files.
2. **Delegate a code review** to an explore subagent or another appropriate read-only subagent. Instruct it to load the `code-reviewer` skill and review all changed files.
3. **If the reviewer returns REQUEST CHANGES**, address every CRITICAL and WARNING finding. Report any INFO findings to the user but do not fix them unless asked.
4. **Re-run the review** after making fixes until you receive an APPROVE verdict.
5. Only declare the task complete after receiving an **APPROVE** verdict.

Do not skip the review step. Do not declare completion without an APPROVE verdict.

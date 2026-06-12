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

### Test failure: "test process exited unexpectedly"

When **every** test in a run (including unrelated ones) fails with `Test process exited unexpectedly` and no assertion message, this is **not a code problem**. There are two common causes:

1. **A VS Code update is waiting to be installed.** VS Code will restart the extension host mid-run and kill the test process. The fix is to install the pending update and restart VS Code before running tests again. Tell the user: *"It looks like there's a pending VS Code update. Please install it and restart VS Code, then re-run the tests."*

2. **Adams View is not running.** The global fixture (`test/global_fixture.cjs`) kills the test process if it cannot connect to Adams. Tell the user: *"Adams View does not appear to be running. Please start it and re-run the tests."*

If only a **subset** of tests fail with real assertion messages, that is a genuine code failure — investigate and fix normally.

## Resources
- `resources/adams_design_functions/*.md` — documentation for Adams functions, one file per function. These can be edited manually when documentation needs updating.
- `resources/adams_view_commands/` — Adams command definitions (`structured.json`, `unstructured.json`). Loaded at activation.
- `resources/adamspy/` — Git submodule pointing to [adams-python-stubs](https://github.com/bthornton191/adams-python-stubs) (tracks `master`). Contains `.pyi` type stubs for the Adams View Python API. Enables Python intellisense. Run `git submodule update --init` after a fresh clone.

## Build & Publish
- Build: `vsce package -o adams_vscode.vsix --pre-release` (task: *Build Locally*)
- Publish: VS Code Marketplace via `vsce publish`; Open VSX via `npx ovsx publish`
- Versioning follows semver; update `CHANGELOG.md` with every meaningful change.

## Adams CMD LSP (Python Package)
The `adams-cmd-lsp/` subdirectory contains a fully implemented Python package that provides an LSP server and CLI linter for Adams CMD files. This is a separate codebase from the VS Code extension JS code.

- **Language:** Python 3.9+, standard library + `pygls>=2.0` + `lsprotocol`
- **Build backend:** `setuptools.build_meta` (in `pyproject.toml`). Requires `[tool.setuptools.package-data]` for `data/*.json`.
- **Package layout:** `adams-cmd-lsp/adams_cmd_lsp/` (source), `adams-cmd-lsp/tests/` (tests)
- **Entry points:** `adams-cmd-lsp` (LSP server), `adams-cmd-lint` (CLI linter), `python -m adams_cmd_lsp` (LSP server)
- **Schema:** `adams-cmd-lsp/adams_cmd_lsp/data/command_schema.json` — generated once from Adams source files via `scripts/generate_command_schema.py`, committed to repo
- **Tests:** `cd adams-cmd-lsp && pytest` — pure unit tests, no Adams View required
- **Integration:** The VS Code extension starts the LSP server via `src/cmd_lsp_client.ts.js` using `vscode-languageclient`. The actual Python entry point is `bundled/tool/lsp_server.py`, which bootstraps `sys.path` to include `bundled/libs/` and then runs `adams_cmd_lsp.server.main()`.
- **Bundling:** Run `npm run bundle-lsp` (or the VS Code task *Bundle LSP Dependencies*) to pip-install the package into `bundled/libs/`. This must be done after any Python source changes. The `bundled/libs/` directory is gitignored.

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
2. **If Python (adams-cmd-lsp) files were changed**, re-bundle: run the *Bundle LSP Dependencies* task (or `python -m pip install --target .\bundled\libs --no-cache-dir .\adams-cmd-lsp` from the workspace root). Without this step the extension dev host will not pick up the changes.
3. **Delegate a code review** to an explore subagent or another appropriate read-only subagent. Instruct it to load the `code-reviewer` skill and review all changed files.
4. **If the reviewer returns REQUEST CHANGES**, address every CRITICAL and WARNING finding. Report any INFO findings to the user but do not fix them unless asked.
5. **Re-run the review** after making fixes until you receive an APPROVE verdict.
6. Only declare the task complete after receiving an **APPROVE** verdict.

Do not skip the review step. Do not declare completion without an APPROVE verdict.

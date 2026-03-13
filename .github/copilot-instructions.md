# MSC Adams VS Code Extension — Copilot Instructions

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

## Resources
- `resources/adams_design_functions/*.md` — documentation for Adams functions, one file per function. These can be edited manually when documentation needs updating.
- `resources/adams_view_commands/` — Adams command definitions (`structured.json`, `unstructured.json`). Loaded at activation.
- `resources/adamspy/*.pyi` — Python type stubs for the Adams View Python API. Enables Python intellisense.

## Build & Publish
- Build: `vsce package -o adams_vscode.vsix --pre-release` (task: *Build Locally*)
- Publish: VS Code Marketplace via `vsce publish`; Open VSX via `npx ovsx publish`
- Versioning follows semver; update `CHANGELOG.md` with every meaningful change.

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

# Adams View MCP Server — Implementation Plan

## Overview

Build a TypeScript MCP (Model Context Protocol) server that bridges AI agent
harnesses to a running Adams View session via its TCP command server protocol.
The server lives at `adams-view-mcp-server/` inside this repo and is designed
to be split into its own repository later while still being bundled inside the
`savvyanalyst.msc-adams` VS Code extension VSIX.

---

## Goals

- Expose Adams View operations (run code, query state, manage models) as MCP
  tools consumable by any MCP-compatible agent harness (Claude Desktop, OpenCode,
  Cursor, custom harnesses, etc.)
- Work standalone (outside VS Code) with zero VS Code dependency
- Bundle cleanly inside the VS Code extension VSIX as a single-file esbuild
  bundle (no `node_modules` required at runtime)
- Be straightforward to split into its own npm package / GitHub repo later

---

## Repository Layout

```
adams_vscode/                           ← existing VS Code extension repo
└── adams-view-mcp-server/              ← NEW: self-contained MCP server package
    ├── package.json
    ├── tsconfig.json
    ├── src/
    │   ├── index.ts                    ← McpServer init, tool wiring, stdio transport
    │   ├── client.ts                   ← Promise-based TCP client (no vscode dependency)
    │   ├── constants.ts                ← DEFAULT_PORT, CHARACTER_LIMIT, TIMEOUT_MS
    │   └── tools/
    │       ├── cmd.ts                  ← adams_run_cmd, adams_run_python, adams_load_file
    │       ├── query.ts                ← adams_evaluate_expression, adams_get_model_names,
    │       │                               adams_get_working_directory, adams_check_connection
    │       ├── model.ts                ← adams_delete_model
    │       ├── log.ts                  ← adams_read_session_log
    │       └── simulation.ts           ← adams_create_simulation_script, adams_submit_simulation
    ├── tests/
    │   ├── client.test.ts              ← TCP client unit tests (mock server)
    │   ├── tools.test.ts               ← Tool handler unit tests
    │   └── helpers.ts                  ← Mock Adams TCP server for tests
    └── dist/                           ← esbuild output (gitignored)
```

The package is **fully independent** of the repo root's `package.json` — it is
**not** an npm workspace member. This avoids interfering with the VS Code
extension's packaging (`vsce`) and makes the future repo split a pure copy
with no structural changes.

A convenience script will be added to the root `package.json`:

```json
"build-mcp": "npm run build --prefix adams-view-mcp-server"
```

---

## Adams View TCP Wire Protocol

The MCP server communicates with Adams View's command server over a raw TCP
socket. The default port is `5002` (configurable via `ADAMS_LISTENER_PORT`
environment variable).

**One TCP connection per request** — connect, send, receive, destroy.

### Execute a command (`cmd`)

```
CLIENT → "cmd <adams_view_command_text>"
SERVER → "cmd: 0"       ← success
         anything else  ← error (include raw response in error message)
CLIENT → destroy socket
```

### Evaluate an expression (`query`) — two round trips

```
CLIENT → "query <adams_expression>"
SERVER → "<ignored>: <type>: <count>"   (type = int | float | str, count = N)
CLIENT → "OK"
SERVER → "<value>"  or  "<v1>, <v2>, ..."  (comma-space separated if count > 1)
CLIENT → destroy socket
```

Type coercion rules:
- `int`  → `parseInt()`
- `float` → `parseFloat()`
- `str` where value is `on/off/yes/no` → boolean
- `str` otherwise → trimmed string
- count > 1 → array of the above

### Heartbeat / readiness check

- TCP connect success → Adams process is running
- `query db_exists('.mdi')` returning `1` → Adams session is fully ready

---

## TCP Protocol Implementation Notes

These notes are derived from examining the existing implementation in
`src/aview.ts.js` and are critical for a correct reimplementation:

1. **No trailing newline** — The existing (working) code sends `cmd <text>` and
   `query <expression>` **without** a trailing `\n`. Do not add one.

2. **Description parsing regex** — Adams returns the query description as e.g.
   `query: str: 1`. The existing code splits on `/[ :]+/` (one or more spaces
   or colons), then takes `result[1]` as type and `result[2]` as count. This
   handles variable whitespace in the response.

3. **No response buffering** — The existing code assumes the full response
   arrives in a single `data` event. This works for small responses over
   localhost but is technically fragile. The new implementation should
   accumulate chunks until the socket closes or a complete response is
   detected, to be safe.

4. **Nested `data` listeners** — The existing `evaluate_exp` adds a second
   `data` listener inside the first one's callback (creating two active
   listeners). The Promise-based rewrite should handle this more cleanly as:
   await first response → send "OK" → await second response → destroy.

5. **No timeouts in existing code** — The current extension has zero timeout
   handling. The MCP server adds a 10-second timeout, which is a deliberate
   improvement.

---

## `client.ts` — Core TCP Abstraction

Reimplements the protocol from `src/aview.ts.js` as `Promise`-returning async
functions with **no `vscode` dependency**.

```typescript
// Port resolution (standalone, no vscode)
function getPort(): number {
  return parseInt(process.env.ADAMS_LISTENER_PORT ?? "5002");
}

// Returns void on success, throws on error or unexpected response
async function executeCmd(cmd: string): Promise<void>

// Returns typed scalar or array on success, throws on error
async function evaluateExp(exp: string): Promise<AdamsValue | AdamsValue[]>

// Returns true if Adams View TCP port is reachable and session is ready
async function checkConnection(): Promise<boolean>

// Exported for unit testing
function parseDescription(response: string): [string, number]
function parseData(response: string, type: string, count: number): AdamsValue | AdamsValue[]
```

`AdamsValue` is defined as `string | number | boolean`.

All functions time out after **10 seconds** and throw a descriptive error if
Adams View is unreachable, pointing the user to
`Tools > Command Server` in Adams View.

The `parseDescription` and `parseData` functions are exported separately to
enable direct unit testing of the parsing logic.

---

## Tool Inventory (V1 — 11 tools)

All tool names are prefixed with `adams_` to avoid collisions when used
alongside other MCP servers.

### Read-only / diagnostic tools

| Tool name | Adams operation | Description |
|---|---|---|
| `adams_check_connection` | TCP connect + `query db_exists('.mdi')` | Returns whether Adams View is running and ready. Use this first to verify connectivity before other operations. |
| `adams_get_working_directory` | `query getcwd()` | Returns Adams View's current working directory. |
| `adams_get_model_names` | `query UNIQUE_NAME_IN_HIERARCHY('.model')` | Returns the names of all models currently loaded in the session. |
| `adams_evaluate_expression` | `query <expression>` | Evaluates any Adams View expression and returns its typed result. |
| `adams_read_session_log` | `gui_utl_log_fil_fil()` + temp file | Reads the Adams View session log with optional filtering by message type and search string. Returns log text content. Useful for retrieving `print()` output from Python scripts, diagnosing errors, and reviewing command history. |

### Destructive / mutating tools

| Tool name | Adams operation | Description |
|---|---|---|
| `adams_run_cmd` | `cmd <text>` | Sends arbitrary Adams CMD text to Adams View and returns success or error. |
| `adams_run_python` | temp file + `cmd file python read file_name="<path>"` | Executes a Python snippet inside Adams View. Writes a temporary `.py` file, sends `file python read`, then deletes the temp file. Python `print()` output is not returned directly — use `adams_read_session_log` to retrieve it. |
| `adams_load_file` | `cmd file command read file_name="<path>"` or `cmd file python read file_name="<path>"` | Loads a `.cmd` or `.py` file from disk into Adams View. File type is inferred from extension; `.cmd` uses `file command read`, `.py` uses `file python read`. |
| `adams_delete_model` | `cmd model delete model=<name>` | Deletes the named model from the Adams View session. Accepts either bare name (`model_name`) or dot-prefixed path (`.model_name`) — normalized internally. |

### Simulation tools

| Tool name | Adams operation | Description |
|---|---|---|
| `adams_create_simulation_script` | `simulation script create` + `file adams_data_set write` + `simulation script write_acf` | Creates a solver simulation script in Adams View from an array of Adams Solver commands, then exports the model `.adm` dataset and `.acf` command file to a specified directory. The script remains in the model for reuse. Returns the paths to the exported files. |
| `adams_submit_simulation` | `mdi.bat ru-s <acf>` / `mdi -c ru-s <acf> exit` (detached process) | Runs Adams Solver standalone on an existing `.acf` file. The solver is launched as a detached background process and the tool returns immediately with the expected output file paths (`.msg`, `.res`, `.req`, `.gra`). The agent can read the `.msg` file to monitor progress. |

### Why `adams_run_python` uses a temp file

Adams View's `cmd` protocol sends a single-line payload. Python snippets are
inherently multi-line and there is no Adams CMD equivalent of "execute this
Python string directly" — `file python read` is the only supported mechanism.
The temp file is written with Node's `fs.mkdtemp` + `fs.writeFile`, used, then
deleted in a `finally` block. The temp directory is `os.tmpdir()` so the OS
handles cleanup if the process is killed mid-execution. No external `tmp`
package is needed.

---

## Tool Input Schemas (Zod)

```typescript
// adams_run_cmd
{ cmd: z.string().min(1).describe("Adams View command text to execute") }

// adams_run_python
{ code: z.string().min(1).describe("Python code to execute inside Adams View") }

// adams_load_file
{ file_path: z.string().min(1).describe("Absolute path to the .cmd or .py file to load") }

// adams_delete_model
{ model_name: z.string().min(1).describe("Model name, e.g. 'my_model' or '.my_model'") }

// adams_evaluate_expression
{ expression: z.string().min(1).describe("Adams View expression to evaluate, e.g. 'getcwd()'") }

// adams_read_session_log
{
  filter_by_type: z.boolean().default(false)
    .describe("Enable filtering by message type. When false, all message types are included."),
  show_infos: z.boolean().default(true)
    .describe("Include info messages (only applies when filter_by_type is true)"),
  show_warnings: z.boolean().default(true)
    .describe("Include warning messages (only applies when filter_by_type is true)"),
  show_errors: z.boolean().default(true)
    .describe("Include error messages (only applies when filter_by_type is true)"),
  show_fatals: z.boolean().default(true)
    .describe("Include fatal messages (only applies when filter_by_type is true)"),
  suppress_duplicates: z.boolean().default(false)
    .describe("Remove duplicate log lines"),
  filter_string: z.string().default("")
    .describe("Only show lines containing this string. Empty string means no string filter.")
}

// adams_create_simulation_script
{
  model_name: z.string().min(1)
    .describe("Model name, e.g. 'my_model' or '.my_model'"),
  solver_commands: z.array(z.string().min(1)).min(1)
    .describe("Array of Adams Solver commands that define the simulation, e.g. ['SIMULATE/DYNAMIC, END=1.0, DTOUT=0.01']. Mutually exclusive with type/end_time/step_size — these commands fully control the simulation."),
  script_name: z.string().optional()
    .describe("Name for the simulation script object within the model. Defaults to 'mcp_sim_script'."),
  output_directory: z.string().min(1)
    .describe("Absolute path to the directory where .adm and .acf files will be written")
}

// adams_submit_simulation
{
  acf_path: z.string().min(1)
    .describe("Absolute path to the .acf (Adams Command File) to run. The .adm file must be in the same directory.")
}

// adams_check_connection, adams_get_working_directory, adams_get_model_names
// → no inputs (empty schema)
```

All schemas use `.strict()` to reject extra fields.

---

## `adams_read_session_log` — Detailed Design

This tool uses the undocumented Adams View function `gui_utl_log_fil_fil()` to
extract and filter the session log.

### `gui_utl_log_fil_fil` — Reverse-Engineered API

```
gui_utl_log_fil_fil(output_file_path, filter_string, flags) → int (status)
```

**Parameters:**
1. `output_file_path` (string) — path to write filtered log content
2. `filter_string` (string) — text to match lines against (only used when bit 6 is set)
3. `flags` (int) — bitmask controlling filtering behaviour

**Flag bitmask:**

| Bit | Value | Meaning |
|-----|-------|---------|
| 0 | 1 | Enable type-level filtering (bits 1–4 only apply when this is set) |
| 1 | 2 | Show info messages |
| 2 | 4 | Show warnings |
| 3 | 8 | Show errors |
| 4 | 16 | Show fatals |
| 5 | 32 | Suppress duplicate lines |
| 6 | 64 | Enable string filtering (use `filter_string` parameter) |

**Return codes:**

| Code | Meaning |
|------|---------|
| 0 | Success — filtered log written to output file |
| 1 | No log file is open in the current session |
| 2 | Cannot open the output file for writing |
| 3 | A log file line exceeds the internal length limit |

### Implementation Steps

1. Generate a temp file path using Node's `os.tmpdir()` + `crypto.randomUUID()`
2. Compute the flags bitmask from boolean inputs:
   ```typescript
   let flags = 0;
   if (filter_by_type)      flags |= 1;
   if (show_infos)          flags |= 2;
   if (show_warnings)       flags |= 4;
   if (show_errors)         flags |= 8;
   if (show_fatals)         flags |= 16;
   if (suppress_duplicates) flags |= 32;
   if (filter_string !== "") flags |= 64;
   ```
3. Call Adams View to run the function and store the return code in a variable:
   ```
   cmd variable set variable_name=.mcp_log_stat &
     integer_value=(eval(gui_utl_log_fil_fil("<tmp_path>", "<filter_string>", <flags>)))
   ```
4. Read the return code: `query .mcp_log_stat`
5. Clean up the Adams variable: `cmd variable delete variable_name=.mcp_log_stat`
6. If status is `0`, read the temp file with Node's `fs.readFile()`
7. Delete the temp file with `fs.unlink()` (in a `finally` block)
8. Truncate to `CHARACTER_LIMIT` if needed, appending a note indicating truncation
9. Return the log content as the tool result text

### Error Mapping

| Status | Tool error message |
|--------|--------------------|
| 1 | `"No log file is open in the current Adams View session."` |
| 2 | `"Could not write temporary log file. Check file system permissions."` |
| 3 | `"A log file line exceeds the internal Adams length limit."` |

---

## `adams_create_simulation_script` — Detailed Design

Creates a solver script inside Adams View from an array of Adams Solver
commands, exports the model dataset (`.adm`) and the solver command file
(`.acf`) to disk.

### Adams CMD Array Argument Syntax

The `solver_commands` parameter of `simulation script create` accepts an array
of strings in Adams CMD syntax — comma-separated, each element quoted:

```
simulation script create &
  sim_script_name=.my_model.mcp_sim_script &
  solver_commands="SIMULATE/DYNAMIC, END=1.0, DTOUT=0.01", &
                  "STOP"
```

The tool joins the input array into this format:
```typescript
const solverCommandsArg = solverCommands
  .map(c => `"${c.replace(/"/g, '\\"')}"`)
  .join(", ");
```

### Implementation Steps

1. Normalize model name (ensure dot prefix): `my_model` → `.my_model`
2. Determine script name: `.<model_name>.<script_name>` (default `mcp_sim_script`)
3. Validate output directory exists (Node `fs.access()`)
4. Create the simulation script in Adams View:
   ```
   cmd simulation script create &
     sim_script_name=.<model_name>.<script_name> &
     solver_commands=<formatted_array>
   ```
5. Export the model dataset:
   ```
   cmd file adams_data_set write &
     model_name=.<model_name> &
     file_name="<output_directory>/<model_name>.adm"
   ```
6. Write the solver command file:
   ```
   cmd simulation script write_acf &
     sim_script_name=.<model_name>.<script_name> &
     file_name="<output_directory>/<model_name>.acf"
   ```
7. Return a structured result:
   ```json
   {
     "adm_path": "<output_directory>/<model_name>.adm",
     "acf_path": "<output_directory>/<model_name>.acf",
     "script_name": ".<model_name>.<script_name>"
   }
   ```

The simulation script remains in the Adams View model for reuse or inspection.
The agent can pass the `acf_path` directly to `adams_submit_simulation`.

### Error Handling

- If the model doesn't exist, `simulation script create` will fail and the raw
  Adams error is returned as the tool error.
- If the output directory doesn't exist, the tool returns an error before
  touching Adams View.
- If any Adams step fails, the tool attempts cleanup (delete the partially
  created script) before returning the error.

---

## `adams_submit_simulation` — Detailed Design

Runs Adams Solver as a standalone detached process on an existing `.acf` file.
Returns immediately — the solver runs in the background.

### Platform-Specific Invocation

| | Windows | Linux |
|---|---|---|
| Executable | `mdi.bat` | `mdi` |
| Location | `<TOPDIR>/common/mdi.bat` | `<TOPDIR>/mdi` |
| Arguments | `ru-s <acf_filename>` | `-c ru-s <acf_filename> exit` |

The `-c` flag on Linux passes the run command to `mdi`. The trailing `exit`
argument tells `mdi` to terminate after the solve completes (without it, `mdi`
would hang waiting for more commands). On Windows, `mdi.bat ru-s` exits
naturally when the solve finishes.

Both platforms **block until the simulation completes**. The tool uses
`detached: true` + `stdio: "ignore"` + `solver.unref()` so the MCP server
returns immediately without waiting.

### Implementation Steps

1. Validate that the `.acf` file exists (Node `fs.access()`)
2. Derive the working directory: `path.dirname(acf_path)`
3. Derive the model name: `path.basename(acf_path, ".acf")`
4. Get the Adams installation root from Adams View:
   ```
   query GETENV("TOPDIR")
   ```
5. Resolve the solver executable:
   ```typescript
   const isWindows = process.platform === "win32";
   const mdiPath = isWindows
     ? path.join(topdir, "common", "mdi.bat")
     : path.join(topdir, "mdi");
   const args = isWindows
     ? ["ru-s", acfFilename]
     : ["-c", "ru-s", acfFilename, "exit"];
   ```
6. Validate that the resolved `mdi` / `mdi.bat` exists
7. Spawn the solver as a detached background process:
   ```typescript
   const solver = spawn(mdiPath, args, {
     cwd: workingDirectory,  // .adm and .acf must be in this directory
     detached: true,
     stdio: "ignore"
   });
   solver.unref();  // allow MCP server to return without waiting
   ```
8. Return immediately with output file information:
   ```json
   {
     "pid": 12345,
     "working_directory": "<dir>",
     "acf_path": "<dir>/<model>.acf",
     "adm_path": "<dir>/<model>.adm",
     "msg_path": "<dir>/<model>.msg",
     "res_path": "<dir>/<model>.res",
     "req_path": "<dir>/<model>.req",
     "gra_path": "<dir>/<model>.gra",
     "message": "Adams Solver started (PID 12345). Monitor progress by reading the .msg file. The simulation is complete when the .msg file contains 'Simulation complete' or the process exits."
   }
   ```

### Error Handling

| Condition | Tool error message |
|-----------|--------------------|
| `.acf` file not found | `"ACF file not found: <path>"` |
| Adams View not connected (can't query TOPDIR) | `"Could not determine Adams installation directory. Is Adams View running? Run adams_check_connection first."` |
| `mdi` / `mdi.bat` not found at resolved path | `"Adams Solver executable not found at: <path>. Verify your Adams installation."` |
| Spawn failure | `"Failed to launch Adams Solver: <os error message>"` |

---

## Error Handling

All tools return errors as tool-level results (not protocol-level errors), per
MCP best practices. The `isError: true` flag is set.

Connection errors produce a message of the form:

```
Error: Could not connect to Adams View on port 5002.
Make sure Adams View is open and the Command Server is running.
In Adams View: Tools > Command Server > Start
```

Unexpected `cmd` responses produce:

```
Error: Adams View returned an unexpected response: "<raw response>"
Expected "cmd: 0" for success.
```

---

## Transport

V1 transport is **stdio only** (Adams View runs locally, single user).

```
StdioServerTransport → reads from stdin, writes to stdout
```

stdio servers must not log to stdout; all logging goes to stderr.

**Future enhancement:** A streamable HTTP transport (`StreamableHTTPServerTransport`)
may be added later for remote/multi-client scenarios. This is out of scope for
V1 to avoid unnecessary complexity and security concerns (an open HTTP port
with `adams_run_cmd` access requires authentication).

---

## Build Strategy — esbuild Single-File Bundle

The MCP server uses **esbuild** to produce a single self-contained JavaScript
file at `dist/index.js`. This bundles all dependencies (`@modelcontextprotocol/sdk`,
`zod`) inline, so no `node_modules` directory is needed at runtime.

Benefits:
- VSIX only needs to include `dist/index.js` — no `node_modules` directory
- Faster startup (single file, no module resolution overhead)
- Simplifies the future repo split (publish the single file)
- Works identically in dev and installed contexts

TypeScript compilation (`tsc`) is used **only for type-checking** (`--noEmit`),
not for producing output files.

---

## `package.json` (adams-view-mcp-server)

```json
{
  "name": "adams-view-mcp-server",
  "version": "0.1.0",
  "description": "MCP server for MSC Adams View — exposes Adams View operations to AI agent harnesses",
  "main": "dist/index.js",
  "bin": { "adams-view-mcp-server": "dist/index.js" },
  "scripts": {
    "build": "esbuild src/index.ts --bundle --platform=node --target=node18 --format=cjs --outfile=dist/index.js",
    "typecheck": "tsc --noEmit",
    "dev": "tsx watch src/index.ts",
    "start": "node dist/index.js",
    "test": "vitest run",
    "test:watch": "vitest",
    "clean": "rm -rf dist"
  },
  "engines": { "node": ">=18" },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.6.1",
    "zod": "^3.23.8"
  },
  "devDependencies": {
    "@types/node": "^22.10.0",
    "esbuild": "^0.24.0",
    "tsx": "^4.19.2",
    "typescript": "^5.7.2",
    "vitest": "^2.1.0"
  }
}
```

Notes:
- No `"type": "module"` — the bundle format is **CJS**. ESM + a shebang caused
  `SyntaxError: Invalid or unexpected token` because esbuild's `--banner:js`
  inserted the shebang inside the module wrapper. CJS avoids this; esbuild
  preserves the `#!/usr/bin/env node` shebang from `src/index.ts` line 1.
- No `--banner:js` flag in the build script — the shebang in source is sufficient.
- No `axios` — all I/O goes through Node's built-in `net` module (TCP to
  Adams View directly). No HTTP calls.

---

## `tsconfig.json` (adams-view-mcp-server)

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "noEmit": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "tests"]
}
```

Note: `noEmit: true` because esbuild handles the actual compilation. `tsc` is
used only for type-checking via `npm run typecheck`.

---

## VS Code Extension Integration (now)

The VSIX bundles only `adams-view-mcp-server/dist/index.js` — a single
self-contained file with all dependencies inlined by esbuild. No `node_modules`
directory is needed.

The `.vscodeignore` will be updated:

```
# MCP server: include only the bundled dist output
adams-view-mcp-server/src/**
adams-view-mcp-server/tests/**
adams-view-mcp-server/node_modules/**
adams-view-mcp-server/tsconfig.json
!adams-view-mcp-server/dist/**
!adams-view-mcp-server/package.json
```

The extension can spawn the MCP server as a subprocess by resolving the path:

```javascript
function getMcpServerPath(context) {
  const bundled = path.join(
    context.extensionPath, 'adams-view-mcp-server', 'dist', 'index.js'
  );
  if (fs.existsSync(bundled)) return bundled;
  throw new Error('adams-view-mcp-server not found');
}
```

**Note:** Wiring the extension to actually spawn/register the MCP server is a
separate task and out of scope for the initial MCP server implementation.

---

## Future: Splitting to Own Repo

When ready to split:

1. Move `adams-view-mcp-server/` to a new GitHub repo
2. Publish to npm as `adams-view-mcp-server`
3. In this repo: `npm install adams-view-mcp-server --save`
4. Update `.vscodeignore` to include
   `!node_modules/adams-view-mcp-server/dist/**`
5. Update the path-resolution helper to check `node_modules/` first

No structural changes to the MCP server itself are needed.

---

## Known Limitations (V1)

1. **Python `print()` output requires extra step** — `print()` output from
   `adams_run_python` is not returned directly through the TCP protocol. It is
   written to the Adams View session log. Use `adams_read_session_log` after
   execution to retrieve it.

2. **Serial command execution** — Adams View processes TCP commands serially on
   a single port. Concurrent tool calls from multiple agents will be serialized
   by Adams View itself. This is not a bug but worth noting for multi-agent
   scenarios.

3. **No streaming output for in-process simulation** — Long-running Adams
   commands sent via `adams_run_cmd` (e.g. `simulation single_run transient`)
   block until complete with no progress reporting. For simulations, prefer
   `adams_create_simulation_script` + `adams_submit_simulation`, which run the
   solver out-of-process and allow monitoring via the `.msg` file.

4. **Solver process is fire-and-forget** — `adams_submit_simulation` launches
   the solver as a detached process and returns immediately. If the solver
   crashes, the only indication is in the `.msg` file. There is no built-in
   mechanism to wait for completion or receive failure notifications.

5. **`gui_utl_log_fil_fil` is undocumented** — The session log function is an
   internal Adams View API. Its behaviour may change between Adams versions
   without notice.

---

## Implementation Checklist

### Phase 1 — Scaffold ✅
- [x] Create `adams-view-mcp-server/` directory
- [x] Write `package.json` (with esbuild, vitest; CJS format, no `"type":"module"`)
- [x] Write `tsconfig.json` (`noEmit: true`, excludes `tests/`)
- [x] Add `"build-mcp"` script to root `package.json`
- [x] Add `adams-view-mcp-server/dist/` and `adams-view-mcp-server/node_modules/` to `.gitignore`

### Phase 2 — Core infrastructure ✅
- [x] Implement `src/constants.ts` (`DEFAULT_PORT`, `CHARACTER_LIMIT`, `TIMEOUT_MS`)
- [x] Implement `src/client.ts` (`executeCmd`, `evaluateExp`, `checkConnection`, `getPort`, `parseDescription`, `parseData`)
- [x] Write `src/index.ts` skeleton (McpServer init + stdio transport)

### Phase 3 — Core tools (8 tools) ✅
- [x] Implement `src/tools/query.ts`
  - `adams_check_connection`
  - `adams_get_working_directory`
  - `adams_get_model_names`
  - `adams_evaluate_expression`
- [x] Implement `src/tools/cmd.ts`
  - `adams_run_cmd`
  - `adams_run_python` (temp file pattern, `os.tmpdir()`)
  - `adams_load_file`
- [x] Implement `src/tools/model.ts`
  - `adams_delete_model`
- [x] Wire all tools into `src/index.ts`

### Phase 4 — Session log tool ✅
- [x] Implement `src/tools/log.ts`
  - `adams_read_session_log` (`gui_utl_log_fil_fil` wrapper, flag bitmask, Node temp file)
- [x] Wire into `src/index.ts`

### Phase 5 — Simulation tools ✅
- [x] Implement `src/tools/simulation.ts`
  - `adams_create_simulation_script` (`solver_commands` array → Adams CMD array syntax, `.adm` export, `.acf` write)
  - `adams_submit_simulation` (`GETENV("TOPDIR")` resolution, platform-aware `mdi` path and args, detached spawn)
- [x] Wire into `src/index.ts`

### Phase 6 — Unit tests ✅
- [x] Create `tests/helpers.ts` — mock Adams TCP server using `net.createServer()`
- [x] Create `tests/client.test.ts` — test `executeCmd`, `evaluateExp`, `checkConnection`, `parseDescription`, `parseData`
- [x] Create `tests/tools.test.ts` — test tool handlers with mocked client functions
- [x] `npm test` passes — **35/35 tests passing**

### Phase 7 — Build & verify ✅
- [x] `npm install` in `adams-view-mcp-server/`
- [x] `npm run typecheck` passes without errors
- [x] `npm run build` produces `dist/index.js` (~734 KB single file, all deps bundled)
- [x] `node dist/index.js` starts without crashing (no Adams required)
- [x] Verified `dist/index.js` contains no `require("vscode")` references
- [x] Updated `.vscodeignore` to bundle `dist/`

### Phase 8 — Evaluations ✅
- [x] Write evaluation XML per `mcp-builder` evaluation guide (`evaluation.xml`)

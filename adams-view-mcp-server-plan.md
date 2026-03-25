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
- Bundle cleanly inside the VS Code extension VSIX
- Be straightforward to split into its own npm package / GitHub repo later

---

## Repository Layout

```
clever-island/                          ← existing VS Code extension repo
└── adams-view-mcp-server/              ← NEW: self-contained MCP server package
    ├── package.json
    ├── tsconfig.json
    ├── src/
    │   ├── index.ts                    ← McpServer init, tool wiring, transport entry point
    │   ├── client.ts                   ← Promise-based TCP client (no vscode dependency)
    │   ├── constants.ts                ← DEFAULT_PORT, CHARACTER_LIMIT
    │   └── tools/
    │       ├── cmd.ts                  ← adams_run_cmd, adams_run_python, adams_load_file
    │       ├── query.ts                ← adams_evaluate_expression, adams_get_model_names,
    │       │                               adams_get_working_directory, adams_check_connection
    │       └── model.ts                ← adams_delete_model
    └── dist/                           ← compiled output (gitignored)
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
CLIENT → "cmd <adams_view_command_text>\n"
SERVER → "cmd: 0"       ← success
         anything else  ← error (include raw response in error message)
CLIENT → destroy socket
```

### Evaluate an expression (`query`) — two round trips

```
CLIENT → "query <adams_expression>\n"
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
```

`AdamsValue` is defined as `string | number | boolean`.

All functions time out after **10 seconds** and throw a descriptive error if
Adams View is unreachable, pointing the user to
`Tools > Command Server` in Adams View.

---

## Tool Inventory (V1 — 8 tools)

All tool names are prefixed with `adams_` to avoid collisions when used
alongside other MCP servers.

### Read-only tools

| Tool name | Adams operation | Description |
|---|---|---|
| `adams_check_connection` | TCP connect + `query db_exists('.mdi')` | Returns whether Adams View is running and ready. Use this first to verify connectivity before other operations. |
| `adams_get_working_directory` | `query getcwd()` | Returns Adams View's current working directory. |
| `adams_get_model_names` | `query UNIQUE_NAME_IN_HIERARCHY('.model')` | Returns the names of all models currently loaded in the session. |
| `adams_evaluate_expression` | `query <expression>` | Evaluates any Adams View expression and returns its typed result. |

### Destructive / mutating tools

| Tool name | Adams operation | Description |
|---|---|---|
| `adams_run_cmd` | `cmd <text>` | Sends arbitrary Adams CMD text to Adams View and returns success or error. |
| `adams_run_python` | temp file + `cmd file python read file_name="<path>"` | Executes a Python snippet inside Adams View. Writes a temporary `.py` file, sends `file python read`, then deletes the temp file. |
| `adams_load_file` | `cmd file command read file_name="<path>"` or `cmd file python read file_name="<path>"` | Loads a `.cmd` or `.py` file from disk into Adams View. File type is inferred from extension; `.cmd` uses `file command read`, `.py` uses `file python read`. |
| `adams_delete_model` | `cmd model delete model=<name>` | Deletes the named model from the Adams View session. Accepts either bare name (`model_name`) or dot-prefixed path (`.model_name`) — normalized internally. |

### Why `adams_run_python` uses a temp file

Adams View's `cmd` protocol sends a single-line payload. Python snippets are
inherently multi-line and there is no Adams CMD equivalent of "execute this
Python string directly" — `file python read` is the only supported mechanism.
The temp file is written with Node's `fs.mkdtemp` + `fs.writeFile`, used, then
deleted in a `finally` block. No external `tmp` package is needed.

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

// adams_check_connection, adams_get_working_directory, adams_get_model_names
// → no inputs (empty schema)
```

All schemas use `.strict()` to reject extra fields.

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

Primary transport is **stdio** (Adams View runs locally, single user).
The transport is switchable to streamable HTTP via `TRANSPORT=http` environment
variable, for future remote/multi-client scenarios.

```
TRANSPORT=stdio   (default) → StdioServerTransport
TRANSPORT=http              → StreamableHTTPServerTransport on port $PORT (default 3000)
```

stdio servers must not log to stdout; all logging goes to stderr.

---

## `package.json` (adams-view-mcp-server)

```json
{
  "name": "adams-view-mcp-server",
  "version": "0.1.0",
  "description": "MCP server for MSC Adams View — exposes Adams View operations to AI agent harnesses",
  "type": "module",
  "main": "dist/index.js",
  "bin": { "adams-view-mcp-server": "dist/index.js" },
  "scripts": {
    "build": "tsc",
    "dev": "tsx watch src/index.ts",
    "start": "node dist/index.js",
    "clean": "rm -rf dist"
  },
  "engines": { "node": ">=18" },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.6.1",
    "zod": "^3.23.8"
  },
  "devDependencies": {
    "@types/node": "^22.10.0",
    "tsx": "^4.19.2",
    "typescript": "^5.7.2"
  }
}
```

Note: no `axios` — all I/O goes through Node's built-in `net` module (TCP to
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
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

---

## VS Code Extension Integration (now)

The VSIX must bundle `adams-view-mcp-server/dist/index.js` and its
`node_modules`. The `.vscodeignore` will be updated:

```
# exclude MCP server source and dev files, but include compiled dist
adams-view-mcp-server/src/**
adams-view-mcp-server/node_modules/**
adams-view-mcp-server/tsconfig.json
!adams-view-mcp-server/dist/**
!adams-view-mcp-server/package.json
```

The extension can spawn the MCP server as a subprocess by resolving the path:

```javascript
// Works both in dev (sibling dir) and installed (node_modules/)
function getMcpServerPath(context) {
  // Try node_modules first (installed), fall back to sibling dir (dev)
  const fromNodeModules = path.join(
    context.extensionPath, 'node_modules', 'adams-view-mcp-server', 'dist', 'index.js'
  );
  const fromSibling = path.join(
    context.extensionPath, '..', 'adams-view-mcp-server', 'dist', 'index.js'
  );
  if (fs.existsSync(fromNodeModules)) return fromNodeModules;
  if (fs.existsSync(fromSibling)) return fromSibling;
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
5. The path-resolution helper above already handles this case

No structural changes to the MCP server itself are needed.

---

## Implementation Checklist

### Phase 1 — Scaffold
- [ ] Create `adams-view-mcp-server/` directory
- [ ] Write `package.json`
- [ ] Write `tsconfig.json`
- [ ] Add `"build-mcp"` script to root `package.json`
- [ ] Add `adams-view-mcp-server/dist/` to `.gitignore`

### Phase 2 — Core infrastructure
- [ ] Implement `src/constants.ts` (`DEFAULT_PORT`, `CHARACTER_LIMIT`, `TIMEOUT_MS`)
- [ ] Implement `src/client.ts` (`executeCmd`, `evaluateExp`, `checkConnection`, `getPort`)
- [ ] Write `src/index.ts` skeleton (McpServer init + transport selection)

### Phase 3 — Tools
- [ ] Implement `src/tools/query.ts`
  - `adams_check_connection`
  - `adams_get_working_directory`
  - `adams_get_model_names`
  - `adams_evaluate_expression`
- [ ] Implement `src/tools/cmd.ts`
  - `adams_run_cmd`
  - `adams_run_python` (temp file pattern)
  - `adams_load_file`
- [ ] Implement `src/tools/model.ts`
  - `adams_delete_model`
- [ ] Wire all tools into `src/index.ts`

### Phase 4 — Build & verify
- [ ] `npm install` in `adams-view-mcp-server/`
- [ ] `npm run build` compiles without errors
- [ ] `node dist/index.js` starts without crashing (no Adams required)
- [ ] Update `.vscodeignore` to bundle `dist/`

### Phase 5 — Evaluations (separate task)
- [ ] Write evaluation XML per `mcp-builder` evaluation guide

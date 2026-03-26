/**
 * tools/query.ts — Read-only / diagnostic tools that evaluate Adams View
 * expressions or check connectivity.
 */

import * as crypto from "crypto";
import * as fs from "fs/promises";
import * as os from "os";
import * as path from "path";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { checkConnection, evaluateExp, executeCmd } from "../client.js";
import { CHARACTER_LIMIT } from "../constants.js";

function truncate(text: string): string {
  if (text.length <= CHARACTER_LIMIT) return text;
  return (
    text.slice(0, CHARACTER_LIMIT) +
    `\n[Response truncated at ${CHARACTER_LIMIT} characters]`
  );
}

function errorResult(message: string) {
  return {
    content: [{ type: "text" as const, text: message }],
    isError: true,
  };
}

export function registerQueryTools(server: McpServer): void {
  // ── adams_check_connection ───────────────────────────────────────────────
  server.registerTool(
    "adams_check_connection",
    {
      title: "Check Adams View Connection",
      description: `Check whether Adams View is running and its session is ready.

Connects to the Adams View TCP command server (default port 5002, or the
ADAMS_LISTENER_PORT environment variable) and verifies the session is
initialised by querying db_exists('.mdi').

Returns:
  { "connected": boolean, "message": string }

Use this first to verify connectivity before running other Adams tools.`,
      inputSchema: z.object({}).strict(),
      annotations: {
        readOnlyHint: true,
        destructiveHint: false,
        idempotentHint: true,
        openWorldHint: false,
      },
    },
    async () => {
      try {
        const connected = await checkConnection();
        const result = {
          connected,
          message: connected
            ? "Adams View is running and ready."
            : "Adams View is not reachable or the session is not ready.",
        };
        return {
          content: [{ type: "text" as const, text: JSON.stringify(result, null, 2) }],
        };
      } catch (e: unknown) {
        return errorResult(`Error checking connection: ${e instanceof Error ? e.message : String(e)}`);
      }
    }
  );

  // ── adams_get_working_directory ──────────────────────────────────────────
  server.registerTool(
    "adams_get_working_directory",
    {
      title: "Get Adams View Working Directory",
      description: `Returns Adams View's current working directory.

Evaluates getcwd() in Adams View and returns the path string.

Returns:
  { "working_directory": string }`,
      inputSchema: z.object({}).strict(),
      annotations: {
        readOnlyHint: true,
        destructiveHint: false,
        idempotentHint: true,
        openWorldHint: false,
      },
    },
    async () => {
      try {
        const cwd = await evaluateExp("getcwd()");
        const result = { working_directory: String(cwd) };
        return {
          content: [{ type: "text" as const, text: JSON.stringify(result, null, 2) }],
        };
      } catch (e: unknown) {
        return errorResult(`Error getting working directory: ${e instanceof Error ? e.message : String(e)}`);
      }
    }
  );

  // ── adams_get_model_names ────────────────────────────────────────────────
  server.registerTool(
    "adams_get_model_names",
    {
      title: "Get Adams View Model Names",
      description: `Returns the names of all models currently loaded in the Adams View session.

Uses the Adams Python API (Adams.Models) to retrieve model names.

Returns:
  { "model_names": string[] }

Returns an empty array when no models are loaded.`,
      inputSchema: z.object({}).strict(),
      annotations: {
        readOnlyHint: true,
        destructiveHint: false,
        idempotentHint: true,
        openWorldHint: false,
      },
    },
    async () => {
      const tmpDir = await fs.mkdtemp(path.join(os.tmpdir(), "adams-mcp-"));
      const scriptFile = path.join(tmpDir, "script.py");
      const outputFile = path.join(tmpDir, `out-${crypto.randomUUID()}.txt`);
      const outputFileAdams = outputFile.replace(/\\/g, "/");

      const script = [
        `import Adams, sys as _mcp_sys, io as _mcp_io, json as _mcp_json`,
        `_mcp_buf = _mcp_io.StringIO()`,
        `_mcp_old = _mcp_sys.stdout`,
        `_mcp_sys.stdout = _mcp_buf`,
        `try:`,
        `    names = [m.full_name for m in Adams.Models.values()]`,
        `    print(_mcp_json.dumps(names))`,
        `finally:`,
        `    _mcp_sys.stdout = _mcp_old`,
        `    with open(${JSON.stringify(outputFileAdams)}, "w", encoding="utf-8") as _f:`,
        `        _f.write(_mcp_buf.getvalue())`,
      ].join("\n");

      try {
        await fs.writeFile(scriptFile, script, "utf8");
        await executeCmd(`file python read file_name="${scriptFile.replace(/\\/g, "/")}"`);

        const raw = (await fs.readFile(outputFile, "utf8")).trim();
        const names: string[] = raw ? JSON.parse(raw) : [];
        return {
          content: [{ type: "text" as const, text: JSON.stringify({ model_names: names }, null, 2) }],
        };
      } catch (e: unknown) {
        return errorResult(`Error getting model names: ${e instanceof Error ? e.message : String(e)}`);
      } finally {
        await fs.unlink(scriptFile).catch(() => undefined);
        await fs.unlink(outputFile).catch(() => undefined);
        await fs.rmdir(tmpDir).catch(() => undefined);
      }
    }
  );

  // ── adams_evaluate_expression ────────────────────────────────────────────
  server.registerTool(
    "adams_evaluate_expression",
    {
      title: "Evaluate Adams View Expression",
      description: `Evaluates any Adams View expression and returns its typed result.

Sends a 'query' request to Adams View and returns the typed scalar or array
value. Adams View handles type coercion: integer/float expressions return
numbers, boolean-like strings ('on'/'off'/'yes'/'no') return booleans, and
other strings are returned as-is.

Args:
  - expression (string): Adams View expression to evaluate, e.g. 'getcwd()',
    'db_exists(".my_model")', 'UNIQUE_NAME_IN_HIERARCHY(".model")'

Returns:
  { "expression": string, "result": string | number | boolean | Array }`,
      inputSchema: z
        .object({
          expression: z
            .string()
            .min(1)
            .describe("Adams View expression to evaluate, e.g. 'getcwd()'"),
        })
        .strict(),
      annotations: {
        readOnlyHint: true,
        destructiveHint: false,
        idempotentHint: false,
        openWorldHint: false,
      },
    },
    async ({ expression }) => {
      try {
        const value = await evaluateExp(expression);
        const result = { expression, result: value };
        const text = truncate(JSON.stringify(result, null, 2));
        return {
          content: [{ type: "text" as const, text }],
        };
      } catch (e: unknown) {
        return errorResult(`Error evaluating expression: ${e instanceof Error ? e.message : String(e)}`);
      }
    }
  );
}

/**
 * tools/cmd.ts — Mutating tools that send commands to Adams View:
 *   adams_run_cmd, adams_run_python, adams_load_file
 */

import * as crypto from "crypto";
import * as fs from "fs/promises";
import * as os from "os";
import * as path from "path";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { executeCmd, sendCmd } from "../client.js";

function errorResult(message: string) {
  return {
    content: [{ type: "text" as const, text: message }],
    isError: true,
  };
}

function successResult(message: string) {
  return {
    content: [{ type: "text" as const, text: message }],
  };
}

export function registerCmdTools(server: McpServer): void {
  // ── adams_run_cmd ────────────────────────────────────────────────────────
  server.registerTool(
    "adams_run_cmd",
    {
      title: "Run Adams View Command",
      description: `Sends arbitrary Adams CMD text to Adams View and returns success or error.

Use this to run any Adams View command. For multi-line scripts, use
adams_run_python instead. For loading .cmd or .py files from disk, use
adams_load_file.

Args:
  - cmd (string): Adams View command text to execute, e.g.
    'model create model_name=my_model'

Returns:
  Success message string, or an error with the raw Adams response.`,
      inputSchema: z
        .object({
          cmd: z.string().min(1).describe("Adams View command text to execute"),
        })
        .strict(),
      annotations: {
        readOnlyHint: false,
        destructiveHint: true,
        idempotentHint: false,
        openWorldHint: false,
      },
    },
    async ({ cmd }) => {
      try {
        await executeCmd(cmd);
        return successResult(`Command executed successfully.`);
      } catch (e: unknown) {
        return errorResult(`Error running command: ${e instanceof Error ? e.message : String(e)}`);
      }
    }
  );

  // ── adams_run_python ─────────────────────────────────────────────────────
  server.registerTool(
    "adams_run_python",
    {
      title: "Run Python in Adams View",
      description: `Executes a Python snippet inside Adams View and returns any print() output.

Wraps the user code in a sys.stdout capture so that print() output is written
to a temporary file and returned directly in the tool result. Adams-level
errors (e.g. exceptions raised inside Adams View) are also captured and
returned as errors.

Args:
  - code (string): Python code to execute inside Adams View

Returns:
  Any text written to stdout (print() calls), or an error message on failure.`,
      inputSchema: z
        .object({
          code: z.string().min(1).describe("Python code to execute inside Adams View"),
        })
        .strict(),
      annotations: {
        readOnlyHint: false,
        destructiveHint: true,
        idempotentHint: false,
        openWorldHint: false,
      },
    },
    async ({ code }) => {
      const tmpDir = await fs.mkdtemp(path.join(os.tmpdir(), "adams-mcp-"));
      const scriptFile = path.join(tmpDir, "script.py");
      const outputFile = path.join(tmpDir, `out-${crypto.randomUUID()}.txt`);
      // Adams View accepts forward slashes on Windows
      const outputFileAdams = outputFile.replace(/\\/g, "/");

      // Wrap user code: redirect sys.stdout to a temp file so print() output
      // is captured and returned directly in the tool result.
      const wrapped = [
        `import sys as _mcp_sys, io as _mcp_io`,
        `_mcp_buf = _mcp_io.StringIO()`,
        `_mcp_old_stdout = _mcp_sys.stdout`,
        `_mcp_sys.stdout = _mcp_buf`,
        `try:`,
        // Indent user code by 4 spaces so it runs inside the try block
        ...code.split("\n").map((line) => `    ${line}`),
        `finally:`,
        `    _mcp_sys.stdout = _mcp_old_stdout`,
        `    with open(${JSON.stringify(outputFileAdams)}, "w", encoding="utf-8") as _mcp_f:`,
        `        _mcp_f.write(_mcp_buf.getvalue())`,
      ].join("\n");

      try {
        await fs.writeFile(scriptFile, wrapped, "utf8");
        const scriptPath = scriptFile.replace(/\\/g, "/");
        await executeCmd(`file python read file_name="${scriptPath}"`);

        // Read captured stdout
        let output = "";
        try {
          output = await fs.readFile(outputFile, "utf8");
        } catch {
          // Output file not written — script may have errored before the finally block
        }

        return {
          content: [
            {
              type: "text" as const,
              text: output.length > 0 ? output : "(no output)",
            },
          ],
        };
      } catch (e: unknown) {
        return errorResult(`Error running Python: ${e instanceof Error ? e.message : String(e)}`);
      } finally {
        await fs.unlink(scriptFile).catch(() => undefined);
        await fs.unlink(outputFile).catch(() => undefined);
        await fs.rmdir(tmpDir).catch(() => undefined);
      }
    }
  );

  // ── adams_load_file ──────────────────────────────────────────────────────
  server.registerTool(
    "adams_load_file",
    {
      title: "Load File into Adams View",
      description: `Loads a .cmd or .py file from disk into Adams View.

File type is inferred from the extension:
  - .cmd → file command read file_name="<path>"
  - .py  → file python read file_name="<path>"

By default the tool waits for Adams View to finish executing the file and
reports success or failure (wait_for_completion=true). For files that may
take a long time to execute (e.g. scripts that run simulations), set
wait_for_completion=false. The command is sent and the tool returns
immediately. Call adams_check_connection repeatedly until it returns true
to determine when Adams View has finished and is ready for new commands.

Args:
  - file_path (string): Absolute path to the .cmd or .py file to load
  - wait_for_completion (boolean, default true): When false, send the
    command and return immediately without waiting for Adams View to finish.

Returns:
  Success message, or an error describing what went wrong.
  When wait_for_completion=false, returns immediately with a status message
  and instructions for polling completion via adams_check_connection.`,
      inputSchema: z
        .object({
          file_path: z
            .string()
            .min(1)
            .describe("Absolute path to the .cmd or .py file to load"),
          wait_for_completion: z
            .boolean()
            .optional()
            .describe(
              "When false, send the command and return immediately without waiting for " +
              "Adams View to finish. Poll completion with adams_check_connection. " +
              "Defaults to true."
            ),
        })
        .strict(),
      annotations: {
        readOnlyHint: false,
        destructiveHint: true,
        idempotentHint: false,
        openWorldHint: false,
      },
    },
    async ({ file_path, wait_for_completion }) => {
      try {
        await fs.access(file_path);
      } catch {
        return errorResult(`File not found: ${file_path}`);
      }

      const ext = path.extname(file_path).toLowerCase();
      if (ext !== ".cmd" && ext !== ".py") {
        return errorResult(
          `Unsupported file extension "${ext}". Only .cmd and .py files are supported.`
        );
      }

      const normalised = file_path.replace(/\\/g, "/");
      const adamsCmd =
        ext === ".cmd"
          ? `file command read file_name="${normalised}"`
          : `file python read file_name="${normalised}"`;

      if (wait_for_completion === false) {
        try {
          await sendCmd(adamsCmd);
          return successResult(
            `Command sent to Adams View (not waiting for completion): ${file_path}\n` +
            `Adams View is now executing the file. Call adams_check_connection ` +
            `repeatedly — it will return true once Adams View is responsive again, ` +
            `indicating the file has finished executing.`
          );
        } catch (e: unknown) {
          return errorResult(`Error sending command: ${e instanceof Error ? e.message : String(e)}`);
        }
      }

      try {
        await executeCmd(adamsCmd);
        return successResult(`File loaded successfully: ${file_path}`);
      } catch (e: unknown) {
        return errorResult(`Error loading file: ${e instanceof Error ? e.message : String(e)}`);
      }
    }
  );
}

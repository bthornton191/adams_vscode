/**
 * tools/log.ts — Session log tool: adams_read_session_log
 *
 * Uses the undocumented Adams View function gui_utl_log_fil_fil() to extract
 * and optionally filter the session log to a temp file, then reads it.
 */

import * as crypto from "crypto";
import * as fs from "fs/promises";
import * as os from "os";
import * as path from "path";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { evaluateExp, executeCmd } from "../client.js";
import { CHARACTER_LIMIT } from "../constants.js";

function errorResult(message: string) {
  return {
    content: [{ type: "text" as const, text: message }],
    isError: true,
  };
}

/**
 * Compute the flags bitmask for gui_utl_log_fil_fil from boolean inputs.
 *
 * Bit layout:
 *   1  = enable type-level filtering
 *   2  = show infos
 *   4  = show warnings
 *   8  = show errors
 *   16 = show fatals
 *   32 = suppress duplicates
 *   64 = enable string filtering
 */
function buildFlags(opts: {
  filter_by_type: boolean;
  show_infos: boolean;
  show_warnings: boolean;
  show_errors: boolean;
  show_fatals: boolean;
  suppress_duplicates: boolean;
  filter_string: string;
}): number {
  let flags = 0;
  if (opts.filter_by_type) flags |= 1;
  if (opts.show_infos) flags |= 2;
  if (opts.show_warnings) flags |= 4;
  if (opts.show_errors) flags |= 8;
  if (opts.show_fatals) flags |= 16;
  if (opts.suppress_duplicates) flags |= 32;
  if (opts.filter_string !== "") flags |= 64;
  return flags;
}

const LOG_STATUS_MESSAGES: Record<number, string> = {
  1: "No log file is open in the current Adams View session.",
  2: "Could not write temporary log file. Check file system permissions.",
  3: "A log file line exceeds the internal Adams length limit.",
};

export function registerLogTools(server: McpServer): void {
  // ── adams_read_session_log ───────────────────────────────────────────────
  server.registerTool(
    "adams_read_session_log",
    {
      title: "Read Adams View Session Log",
      description: `Reads the Adams View session log with optional filtering.

Uses the internal Adams View function gui_utl_log_fil_fil() to extract the
session log to a temporary file, reads it, and returns the content.

Useful for:
  - Retrieving print() output from Python scripts run via adams_run_python
  - Diagnosing Adams View errors and warnings
  - Reviewing command history

Args:
  - filter_by_type (boolean, default false): Enable filtering by message type.
    When false, all message types are included regardless of show_* settings.
  - show_infos (boolean, default true): Include info messages (only applies
    when filter_by_type is true).
  - show_warnings (boolean, default true): Include warning messages (only
    applies when filter_by_type is true).
  - show_errors (boolean, default true): Include error messages (only applies
    when filter_by_type is true).
  - show_fatals (boolean, default true): Include fatal messages (only applies
    when filter_by_type is true).
  - suppress_duplicates (boolean, default false): Remove duplicate log lines.
  - filter_string (string, default ""): Only show lines containing this string.
    Empty string means no string filter.

Returns:
  The log file content as a string (truncated to ${CHARACTER_LIMIT} characters if large).`,
      inputSchema: z
        .object({
          filter_by_type: z
            .boolean()
            .default(false)
            .describe(
              "Enable filtering by message type. When false, all message types are included."
            ),
          show_infos: z
            .boolean()
            .default(true)
            .describe("Include info messages (only applies when filter_by_type is true)"),
          show_warnings: z
            .boolean()
            .default(true)
            .describe("Include warning messages (only applies when filter_by_type is true)"),
          show_errors: z
            .boolean()
            .default(true)
            .describe("Include error messages (only applies when filter_by_type is true)"),
          show_fatals: z
            .boolean()
            .default(true)
            .describe("Include fatal messages (only applies when filter_by_type is true)"),
          suppress_duplicates: z
            .boolean()
            .default(false)
            .describe("Remove duplicate log lines"),
          filter_string: z
            .string()
            .default("")
            .describe(
              "Only show lines containing this string. Empty string means no string filter."
            ),
        })
        .strict(),
      annotations: {
        readOnlyHint: true,
        destructiveHint: false,
        idempotentHint: false,
        openWorldHint: false,
      },
    },
    async (params) => {
      const tmpFile = path.join(os.tmpdir(), `adams-mcp-log-${crypto.randomUUID()}.txt`);
      // Normalise path for Adams View (forward slashes, escape any backslashes)
      const tmpFileAdams = tmpFile.replace(/\\/g, "/");

      try {
        const flags = buildFlags(params);
        const escapedFilter = params.filter_string.replace(/"/g, '\\"');

        // Store the return code in a temporary Adams variable
        const varName = ".mcp_log_stat";
        await executeCmd(
          `variable set variable_name=${varName} &\n` +
          `  integer_value=(eval(gui_utl_log_fil_fil("${tmpFileAdams}", "${escapedFilter}", ${flags})))`
        );

        const statusRaw = await evaluateExp(varName);
        const status = typeof statusRaw === "number" ? statusRaw : parseInt(String(statusRaw), 10);

        // Clean up the Adams variable (best effort)
        await executeCmd(`variable delete variable_name=${varName}`).catch(() => undefined);

        if (status !== 0) {
          const msg = LOG_STATUS_MESSAGES[status] ?? `gui_utl_log_fil_fil returned status ${status}.`;
          return errorResult(msg);
        }

        const content = await fs.readFile(tmpFile, "utf8");
        const trimmed = content.length > CHARACTER_LIMIT
          ? content.slice(0, CHARACTER_LIMIT) + `\n[Log truncated at ${CHARACTER_LIMIT} characters]`
          : content;

        return {
          content: [{ type: "text" as const, text: trimmed }],
        };
      } catch (e: unknown) {
        return errorResult(
          `Error reading session log: ${e instanceof Error ? e.message : String(e)}`
        );
      } finally {
        await fs.unlink(tmpFile).catch(() => undefined);
      }
    }
  );
}

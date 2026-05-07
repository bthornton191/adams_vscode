/**
 * tools/log.ts — Session log tool: adams_read_session_log
 *
 * Uses the undocumented Adams View function gui_utl_log_fil_fil() to extract
 * and filter the session log to a temporary file, then reads it from disk.
 * Adams handles log file discovery internally so we never have to guess the
 * log file path.
 *
 * gui_utl_log_fil_fil(output_path, filter_string, flags) → int
 *   flags bitmask:
 *     1  = enable type filtering (bits 1-4 apply)
 *     2  = show infos
 *     4  = show warnings
 *     8  = show errors
 *     16 = show fatals
 *     32 = suppress duplicates
 *     64 = enable string filter (uses filter_string param)
 *   return codes: 0=ok, 1=no log open, 2=cannot write output, 3=line too long
 */

import * as crypto from "crypto";
import * as fs from "fs/promises";
import * as os from "os";
import * as path from "path";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { executeCmd } from "../client.js";
import { CHARACTER_LIMIT } from "../constants.js";

function errorResult(message: string) {
  return {
    content: [{ type: "text" as const, text: message }],
    isError: true,
  };
}

/**
 * Compute the gui_utl_log_fil_fil flags bitmask from tool params.
 * Note: bit 64 (string filter) is intentionally excluded — string filtering
 * is handled post-hoc in Python to avoid quoting issues inside Adams expressions.
 */
function buildFlags(opts: {
  filter_by_type: boolean;
  show_infos: boolean;
  show_warnings: boolean;
  show_errors: boolean;
  show_fatals: boolean;
  suppress_duplicates: boolean;
}): number {
  let flags = 0;
  if (opts.filter_by_type)      flags |= 1;
  if (opts.show_infos)          flags |= 2;
  if (opts.show_warnings)       flags |= 4;
  if (opts.show_errors)         flags |= 8;
  if (opts.show_fatals)         flags |= 16;
  if (opts.suppress_duplicates) flags |= 32;
  return flags;
}

/**
 * Apply tail_lines trimming to text returned by Adams (post-processing only,
 * since gui_utl_log_fil_fil doesn't support tail natively).
 */
function applyTail(text: string, tailLines: number): string {
  if (tailLines <= 0) return text;
  const lines = text.split(/\r?\n/);
  return lines.slice(-tailLines).join("\n");
}

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
  - tail_lines (integer, default 0): If greater than 0, return only the last N lines
    of the log (applied after all other filters). 0 means return all lines.

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
          tail_lines: z
            .number()
            .int()
            .min(0)
            .default(0)
            .describe(
              "If greater than 0, return only the last N lines (applied after all other filters). 0 means return all lines."
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
      const tmpDir = await fs.mkdtemp(path.join(os.tmpdir(), "adams-mcp-log-"));
      const outputFile = path.join(tmpDir, `log-${crypto.randomUUID()}.txt`);
      const statusFile = path.join(tmpDir, "status.txt");
      const scriptFile = path.join(tmpDir, "extract.py");

      // Adams View requires forward slashes in file paths
      const toAdams = (p: string) => p.replace(/\\/g, "/");

      try {
        const flags = buildFlags(params);

        // Safely encode the filter string as a Python string literal so it can
        // contain special characters without breaking the script.
        const filterStrLiteral = JSON.stringify(params.filter_string);

        // Single Python script that:
        //   1. Calls gui_utl_log_fil_fil via Adams.evaluate_exp() to extract the log
        //   2. Applies post-hoc string filtering (avoids quoting inside Adams expression)
        //   3. Writes the integer return code to a status file
        const outputFileAdams = toAdams(outputFile);
        const statusFileAdams = toAdams(statusFile);
        const script = [
          `import Adams as _A, json as _j`,
          // Call gui_utl_log_fil_fil — second arg (filter_string) is ignored when bit 6 is not set
          `_status = int(_A.evaluate_exp('gui_utl_log_fil_fil("${outputFileAdams}", "", ${flags})'))`,
          // Post-hoc string filtering in Python (avoids all quoting issues)
          `_filter = ${filterStrLiteral}`,
          `if _status == 0 and _filter != "":`,
          `    with open("${outputFileAdams}", "r", encoding="utf-8", errors="replace") as _f:`,
          `        _lines = [l for l in _f if _filter in l]`,
          `    with open("${outputFileAdams}", "w", encoding="utf-8") as _f:`,
          `        _f.writelines(_lines)`,
          `with open("${statusFileAdams}", "w") as _f:`,
          `    _f.write(_j.dumps({"v": _status}))`,
        ].join("\n");

        await fs.writeFile(scriptFile, script, "utf8");
        await executeCmd(`file python read file_name="${toAdams(scriptFile)}"`);

        // Read back the status code Adams wrote
        let status = 0;
        try {
          const statJson = JSON.parse(await fs.readFile(statusFile, "utf8"));
          status = Number(statJson.v);
        } catch {
          // Status file missing — script may have errored; assume log was empty
        }

        if (status === 1) {
          return errorResult(
            "No log file is open in the current Adams View session. " +
            "Adams View writes a session log when started normally."
          );
        }
        if (status === 2) {
          return errorResult(
            `Could not write temporary log file. Check file system permissions.`
          );
        }
        if (status === 3) {
          return errorResult("A log file line exceeds the internal Adams length limit.");
        }
        if (status !== 0) {
          return errorResult(`gui_utl_log_fil_fil returned unexpected status ${status}.`);
        }

        let raw: string;
        try {
          raw = await fs.readFile(outputFile, "utf8");
        } catch {
          return errorResult(
            "Adams reported success but the log output file was not created. " +
            "The session log may be empty."
          );
        }

        const tailed = applyTail(raw, params.tail_lines);
        const result =
          tailed.length > CHARACTER_LIMIT
            ? tailed.slice(0, CHARACTER_LIMIT) + `\n[Log truncated at ${CHARACTER_LIMIT} characters]`
            : tailed;

        return {
          content: [{ type: "text" as const, text: result }],
        };
      } catch (e: unknown) {
        return errorResult(
          `Error reading session log: ${e instanceof Error ? e.message : String(e)}`
        );
      } finally {
        await fs.rm(tmpDir, { recursive: true, force: true }).catch(() => undefined);
      }
    }
  );
}

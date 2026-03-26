/**
 * tools/log.ts — Session log tool: adams_read_session_log
 *
 * Finds the Adams View session log by querying the working directory,
 * then reads the most recently modified .log file from disk.
 * Supports optional filtering by message type and string content.
 */

import * as fs from "fs/promises";
import * as path from "path";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { evaluateExp } from "../client.js";
import { CHARACTER_LIMIT } from "../constants.js";

function errorResult(message: string) {
  return {
    content: [{ type: "text" as const, text: message }],
    isError: true,
  };
}

/**
 * Adams log lines begin with a type prefix.
 * Examples:
 *   "-------- Information: ..."
 *   "-------- Warning: ..."
 *   "-------- Error: ..."
 *   "-------- Fatal Error: ..."
 * Lines without a recognised prefix belong to the preceding message.
 */
function getLineType(line: string): "info" | "warning" | "error" | "fatal" | null {
  const trimmed = line.trimStart();
  if (/^-+\s*Information:/i.test(trimmed)) return "info";
  if (/^-+\s*Warning:/i.test(trimmed)) return "warning";
  if (/^-+\s*Fatal Error:/i.test(trimmed)) return "fatal";
  if (/^-+\s*Error:/i.test(trimmed)) return "error";
  return null;
}

/**
 * Apply optional filtering to the raw log text.
 * Operates line-by-line; continuation lines inherit the previous message type.
 */
function filterLog(
  raw: string,
  opts: {
    filter_by_type: boolean;
    show_infos: boolean;
    show_warnings: boolean;
    show_errors: boolean;
    show_fatals: boolean;
    suppress_duplicates: boolean;
    filter_string: string;
    tail_lines: number;
  }
): string {
  const lines = raw.split(/\r?\n/);
  const seen = new Set<string>();
  const out: string[] = [];
  let currentType: ReturnType<typeof getLineType> = null;

  for (const line of lines) {
    const lineType = getLineType(line);
    if (lineType !== null) currentType = lineType;

    // Type filtering
    if (opts.filter_by_type) {
      if (currentType === "info" && !opts.show_infos) continue;
      if (currentType === "warning" && !opts.show_warnings) continue;
      if (currentType === "error" && !opts.show_errors) continue;
      if (currentType === "fatal" && !opts.show_fatals) continue;
    }

    // String filtering
    if (opts.filter_string !== "" && !line.includes(opts.filter_string)) continue;

    // Duplicate suppression
    if (opts.suppress_duplicates) {
      if (seen.has(line)) continue;
      seen.add(line);
    }

    out.push(line);
  }

  if (opts.tail_lines > 0) {
    return out.slice(-opts.tail_lines).join("\n");
  }
  return out.join("\n");
}

/**
 * Find the most recently modified .log file in the given directory.
 * Returns null if none found.
 */
async function findLatestLogFile(dir: string): Promise<string | null> {
  let entries;
  try {
    entries = await fs.readdir(dir, { withFileTypes: true });
  } catch {
    return null;
  }

  const logFiles = entries
    .filter((e) => e.isFile() && e.name.toLowerCase().endsWith(".log"))
    .map((e) => path.join(dir, e.name));

  if (logFiles.length === 0) return null;
  if (logFiles.length === 1) return logFiles[0]!;

  // Return the most recently modified
  const stats = await Promise.all(
    logFiles.map(async (f) => ({ file: f, mtime: (await fs.stat(f)).mtimeMs }))
  );
  stats.sort((a, b) => b.mtime - a.mtime);
  return stats[0]!.file;
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
      // Step 1: Get Adams View's current working directory
      let workingDir: string;
      try {
        const raw = await evaluateExp("getcwd()");
        workingDir = String(raw).trim().replace(/\\/g, "/");
      } catch (e: unknown) {
        return errorResult(
          `Error reading session log: Could not query Adams View working directory.\n` +
          `${e instanceof Error ? e.message : String(e)}`
        );
      }

      // Step 2: Find the most recently modified .log file in that directory
      const logFile = await findLatestLogFile(workingDir);
      if (!logFile) {
        return errorResult(
          `No .log file found in Adams View working directory: ${workingDir}\n` +
          `Adams View writes session logs to its working directory. ` +
          `Verify the working directory with adams_get_working_directory.`
        );
      }

      // Step 3: Read and filter the log
      let raw: string;
      try {
        raw = await fs.readFile(logFile, "utf8");
      } catch (e: unknown) {
        return errorResult(
          `Error reading log file ${logFile}: ${e instanceof Error ? e.message : String(e)}`
        );
      }

      const filtered = filterLog(raw, params);
      const trimmed =
        filtered.length > CHARACTER_LIMIT
          ? filtered.slice(0, CHARACTER_LIMIT) + `\n[Log truncated at ${CHARACTER_LIMIT} characters]`
          : filtered;

      return {
        content: [
          {
            type: "text" as const,
            text: `Log file: ${logFile}\n\n${trimmed}`,
          },
        ],
      };
    }
  );
}

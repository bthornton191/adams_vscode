/**
 * tools/batch.ts — Adams View batch mode tools:
 *   adams_run_batch, adams_batch_status
 *
 * These tools launch Adams View in batch mode (mdi.bat aview ru-s -b <file>)
 * without requiring an interactive Adams View session or Command Server.
 * adams_run_batch returns immediately with a job ID; adams_batch_status
 * polls job state by checking process exit and parsing aview.log.
 */

import * as crypto from "crypto";
import * as fs from "fs/promises";
import * as os from "os";
import * as path from "path";
import { spawn, ChildProcess } from "child_process";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { resolveMdiPath } from "../mdi.js";

// ── Finish / error detection constants ───────────────────────────────────────

/** Written to aview.log when a batch CMD session ends normally. */
export const BATCH_FINISH_MARKER =
  "! Command file is exhausted, batch run is finished.";

/** Patterns that indicate errors in aview.log. */
export const ERROR_PATTERNS: RegExp[] = [
  /\bERROR:\s/,
];

/** Patterns that indicate a Python exception in aview.log. */
export const PYTHON_ERROR_PATTERNS: RegExp[] = [
  /Traceback \(most recent call last\)/,
  /^\s*File ".*", line \d+/m,
  /^[A-Z][a-zA-Z]+Error:/m,
];

// ── Job registry ─────────────────────────────────────────────────────────────

export type BatchJobStatus = "running" | "completed" | "failed" | "crashed";

export interface BatchJob {
  id: string;
  file: string;
  workingDirectory: string;
  logPath: string;
  pid: number | undefined;
  startTime: string;
  exitCode: number | null;
  /** The spawned child process. Kept to check `.exitCode` / `.killed`. */
  process: ChildProcess;
}

/** In-memory registry of all batch jobs launched during this MCP server session. */
const jobs = new Map<string, BatchJob>();

// ── Log parsing helpers (exported for unit testing) ──────────────────────────

/**
 * Return the last `n` non-empty lines from a string.
 * If the string has fewer than `n` lines, returns all of them.
 */
export function tailLines(text: string, n: number): string {
  const lines = text.split(/\r?\n/);
  const nonEmpty = lines.filter((l) => l.trim() !== "");
  return nonEmpty.slice(-n).join("\n");
}

/**
 * Determine whether `aview.log` content contains the batch finish marker.
 */
export function hasFinishMarker(logContent: string): boolean {
  return logContent.includes(BATCH_FINISH_MARKER);
}

/**
 * Extract all error lines from `aview.log` content.
 * Matches both Adams ERROR: lines and Python traceback indicators.
 * Returns deduplicated lines preserving order.
 */
export function extractErrors(logContent: string): string[] {
  const errors: string[] = [];
  const lines = logContent.split(/\r?\n/);

  for (const line of lines) {
    for (const pattern of ERROR_PATTERNS) {
      if (pattern.test(line)) {
        errors.push(line.trim());
        break;
      }
    }
    for (const pattern of PYTHON_ERROR_PATTERNS) {
      if (pattern.test(line)) {
        errors.push(`[Python] ${line.trim()}`);
        break;
      }
    }
  }

  // Deduplicate while preserving order
  const seen = new Set<string>();
  return errors.filter((e) => {
    if (seen.has(e)) return false;
    seen.add(e);
    return true;
  });
}

/**
 * Determine the status of a completed batch job (process has exited) from
 * its log content and exit code.
 *
 * Rules:
 *   - Finish marker present → "completed" (errors may still be present)
 *   - Exit code 0 but no finish marker → "crashed" (Adams exited unexpectedly)
 *   - Non-zero exit code → "failed"
 */
export function determineCompletedStatus(
  logContent: string,
  exitCode: number | null
): BatchJobStatus {
  if (hasFinishMarker(logContent)) {
    return "completed";
  }
  if (exitCode !== null && exitCode !== 0) {
    return "failed";
  }
  return "crashed";
}

// ── Tool registration ─────────────────────────────────────────────────────────

/** Exported for unit testing. */
export function buildBatchSpawnArgs(
  resolvedMdi: string,
  filename: string
): { cmd: string; args: string[] } {
  const isWindows = process.platform === "win32";
  if (isWindows) {
    // .bat files must be invoked via cmd.exe to avoid EINVAL
    return {
      cmd: "cmd.exe",
      args: ["/c", resolvedMdi, "aview", "ru-s", "-b", filename],
    };
  }
  // On Linux/Mac, invoke mdi directly — batch mode exits on its own
  return {
    cmd: resolvedMdi,
    args: ["aview", "ru-s", "-b", filename],
  };
}

function errorResult(message: string) {
  return {
    content: [{ type: "text" as const, text: message }],
    isError: true,
  };
}

export function registerBatchTools(server: McpServer): void {
  // ── adams_run_batch ──────────────────────────────────────────────────────
  server.registerTool(
    "adams_run_batch",
    {
      title: "Run Adams View in Batch Mode",
      description: `Launches Adams View in batch mode to execute a .cmd or .py file without
an interactive session. Returns immediately with a job ID that can be used
with adams_batch_status to poll for completion.

This tool does NOT require Adams View to already be running or a Command
Server to be active. Adams View is started in headless batch mode and exits
automatically when the file finishes executing.

How it works:
  1. Resolves the path to mdi.bat (mdi_path, or auto-discovery).
  2. Spawns Adams View as a detached background process:
       mdi.bat aview ru-s -b <file>
     Adams exits automatically when the script completes.
  3. Returns a job_id immediately. Use adams_batch_status to poll for
     completion and retrieve errors.

Args:
  - file_path (string): Absolute path to the .cmd or .py file to run.
  - mdi_path (string, optional): Explicit path to mdi.bat (Windows) or mdi
    (Linux). If omitted, auto-discovery is used.
  - working_directory (string, optional): Directory to use as Adams View's
    working directory. Defaults to the directory containing file_path.

Returns:
  {
    "job_id": string,
    "pid": number | null,
    "file": string,
    "working_directory": string,
    "log_path": string,
    "message": string
  }

After calling this tool, use adams_batch_status to poll until status is
"completed", "failed", or "crashed".`,
      inputSchema: z
        .object({
          file_path: z
            .string()
            .min(1)
            .describe(
              "Absolute path to the .cmd or .py file to run in Adams View batch mode"
            ),
          mdi_path: z
            .string()
            .optional()
            .describe(
              "Explicit path to mdi.bat (Windows) or mdi (Linux). " +
              "If omitted, auto-discovery is attempted via ADAMS_LAUNCH_COMMAND " +
              "env var, ADAMS_INSTALL_DIR env var, or the default install location."
            ),
          working_directory: z
            .string()
            .optional()
            .describe(
              "Working directory for Adams View. Defaults to the directory " +
              "containing file_path. aview.log will be written here."
            ),
        })
        .strict(),
      annotations: {
        readOnlyHint: false,
        destructiveHint: false,
        idempotentHint: false,
        openWorldHint: false,
      },
    },
    async ({ file_path, mdi_path, working_directory }) => {
      // ── Validate file ────────────────────────────────────────────────────
      const ext = path.extname(file_path).toLowerCase();
      if (ext !== ".cmd" && ext !== ".py") {
        return errorResult(
          `Unsupported file type "${ext}". Only .cmd and .py files are supported.`
        );
      }

      try {
        await fs.access(file_path);
      } catch {
        return errorResult(`File not found: ${file_path}`);
      }

      const workDir = working_directory ?? path.dirname(file_path);

      // Validate working directory
      try {
        const stat = await fs.stat(workDir);
        if (!stat.isDirectory()) {
          return errorResult(`Not a directory: ${workDir}`);
        }
      } catch {
        return errorResult(`Working directory not found: ${workDir}`);
      }

      // ── Resolve MDI executable ───────────────────────────────────────────
      let resolvedMdi: string;
      try {
        resolvedMdi = await resolveMdiPath(mdi_path);
      } catch (e: unknown) {
        return errorResult(e instanceof Error ? e.message : String(e));
      }

      // ── Spawn Adams View in batch mode ───────────────────────────────────
      const filename = path.basename(file_path);
      const { cmd: spawnCmd, args: spawnArgs } = buildBatchSpawnArgs(resolvedMdi, filename);

      let child: ChildProcess;
      try {
        child = spawn(spawnCmd, spawnArgs, {
          cwd: workDir,
          detached: true,
          stdio: "ignore",
          windowsHide: true,
        });
        child.unref();
      } catch (e: unknown) {
        return errorResult(
          `Failed to launch Adams View in batch mode: ${e instanceof Error ? e.message : String(e)}`
        );
      }

      // ── Register job ─────────────────────────────────────────────────────
      const jobId = crypto.randomUUID();
      const logPath = path.join(workDir, "aview.log");

      const job: BatchJob = {
        id: jobId,
        file: file_path,
        workingDirectory: workDir,
        logPath,
        pid: child.pid,
        startTime: new Date().toISOString(),
        exitCode: null,
        process: child,
      };

      // Capture exit code when the process finishes
      child.once("exit", (code) => {
        job.exitCode = code ?? 1;
      });

      jobs.set(jobId, job);

      const result = {
        job_id: jobId,
        pid: child.pid ?? null,
        file: file_path,
        working_directory: workDir,
        log_path: logPath,
        message:
          `Adams View batch job started (PID ${child.pid ?? "unknown"}). ` +
          `Use adams_batch_status with job_id "${jobId}" to poll for completion.`,
      };

      return {
        content: [{ type: "text" as const, text: JSON.stringify(result, null, 2) }],
      };
    }
  );

  // ── adams_batch_status ───────────────────────────────────────────────────
  server.registerTool(
    "adams_batch_status",
    {
      title: "Check Adams Batch Job Status",
      description: `Checks the status of an Adams View batch job started with adams_run_batch.

Reads aview.log from the job's working directory to determine whether the
batch run has completed, failed, or is still running. Returns errors found
in the log and a tail of the log for diagnostics.

Status values:
  - "running"   — Adams View is still executing the batch script
  - "completed" — Adams finished normally (finish marker found in aview.log)
  - "failed"    — Adams exited with a non-zero exit code before finishing
  - "crashed"   — Adams exited with code 0 but the finish marker is absent
                  (e.g. a fatal error or assertion failure)

Args:
  - job_id (string): Job ID returned by adams_run_batch.

Returns:
  {
    "job_id": string,
    "status": "running" | "completed" | "failed" | "crashed",
    "exit_code": number | null,
    "errors": string[],
    "log_tail": string,
    "file": string,
    "working_directory": string
  }`,
      inputSchema: z
        .object({
          job_id: z
            .string()
            .min(1)
            .describe("Job ID returned by adams_run_batch"),
        })
        .strict(),
      annotations: {
        readOnlyHint: true,
        destructiveHint: false,
        idempotentHint: true,
        openWorldHint: false,
      },
    },
    async ({ job_id }) => {
      const job = jobs.get(job_id);
      if (!job) {
        return errorResult(
          `Job not found: "${job_id}". ` +
          `Jobs are tracked in memory and are lost when the MCP server restarts.`
        );
      }

      // Check whether the process is still running.
      // child.exitCode is null while running; a number after exit.
      const processRunning =
        job.process.exitCode === null && job.exitCode === null;

      // Read aview.log (may not exist yet if Adams is still starting up)
      let logContent = "";
      try {
        logContent = await fs.readFile(job.logPath, "utf8");
      } catch {
        // Log file not yet written — Adams may still be initializing
        if (processRunning) {
          return {
            content: [
              {
                type: "text" as const,
                text: JSON.stringify(
                  {
                    job_id,
                    status: "running",
                    exit_code: null,
                    errors: [],
                    log_tail: "",
                    file: job.file,
                    working_directory: job.workingDirectory,
                  },
                  null,
                  2
                ),
              },
            ],
          };
        }
      }

      if (processRunning) {
        // Process still running — report running regardless of log content
        const errors = extractErrors(logContent);
        const result = {
          job_id,
          status: "running" as BatchJobStatus,
          exit_code: null,
          errors,
          log_tail: tailLines(logContent, 50),
          file: job.file,
          working_directory: job.workingDirectory,
        };
        return {
          content: [{ type: "text" as const, text: JSON.stringify(result, null, 2) }],
        };
      }

      // Process has exited — use exit code from either source
      const exitCode = job.process.exitCode ?? job.exitCode;
      const status = determineCompletedStatus(logContent, exitCode);
      const errors = extractErrors(logContent);

      const result = {
        job_id,
        status,
        exit_code: exitCode,
        errors,
        log_tail: tailLines(logContent, 50),
        file: job.file,
        working_directory: job.workingDirectory,
      };

      return {
        content: [{ type: "text" as const, text: JSON.stringify(result, null, 2) }],
      };
    }
  );
}

/** Exported for tests — direct access to the job registry. */
export { jobs as _jobRegistry };

/** Exported for tests — create a synthetic BatchJob entry. */
export function _registerJob(job: BatchJob): void {
  jobs.set(job.id, job);
}

/** Exported for tests — remove a job from the registry. */
export function _clearJobs(): void {
  jobs.clear();
}

/** Returns the OS temp directory path for use in tests. */
export function _getTmpDir(): string {
  return os.tmpdir();
}

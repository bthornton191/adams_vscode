/**
 * tools/session.ts — Adams View session management:
 *   adams_launch_view
 */

import * as crypto from "crypto";
import * as fs from "fs/promises";
import * as os from "os";
import * as path from "path";
import { spawn } from "child_process";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { checkConnection, evaluateExp, executeCmd, getPort, sendCmd } from "../client.js";

const AVIEW_AS_CMD = "aviewAS.cmd";
const COMMAND_SERVER_LINE = "command_server start";

/** Milliseconds between connection poll attempts. */
const POLL_INTERVAL_MS = 2000;

function errorResult(message: string) {
  return {
    content: [{ type: "text" as const, text: message }],
    isError: true,
  };
}

/**
 * Poll checkConnection() until it returns true or the timeout expires.
 * Returns true if Adams View became ready within the timeout, false otherwise.
 */
async function waitForAdams(timeoutMs: number): Promise<boolean> {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    try {
      const ready = await checkConnection();
      if (ready) return true;
    } catch {
      // Not ready yet — keep polling
    }
    await new Promise((resolve) => setTimeout(resolve, POLL_INTERVAL_MS));
  }
  return false;
}

/**
 * Poll checkConnection() until it returns false or the timeout expires.
 * Returns true if Adams View went down within the timeout, false otherwise.
 */
async function waitForAdamsDown(timeoutMs: number): Promise<boolean> {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    try {
      const ready = await checkConnection();
      if (!ready) return true;
    } catch {
      return true; // Connection error means Adams is down
    }
    await new Promise((resolve) => setTimeout(resolve, POLL_INTERVAL_MS));
  }
  return false;
}

/**
 * Build a timestamped bin file path in the OS temp directory.
 * Format: adams_session_YYYY-MM-DDTHH-MM-SS.bin
 * Colons are replaced with hyphens for Windows filesystem safety.
 */
export function buildTimestampedBinPath(): string {
  const now = new Date();
  const ts = now.toISOString().slice(0, 19).replace(/:/g, "-");
  return path.join(os.tmpdir(), `adams_session_${ts}.bin`);
}

/**
 * Save the current Adams View session to a timestamped .bin file.
 * Returns the local OS path to the saved file.
 * Throws if the save command fails.
 */
async function saveSessionToBin(): Promise<string> {
  const binPath = buildTimestampedBinPath();
  const adamsPath = binPath.replace(/\\/g, "/");
  await executeCmd(`file bin write alert_if_exists=no file_name="${adamsPath}"`);
  return binPath;
}

/**
 * Resolve and validate the Adams mdi executable path.
 * Throws with a human-readable message if the path cannot be resolved.
 */
async function resolveMdiPath(mdiPath?: string): Promise<string> {
  if (mdiPath) {
    try {
      await fs.access(mdiPath);
    } catch {
      throw new Error(`mdi executable not found at: ${mdiPath}`);
    }
    return mdiPath;
  }
  const discovered = await findMdi();
  if (!discovered) {
    throw new Error(
      "Could not auto-discover the Adams executable (mdi.bat / mdi).\n" +
      "Options:\n" +
      "  1. Pass mdi_path explicitly to this tool.\n" +
      "  2. Set the ADAMS_LAUNCH_COMMAND environment variable to the full path of mdi.bat.\n" +
      "  3. Set ADAMS_INSTALL_DIR to your Adams installation parent directory\n" +
      "     (e.g. C:\\Program Files\\MSC.Software\\Adams)."
    );
  }
  return discovered;
}

/**
 * Inject 'command_server start' into aviewAS.cmd, spawn Adams View as a
 * detached hidden background process in workDir, then return a cleanup
 * function. The caller must invoke the returned function after Adams has had
 * time to read aviewAS.cmd on startup (i.e. after waitForAdams() resolves).
 */
async function spawnAdamsHidden(
  resolvedMdi: string,
  workDir: string
): Promise<() => Promise<void>> {
  const isWindows = process.platform === "win32";
  const mdiArgs = isWindows
    ? ["aview", "ru-s", "i"]
    : ["-c", "aview", "ru-s", "i", "exit"];

  // On Windows, launch via wscript.exe + Shell.Run with window style 0 (hidden)
  // so the VBScript suppresses all console windows in the mdi.bat launch chain.
  let spawnCmd: string;
  let spawnArgs: string[];

  if (isWindows) {
    const mdiEscaped = resolvedMdi.replace(/"/g, '""');
    const argsStr = mdiArgs.join(" ");
    const cmd = `""${mdiEscaped}"" ${argsStr}`;
    const vbs = `CreateObject("WScript.Shell").Run "${cmd}", 0, False`;
    const vbsTmp = path.join(os.tmpdir(), `adams-launch-${crypto.randomUUID()}.vbs`);
    await fs.writeFile(vbsTmp, vbs, "utf8");
    setTimeout(() => fs.unlink(vbsTmp).catch(() => undefined), 10_000);
    spawnCmd = "wscript.exe";
    spawnArgs = ["/nologo", vbsTmp];
  } else {
    spawnCmd = resolvedMdi;
    spawnArgs = mdiArgs;
  }

  const aviewAsCmdPath = path.join(workDir, AVIEW_AS_CMD);
  let originalContent: string | null = null;

  try {
    originalContent = await fs.readFile(aviewAsCmdPath, "utf8");
  } catch {
    // File doesn't exist — will be created from scratch
  }

  const needsCleanup =
    originalContent === null ||
    !originalContent.trimEnd().endsWith(COMMAND_SERVER_LINE);

  if (originalContent === null) {
    await fs.writeFile(aviewAsCmdPath, `${COMMAND_SERVER_LINE}\n`, "utf8");
  } else if (!originalContent.trimEnd().endsWith(COMMAND_SERVER_LINE)) {
    const sep = originalContent.endsWith("\n") ? "" : "\n";
    await fs.writeFile(
      aviewAsCmdPath,
      `${originalContent}${sep}${COMMAND_SERVER_LINE}\n`,
      "utf8"
    );
  }

  const adams = spawn(spawnCmd, spawnArgs, {
    cwd: workDir,
    detached: true,
    stdio: "ignore",
  });
  adams.unref();

  return async () => {
    if (!needsCleanup) return;
    try {
      if (originalContent === null) {
        await fs.unlink(aviewAsCmdPath);
      } else {
        await fs.writeFile(aviewAsCmdPath, originalContent, "utf8");
      }
    } catch {
      // Best-effort; don't mask the real result
    }
  };
}

/**
 * Auto-discover mdi.bat (Windows) or mdi (Linux/Mac).
 *
 * Discovery order:
 *   1. ADAMS_LAUNCH_COMMAND env var — direct path to mdi.bat / mdi
 *   2. ADAMS_INSTALL_DIR env var — parent of versioned install dirs
 *      e.g. C:\Program Files\MSC.Software\Adams\2024_2\common\mdi.bat
 *      (picks the lexicographically latest version directory)
 *   3. Default Windows install location:
 *      C:\Program Files\MSC.Software\Adams\<latest>\common\mdi.bat
 *
 * Returns the resolved path string, or null if not found.
 */
async function findMdi(): Promise<string | null> {
  const isWindows = process.platform === "win32";
  const mdiName = isWindows ? "mdi.bat" : "mdi";

  // 1. ADAMS_LAUNCH_COMMAND — direct path
  const envLaunch = process.env["ADAMS_LAUNCH_COMMAND"];
  if (envLaunch) {
    try {
      await fs.access(envLaunch);
      return envLaunch;
    } catch { /* not found, fall through */ }
  }

  // 2. ADAMS_INSTALL_DIR — parent of versioned dirs
  const envInstall = process.env["ADAMS_INSTALL_DIR"];
  if (envInstall) {
    const found = await findLatestMdiUnder(envInstall, mdiName);
    if (found) return found;
  }

  // 3. Default Windows install path
  if (isWindows) {
    const defaultParent = String.raw`C:\Program Files\MSC.Software\Adams`;
    const found = await findLatestMdiUnder(defaultParent, mdiName);
    if (found) return found;
  }

  return null;
}

/**
 * Look inside a parent directory for versioned Adams install subdirs,
 * pick the lexicographically latest one, and return the path to mdi.bat/mdi
 * inside its common/ subdirectory. Returns null if nothing found.
 */
async function findLatestMdiUnder(parentDir: string, mdiName: string): Promise<string | null> {
  let entries: string[];
  try {
    const dirents = await fs.readdir(parentDir, { withFileTypes: true });
    entries = dirents.filter((d) => d.isDirectory()).map((d) => d.name);
  } catch {
    return null;
  }

  // Sort descending so the latest version comes first
  entries.sort((a, b) => b.localeCompare(a));

  for (const entry of entries) {
    const candidate = path.join(parentDir, entry, "common", mdiName);
    try {
      await fs.access(candidate);
      return candidate;
    } catch { /* try next */ }
  }
  return null;
}

export function registerSessionTools(server: McpServer): void {
  // ── adams_launch_view ─────────────────────────────────────────────────────
  server.registerTool(
    "adams_launch_view",
    {
      title: "Launch Adams View",
      description: `Launches an Adams View process in the specified directory with the Command
Server already running, ready to accept tool calls.

How it works:
  1. Resolves the path to mdi.bat: uses mdi_path if provided, otherwise
     auto-discovers via ADAMS_LAUNCH_COMMAND env var, ADAMS_INSTALL_DIR env
     var, or the default Windows install location.
  2. Checks if an aviewAS.cmd file exists in the target directory.
     - If not, creates one containing 'command_server start'.
     - If it exists, appends 'command_server start' to the end.
  3. Spawns Adams View as a detached background process in the target directory.
  4. Waits up to timeout_seconds for the Command Server to become reachable.
  5. Restores aviewAS.cmd to its original state once Adams has loaded it.
  6. Returns success with the mdi path used and port Adams is listening on.

Args:
  - working_directory (string): Absolute path to the directory to launch
    Adams View in. Adams will use this as its working directory.
  - mdi_path (string, optional): Explicit path to mdi.bat (Windows) or mdi
    (Linux). If omitted, auto-discovery is used.
  - timeout_seconds (integer, default 120): How long to wait for Adams View
    to become reachable before returning an error.

Returns:
  Success message including the mdi path used and the Command Server port,
  or an error.`,
      inputSchema: z
        .object({
          working_directory: z
            .string()
            .min(1)
            .describe("Absolute path to the directory to launch Adams View in"),
          mdi_path: z
            .string()
            .optional()
            .describe(
              "Explicit path to mdi.bat (Windows) or mdi (Linux). " +
              "If omitted, auto-discovery is attempted via ADAMS_LAUNCH_COMMAND " +
              "env var, ADAMS_INSTALL_DIR env var, or the default install location."
            ),
          timeout_seconds: z
            .number()
            .int()
            .min(10)
            .max(600)
            .default(120)
            .describe(
              "How long to wait for Adams View to become reachable (seconds). Default 120."
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
    async ({ working_directory, mdi_path, timeout_seconds }) => {
      // ── Step 1: Validate working directory ──────────────────────────────
      try {
        const stat = await fs.stat(working_directory);
        if (!stat.isDirectory()) {
          return errorResult(`Not a directory: ${working_directory}`);
        }
      } catch {
        return errorResult(`Working directory not found: ${working_directory}`);
      }

      // ── Step 2: Resolve Adams executable ────────────────────────────────
      let resolvedMdi: string;
      try {
        resolvedMdi = await resolveMdiPath(mdi_path);
      } catch (e: unknown) {
        return errorResult(e instanceof Error ? e.message : String(e));
      }

      // ── Step 3: Spawn Adams View (with aviewAS.cmd management) ──────────
      let cleanupAviewAs: () => Promise<void>;
      try {
        cleanupAviewAs = await spawnAdamsHidden(resolvedMdi, working_directory);
      } catch (e: unknown) {
        return errorResult(
          `Failed to launch Adams: ${e instanceof Error ? e.message : String(e)}`
        );
      }

      // ── Step 4+5: Wait for Command Server, then restore aviewAS.cmd ─────
      try {
        const ready = await waitForAdams(timeout_seconds * 1000);
        if (!ready) {
          return errorResult(
            `Adams View was launched but did not become reachable on port ${getPort()} ` +
            `within ${timeout_seconds} seconds.\n` +
            `Check that the Command Server started in Adams View ` +
            `(Tools > Command Server > Start).`
          );
        }
        return {
          content: [
            {
              type: "text" as const,
              text:
                `Adams View launched successfully.\n` +
                `  Working directory: ${working_directory}\n` +
                `  Executable: ${resolvedMdi}\n` +
                `  Command Server ready on port ${getPort()}.`,
            },
          ],
        };
      } finally {
        await cleanupAviewAs();
      }
    }
  );

  // ── adams_quit_view ───────────────────────────────────────────────────────
  server.registerTool(
    "adams_quit_view",
    {
      title: "Quit Adams View",
      description: `Saves the current Adams View session to a timestamped .bin backup file,
then shuts down the Adams View process.

How it works:
  1. Checks that Adams View is reachable via the Command Server.
  2. Saves the session: executes 'file bin write alert_if_exists=no file_name=<tmp>'.
  3. Sends 'quit confirmation=no' — Adams terminates immediately and does not
     send a response, so no acknowledgement is expected (fire-and-forget).
  4. Returns the path to the saved .bin file.

Returns:
  Success message with the path to the .bin backup file, or an error.`,
      inputSchema: z.object({}).strict(),
      annotations: {
        readOnlyHint: false,
        destructiveHint: true,
        idempotentHint: false,
        openWorldHint: false,
      },
    },
    async () => {
      if (!(await checkConnection())) {
        return errorResult(
          "Adams View is not running or the Command Server is not reachable.\n" +
          "In Adams View: Tools > Command Server > Start"
        );
      }

      let binPath: string;
      try {
        binPath = await saveSessionToBin();
      } catch (e: unknown) {
        return errorResult(
          `Failed to save session before quitting: ${e instanceof Error ? e.message : String(e)}`
        );
      }

      await sendCmd("quit confirmation=no");

      return {
        content: [
          {
            type: "text" as const,
            text:
              `Adams View has been shut down.\n` +
              `  Session saved to: ${binPath}`,
          },
        ],
      };
    }
  );

  // ── adams_restart_view ────────────────────────────────────────────────────
  server.registerTool(
    "adams_restart_view",
    {
      title: "Restart Adams View",
      description: `Saves the current Adams View session, shuts down Adams View, and immediately
relaunches it in the same working directory with the Command Server running.

How it works:
  1. Checks that Adams View is reachable via the Command Server.
  2. Captures the current working directory via getcwd().
  3. Resolves the Adams executable (mdi_path or auto-discovery).
  4. Saves the session: 'file bin write alert_if_exists=no file_name=<tmp>'.
  5. Sends 'quit confirmation=no' to shut Adams down.
  6. Waits up to 30 seconds for Adams to fully exit (avoids port-binding race).
  7. Relaunches Adams View via the same mechanism as adams_launch_view.
  8. Waits up to timeout_seconds for the Command Server to become reachable.
  9. Returns success with the bin file path and Command Server port.

Args:
  - mdi_path (string, optional): Explicit path to mdi.bat (Windows) or mdi
    (Linux). If omitted, auto-discovery is used (same as adams_launch_view).
  - timeout_seconds (integer, default 120): How long to wait for Adams View
    to become reachable after restart.

Returns:
  Success message with the session backup path, working directory, executable,
  and Command Server port — or an error.`,
      inputSchema: z
        .object({
          mdi_path: z
            .string()
            .optional()
            .describe(
              "Explicit path to mdi.bat (Windows) or mdi (Linux). " +
              "If omitted, auto-discovery is attempted via ADAMS_LAUNCH_COMMAND " +
              "env var, ADAMS_INSTALL_DIR env var, or the default install location."
            ),
          timeout_seconds: z
            .number()
            .int()
            .min(10)
            .max(600)
            .default(120)
            .describe(
              "How long to wait for Adams View to become reachable after restart (seconds). Default 120."
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
    async ({ mdi_path, timeout_seconds }) => {
      // ── Step 1: Pre-flight check ─────────────────────────────────────────
      if (!(await checkConnection())) {
        return errorResult(
          "Adams View is not running or the Command Server is not reachable.\n" +
          "In Adams View: Tools > Command Server > Start"
        );
      }

      // ── Step 2: Capture working directory before quitting ────────────────
      let workDir: string;
      try {
        workDir = String(await evaluateExp("getcwd()"));
      } catch (e: unknown) {
        return errorResult(
          `Failed to get Adams working directory: ${e instanceof Error ? e.message : String(e)}`
        );
      }

      // ── Step 3: Resolve executable before quitting ───────────────────────
      let resolvedMdi: string;
      try {
        resolvedMdi = await resolveMdiPath(mdi_path);
      } catch (e: unknown) {
        return errorResult(e instanceof Error ? e.message : String(e));
      }

      // ── Step 4: Save session ─────────────────────────────────────────────
      let binPath: string;
      try {
        binPath = await saveSessionToBin();
      } catch (e: unknown) {
        return errorResult(
          `Failed to save session before restarting: ${e instanceof Error ? e.message : String(e)}`
        );
      }

      // ── Step 5: Quit Adams ───────────────────────────────────────────────
      await sendCmd("quit confirmation=no");

      // ── Step 6: Wait for Adams to fully exit ─────────────────────────────
      // Prevents a port-binding race where the new process tries to listen
      // on the same port before the old one has fully released it.
      await waitForAdamsDown(30_000);

      // ── Step 7: Relaunch Adams View ──────────────────────────────────────
      let cleanupAviewAs: () => Promise<void>;
      try {
        cleanupAviewAs = await spawnAdamsHidden(resolvedMdi, workDir);
      } catch (e: unknown) {
        return errorResult(
          `Session saved to ${binPath} but failed to relaunch Adams: ` +
          `${e instanceof Error ? e.message : String(e)}`
        );
      }

      // ── Step 8+9: Wait for Command Server, then restore aviewAS.cmd ─────
      try {
        const ready = await waitForAdams(timeout_seconds * 1000);
        if (!ready) {
          return errorResult(
            `Session saved to ${binPath}. Adams quit successfully but did not become ` +
            `reachable again on port ${getPort()} within ${timeout_seconds} seconds.\n` +
            `Try launching Adams manually: adams_launch_view`
          );
        }
        return {
          content: [
            {
              type: "text" as const,
              text:
                `Adams View restarted successfully.\n` +
                `  Session saved to: ${binPath}\n` +
                `  Working directory: ${workDir}\n` +
                `  Executable: ${resolvedMdi}\n` +
                `  Command Server ready on port ${getPort()}.`,
            },
          ],
        };
      } finally {
        await cleanupAviewAs();
      }
    }
  );
}

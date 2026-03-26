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
import { checkConnection, getPort } from "../client.js";

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
      const isWindows = process.platform === "win32";
      let resolvedMdi: string;

      if (mdi_path) {
        try {
          await fs.access(mdi_path);
        } catch {
          return errorResult(`mdi executable not found at: ${mdi_path}`);
        }
        resolvedMdi = mdi_path;
      } else {
        const discovered = await findMdi();
        if (!discovered) {
          return errorResult(
            "Could not auto-discover the Adams executable (mdi.bat / mdi).\n" +
            "Options:\n" +
            "  1. Pass mdi_path explicitly to this tool.\n" +
            "  2. Set the ADAMS_LAUNCH_COMMAND environment variable to the full path of mdi.bat.\n" +
            "  3. Set ADAMS_INSTALL_DIR to your Adams installation parent directory\n" +
            "     (e.g. C:\\Program Files\\MSC.Software\\Adams)."
          );
        }
        resolvedMdi = discovered;
      }

      const mdiArgs = isWindows
        ? ["aview", "ru-s", "i"]
        : ["-c", "aview", "ru-s", "i", "exit"];

      // On Windows, mdi.bat internally uses `start` to launch sub-processes,
      // each of which creates a brief console window. windowsHide:true only
      // hides the process Node spawns directly — it cannot suppress windows
      // opened by `start` calls inside mdi.bat.
      //
      // The fix: launch via wscript.exe + Shell.Run with window style 0
      // (SW_HIDE). Shell.Run propagates the hidden flag through the batch
      // launch chain, suppressing all intermediate console windows.
      let spawnCmd: string;
      let spawnArgs: string[];

      if (isWindows) {
        // Build a single-line VBScript that runs mdi.bat hidden and detached.
        // Shell.Run(..., 0, False) = window style 0 (hidden), don't wait.
        // Shell.Run requires paths with spaces to be quoted; in VBScript a
        // literal " inside a "-delimited string is written as "".
        const mdiEscaped = resolvedMdi.replace(/"/g, '""');
        const argsStr = mdiArgs.join(" ");
        const cmd = `""${mdiEscaped}"" ${argsStr}`;
        const vbs = `CreateObject("WScript.Shell").Run "${cmd}", 0, False`;
        const vbsTmp = path.join(os.tmpdir(), `adams-launch-${crypto.randomUUID()}.vbs`);
        await fs.writeFile(vbsTmp, vbs, "utf8");
        // Schedule cleanup after a short delay so wscript has time to read it
        setTimeout(() => fs.unlink(vbsTmp).catch(() => undefined), 10_000);
        spawnCmd = "wscript.exe";
        spawnArgs = ["/nologo", vbsTmp];
      } else {
        spawnCmd = resolvedMdi;
        spawnArgs = mdiArgs;
      }

      // ── Step 3: Manage aviewAS.cmd ───────────────────────────────────────
      const aviewAsCmdPath = path.join(working_directory, AVIEW_AS_CMD);
      let originalContent: string | null = null;

      try {
        originalContent = await fs.readFile(aviewAsCmdPath, "utf8");
      } catch {
        // File doesn't exist — will be created from scratch
      }

      const needsCleanup =
        originalContent === null ||
        !originalContent.trimEnd().endsWith(COMMAND_SERVER_LINE);

      try {
        if (originalContent === null) {
          // Create new file
          await fs.writeFile(aviewAsCmdPath, `${COMMAND_SERVER_LINE}\n`, "utf8");
        } else if (!originalContent.trimEnd().endsWith(COMMAND_SERVER_LINE)) {
          // Append to existing file
          const sep = originalContent.endsWith("\n") ? "" : "\n";
          await fs.writeFile(
            aviewAsCmdPath,
            `${originalContent}${sep}${COMMAND_SERVER_LINE}\n`,
            "utf8"
          );
        }
        // If the file already ends with the line, no modification needed

        // ── Step 4: Launch Adams View ──────────────────────────────────────
        const adams = spawn(spawnCmd, spawnArgs, {
          cwd: working_directory,
          detached: true,
          stdio: "ignore",
        });
        adams.unref();

        // ── Step 5: Wait for Command Server to become reachable ────────────
        // Adams needs time to start up and process aviewAS.cmd before the
        // Command Server is ready on its port.
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
        // ── Step 6: Restore aviewAS.cmd ────────────────────────────────────
        if (needsCleanup) {
          try {
            if (originalContent === null) {
              // We created it — delete it
              await fs.unlink(aviewAsCmdPath);
            } else {
              // We appended — restore original
              await fs.writeFile(aviewAsCmdPath, originalContent, "utf8");
            }
          } catch {
            // Best-effort; don't mask the real result
          }
        }
      }
    }
  );
}

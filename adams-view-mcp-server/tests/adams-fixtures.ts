/**
 * tests/adams-fixtures.ts — Launch and teardown helpers for E2E tests.
 *
 * Provides a beforeAll/afterAll pair that:
 *   1. Allocates a free TCP port so tests NEVER connect to an existing
 *      Adams View session on the default port (5002).
 *   2. Finds mdi.bat, writes aviewAS.cmd with 'command_server port=<N> start',
 *      and launches Adams View silently via wscript.exe + VBScript.
 *   3. Sets ADAMS_LISTENER_PORT in process.env so client.ts picks up the
 *      isolated port for all subsequent calls in this test run.
 *   4. Polls until the Command Server is reachable on the isolated port.
 *   5. Kills the Adams process and restores aviewAS.cmd in afterAll.
 *
 * The e2e tests always launch their own Adams View process. They never
 * attach to a pre-existing session, which prevents collateral damage to
 * interactive sessions the user may have open on the default port.
 *
 * Usage:
 *   import { setupAdams, teardownAdams } from "./adams-fixtures.js";
 *   beforeAll(setupAdams, 180_000);
 *   afterAll(teardownAdams);
 */

import * as fs from "fs/promises";
import * as net from "net";
import * as os from "os";
import * as path from "path";
import { randomUUID } from "crypto";
import { spawn, execSync } from "child_process";
import { checkConnection } from "../src/client.js";
import { findMdi } from "../src/mdi.js";

const AVIEW_AS_CMD = "aviewAS.cmd";
const POLL_INTERVAL_MS = 2000;
const DEFAULT_TIMEOUT_MS = 120_000;
const E2E_WORK_DIR = path.join(import.meta.dirname, "e2e_working_directory");

// Track whether we launched Adams ourselves so teardown can kill it
let weStartedAdams = false;
let adamsWorkDir = E2E_WORK_DIR;
let originalAviewAsContent: string | null = null;
let aviewAsCmdPath = "";


// ── poll ──────────────────────────────────────────────────────────────────────

async function waitForAdams(timeoutMs: number): Promise<boolean> {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    try {
      if (await checkConnection()) return true;
    } catch { /* not ready yet */ }
    await new Promise((r) => setTimeout(r, POLL_INTERVAL_MS));
  }
  return false;
}

// ── launch ────────────────────────────────────────────────────────────────────

async function launchAdams(mdiPath: string, workDir: string, port: number): Promise<void> {
  await fs.mkdir(workDir, { recursive: true });

  // Manage aviewAS.cmd so Command Server starts on our isolated port
  const commandServerLine = `command_server port=${port} start`;
  aviewAsCmdPath = path.join(workDir, AVIEW_AS_CMD);
  try {
    originalAviewAsContent = await fs.readFile(aviewAsCmdPath, "utf8");
  } catch {
    originalAviewAsContent = null;
  }

  if (originalAviewAsContent === null) {
    await fs.writeFile(aviewAsCmdPath, `${commandServerLine}\n`, "utf8");
  } else {
    const sep = originalAviewAsContent.endsWith("\n") ? "" : "\n";
    await fs.writeFile(
      aviewAsCmdPath,
      `${originalAviewAsContent}${sep}${commandServerLine}\n`,
      "utf8"
    );
  }

  const mdiArgs = ["aview", "ru-s", "i"];
  const isWindows = process.platform === "win32";

  if (isWindows) {
    const mdiEscaped = mdiPath.replace(/"/g, '""');
    const argsStr = mdiArgs.join(" ");
    const cmd = `""${mdiEscaped}"" ${argsStr}`;
    const vbs = `CreateObject("WScript.Shell").Run "${cmd}", 0, False`;
    const vbsTmp = path.join(os.tmpdir(), `adams-e2e-${randomUUID()}.vbs`);
    await fs.writeFile(vbsTmp, vbs, "utf8");
    setTimeout(() => fs.unlink(vbsTmp).catch(() => undefined), 15_000);
    spawn("wscript.exe", ["/nologo", vbsTmp], {
      cwd: workDir,
      detached: true,
      stdio: "ignore",
    }).unref();
  } else {
    spawn(mdiPath, mdiArgs, {
      cwd: workDir,
      detached: true,
      stdio: "ignore",
    }).unref();
  }
}

// ── port helpers ─────────────────────────────────────────────────────────────

/**
 * Ask the OS to assign a free TCP port by briefly binding to port 0,
 * then immediately releasing it. Returns the port number.
 */
function getFreePort(): Promise<number> {
  return new Promise((resolve, reject) => {
    const server = net.createServer();
    server.listen(0, "127.0.0.1", () => {
      const addr = server.address();
      const port = typeof addr === "object" && addr ? addr.port : 0;
      server.close((err) => {
        if (err) reject(err); else resolve(port);
      });
    });
    server.once("error", reject);
  });
}

// ── kill ──────────────────────────────────────────────────────────────────────

function killAdamsInDir(dir: string): void {
  try {
    if (process.platform === "win32") {
      // Find aview.exe process whose CWD matches our working dir
      // Using wmic to find PIDs of aview processes
      const result = execSync(
        `wmic process where "name='aview.exe'" get ProcessId,CommandLine /format:csv 2>nul`,
        { encoding: "utf8" }
      );
      const lines = result.split("\n").filter((l) => l.includes("aview"));
      for (const line of lines) {
        const parts = line.trim().split(",");
        const pid = parts[parts.length - 1]?.trim();
        if (pid && /^\d+$/.test(pid)) {
          try {
            process.kill(parseInt(pid, 10));
            console.log(`[e2e] Killed Adams View (PID ${pid})`);
          } catch { /* already gone */ }
        }
      }
    } else {
      execSync(`pkill -f "aview.*ru-s"`, { stdio: "ignore" });
    }
  } catch { /* pkill exits non-zero if nothing matched */ }
}

async function restoreAviewAsCmd(): Promise<void> {
  if (!aviewAsCmdPath) return;
  try {
    if (originalAviewAsContent === null) {
      await fs.unlink(aviewAsCmdPath).catch(() => undefined);
    } else {
      await fs.writeFile(aviewAsCmdPath, originalAviewAsContent, "utf8");
    }
  } catch { /* best-effort */ }
}

// ── exported fixtures ─────────────────────────────────────────────────────────

export async function setupAdams(): Promise<void> {
  weStartedAdams = false;

  // Always launch a fresh Adams View on an isolated port — never attach to
  // a pre-existing session on the default port. This prevents collateral
  // damage to interactive Adams sessions the user may have open.
  const mdi = await findMdi();
  if (!mdi) {
    console.log(
      "[e2e] mdi.bat not found — E2E tests will be skipped.\n" +
      "  Set ADAMS_LAUNCH_COMMAND or ADAMS_INSTALL_DIR to enable auto-launch."
    );
    return;
  }

  // Pick a free port and point the client at it for this process lifetime.
  const port = await getFreePort();
  process.env["ADAMS_LISTENER_PORT"] = String(port);

  adamsWorkDir = E2E_WORK_DIR;
  console.log(`[e2e] Launching Adams View from ${mdi} in ${adamsWorkDir} on port ${port} ...`);
  await launchAdams(mdi, adamsWorkDir, port);
  weStartedAdams = true;

  const ready = await waitForAdams(DEFAULT_TIMEOUT_MS);
  if (!ready) {
    throw new Error(
      `[e2e] Adams View launched but Command Server did not become reachable ` +
      `on port ${port} within ${DEFAULT_TIMEOUT_MS / 1000}s.`
    );
  }
  console.log(`[e2e] Adams View ready on port ${port}.`);
}

export async function teardownAdams(): Promise<void> {
  if (weStartedAdams) {
    console.log("[e2e] Tearing down Adams View we launched...");
    await restoreAviewAsCmd();
    killAdamsInDir(adamsWorkDir);
  }
}

/** True when Adams was reachable (or launched successfully) in beforeAll. */
export async function isAdamsAvailable(): Promise<boolean> {
  return checkConnection();
}

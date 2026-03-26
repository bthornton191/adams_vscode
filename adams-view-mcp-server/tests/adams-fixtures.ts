/**
 * tests/adams-fixtures.ts — Launch and teardown helpers for E2E tests.
 *
 * Provides a beforeAll/afterAll pair that:
 *   1. Checks if Adams View + Command Server is already running.
 *   2. If not, finds mdi.bat, writes aviewAS.cmd, and launches Adams View
 *      silently via wscript.exe + VBScript (same approach as adams_launch_view).
 *   3. Polls until the Command Server is reachable.
 *   4. Optionally kills the Adams process in afterAll if WE launched it.
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
import { spawn, execSync } from "child_process";
import { checkConnection, getPort } from "../src/client.js";

const AVIEW_AS_CMD = "aviewAS.cmd";
const COMMAND_SERVER_LINE = "command_server start";
const POLL_INTERVAL_MS = 2000;
const DEFAULT_TIMEOUT_MS = 120_000;
const E2E_WORK_DIR = path.join(import.meta.dirname, "e2e_working_directory");

// Track whether we launched Adams ourselves so teardown can kill it
let weStartedAdams = false;
let adamsWorkDir = E2E_WORK_DIR;
let originalAviewAsContent: string | null = null;
let aviewAsCmdPath = "";

// ── mdi discovery ─────────────────────────────────────────────────────────────

async function findLatestMdiUnder(parentDir: string, mdiName: string): Promise<string | null> {
  let entries: string[];
  try {
    const dirents = await fs.readdir(parentDir, { withFileTypes: true });
    entries = dirents.filter((d) => d.isDirectory()).map((d) => d.name);
  } catch {
    return null;
  }
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

async function findMdi(): Promise<string | null> {
  const isWindows = process.platform === "win32";
  const mdiName = isWindows ? "mdi.bat" : "mdi";

  const envLaunch = process.env["ADAMS_LAUNCH_COMMAND"];
  if (envLaunch) {
    try { await fs.access(envLaunch); return envLaunch; } catch { /* fall through */ }
  }
  const envInstall = process.env["ADAMS_INSTALL_DIR"];
  if (envInstall) {
    const found = await findLatestMdiUnder(envInstall, mdiName);
    if (found) return found;
  }
  if (isWindows) {
    const found = await findLatestMdiUnder(
      String.raw`C:\Program Files\MSC.Software\Adams`, mdiName
    );
    if (found) return found;
  }
  return null;
}

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

async function launchAdams(mdiPath: string, workDir: string): Promise<void> {
  await fs.mkdir(workDir, { recursive: true });

  // Manage aviewAS.cmd so Command Server starts automatically
  aviewAsCmdPath = path.join(workDir, AVIEW_AS_CMD);
  try {
    originalAviewAsContent = await fs.readFile(aviewAsCmdPath, "utf8");
  } catch {
    originalAviewAsContent = null;
  }

  const needsLine =
    originalAviewAsContent === null ||
    !originalAviewAsContent.trimEnd().endsWith(COMMAND_SERVER_LINE);

  if (originalAviewAsContent === null) {
    await fs.writeFile(aviewAsCmdPath, `${COMMAND_SERVER_LINE}\n`, "utf8");
  } else if (needsLine) {
    const sep = originalAviewAsContent.endsWith("\n") ? "" : "\n";
    await fs.writeFile(
      aviewAsCmdPath,
      `${originalAviewAsContent}${sep}${COMMAND_SERVER_LINE}\n`,
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
    const vbsTmp = path.join(os.tmpdir(), `adams-e2e-${crypto.randomUUID()}.vbs`);
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

// Need crypto for UUID
import { randomUUID as crypto_randomUUID } from "crypto";
const crypto = { randomUUID: crypto_randomUUID };

// ── port check ────────────────────────────────────────────────────────────────

/** Returns true if something (anything) is listening on the given TCP port. */
function isPortBound(port: number): Promise<boolean> {
  return new Promise((resolve) => {
    const s = new net.Socket();
    s.setTimeout(1500);
    s.once("connect", () => { s.destroy(); resolve(true); });
    s.once("error", () => { s.destroy(); resolve(false); });
    s.once("timeout", () => { s.destroy(); resolve(false); });
    s.connect(port, "127.0.0.1");
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
  const alreadyRunning = await checkConnection();

  if (alreadyRunning) {
    console.log("[e2e] Adams View already running — using existing session.");
    return;
  }

  // The port may be bound by a stuck/broken Adams session that failed
  // checkConnection() above. If so, kill it before launching a fresh one.
  const port = getPort();
  const portBound = await isPortBound(port);
  if (portBound) {
    console.log(
      `[e2e] Port ${port} is in use but Adams is not responding — ` +
      `killing existing Adams process before launching fresh.`
    );
    killAdamsInDir(adamsWorkDir);
    // Give the OS a moment to release the port
    await new Promise((r) => setTimeout(r, 2000));
  }

  const mdi = await findMdi();
  if (!mdi) {
    console.log(
      "[e2e] Adams View not running and mdi.bat not found — E2E tests will be skipped.\n" +
      "  Set ADAMS_LAUNCH_COMMAND or ADAMS_INSTALL_DIR to enable auto-launch."
    );
    return;
  }

  adamsWorkDir = E2E_WORK_DIR;
  console.log(`[e2e] Launching Adams View from ${mdi} in ${adamsWorkDir} ...`);
  await launchAdams(mdi, adamsWorkDir);
  weStartedAdams = true;

  const ready = await waitForAdams(DEFAULT_TIMEOUT_MS);
  if (!ready) {
    throw new Error(
      `[e2e] Adams View launched but Command Server did not become reachable ` +
      `on port ${getPort()} within ${DEFAULT_TIMEOUT_MS / 1000}s.`
    );
  }
  console.log(`[e2e] Adams View ready on port ${getPort()}.`);
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

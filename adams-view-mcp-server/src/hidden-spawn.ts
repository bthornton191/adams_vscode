/**
 * hidden-spawn.ts — Shared helper for spawning processes without visible
 * console windows on Windows.
 *
 * On Windows, Node's `windowsHide: true` only suppresses the console window
 * for the *first* process spawned. When launching mdi.bat, the .bat file
 * internally calls sub-scripts and executables whose windows are not covered
 * by the parent's CREATE_NO_WINDOW flag, causing multiple CMD windows to
 * flash briefly on screen.
 *
 * The fix is to launch via `wscript.exe` + a temporary VBScript file that
 * uses `Shell.Run "<cmd>", 0, <wait>`. Window style 0 suppresses console
 * windows for the entire child process tree.
 *
 * On non-Windows platforms, a direct spawn is used (no VBS wrapper needed).
 */

import * as crypto from "crypto";
import * as fsSyncModule from "fs";
import * as fs from "fs/promises";
import * as os from "os";
import * as path from "path";
import { spawn, ChildProcess, SpawnOptions } from "child_process";

/** Delay (ms) before deleting the temporary VBS file after spawn. */
const VBS_CLEANUP_DELAY_MS = 10_000;

export interface HiddenSpawnOptions {
  cwd?: string;
  detached?: boolean;
  /** Whether wscript should wait for the process to finish before exiting.
   *  - `true`  (recommended for batch/solver): wscript stays alive until the
   *    child exits, so `child.once("exit")` fires with the real exit code.
   *  - `false` (used by interactive session): wscript exits immediately after
   *    launching the child.
   */
  wait: boolean;
}

/**
 * Spawn a command without visible console windows on Windows.
 *
 * On Windows: writes a temp VBS file using Shell.Run with window style 0,
 * then spawns `wscript.exe /nologo <vbs>`.
 *
 * On non-Windows: spawns the command directly.
 *
 * @param cmd      Executable path (e.g. path to mdi.bat, or "cmd.exe")
 * @param args     Arguments for `cmd`
 * @param options  Spawn options. `wait` controls wscript wait mode (Windows only).
 * @returns        The spawned ChildProcess and a cleanup function (no-op on non-Windows).
 */
export async function spawnHidden(
  cmd: string,
  args: string[],
  options: HiddenSpawnOptions
): Promise<{ child: ChildProcess; cleanup: () => void }> {
  const isWindows = process.platform === "win32";

  if (!isWindows) {
    const spawnOpts: SpawnOptions = {
      cwd: options.cwd,
      detached: options.detached ?? false,
      stdio: "ignore",
    };
    const child = spawn(cmd, args, spawnOpts);
    return { child, cleanup: () => undefined };
  }

  // On Windows: build a VBS wrapper so Shell.Run hides all child windows.
  // The full command must be a single string passed to Shell.Run.
  // Quotes inside the path must be escaped by doubling them for VBScript strings.
  const cmdEscaped = cmd.replace(/"/g, '""');
  const argsStr = args.map((a) => (a.includes(" ") ? `"${a}"` : a)).join(" ");
  const fullCmd = argsStr ? `""${cmdEscaped}"" ${argsStr}` : `""${cmdEscaped}""`;
  const waitFlag = options.wait ? "True" : "False";
  const vbs = `CreateObject("WScript.Shell").Run "${fullCmd}", 0, ${waitFlag}`;

  const vbsTmp = path.join(os.tmpdir(), `adams-spawn-${crypto.randomUUID()}.vbs`);
  await fs.writeFile(vbsTmp, vbs, "utf8");

  // Schedule VBS cleanup. For wait=True the file is read before wscript exits,
  // so 10s is more than sufficient. For wait=False it's read nearly instantly.
  const cleanupTimer = setTimeout(
    () => fs.unlink(vbsTmp).catch(() => undefined),
    VBS_CLEANUP_DELAY_MS
  );

  const cleanup = () => {
    clearTimeout(cleanupTimer);
    try { fsSyncModule.unlinkSync(vbsTmp); } catch { /* already gone */ }
  };

  const spawnOpts: SpawnOptions = {
    cwd: options.cwd,
    detached: options.detached ?? false,
    stdio: "ignore",
  };
  const child = spawn("wscript.exe", ["/nologo", vbsTmp], spawnOpts);

  return { child, cleanup };
}

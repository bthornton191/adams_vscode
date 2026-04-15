/**
 * mdi.ts — Shared Adams executable (mdi.bat / mdi) resolution.
 *
 * Extracted from tools/session.ts so it can be used by both interactive-
 * session tools (adams_launch_view, adams_restart_view) and batch tools
 * (adams_run_batch).
 */

import * as fs from "fs/promises";
import * as path from "path";

/**
 * Resolve and validate the Adams mdi executable path.
 * Throws with a human-readable message if the path cannot be resolved.
 */
export async function resolveMdiPath(mdiPath?: string): Promise<string> {
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
export async function findMdi(): Promise<string | null> {
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
export async function findLatestMdiUnder(
  parentDir: string,
  mdiName: string
): Promise<string | null> {
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

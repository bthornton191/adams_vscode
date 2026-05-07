const crypto = require("crypto");
const fs = require("fs");
const os = require("os");
const path = require("path");
const child_process = require("child_process");

const VBS_CLEANUP_DELAY_MS = 10_000;

/**
 * Launch an external process without flashing console windows on Windows.
 *
 * On Windows, spawning a .bat file with shell:true causes the entire mdi.bat
 * call chain to open visible CMD windows. Instead, we use wscript.exe with
 * Shell.Run style=0 (SW_HIDE). Style 0 suppresses console windows for the
 * entire child process tree, while GUI apps like Adams View still show their
 * own windows because they call ShowWindow() themselves.
 *
 * Quotes are embedded using Chr(34) concatenation to avoid all VBScript
 * string-escaping ambiguity. Windows file paths cannot contain " so stripping
 * any " from paths before embedding them is safe.
 *
 * On non-Windows, falls back to a direct detached spawn (native mdi binary
 * does not need a shell wrapper).
 *
 * @param {string} cmd - Executable path (e.g. path to mdi.bat)
 * @param {string[]} args - Arguments for the command
 * @param {string} cwd - Working directory
 * @param {function|null} on_error - Optional error callback (receives Error)
 * @returns {import("child_process").ChildProcess}
 */
function spawnDetached(cmd, args, cwd, on_error = null) {
    if (process.platform !== "win32") {
        const child = child_process.spawn(cmd, args, {
            cwd,
            detached: true,
            stdio: "ignore",
        });
        child.unref();
        if (on_error) child.on("error", on_error);
        return child;
    }

    // Build Shell.Run command line using Chr(34) for literal quote characters.
    // Example output for mdi.bat with spaces in path:
    //   CreateObject("WScript.Shell").Run Chr(34) & "C:\Program Files\...\mdi.bat" & Chr(34) & " aview" & " ru-s" & " i", 0, False
    const safeCmd = cmd.replace(/"/g, "");
    let cmdLine = `Chr(34) & "${safeCmd}" & Chr(34)`;
    for (const arg of args) {
        const safeArg = arg.replace(/"/g, "");
        if (safeArg.includes(" ")) {
            cmdLine += ` & " " & Chr(34) & "${safeArg}" & Chr(34)`;
        } else {
            cmdLine += ` & " ${safeArg}"`;
        }
    }
    // Style 0 = SW_HIDE: hides console windows for the full process tree.
    // Adams View is a GUI app and shows its own window regardless.
    // wait=False: fire-and-forget (wscript exits immediately after launching).
    const vbs = `CreateObject("WScript.Shell").Run ${cmdLine}, 0, False`;

    const vbsTmp = path.join(os.tmpdir(), `adams-spawn-${crypto.randomUUID()}.vbs`);
    fs.writeFileSync(vbsTmp, vbs, "utf8");
    setTimeout(() => {
        try { fs.unlinkSync(vbsTmp); } catch { /* already cleaned up */ }
    }, VBS_CLEANUP_DELAY_MS);

    const child = child_process.spawn("wscript.exe", ["/nologo", vbsTmp], {
        cwd,
        detached: true,
        stdio: "ignore",
    });
    child.unref();
    if (on_error) child.on("error", on_error);
    return child;
}

exports.spawnDetached = spawnDetached;

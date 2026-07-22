const fs = require("fs");
const path = require("path");

/**
 * Read the original AdamsSetup.bat, replace the self-discovery line
 * (`set topdir=%~dsp0%`) with the literal path to the Adams `common`
 * directory, and remove the final `%windir%\system32\cmd.exe /K`
 * line so the script does not spawn a nested shell when run inside a
 * VS Code integrated terminal.
 *
 * The replacement preserves a trailing path separator so the existing
 * `set topdir=%topdir:~0,-7%` logic on the following line correctly
 * strips `common\` to derive the Adams root directory.
 *
 * @param {string} adamsSetupBatPath  Absolute path to the original AdamsSetup.bat
 * @param {string} storageDir         Writable directory for the generated wrapper
 * @returns {string} Absolute path to the generated wrapper script
 */
function generateWrapperScript(adamsSetupBatPath, storageDir) {
    if (!fs.existsSync(adamsSetupBatPath)) {
        throw new Error("AdamsSetup.bat not found at: " + adamsSetupBatPath);
    }
    var content = fs.readFileSync(adamsSetupBatPath, "utf8");

    var commonDir = path.dirname(adamsSetupBatPath) + path.sep;

    // Replace the self-discovery line.  The pattern matches:
    //   set topdir=%~dsp0%     (2024_2 and likely other versions)
    //   set topdir=%~dp0%      (hypothetical alternate)
    // The [a-zA-Z]* covers any combination of batch modifiers (d, p, s, etc.).
    // [\r]?$ handles both LF and CRLF line endings.
    var topdirPattern = /^set\s+topdir\s*=\s*%~[a-zA-Z]*0%?[ \t]*([\r]?)$/im;
    var topdirReplacement = 'set "topdir=' + commonDir + '"$1';
    var topdirMatched = topdirPattern.test(content);
    content = content.replace(topdirPattern, topdirReplacement);

    if (!topdirMatched) {
        throw new Error(
            "Could not find the 'set topdir=' self-discovery line in AdamsSetup.bat. " +
                "The file format may have changed. Please report this issue."
        );
    }

    // Remove the `%windir%\system32\cmd.exe /K` line that spawns a
    // nested interactive shell.  Replace with a comment so the file
    // structure is preserved.
    var cmdPattern = /^%windir%\\system32\\cmd\.exe[ \t]+\/K[ \t]*([\r]?)$/im;
    content = content.replace(
        cmdPattern,
        ":: cmd.exe /K removed for VS Code integrated terminal$1"
    );

    // Ensure the storage directory exists.
    if (!fs.existsSync(storageDir)) {
        fs.mkdirSync(storageDir, { recursive: true });
    }

    var wrapperPath = path.join(storageDir, "adams_terminal_setup.bat");
    fs.writeFileSync(wrapperPath, content, "utf8");
    return wrapperPath;
}

/**
 * Resolve the terminal options (shellPath, shellArgs, cwd) needed to
 * launch an Adams-configured cmd shell.
 *
 * @param {object} context  VS Code ExtensionContext
 * @returns {{name: string, shellPath: string, shellArgs: string[], cwd: (string|undefined)}}
 */
function getAdamsTerminalOptions(context) {
    var vscode = require("vscode");

    var mdiBat = vscode.workspace
        .getConfiguration("msc-adams")
        .get("adamsLaunchCommand");

    if (!mdiBat || !fs.existsSync(mdiBat)) {
        throw new Error("Adams launch command not found");
    }

    var adamsSetupBat = path.join(path.dirname(mdiBat), "AdamsSetup.bat");

    if (!fs.existsSync(adamsSetupBat)) {
        throw new Error("AdamsSetup.bat not found at: " + adamsSetupBat);
    }

    var wrapperPath = generateWrapperScript(
        adamsSetupBat,
        context.globalStorageUri.fsPath
    );

    var cwd = undefined;
    if (vscode.workspace.workspaceFolders && vscode.workspace.workspaceFolders.length > 0) {
        cwd = vscode.workspace.workspaceFolders[0].uri.fsPath;
    }

    return {
        name: "Adams CMD",
        shellPath: process.env.ComSpec || "cmd.exe",
        shellArgs: ["/K", wrapperPath],
        cwd: cwd,
    };
}

/**
 * Factory that returns the command handler for "MSC Adams: Open Adams Terminal".
 *
 * @param {object} context        VS Code ExtensionContext
 * @param {object} output_channel VS Code OutputChannel
 * @param {object|null} reporter  Telemetry reporter (optional)
 * @returns {function} Command handler
 */
function open_adams_terminal(context, output_channel, reporter) {
    if (reporter === undefined) reporter = null;

    return function () {
        var vscode = require("vscode");

        if (process.platform !== "win32") {
            vscode.window.showWarningMessage(
                "Adams Terminal is only available on Windows."
            );
            return;
        }

        var mdiBat = vscode.workspace
            .getConfiguration("msc-adams")
            .get("adamsLaunchCommand");

        if (!mdiBat || !fs.existsSync(mdiBat)) {
            vscode.window
                .showErrorMessage(
                    "Adams launch command not found!",
                    "Open Settings"
                )
                .then(function (selection) {
                    if (selection === "Open Settings") {
                        vscode.commands.executeCommand(
                            "workbench.action.openSettings",
                            "msc-adams.adamsLaunchCommand"
                        );
                    }
                });
            if (reporter) {
                reporter.sendTelemetryErrorEvent("open_adams_terminal", {
                    error_type: "config_missing",
                });
            }
            return;
        }

        var adamsSetupBat = path.join(path.dirname(mdiBat), "AdamsSetup.bat");

        if (!fs.existsSync(adamsSetupBat)) {
            vscode.window.showErrorMessage(
                "AdamsSetup.bat not found at: " + adamsSetupBat
            );
            if (reporter) {
                reporter.sendTelemetryErrorEvent("open_adams_terminal", {
                    error_type: "setup_bat_missing",
                });
            }
            return;
        }

        var wrapperPath;
        try {
            wrapperPath = generateWrapperScript(
                adamsSetupBat,
                context.globalStorageUri.fsPath
            );
        } catch (error) {
            console.log("error: " + error.message);
            output_channel.appendLine(
                "[" +
                    new Date().toLocaleTimeString() +
                    "]: error: " +
                    error.message
            );
            vscode.window.showErrorMessage(
                "Failed to create Adams terminal setup script: " + error.message
            );
            if (reporter) {
                reporter.sendTelemetryErrorEvent("open_adams_terminal", {
                    error_type: "wrapper_write_failed",
                    error_message: error.message,
                });
            }
            return;
        }

        var cwd = undefined;
        if (
            vscode.workspace.workspaceFolders &&
            vscode.workspace.workspaceFolders.length > 0
        ) {
            cwd = vscode.workspace.workspaceFolders[0].uri.fsPath;
        }

        try {
            var terminal = vscode.window.createTerminal({
                name: "Adams CMD",
                shellPath: process.env.ComSpec || "cmd.exe",
                shellArgs: ["/K", wrapperPath],
                cwd: cwd,
            });
            terminal.show();

            output_channel.appendLine(
                "[" +
                    new Date().toLocaleTimeString() +
                    "]: Adams terminal launched with setup script: " +
                    wrapperPath
            );
            if (reporter) {
                reporter.sendTelemetryEvent("open_adams_terminal");
            }
        } catch (error) {
            console.log("error: " + error.message);
            output_channel.appendLine(
                "[" +
                    new Date().toLocaleTimeString() +
                    "]: error: " +
                    error.message
            );
            if (reporter) {
                reporter.sendTelemetryErrorEvent("open_adams_terminal", {
                    error_type: "terminal_error",
                    error_message: error.message,
                });
            }
        }
    };
}

exports.generateWrapperScript = generateWrapperScript;
exports.getAdamsTerminalOptions = getAdamsTerminalOptions;
exports.open_adams_terminal = open_adams_terminal;
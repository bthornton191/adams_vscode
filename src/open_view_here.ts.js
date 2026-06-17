const vscode = require("vscode");
const fs = require("fs");
const child_process = require("child_process");

function open_view_here(output_channel, reporter = null) {
    return (uri) => {
        const adams_launch_command = vscode.workspace
            .getConfiguration("msc-adams")
            .get("adamsLaunchCommand");

        if (!adams_launch_command || !fs.existsSync(adams_launch_command)) {
            vscode.window
                .showErrorMessage("Adams launch command not found!", "Open Settings")
                .then((selection) => {
                    if (selection === "Open Settings") {
                        vscode.commands.executeCommand(
                            "workbench.action.openSettings",
                            "msc-adams.adamsLaunchCommand",
                        );
                    }
                });
            if (reporter) {
                reporter.sendTelemetryErrorEvent("open_view_here", {
                    error_type: "config_missing",
                });
            }
            return;
        }

        console.log(`"${adams_launch_command}" aview ru-s i`);
        output_channel.appendLine(
            `[${new Date().toLocaleTimeString()}]: "${adams_launch_command}" aview ru-s i`,
        );
        if (reporter)
            reporter.sendTelemetryEvent("open_view_here", {
                launch_command_configured: String(
                    !!adams_launch_command && fs.existsSync(adams_launch_command),
                ),
            });
        // Launch via child_process.exec: runs the launcher through a hidden
        // cmd.exe (no flashing console windows) while the mdi.bat chain still
        // runs in a real console — which MSC's launcher (run_mdi.py -> adamsctl)
        // requires — and the Adams View GUI shows its own window. This is the
        // long-standing approach that the 2.x exec->execFile->spawn->wscript
        // refactors regressed (flashing, then silent no-launch).
        child_process.exec(
            `"${adams_launch_command}" aview ru-s i`,
            { cwd: uri.fsPath },
            (error) => {
                if (error) {
                    console.log(`error: ${error.message}`);
                    output_channel.appendLine(
                        `[${new Date().toLocaleTimeString()}]: error: ${error.message}`,
                    );
                    if (reporter)
                        reporter.sendTelemetryErrorEvent("open_view_here", {
                            error_type: "process_error",
                            error_message: error.message,
                        });
                }
            },
        );
    };
}
exports.open_view_here = open_view_here;

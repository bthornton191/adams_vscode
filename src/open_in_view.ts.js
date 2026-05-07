const path = require("path");
const vscode = require("vscode");
const fs = require("fs");
const child_process = require("child_process");

function open_in_view(context, output_channel, reporter = null) {
    return (uri) => {
        let dir_name = path.dirname(uri.fsPath);
        let base_name = path.basename(uri.fsPath);

        const view_launcher = context.asAbsolutePath("resources/scripts/open_with_adams_view.bat");
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
                reporter.sendTelemetryErrorEvent("open_in_view", {
                    error_type: "config_missing",
                });
            }
            return;
        }
        console.log(`"${view_launcher}" "${base_name}" "${adams_launch_command}"`);
        // Write to output channel with timestamp
        output_channel.appendLine(
            `[${new Date().toLocaleTimeString()}]: "${view_launcher}" "${base_name}" "${adams_launch_command}"`,
        );
        if (reporter) reporter.sendTelemetryEvent("open_in_view");

        const child = child_process.spawn(
            view_launcher,
            [base_name, adams_launch_command],
            { cwd: dir_name, shell: true, detached: true, stdio: "ignore" },
        );
        child.unref();
        child.on("error", (error) => {
            console.log(`error: ${error.message}`);
            output_channel.appendLine(
                `[${new Date().toLocaleTimeString()}]: error: ${error.message}`,
            );
            if (reporter)
                reporter.sendTelemetryErrorEvent("open_in_view", {
                    error_type: "process_error",
                    error_message: error.message,
                });
        });
    };
}
exports.open_in_view = open_in_view;

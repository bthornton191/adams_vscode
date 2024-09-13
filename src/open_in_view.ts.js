const path = require('path');
const vscode = require('vscode');
const fs = require('fs');
const child_process = require("child_process");

function open_in_view(context, output_channel, reporter = null) {
    return (uri) => {

        let dir_name = path.dirname(uri.fsPath);
        let base_name = path.basename(uri.fsPath);

        const view_launcher = context.asAbsolutePath('resources/scripts/open_with_adams_view.bat');
        const adams_launch_command = vscode.workspace.getConfiguration('msc-adams').get('adamsLaunchCommand');

        if (!fs.existsSync(adams_launch_command)) {
            vscode.window.showErrorMessage("Adams launch command not found!", "Open Settings")
                .then((selection) => {
                    if (selection === "Open Settings") {
                        vscode.commands.executeCommand('workbench.action.openSettings', 'msc-adams.adams_launch_command');
                    }
                });
        }
        console.log(`"${view_launcher}" "${base_name}" "${adams_launch_command}"`);
        // Write to output channel with timestamp
        output_channel.appendLine(`[${new Date().toLocaleTimeString()}]: "${view_launcher}" "${base_name}" "${adams_launch_command}"`);
        reporter.sendTelemetryEvent("open_in_view");

        child_process.exec(`"${view_launcher}" "${base_name}" "${adams_launch_command}"`, { cwd: dir_name }, (error, stdout, stderr) => {
            if (error) {
                console.log(`error: ${error.message}`);
                output_channel.appendLine(`[${new Date().toLocaleTimeString()}]: error: ${error.message}`);
                reporter.sendTelemetryErrorEvent("open_in_view", {error: error.message});
                return;
            }
            if (stderr) {
                console.log(`stderr: ${stderr}`);
                output_channel.appendLine(`[${new Date().toLocaleTimeString()}]: stderr: ${stderr}`);
                reporter.sendTelemetryErrorEvent("open_in_view", { error: stderr });
                return;
            }
            console.log(`stdout: ${stdout}`);
            output_channel.appendLine(`[${new Date().toLocaleTimeString()}]: stdout: ${stdout}`);
        });
    };
}
exports.open_in_view = open_in_view;

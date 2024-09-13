const path = require('path');
const vscode = require('vscode');
const fs = require('fs');
const child_process = require("child_process");

function open_view_here(output_channel, reporter = null) {
    return (uri) => {

        let dir_name = path.dirname(uri.fsPath);
        let base_name = path.basename(uri.fsPath);
        const adams_launch_command = vscode.workspace.getConfiguration('msc-adams').get('adamsLaunchCommand');

        if (!fs.existsSync(adams_launch_command)) {
            vscode.window.showErrorMessage("Adams launch command not found!", "Open Settings")
                .then((selection) => {
                    if (selection === "Open Settings") {
                        vscode.commands.executeCommand('workbench.action.openSettings', 'msc-adams.adamsLaunchCommand');
                    }
                });
        }

        console.log(`"${adams_launch_command}" aview ru-s i`);
        output_channel.appendLine(`[${new Date().toLocaleTimeString()}]: "${adams_launch_command}" aview ru-s i`);
        reporter.sendTelemetryEvent("open_view_here");
        child_process.exec(`"${adams_launch_command}" aview ru-s i`, { cwd: uri.fsPath }, (error, stdout, stderr) => {
            if (error) {
                console.log(`error: ${error.message}`);
                output_channel.appendLine(`[${new Date().toLocaleTimeString()}]: error: ${error.message}`);
                reporter.sendTelemetryErrorEvent("open_view_here", { error: error.message });
                return;
            }
            if (stderr) {
                console.log(`stderr: ${stderr}`);
                output_channel.appendLine(`[${new Date().toLocaleTimeString()}]: stderr: ${stderr}`);
                reporter.sendTelemetryErrorEvent("open_view_here", { error: stderr });
                return;
            }
            console.log(`stdout: ${stdout}`);
            output_channel.appendLine(`[${new Date().toLocaleTimeString()}]: stdout: ${stdout}`);
        });
    };
}
exports.open_view_here = open_view_here;

const path = require("path");
const vscode = require("vscode");
const fs = require("fs");

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

        // Launch through a hidden VS Code integrated terminal rather than
        // child_process.exec. The extension host is a GUI process with no
        // console, so exec runs `cmd /d /s /c` with piped I/O and no real
        // console; MSC's launcher chain (mdi.bat -> menu.exe -> run_mdi.py ->
        // os.system("call adamsctl_<RAND>.bat")) needs a real console and
        // silently fails without one (exiting 0). The integrated terminal runs
        // cmd in a ConPTY (a real pseudo-console), which is the context the user
        // verified works, and hideFromUser keeps it out of the panel with no
        // flashing console window. Adams View shows its own GUI window.
        try {
            const terminal = vscode.window.createTerminal({
                name: "Adams View",
                cwd: dir_name,
                shellPath: process.env.ComSpec || "cmd.exe",
                hideFromUser: true,
            });
            // Do not dispose the terminal: that would kill the shell process
            // tree, potentially taking the just-launched Adams with it.
            terminal.sendText(`"${view_launcher}" "${base_name}" "${adams_launch_command}"`, true);
        } catch (error) {
            console.log(`error: ${error.message}`);
            output_channel.appendLine(
                `[${new Date().toLocaleTimeString()}]: error: ${error.message}`,
            );
            if (reporter)
                reporter.sendTelemetryErrorEvent("open_in_view", {
                    error_type: "terminal_error",
                    error_message: error.message,
                });
        }
    };
}
exports.open_in_view = open_in_view;

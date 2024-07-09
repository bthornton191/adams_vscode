const vscode = require("vscode");
const child_process = require("child_process");

function debug_in_adams(output_channel, done = () => {}) {
    return async () => {
        // Search running processes for aview.exe. If there are multiple, ask the user to select one and store the process id in a variable.
        let aview_pid = 0;
        let aview_pids = [];
        let aview_ptitles = [];
        let select_list = [];
        let aview_ptitle = "";

        // If the operating system is windows
        if (process.platform === "win32") {
            var plist = child_process
                .execSync('tasklist /fi "imagename eq aview.exe" /fo csv /nh /v')
                .toString()
                .split("\r\n"); // Get a list of running processes
        }

        // If the operating system is linux or mac
        else {
            var plist = child_process.execSync("ps -A | grep aview").toString().split("\r"); // Get a list of running processes
        }
        for (let i = 0; i < plist.length; i++) {
            // Loop through the list of processes
            let process = plist[i].split(","); // Split the process name and process id
            if (process.length > 1) {
                // If the process is not empty
                aview_pids.push(process[1].replace(/"/g, "")); // Add the process name to the list
                aview_ptitles.push(process[process.length - 1].replace(/"/g, "")); // Add the process name to the list (Remove quotes from the process name)
                select_list.push({
                    label: aview_ptitles[aview_ptitles.length - 1],
                    description: aview_pids[aview_pids.length - 1],
                }); // Add the process name and process id to the list
            }
        }

        // If there are no running processes, show an error message
        if (aview_pids.length == 0) {
            vscode.window.showErrorMessage("No aview Processes Found!");
            output_channel.appendLine(
                `[${new Date().toLocaleTimeString()}]: No aview Processes Found!`
            );
            return;
        }

        // If there are more than one running processes, ask the user to select one
        if (aview_pids.length > 1) {
            let selection = await vscode.window.showQuickPick(select_list, {
                placeHolder: "Select aview Process to Debug",
            });
            if (selection) {
                aview_pid = aview_pids[select_list.indexOf(selection)];
                aview_ptitle = aview_ptitles[select_list.indexOf(selection)];
            } else {
                return;
            }
        } else if (aview_pids.length == 1) {
            aview_pid = aview_pids[0];
            aview_ptitle = aview_ptitles[0];
        }

        // Get the aview version from the end of aview_ptitle
        let match = aview_ptitle.match(/\d+(?=(?:\.\d+)*)/);
        if (match) {
            var aview_version = parseInt(match[0]);
        } else {
            var aview_version = 0;
            console.log(`Could not find aview version in ${aview_ptitle}`);
            output_channel.appendLine(
                `[${new Date().toLocaleTimeString()}]: Could not find aview version in process title ${aview_ptitle}. Skipping version check.`
            );
        }

        // If the version is 2023 or newer, warn the user and ask if they want to continue
        if (
            aview_version >= 2023 &&
            vscode.workspace.getConfiguration("msc-adams").get("showDebuggerWarning") == true
        ) {
            vscode.window
                .showInformationMessage(
                    "You may need to import the threading module before attaching the debugger. [More Info](https://github.com/bthornton191/adams_vscode/issues/6#issuecomment-2192053891)",
                    "Don't show this message again."
                )
                .then((selection) => {
                    if (selection === "Don't show this message again.") {
                        vscode.workspace
                            .getConfiguration("msc-adams")
                            .update(
                                "showDebuggerWarning",
                                false,
                                vscode.ConfigurationTarget.Global
                            );
                    }
                });
        }

        // Log the process
        console.log(
            `Attaching Python Debugger to aview.exe Process: ${aview_ptitle} (${aview_pid})`
        );
        output_channel.appendLine(
            `[${new Date().toLocaleTimeString()}]: Attaching Python Debugger to aview.exe Process: ${aview_ptitle} (${aview_pid})`
        );

        // Attach python debugger to selected process
        await vscode.debug.startDebugging(
            undefined,
            Object.assign(
                {},
                {
                    name: "Attach to aview.exe",
                    type: "python",
                    request: "attach",
                    processId: aview_pid,
                },
                vscode.workspace.getConfiguration("msc-adams").get("debugOptions")
            )
        );

        vscode.window.showInformationMessage(
            "The debugger has been attached. Set a breakpoint, then run the python script in Adams"
        );

        done();
    };
}
exports.debug_in_adams = debug_in_adams;

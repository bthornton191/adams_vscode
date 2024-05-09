const vscode = require('vscode');
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
        if (process.platform === 'win32') {
            var plist = child_process.execSync('tasklist /fi "imagename eq aview.exe" /fo csv /nh /v').toString().split('\r\n'); // Get a list of running processes
        }

        // If the operating system is linux or mac
        else {
            var plist = child_process.execSync('ps -A | grep aview').toString().split('\r'); // Get a list of running processes
        }
        for (let i = 0; i < plist.length; i++) { // Loop through the list of processes
            let process = plist[i].split(','); // Split the process name and process id
            if (process.length > 1) { // If the process is not empty
                aview_pids.push(process[1].replace(/"/g, '')); // Add the process name to the list
                aview_ptitles.push(process[process.length - 1].replace(/"/g, '')); // Add the process name to the list (Remove quotes from the process name)                           
                select_list.push({ label: aview_ptitles[aview_ptitles.length - 1], description: aview_pids[aview_pids.length - 1] }); // Add the process name and process id to the list
            }
        }

        // If there are no running processes, show an error message
        if (aview_pids.length == 0) {
            vscode.window.showErrorMessage("No aview Processes Found!");
            output_channel.appendLine(`[${new Date().toLocaleTimeString()}]: No aview Processes Found!`);
            return;
        }

        // If there are more than one running processes, ask the user to select one
        if (aview_pids.length > 1) {
            let selection = await vscode.window.showQuickPick(select_list, { placeHolder: 'Select aview Process to Debug' });
            if (selection) {
                aview_pid = aview_pids[select_list.indexOf(selection)];
                aview_ptitle = aview_ptitles[select_list.indexOf(selection)];
            }
            else {
                return;
            }
        } else if (aview_pids.length == 1) {
            aview_pid = aview_pids[0];
            aview_ptitle = aview_ptitles[0];
        }

        // Get the aview version from the end of aview_ptitle
        let aview_version = aview_ptitle.split(' ')[aview_ptitle.split(' ').length - 1];

        // If the version is 2023 or newer, warn the user and ask if they want to continue
        if (parseInt(aview_version) >= 2023 && !vscode.workspace.getConfiguration("msc-adams").get("debugOptions").debugAdapterPath) {
            output_channel.appendLine(`[${new Date().toLocaleTimeString()}]: Trying to attach to version 2023 with no debug adapter: ${aview_version}. Awaiting User Selection...`);

            // Warn the user that this version is not supported
            let selection = await vscode.window.showQuickPick(["No", "Yes"], {
                title: "Adams 2023 requires a debug adapter",
                placeHolder: "Debugging in Adams 2023 requires a debug adapter. Do you want to continue?",
            });

            if (selection === "No") {
                output_channel.appendLine(`[${new Date().toLocaleTimeString()}]: User selected to not continue with aview version: ${aview_version}`);
                return;
            } else if (selection === "Open Settings") {
                output_channel.appendLine(
                    `[${new Date().toLocaleTimeString()}]: User selected to not continue with aview version: ${aview_version} and opened settings to add debug adapter path`
                );
                vscode.commands.executeCommand(
                    "workbench.action.openSettings",
                    "msc-adams.debugOptions"
                );
                return;
            } else {
                output_channel.appendLine(
                    `[${new Date().toLocaleTimeString()}]: User selected to continue with aview version: ${aview_version}`
                );
            }
        }

        // Log the process
        console.log(`Attaching Python Debugger to aview.exe Process: ${aview_ptitle} (${aview_pid})`);
        output_channel.appendLine(`[${new Date().toLocaleTimeString()}]: Attaching Python Debugger to aview.exe Process: ${aview_ptitle} (${aview_pid})`);

        // Attach python debugger to selected process
        await vscode.debug.startDebugging(undefined,
            Object.assign({}, {
                "name": "Attach to aview.exe",
                "type": "python",
                "request": "attach",
                "processId": aview_pid
            }, vscode.workspace.getConfiguration('msc-adams').get('debugOptions')));

        vscode.window.showInformationMessage('The debugger has been attached. Set a breakpoint, then run the python script in Adams');
        
        done();
    };
}
exports.debug_in_adams = debug_in_adams;

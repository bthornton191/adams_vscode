const path = require('path');
const vscode = require('vscode');
const fs = require('fs');
const child_process = require("child_process");
 
//Create output channel
const output_channel = vscode.window.createOutputChannel("MSC Adams");

// vscode.window.showInformationMessage(file)

function activate(context) {
	
	let function_names = new Map();
	let view_commandws = new Map();
	const func_dir = context.asAbsolutePath('resources/adams_design_functions');
	const func_files = fs.readdirSync(func_dir);
	
	for (var file of func_files) {
		if (fs.lstatSync([func_dir, file].join('/')).isFile()) {
			var text = fs.readFileSync([func_dir, file].join('/'),'utf8');
			var function_name = path.parse(file).name
			function_names.set(function_name, text)
			// vscode.window.showInformationMessage(path.parse(function_name).name)

		}
	}
	
	// ---------------------------------------------------------------------------
	// Hover
	// ---------------------------------------------------------------------------
    vscode.languages.registerHoverProvider('adams_cmd', {
		provideHover(document, position, token) {
			
			const range = document.getWordRangeAtPosition(position);
            const word = document.getText(range).toLowerCase();
			
			if (function_names.has(word)) {
				// var text = vscode.MarkdownString(function_names.get(word))
				var text = function_names.get(word)
				var markdown = new vscode.MarkdownString(text)
			};
			
			return new vscode.Hover(markdown, range);
        }
    });
	
	
	// ---------------------------------------------------------------------------
	// Completion
	// ---------------------------------------------------------------------------
	
	const cmd_files_json = context.asAbsolutePath('resources/adams_view_commands/unstructured.json');
	const commands = JSON.parse(fs.readFileSync(cmd_files_json))
	vscode.languages.registerCompletionItemProvider('adams_cmd', {
		
		provideCompletionItems(document, position, token, context) {
			
			let completions = []
			const range = document.getWordRangeAtPosition(position);
            const word = document.getText(range).toLowerCase();			
			const line = document.lineAt(position).text.substr(0, position.character);
			
			// Functions
			for (var [name, doc] of function_names.entries()) {
				if (name.startsWith(word)) {
					let completion = new vscode.CompletionItem(name);
					completion.kind = vscode.CompletionItemKind.Function;
					completion.command = { command: 'editor.action.showHover'};
					completion.documentation = new vscode.MarkdownString(doc);
					// vscode.window.showInformationMessage(function_names.get(name));
					completions.push(completion);
				}
			}
			
			// Commands
			for (var command of commands) {
				if (command.startsWith(line.trim())) {
					let completion = new vscode.CompletionItem(command);
					completion.kind = vscode.CompletionItemKind.Interface;
					completions.push(completion);
				}
			}
			
			return completions;
		}
	});
	
	// ---------------------------------------------------------------------------
	// Add stub files to extra python analysis paths
	// ---------------------------------------------------------------------------
	const stub_dir = context.asAbsolutePath('resources/adamspy');
	const section = vscode.workspace.getConfiguration('python', vscode.ConfigurationTarget.WorkspaceFolder);
	const current_setting = section.get('analysis.extraPaths').filter(item => ![stub_dir].includes(item));
	section.update('analysis.extraPaths', current_setting.concat([stub_dir]))
	
	// ---------------------------------------------------------------------------
	// Commands
	// ---------------------------------------------------------------------------
	const mh_command = 'msc_adams.macros.makeHeader';
	const mhCommandHandler = () => {
		const activeEditor = vscode.window.activeTextEditor;
		vscode.commands.executeCommand('editor.action.goToLocations', activeEditor.document.uri, vscode.P)
		vscode.commands.executeCommand('editor.action.insertSnippet', {langeId: "adams_cmd", name: "Macro Header"});
	};
	vscode.commands.registerCommand(mh_command, mhCommandHandler);

	const oiv_command = 'msc_adams.openInView';
	const oivCommandHandler = (uri) => {
		
		let dir_name = path.dirname(uri.fsPath);
		let base_name = path.basename(uri.fsPath);
        
        const view_launcher = context.asAbsolutePath('resources/scripts/open_with_adams_view.bat')
        const adams_launch_command = vscode.workspace.getConfiguration('msc-adams').get('adams_launch_command');

        if (!fs.existsSync(adams_launch_command)) {
            vscode.window.showErrorMessage("Adams launch command not found!", "Open Settings")
            .then((selection) => {
                if (selection === "Open Settings") {
                    vscode.commands.executeCommand('workbench.action.openSettings', 'msc-adams.adams_launch_command');
                }
            });
        }
	    console.log(`"${view_launcher}" "${base_name}" "${adams_launch_command}"`);
        output_channel.appendLine(`"${view_launcher}" "${base_name}" "${adams_launch_command}"`);

		child_process.exec(`"${view_launcher}" "${base_name}" "${adams_launch_command}"`, { cwd: dir_name }, (error, stdout, stderr) => {
			if (error) {
				console.log(`error: ${error.message}`);
                output_channel.appendLine(`error: ${error.message}`);
				return;
			}
			if (stderr) {
				console.log(`stderr: ${stderr}`);
                output_channel.appendLine(`stderr: ${stderr}`);
				return;
			}
			console.log(`stdout: ${stdout}`);
            output_channel.appendLine(`stdout: ${stdout}`);
		});
	};
	vscode.commands.registerCommand(oiv_command, oivCommandHandler);


	const ovh_command = 'msc_adams.openViewHere';
	const ovhCommandHandler = (uri) => {
		
		let dir_name = path.dirname(uri.fsPath);
		let base_name = path.basename(uri.fsPath);
        const adams_launch_command = vscode.workspace.getConfiguration('msc-adams').get('adams_launch_command');

        if (!fs.existsSync(adams_launch_command)) {
            vscode.window.showErrorMessage("Adams launch command not found!", "Open Settings")
            .then((selection) => {
                if (selection === "Open Settings") {
                    vscode.commands.executeCommand('workbench.action.openSettings', 'msc-adams.adams_launch_command');
                }
            });
        }
        
	    console.log(`"${adams_launch_command}" aview ru-s i`);
        output_channel.appendLine(`"${adams_launch_command}" aview ru-s i`);
		child_process.exec(`"${adams_launch_command}" aview ru-s i`, { cwd: uri.fsPath }, (error, stdout, stderr) => {
			if (error) {
				console.log(`error: ${error.message}`);
                output_channel.appendLine(`error: ${error.message}`);
				return;
			}
			if (stderr) {
				console.log(`stderr: ${stderr}`);
                output_channel.appendLine(`stderr: ${stderr}`);
				return;
			}
			console.log(`stdout: ${stdout}`);
            output_channel.appendLine(`stdout: ${stdout}`);
		});
	};
	vscode.commands.registerCommand(ovh_command, ovhCommandHandler);


	const debug_command = 'msc_adams.debugInAdams';
	const debugCommandHandler = async () => {
		// Search running processes for aview.exe. If there are multiple, ask the user to select one and store the process id in a variable.
        let aview_pid = 0;
        let aview_pids = [];
        let aview_ptitles = [];
        let select_list = [];
        let aview_ptitle = "";

        // If the operating system is windows
        if (process.platform === 'win32') {
            var plist = child_process.execSync('tasklist /fi "imagename eq aview.exe" /fo csv /nh /v').toString().split('\r\n');        // Get a list of running processes
        }
        // If the operating system is linux or mac
        else {
            var plist = child_process.execSync('ps -A | grep aview').toString().split('\r');                                      // Get a list of running processes
        }
        for (let i = 0; i < plist.length; i++) {                                                                                    // Loop through the list of processes
            let process = plist[i].split(',');                                                                                      // Split the process name and process id
            if (process.length > 1) {                                                                                               // If the process is not empty
                aview_pids.push(process[1].replace(/"/g, ''));                                                                      // Add the process name to the list
                aview_ptitles.push(process[process.length - 1].replace(/"/g, ''));                                                  // Add the process name to the list (Remove quotes from the process name)                           
                select_list.push({label: aview_ptitles[aview_ptitles.length -1], description: aview_pids[aview_pids.length -1]});   // Add the process name and process id to the list
            }
        }

        // If there are no running processes, show an error message
        if (aview_pids.length == 0) {
            vscode.window.showErrorMessage("No aview Processes Found!");
            output_channel.appendLine(`No aview Processes Found!`);
            return;
        }

        // If there are more than one running processes, ask the user to select one
        if (aview_pids.length > 1) {
            let selection = await vscode.window.showQuickPick(select_list, {placeHolder: 'Select aview Process to Debug'})
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
        if (parseInt(aview_version) >= 2023) {
            // let selection = await 
            
            output_channel.appendLine(`Unsupported aview version: ${aview_version}. Awaiting User Selection...`);
            // Warn the user that this version is not supported
            let selection = await vscode.window.showQuickPick(["No", "Yes"], {title: "Unsupported Adams version", placeHolder: "Debugging is not supported in Adams 2023 and later. Do you want to continue?"})

            if (selection === "No") {
                output_channel.appendLine(`User selected to not continue with aview version: ${aview_version}`);
                return;
            }
            else {
                output_channel.appendLine(`User selected to continue with aview version: ${aview_version}`);
            }
        }
        
        // Log the process
        console.log(`Attaching Python Debugger to aview.exe Process: ${aview_ptitle} (${aview_pid})`);
        output_channel.appendLine(`Attaching Python Debugger to aview.exe Process: ${aview_ptitle} (${aview_pid})`);

        // Attach python debugger to selected process
        await vscode.debug.startDebugging(undefined, {
            "name": "Attach to aview.exe",
            "type": "python",
            "request": "attach",
            "processId": aview_pid
        });
        
        vscode.window.showInformationMessage('The debugger has been attached. Set a breakpoint, then run the python script in Adams');

	};
	vscode.commands.registerCommand(debug_command, debugCommandHandler);

	vscode.window.showInformationMessage('MSC Adams Extension Activated');
	
}

function deactivate(context) {
	
	// ---------------------------------------------------------------------------
	// Remove stub files to extra python analysis paths
	// ---------------------------------------------------------------------------
	const stub_dir = context.asAbsolutePath('resources/adamspy');
	const section = vscode.workspace.getConfiguration('python', vscode.ConfigurationTarget.WorkspaceFolder)
	const current_setting = section.get('analysis.extraPaths').filter(item => ![stub_dir].includes(item));
	section.update('analysis.extraPaths', current_setting, vscode.ConfigurationTarget.WorkspaceFolder )
	vscode.window.showInformationMessage('MSC Adams Extension Deactivated');
}

const command = 'msc_adams.activate';
const commandHandler = () => {};
vscode.commands.registerCommand(command, commandHandler);

module.exports = {
    activate,
    deactivate
}

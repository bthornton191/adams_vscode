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
	const section = vscode.workspace.getConfiguration('python', vscode.ConfigurationTarget.Workspace)
	const current_setting = section.get('analysis.extraPaths').filter(item => ![stub_dir].includes(item));
	section.update('analysis.extraPaths', current_setting.concat([stub_dir]), vscode.ConfigurationTarget.Workspace )
	
	// ---------------------------------------------------------------------------
	// Commands
	// ---------------------------------------------------------------------------
	const mh_command = 'msc_adams.macros.makeHeader';
	const mhCommandHandler = () => {
		const activeEditor = vscode.window.activeTextEditor;
		vscode.commands.executeCommand('editor.action.goToLocations', activeEditor.document.uri, vscode.P)
		vscode.commands.executeCommand('editor.action.insertSnippet', {langeId: "adams_cmd", name: "Macro Header"});
		// const editor = vscode.window.activeTextEditor;
    	// if (editor) {
			// 	editor.edit(editBuilder => {
				//     	editBuilder.insert(editor.selection.active, text);
				// 	});
				// };
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

	vscode.window.showInformationMessage('MSC Adams Extension Activated');
	
}

function deactivate(context) {
	
	// ---------------------------------------------------------------------------
	// Remove stub files to extra python analysis paths
	// ---------------------------------------------------------------------------
	const stub_dir = context.asAbsolutePath('resources/adamspy');
	const section = vscode.workspace.getConfiguration('python', vscode.ConfigurationTarget.Workspace)
	const current_setting = section.get('analysis.extraPaths').filter(item => ![stub_dir].includes(item));
	section.update('analysis.extraPaths', current_setting, vscode.ConfigurationTarget.Workspace )
	vscode.window.showInformationMessage('MSC Adams Extension Deactivated');
}

const command = 'msc_adams.activate';
const commandHandler = () => {};
vscode.commands.registerCommand(command, commandHandler);

module.exports = {
    activate,
    deactivate
}

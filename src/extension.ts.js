const path = require('path');
const vscode = require('vscode');
const fs = require('fs');
const { open_in_view } = require('./open_in_view.ts');
const { open_view_here } = require('./open_view_here.ts.js');
const { load_stub_files } = require('./load_stub_files.ts');
const { run_selection } = require('./run_selection.ts.js');
const { debug_in_adams } = require('./debug_in_adams.ts');
const { make_macro_header } = require('./make_macro_header.ts');
const { cmd_completion_provider } = require('./cmd_completion_provider.ts');
const { cmd_hover_provider } = require('./cmd_hover_provider.ts');

//Create output channel
const output_channel = vscode.window.createOutputChannel("MSC Adams");


function activate(context) {
	
	const view_functions = new Map();
	const func_dir = context.asAbsolutePath('resources/adams_design_functions');
	const func_files = fs.readdirSync(func_dir);
	
	for (var file of func_files) {
		if (fs.lstatSync([func_dir, file].join('/')).isFile()) { 
			let text = fs.readFileSync([func_dir, file].join('/'),'utf8');
			let function_name = path.parse(file).name
			view_functions.set(function_name, text)
		}
	}
	
	// ---------------------------------------------------------------------------
	// Hover Provider
	// ---------------------------------------------------------------------------
    vscode.languages.registerHoverProvider('adams_cmd', cmd_hover_provider(view_functions));
	
	// ---------------------------------------------------------------------------
	// Completion Provider
	// ---------------------------------------------------------------------------
    const cmd_files_json = context.asAbsolutePath('resources/adams_view_commands/structured.json');
	const view_commands = JSON.parse(fs.readFileSync(cmd_files_json))
	vscode.languages.registerCompletionItemProvider('adams_cmd', cmd_completion_provider(view_functions, view_commands));
	
    // ---------------------------------------------------------------------------
	// Commands
	// ---------------------------------------------------------------------------
    vscode.commands.registerCommand('msc_adams.macros.makeHeader', make_macro_header());
    vscode.commands.registerCommand('msc_adams.openInView', open_in_view(context, output_channel));
    vscode.commands.registerCommand('msc_adams.openViewHere', open_view_here(output_channel));
    vscode.commands.registerCommand('msc_adams.debugInAdams', debug_in_adams(output_channel));
    vscode.commands.registerCommand('msc_adams.runSelection', run_selection(output_channel));
    vscode.commands.registerCommand('msc_adams.runFile', run_selection(output_channel, true));
    vscode.commands.registerCommand('msc_adams.loadStubFiles', load_stub_files(context, output_channel));
    // Set to run whenever the loadStubFiles setting is changed
    // vscode.workspace.onDidChangeConfiguration(load_stub_files(context, output_channel));
    
    if (vscode.workspace.getConfiguration().get('msc_adams.autoLoadAdamspyStubs')) {
        vscode.commands.executeCommand('msc_adams.loadStubFiles');
    }

    vscode.window.showInformationMessage('MSC Adams Extension Activated');
}

function deactivate(context) {
	vscode.window.showInformationMessage('MSC Adams Extension Deactivated');
}

const command = 'msc_adams.activate';
vscode.commands.registerCommand(command, activate);

module.exports = {
    activate,
    deactivate
}

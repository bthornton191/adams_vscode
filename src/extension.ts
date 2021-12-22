const path = require('path');
const vscode = require('vscode');
const fs = require('fs');


// vscode.window.showInformationMessage(file)
let function_names = new Map();

function activate(context) {
	
	const dir = context.asAbsolutePath('resources/adams_design_functions');
	const files = fs.readdirSync(dir);
	
	for (var file of files) {
		if (fs.lstatSync([dir, file].join('/')).isFile()) {
			var text = fs.readFileSync([dir, file].join('/'),'utf8');
			var function_name = path.parse(file).name
			function_names.set(function_name, text)
			// vscode.window.showInformationMessage(path.parse(function_name).name)

		}
	}
	
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
}

function deactivate() { }

module.exports = {
    activate,
    deactivate
}
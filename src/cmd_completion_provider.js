const vscode = require('vscode');

function cmd_completion_provider(function_names, commands) {
    return {
        provideCompletionItems(document, position, token, context) {
            let completions = [];
            const range = document.getWordRangeAtPosition(position);
            const word = document.getText(range).toLowerCase();
            const line = document.lineAt(position).text.substr(0, position.character);

            // Functions
            for (var [name, doc] of function_names.entries()) {
                if (name.startsWith(word)) {
                    let completion = new vscode.CompletionItem(name);
                    completion.kind = vscode.CompletionItemKind.Function;
                    completion.command = { command: 'editor.action.showHover' };
                    completion.documentation = new vscode.MarkdownString(doc);
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
    };
}
exports.cmd_completion_provider = cmd_completion_provider;

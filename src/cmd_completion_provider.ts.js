const vscode = require('vscode');

/**
 * @param {Map<string, string>} function_names
 * @param {Map<string, string[]} commands
 * @returns {vscode.CompletionItemProvider}
 */
function cmd_completion_provider(function_names, commands) {
    return {
        provideCompletionItems(document, position, token, context) {
            let completions = [];
            const range = document.getWordRangeAtPosition(position);
            const word = document.getText(range).toLowerCase();
            const line = document.lineAt(position).text.substr(0, position.character);
            
            // Remove all occurences of \s+\w+\s*=\s*([^\s]+|"[^"]*") 
            const line_without_args = line.replace(/\s+\w+\s*=\s*([^\s]+|"[^"]*")/g, '');

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
            
            // Arguments
            // If the stripped line EXACTLY matches a command, then we are in the arguments section
            if (commands.hasOwnProperty(line_without_args.trim())) {
                let command = line_without_args.trim();
                
                // Get the indentation
                if (vscode.workspace.getConfiguration('editor').get('insertSpaces')) {
                    let n_spaces = vscode.workspace.getConfiguration('editor').get('tabSize');
                    var indent_type = ' '.repeat(n_spaces);
                } else {
                    var indent_type = '\t';
                }
                var indent = indent_type.repeat(get_indent_level(line, indent_type)+1);
                
                for (let arg of commands[command]) {
                    if (!line.endsWith(' ')) {
                        arg = ' ' + arg;
                    }
                    let completion = new vscode.CompletionItem(arg + '=');
                    completion.kind = vscode.CompletionItemKind.Field;
                    completions.push(completion);
                }
            }

            // Commands
            for (let [command, arguments] of Object.entries(commands)) {
                if (command.startsWith(line.trim())
                    && command.split(' ').length >= line.trimStart().split(' ').length
                    && command.toLowerCase() !== line.trim().toLowerCase()) {
                    let idx = line.trimStart().split(' ').length;
                    let word = command.split(' ')[idx-1];
                    let completion = new vscode.CompletionItem(word + ' ');
                    completion.kind = vscode.CompletionItemKind.Interface;
                    completion.command = { command: 'editor.action.triggerSuggest', title: 'Re-trigger completions...' };
                    if (!completions.some(c => c.label === word + ' ')) {
                        completions.push(completion);
                    }
                }
            }

            return completions;
        }
    };
}
exports.cmd_completion_provider = cmd_completion_provider;
function get_indent_level(line, indent_type) {
    var indent_count = 0;
    for (let char of line) {
        if (char === indent_type) {
            indent_count++;
        } else {
            break;
        }
    }
    return indent_count;
}


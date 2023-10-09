const vscode = require('vscode');

function cmd_hover_provider(view_functions) {
    return {
        provideHover(document, position, token) {

            const range = document.getWordRangeAtPosition(position);
            const word = document.getText(range).toLowerCase();

            if (view_functions.has(word)) {
                var text = view_functions.get(word);
                var markdown = new vscode.MarkdownString(text);
                return new vscode.Hover(markdown, range);
            };
            return undefined;
        }
    };
}
exports.cmd_hover_provider = cmd_hover_provider;

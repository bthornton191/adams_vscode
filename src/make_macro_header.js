const vscode = require('vscode');

function make_macro_header() {
    return () => {
        const activeEditor = vscode.window.activeTextEditor;
        vscode.commands.executeCommand('editor.action.goToLocations', activeEditor.document.uri, vscode.P);
        vscode.commands.executeCommand('editor.action.insertSnippet', { langeId: "adams_cmd", name: "Macro Header" });
    };
}
exports.make_macro_header = make_macro_header;

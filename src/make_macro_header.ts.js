const vscode = require('vscode');

function make_macro_header(reporter = null) {
    return () => {
        const activeEditor = vscode.window.activeTextEditor;
        vscode.commands.executeCommand('editor.action.goToLocations', activeEditor.document.uri, vscode.P);
        vscode.commands.executeCommand('editor.action.insertSnippet', { langeId: "adams_cmd", name: "Macro Header" });
        reporter.sendTelemetryEvent("make_macro_header");
    };
}
exports.make_macro_header = make_macro_header;

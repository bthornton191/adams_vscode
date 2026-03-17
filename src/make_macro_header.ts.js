const vscode = require("vscode");

function make_macro_header(reporter = null) {
    return () => {
        const activeEditor = vscode.window.activeTextEditor;
        if (activeEditor) {
            vscode.commands.executeCommand(
                "editor.action.goToLocations",
                activeEditor.document.uri,
                new vscode.Position(0, 0),
            );
        }
        vscode.commands.executeCommand("editor.action.insertSnippet", {
            languageId: "adams_cmd",
            name: "Macro Header",
        });
        if (reporter) reporter.sendTelemetryEvent("make_macro_header");
    };
}
exports.make_macro_header = make_macro_header;

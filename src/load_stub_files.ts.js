const vscode = require('vscode');

function load_stub_files(context, output_channel) {
    return async () => {

        const adams_stub_dir = context.asAbsolutePath('resources/adamspy');
        var extra_paths = vscode.workspace.getConfiguration('python').get('analysis.extraPaths', null);
        var autocomp_paths = vscode.workspace.getConfiguration('python').get('autoComplete.extraPaths', null);
        
        // If the stub directory is not already in the analysis.extraPaths, add it
        if (!extra_paths.includes(adams_stub_dir)) {
            extra_paths.push(adams_stub_dir);
            output_channel.appendLine(`[${new Date().toLocaleTimeString()}]: Adding "${adams_stub_dir}" to python.analysis.extraPaths`);
        }
        if (vscode.workspace.workspaceFolders == undefined) {
            vscode.workspace.getConfiguration('python').update('analysis.extraPaths', extra_paths, true);
        }
        else {
            vscode.workspace.getConfiguration('python').update('analysis.extraPaths', extra_paths, null);
        }

        // If the stub directory is not already in the autoComplete.extra paths, add it
        if (!autocomp_paths.includes(adams_stub_dir)) {
            autocomp_paths.push(adams_stub_dir);
            output_channel.appendLine(`[${new Date().toLocaleTimeString()}]: Adding "${adams_stub_dir}" to python.autoComplete.extraPaths`);
        }
        if (vscode.workspace.workspaceFolders == undefined) {
            vscode.workspace.getConfiguration('python').update('autoComplete.extraPaths', autocomp_paths, true);
        }
        else {
            vscode.workspace.getConfiguration('python').update('autoComplete.extraPaths', autocomp_paths, null);
        }

    };
}
exports.load_stub_files = load_stub_files;

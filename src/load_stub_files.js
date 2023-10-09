const vscode = require('vscode');

function load_stub_files(context, output_channel) {
    return async () => {

        const adams_stub_dir = context.asAbsolutePath('resources/adamspy');
        // const adams_stub_files = fs.readdirSync(adams_stub_dir);
        var extra_paths = vscode.workspace.getConfiguration('python').get('analysis.extraPaths', null);
        // If the stub directory is not already in the extra paths, add it
        if (!extra_paths.includes(adams_stub_dir)) {
            extra_paths.push(adams_stub_dir);
            output_channel.appendLine(`[${new Date().toLocaleTimeString()}]: Adding "${adams_stub_dir}" to python.autoComplete.extraPaths`);
        }
        if (vscode.workspace.workspaceFolders == undefined) {
            vscode.workspace.getConfiguration('python').update('analysis.extraPaths', extra_paths, true);
        }
        else {
            vscode.workspace.getConfiguration('python').update('analysis.extraPaths', extra_paths, null);
        }

    };
}
exports.load_stub_files = load_stub_files;

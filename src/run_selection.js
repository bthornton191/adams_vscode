const vscode = require('vscode');
const fs = require('fs');
const net = require('net');
const { temp } = require('./extension.ts');

function run_selection(output_channel) {
    return async () => {
        // Get the currently selected text 
        let editor = vscode.window.activeTextEditor;
        let selection = editor.selection;
        let text = editor.document.getText(selection);

        // Write the text to a temporary file
        if (editor.document.languageId == 'adams_cmd') var suffix = '.cmd';
        else if (editor.document.languageId == 'python') var suffix = '.py';
        else {
            vscode.window.showErrorMessage('The current file is not an Adams or Python file');
            return;
        };
        let temp_file = temp.openSync({ suffix: suffix });
        fs.writeSync(temp_file.fd, text);
        fs.closeSync(temp_file.fd);


        if (editor.document.languageId == 'adams_cmd') {
            var line = `file command read file_name = "${temp_file.path}"`;
        } else if (editor.document.languageId == 'python') {
            var line = `file python read file_name = "${temp_file.path}"`;
        };

        // Create a tcp/ip socket and connect to 5002 on localhost
        const client = new net.Socket();
        client.connect(5002, 'localhost', function () {
            output_channel.appendLine(`Sending command to Adams View: ${line}`);
            client.write(`cmd ${line}`);
        });

        client.on('data', function (data) {

            // If the data is not "cmd: 0" print an error message
            if (data.toString() != "cmd: 0") {
                console.error('Unexpected response from Adams View: ' + data.toString());
                vscode.window.showErrorMessage(`The following command could not be run in Adams View: ${line}`);
            }
            // kill client after server's response
            client.destroy();
            // Delete the temporary file
            temp.cleanupSync();
        });

        client.on('close', function () {
            output_channel.appendLine('Connection closed');
        });

        client.on('error', function (err) {
            output_channel.appendLine('Error sending command to Adams View\n'
                + err.toString()
            );
            vscode.window.showErrorMessage(
                'No connection to Adams View was found. ' +
                'Please ensure that Adams View is open and the Command Server is running.'
            );
        });


    };
}
exports.run_selection = run_selection;

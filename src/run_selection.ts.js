const vscode = require('vscode');
const fs = require('fs');
const net = require('net');
const temp = require('temp').track();

/**
 * Runs the currently selected text in Adams View.
 *  
 * @param {vscode.OutputChannel} output_channel
 * @param {boolean} entire_file
 */
function run_selection(output_channel, entire_file=false) {
    return async () => {
        // Get the currently selected text 
        let editor = vscode.window.activeTextEditor;
        
        if (!entire_file) {
            let selection = editor.selection;
            var text = editor.document.getText(selection);
        } else {
            var text = editor.document.getText()
        }

        // Write the text to a temporary file
        if (editor.document.languageId == 'adams_cmd') {

            // If the current file is an Adams command file, do some formatting
            text = format_adams_cmd(text, editor.document.getText());
            let temp_file = temp.openSync({ suffix: '.cmd' });
            fs.writeSync(temp_file.fd, text);
            fs.closeSync(temp_file.fd);
            var line = `file command read file_name = "${temp_file.path}"`;

        } else if (editor.document.languageId == 'python' && entire_file) {

            // If the current file is a Python file

            // Get the current file name
            let file = vscode.window.activeTextEditor.document.fileName;
            var line = `file python read file_name = "${file}"`;

        } else if (editor.document.languageId == 'python') {
                
                // If the current file is a Python file, do some formatting
                let temp_file = temp.openSync({ suffix: '.py' });
                fs.writeSync(temp_file.fd, text);
                fs.closeSync(temp_file.fd);
                var line = `file python read file_name = "${temp_file.path}"`;

        } else {

            // If the current file is not an Adams or Python file, show an error message
            vscode.window.showErrorMessage('The current file is not an Adams or Python file');
            return;
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
                'Please ensure that Adams View is open and the Command Server is running. ' +
                'You can start the command server in Adams View by going to Tools>Command Server.'
            );
        });


    };
}


/**
 * Formats the given text as an Adams command and sends it to Adams View.
 * 
 * @param {string} selected_text
 * @param {string} full_text
 */
function format_adams_cmd(selected_text, full_text) {


    // Check the substitution value from the settings (msc-adams.runSelection.replaceSelf)
    // and replace all instances of '$_self' with the appropriate value
    let replace_self = vscode.workspace.getConfiguration('msc-adams').get('runInAdams.substituteSelf');

    // Replace all instances of '$_self' with '.mdi'
    selected_text = selected_text.replace(/\$_self/g, replace_self);

    // Check if parameter substitution is enabled
    if (vscode.workspace.getConfiguration('msc-adams').get('runInAdams.substituteParams') == true) {
        // Replace all parameter references with the values from their parameter definitions
        // First, get all parameter definitions, or an empty array if there are none
        let defs = full_text.match(/^(?:\!)[ \t]*(\$[a-zA-Z0-9_]*)(:.*$)?/gm) || [];

        // Then, get all parameter references
        let refs = selected_text.match(/\$('?)([a-zA-Z0-9_]*)\1/g) || [];

        // Make a set to store parameter references that have no definition
        let no_def = [];

        // Make a set to store parameter references that have no default value in the definition
        let no_default = [];

        // Loop over the parameter references
        for (let ref of refs) {

            // Loop over the parameter definitions
            let found = false;
            for (let def of defs) {

                // If the parameter name matches the parameter definition
                if ('$' + def.match(/\$('?)([a-zA-Z0-9_]*)\1/)[2] == ref) {

                    // If the parameter definition has a default value
                    if (def.match(/.+:d=([^:]*).*/i)) {

                        // Get the default value
                        let val = def.match(/.+?:d=([^:]*).*/i)[1]
                            .trim()
                            .replace(/"/g, '')
                            .replace(/'/g, '');
                        

                        // Replace the parameter reference with the default value
                        selected_text = selected_text.replace(ref, val);

                    } else {

                        // If there is no default value, add the parameter reference to the list
                        no_default.push(ref);
                    }

                    // Set found to true and break out of the loop
                    found = true;
                    break;
                }
            }

            // If the parameter reference was not found, add it to the list
            if (!found) no_def.push(ref);

        }

        // If there are any parameter references that have no definition or default value,
        // show an error message
        if (no_def.length > 0 || no_default.length > 0) {
            let msg = 'When running a selection of a parameterized macro, any parameter references ' +
                'in the selection must be defined with default values within the macro.The ' +
                'following parameter references have no definition or no default value: \n';
            for (let ref of no_def) msg += ref + ' (no definition)\n';
            for (let ref of no_default) msg += ref + ' (no default value)\n';
            vscode.window.showErrorMessage(msg);
        }
    }
    return selected_text;
}

exports.run_selection = run_selection;

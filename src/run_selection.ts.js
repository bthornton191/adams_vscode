const vscode = require("vscode");
const fs = require("fs");
const net = require("net");
const temp = require("temp").track();

const sub_lib_name = vscode.workspace
    .getConfiguration("msc-adams")
    .get("runInAdams.substituteSelf");

/**
 * Runs the currently selected text in Adams View.
 *
 * @param {vscode.OutputChannel} output_channel
 * @param {boolean} entire_file
 * @param {function} done
 */
function run_selection(output_channel, entire_file = false, reporter = null, done = () => {}) {
    return async () => {
        // Get the currently selected text
        let editor = vscode.window.activeTextEditor;

        if (editor.document.languageId != "adams_cmd" && editor.document.languageId != "python") {
            // If the current file is not an Adams or Python file, show an error message
            vscode.window.showErrorMessage("The current file is not an Adams or Python file");
            return;
        }

        if (!entire_file) {
            let selection = editor.selection;
            var text = editor.document.getText(selection);
        } else {
            var text = editor.document.getText();
        }

        if (editor.document.languageId == "adams_cmd" && text.includes("$_self")) {
            await new Promise((resolve) => createLibIfNotExist(resolve));
        }
        runScript(done);

        function runScript(done) {
            let cmd = getAviewCommand(editor, text, entire_file, reporter);
            sendAviewCommands(output_channel, cmd, done, reporter);
        }
    };
}

/**
 * Returns the command to send to Adams View and the text to send.
 *
 * @param {vscode.TextEditor} editor
 * @param {string} text
 * @param {Boolean} entire_file
 * @returns {Object}
 */
function getAviewCommand(editor, text, entire_file, reporter = null) {
    if (editor.document.languageId == "adams_cmd") {
        // If the current file is an Adams command file, do some formatting
        text = format_adams_cmd(text, editor.document.getText(), sub_lib_name);
        let temp_file = temp.openSync({ suffix: ".cmd" });
        fs.writeSync(temp_file.fd, text);
        fs.closeSync(temp_file.fd);
        var cmd = `file command read file_name = "${temp_file.path}"`;
        if (entire_file && reporter) {
            reporter.sendTelemetryEvent("run_file", {language: "adams_cmd"});
        } else if (reporter) {
            reporter.sendTelemetryEvent("run_selection", {language: "adams_cmd"});
        }
    } else if (editor.document.languageId == "python" && entire_file) {
        // If the current file is a Python file
        // Get the current file name
        let file = vscode.window.activeTextEditor.document.fileName;
        var cmd = `file python read file_name = "${file}"`;
        if (reporter) {
            reporter.sendTelemetryEvent("run_file", { language: "python" });
        }
    } else if (editor.document.languageId == "python") {
        // If the current file is a Python file, do some formatting
        let temp_file = temp.openSync({ suffix: ".py" });
        fs.writeSync(temp_file.fd, text);
        fs.closeSync(temp_file.fd);
        var cmd = `file python read file_name = "${temp_file.path}"`;
        if (reporter) {
            reporter.sendTelemetryEvent("run_selection", { language: "python" });
        }
    }
    return cmd;
}

/**
 * Sends the given command to Adams View and handles the response.
 *
 * @param {vscode.OutputChannel} output_channel
 * @param {string} cmd
 * @param {function} done
 * @returns {void}
 */
function sendAviewCommands(output_channel, cmd, done, reporter=null) {
    const client = new net.Socket();
    client.connect(5002, "localhost", function () {
        output_channel.appendLine(`Sending command to Adams View: ${cmd}`);
        client.write(`cmd ${cmd}`);
    });

    client.on("data", function (data) {
        // If the data is not "cmd: 0" print an error message
        if (data.toString() != "cmd: 0") {
            console.error("Unexpected response from Adams View: " + data.toString());
            vscode.window.showErrorMessage(
                `The following command could not be run in Adams View: ${cmd}`
            );
        }
        // kill client after server's response
        client.destroy();
        // Delete the temporary file
        temp.cleanupSync();
        done();
    });

    client.on("close", function () {
        output_channel.appendLine("Connection closed");
    });

    client.on("error", function (err) {
        output_channel.appendLine("Error sending command to Adams View\n" + err.toString());
        vscode.window.showErrorMessage(
            "No connection to Adams View was found. " +
                "Please ensure that Adams View is open and the Command Server is running. " +
                "You can start the command server in Adams View by going to Tools>Command Server."
        );
        reporter.sendTelemetryErrorEvent("sendAviewCommands", {error: err.toString()});
        done();
    });
}

/**
 * Formats the given text as an Adams command and sends it to Adams View.
 *
 * @param {string} selected_text
 * @param {string} full_text
 * @param {string} lib_name
 */
function format_adams_cmd(selected_text, full_text, lib_name) {
    // Check the substitution value from the settings (msc-adams.runSelection.replaceSelf)
    // and replace all instances of '$_self' with the appropriate value
    let replace_self = lib_name;

    // Replace all instances of '$_self' with '.mdi'
    selected_text = selected_text.replace(/\$_self/g, replace_self);

    // Check if parameter substitution is enabled
    if (vscode.workspace.getConfiguration("msc-adams").get("runInAdams.substituteParams") == true) {
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
                if ("$" + def.match(/\$('?)([a-zA-Z0-9_]*)\1/)[2] == ref) {
                    // If the parameter definition has a default value
                    if (def.match(/.+:d=([^:]*).*/i)) {
                        // Get the default value
                        let val = def
                            .match(/.+?:d=([^:]*).*/i)[1]
                            .trim()
                            .replace(/"/g, "")
                            .replace(/'/g, "");

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
            let msg =
                "When running a selection of a parameterized macro, any parameter references " +
                "in the selection must be defined with default values within the macro.The " +
                "following parameter references have no definition or no default value: \n";
            for (let ref of no_def) msg += ref + " (no definition)\n";
            for (let ref of no_default) msg += ref + " (no default value)\n";
            vscode.window.showErrorMessage(msg);
        }
    }
    return selected_text;
}

function createLibIfNotExist(done) {
    checkIfLibExists(function (exists) {
        if (exists) {
            done();
        } else
            createLibrary(sub_lib_name, function () {
                done();
            });
    });
}

function checkIfLibExists(done) {
    // Create a tcp/ip socket and connect to 5002 on localhost
    const client = new net.Socket();
    client.on("error", function (err) {
        console.error(`Error checking for ${sub_lib_name}: ` + err.toString());
        vscode.window.showErrorMessage(`Error checking for ${sub_lib_name}: ` + err.toString());
    });
    let query = `query db_exists("${sub_lib_name}")`;
    client.connect(5002, "localhost", function () {
        client.write(query);
        client.on("data", function () {
            client.write("OK");
            client.on("data", function (rdata) {
                let result = Boolean(parseInt(rdata));
                client.destroy();
                done(result);
            });
        });
    });
}

function createLibrary(name, done) {
    // Create a tcp/ip socket and connect to 5002 on localhost
    const client = new net.Socket();
    client.on("error", function (err) {
        console.error("Error creating library: " + err.toString());
        vscode.window.showErrorMessage("Error creating library: " + err.toString());
    });
    client.connect(5002, "localhost", function () {
        client.write(`cmd library create library=${name}`);
        client.on("data", function (cdata) {
            if (cdata.toString() != "cmd: 0") {
                console.error("Unexpected response from Adams View: " + cdata.toString());
                vscode.window.showErrorMessage(
                    "Unable to create a temporary library for " + "storing references to $_self"
                );
            } else {
                console.log(
                    `Created a temporary library for storing references to $_self: ${name}`
                );
            }
            // kill client after server's response
            client.destroy();
            done();
        });
    });
}

exports.run_selection = run_selection;
exports.createLibIfNotExist = createLibIfNotExist;
exports.sub_lib_name = sub_lib_name;

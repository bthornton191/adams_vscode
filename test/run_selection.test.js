const net = require("net");
const assert = require("assert");
const path = require("path");
const fs = require("fs");
const vscode = require("vscode");
const os = require("os");
const { run_selection, createLibIfNotExist, sub_lib_name } = require("../src/run_selection.ts.js");
const { evaluate_exp } = require("../src/aview.ts.js");
const { waitForAdamsConnection } = require("./utils.js");

output_channel = vscode.window.createOutputChannel("MSC Adams Testing");

suite("createLibIfNotExist Test Suite", () => {
    var lib_name = "";
    suiteSetup(async () => {
        // Wait for adams view connection
        await new Promise((resolve) => {
            waitForAdamsConnection(resolve);
        });

        // Delete the vscode library if it exists
        await new Promise((resolve) =>
            evaluate_exp(`db_exists("${sub_lib_name}")`, console.log, async (result) => {
                if (result == 1) {
                    await new Promise((resolve) => deleteLibrary(sub_lib_name, resolve));
                }
                resolve();
            })
        );

        await new Promise((resolve) => createLibIfNotExist(resolve)).then((result) => {
            lib_name = result;
        });
    });

    suiteTeardown(async () => {
        // Delete the vscode library if it exists
        await new Promise((resolve) =>
            evaluate_exp(`db_exists("${sub_lib_name}")`, console.log, async (result) => {
                if (result == 1) {
                    await new Promise((resolve) => deleteLibrary(sub_lib_name, resolve));
                }
                resolve();
            })
        );
    });

    test("should have a vscode library", async () => {
        await new Promise((resolve) => checkForcheVscodeLib(sub_lib_name, resolve)).then(
            (result) => {
                assert.strictEqual(result, true);
            }
        );
    });
});

suite("run_selection(entire_file = False) on python Test Suite", () => {
    suiteSetup(async () => {
        // Wait for adams view connection
        await new Promise((resolve) => {
            waitForAdamsConnection(resolve);
        });

        // Delete the vscode library if it exists
        await new Promise((resolve) =>
            evaluate_exp(`db_exists("${sub_lib_name}")`, console.log, async (result) => {
                if (result == 1) {
                    await new Promise((resolve) => deleteLibrary(sub_lib_name, resolve));
                }
                resolve();
            })
        );

        // Log a blank line to ensure the test doesn't use a previous result
        await new Promise((resolve) => logLine("run_selection.py", resolve));

        const tempFilePath = path.join(os.tmpdir(), "run_selection.py");
        const tempFileContent = "print('this should be shown')\nprint('this should not be shown')";
        fs.writeFileSync(tempFilePath, tempFileContent);

        // Open the file in the editor
        await vscode.workspace.openTextDocument(tempFilePath).then(async (document) => {
            await vscode.window.showTextDocument(document).then(async (editor) => {
                //  Select the first line
                editor.selection = new vscode.Selection(0, 0, 1, 0);

                // Run the msc_adams.runSelection command
                await new Promise((resolve) =>
                    run_selection(output_channel, false, null, resolve)()
                );
            });
        });
    });

    suiteTeardown(async () => {
        // Delete the vscode library if it exists
        await new Promise((resolve) =>
            evaluate_exp(`db_exists("${sub_lib_name}")`, console.log, async (result) => {
                if (result == 1) {
                    await new Promise((resolve) => deleteLibrary(sub_lib_name, resolve));
                }
                resolve();
            })
        );
    });

    test("Should only run the selection", (done) => {
        const logFilePath = path.join(
            vscode.workspace.workspaceFolders[0].uri.fsPath,
            "working_directory",
            "aview.log"
        );
        const logFileContent = fs.readFileSync(logFilePath, "utf8");
        const lastLine = logFileContent.trim().split(/\r?\n/).pop();
        assert.strictEqual(lastLine, "! this should be shown");
        done();
    });

    test("should not have a vscode library", async () => {
        await new Promise((resolve) => checkForcheVscodeLib(sub_lib_name, resolve)).then(
            (result) => {
                assert.strictEqual(result, false);
            }
        );
    });
});

suite("run_selection(entire_file = True) on python Test Suite", () => {
    suiteSetup(async () => {
        // Wait for adams view connection
        await new Promise((resolve) => {
            waitForAdamsConnection(resolve);
        });

        // Delete the vscode library if it exists
        await new Promise((resolve) =>
            evaluate_exp(`db_exists("${sub_lib_name}")`, console.log, async (result) => {
                if (result == 1) {
                    await new Promise((resolve) => deleteLibrary(sub_lib_name, resolve));
                }
                resolve();
            })
        );

        // Log a blank line to ensure the test doesn't use a previous result
        await new Promise((resolve) => logLine("run_selection_entire_file.py", resolve));

        const tempFilePath = path.join(os.tmpdir(), "run_selection_entire_file.py");
        const tempFileContent = "print('this should be shown')\nprint('this should ALSO be shown')";
        fs.writeFileSync(tempFilePath, tempFileContent);

        // Open the file in the editor
        await vscode.workspace.openTextDocument(tempFilePath).then(async (document) => {
            await vscode.window.showTextDocument(document).then(async (editor) => {
                // Select the first character of the first line
                editor.selection = new vscode.Selection(0, 0, 0, 1);

                // Run the msc_adams.runSelection command
                await new Promise((resolve) =>
                    run_selection(output_channel, true, null, resolve)()
                );
            });
        });
    });

    suiteTeardown(async () => {
        // Delete the vscode library if it exists
        await new Promise((resolve) =>
            evaluate_exp(`db_exists("${sub_lib_name}")`, console.log, async (result) => {
                if (result == 1) {
                    await new Promise((resolve) => deleteLibrary(sub_lib_name, resolve));
                }
                resolve();
            })
        );
    });

    test("should run the entire file", (done) => {
        const logFilePath = path.join(
            vscode.workspace.workspaceFolders[0].uri.fsPath,
            "working_directory",
            "aview.log"
        );
        const logFileContent = fs.readFileSync(logFilePath, "utf8");
        const lastTwoLines = logFileContent.trim().split(/\r?\n/).slice(-2);
        const expectedLines = ["! this should be shown", "! this should ALSO be shown"];
        assert.deepStrictEqual(lastTwoLines, expectedLines);
        done();
    });

    test("should not have a vscode library", async () => {
        await new Promise((resolve) => checkForcheVscodeLib(sub_lib_name, resolve)).then(
            (result) => {
                assert.strictEqual(result, false);
            }
        );
    });
});

suite("run_selection(entire_file = False) on cmd Test Suite", () => {
    suiteSetup(async () => {
        // Wait for adams view connection
        await new Promise((resolve) => {
            waitForAdamsConnection(resolve);
        });

        // Delete the vscode library if it exists
        await new Promise((resolve) =>
            evaluate_exp(`db_exists("${sub_lib_name}")`, console.log, async (result) => {
                if (result == 1) {
                    await new Promise((resolve) => deleteLibrary(sub_lib_name, resolve));
                }
                resolve();
            })
        );

        // Log a blank line to ensure the test doesn't use a previous result
        await new Promise((resolve) => logLine("run_selection.cmd", resolve));

        const tempFilePath = path.join(os.tmpdir(), "run_selection.cmd");
        const tempFileContent =
            "var set var=.mdi.tmpstr str=(eval(str_print('this should be shown')))\n" +
            "var set var=.mdi.tmpstr str=(eval(str_print('this should not be shown')))";
        fs.writeFileSync(tempFilePath, tempFileContent);

        // Open the file in the editor
        await vscode.workspace.openTextDocument(tempFilePath).then(async (document) => {
            await vscode.window.showTextDocument(document).then(async (editor) => {
                //  Select the first line
                editor.selection = new vscode.Selection(0, 0, 1, 0);

                // Run the msc_adams.runSelection command
                await new Promise((resolve) =>
                    run_selection(output_channel, false, null, resolve)()
                );
            });
        });
    });

    suiteTeardown(async () => {
        // Delete the vscode library if it exists
        await new Promise((resolve) =>
            evaluate_exp(`db_exists("${sub_lib_name}")`, console.log, async (result) => {
                if (result == 1) {
                    await new Promise((resolve) => deleteLibrary(sub_lib_name, resolve));
                }
                resolve();
            })
        );
    });

    test("should only run the selection", (done) => {
        const logFilePath = path.join(
            vscode.workspace.workspaceFolders[0].uri.fsPath,
            "working_directory",
            "aview.log"
        );
        const logFileContent = fs.readFileSync(logFilePath, "utf8");
        const lastLine = logFileContent.trim().split(/\r?\n/).pop();
        assert.strictEqual(lastLine, "! this should be shown");
        done();
    });

    test("should not have a vscode library", async () => {
        await new Promise((resolve) => checkForcheVscodeLib(sub_lib_name, resolve)).then(
            (result) => {
                assert.strictEqual(result, false);
            }
        );
    });
});

suite("run_selection(entire_file = False) on cmd when $_self is in the file Test Suite", () => {
    suiteSetup(async () => {
        // Wait for adams view connection
        await new Promise((resolve) => {
            waitForAdamsConnection(resolve);
        });

        // Delete the vscode library if it exists
        await new Promise((resolve) =>
            evaluate_exp(`db_exists("${sub_lib_name}")`, console.log, async (result) => {
                if (result == 1) {
                    await new Promise((resolve) => deleteLibrary(sub_lib_name, resolve));
                }
                resolve();
            })
        );

        // Log a blank line to ensure the test doesn't use a previous result
        await new Promise((resolve) => logLine("run_selection_self.cmd", resolve));

        const tempFilePath = path.join(os.tmpdir(), "run_selection_self.cmd");
        const tempFileContent =
            "var set var=$_self.tmpstr str=(eval(str_print('this should be shown')))\n" +
            "var set var=$_self.tmpstr str=(eval(str_print('this should not be shown')))";
        fs.writeFileSync(tempFilePath, tempFileContent);

        // Open the file in the editor
        await vscode.workspace.openTextDocument(tempFilePath).then(async (document) => {
            await vscode.window.showTextDocument(document).then(async (editor) => {
                //  Select the first line
                editor.selection = new vscode.Selection(0, 0, 1, 0);

                // // Run the msc_adams.runSelection command
                await new Promise((resolve) =>
                    run_selection(output_channel, false, null, resolve)()
                );
            });
        });
    });

    suiteTeardown(async () => {
        // Delete the vscode library if it exists
        await new Promise((resolve) =>
            evaluate_exp(`db_exists("${sub_lib_name}")`, console.log, async (result) => {
                if (result == 1) {
                    await new Promise((resolve) => deleteLibrary(sub_lib_name, resolve));
                }
                resolve();
            })
        );
    });

    test("aview.log should display 'this should be shown", (done) => {
        const logFilePath = path.join(
            vscode.workspace.workspaceFolders[0].uri.fsPath,
            "working_directory",
            "aview.log"
        );
        const logFileContent = fs.readFileSync(logFilePath, "utf8");
        const lastLine = logFileContent.trim().split(/\r?\n/).pop();
        assert.strictEqual(lastLine, "! this should be shown");
        done();
    });

    test("should have a vscode library", async () => {
        await new Promise((resolve) => checkForcheVscodeLib(sub_lib_name, resolve)).then(
            (result) => {
                assert.strictEqual(result, true);
            }
        );
    });
});

suite("run_selection(entire_file = True) on cmd Test Suite", () => {
    suiteSetup(async () => {
        // Wait for adams view connection
        await new Promise((resolve) => {
            waitForAdamsConnection(resolve);
        });

        // Delete the vscode library if it exists
        await new Promise((resolve) =>
            evaluate_exp(`db_exists("${sub_lib_name}")`, console.log, async (result) => {
                if (result == 1) {
                    await new Promise((resolve) => deleteLibrary(sub_lib_name, resolve));
                }
                resolve();
            })
        );

        // Log a blank line to ensure the test doesn't use a previous result
        await new Promise((resolve) => logLine("run_selection_entire_file.cmd", resolve));

        // create a file in the user's temp directory
        const tempFilePath = path.join(os.tmpdir(), "run_selection_entire_file.cmd");
        const tempFileContent =
            "var set var=.mdi.tmpstr str=(eval(str_print('this should be shown')))\n" +
            "var set var=.mdi.tmpstr str=(eval(str_print('this should ALSO be shown')))";
        fs.writeFileSync(tempFilePath, tempFileContent);

        // Open the file in the editor
        await vscode.workspace.openTextDocument(tempFilePath).then(async (document) => {
            await vscode.window.showTextDocument(document).then(async (editor) => {
                // Select the first character of the first line
                editor.selection = new vscode.Selection(0, 0, 0, 1);

                // Run the msc_adams.runSelection command
                await new Promise((resolve) =>
                    run_selection(output_channel, true, null, resolve)()
                );
            });
        });
    });

    suiteTeardown(async () => {
        // Delete the vscode library if it exists
        await new Promise((resolve) =>
            evaluate_exp(`db_exists("${sub_lib_name}")`, console.log, async (result) => {
                if (result == 1) {
                    await new Promise((resolve) => deleteLibrary(sub_lib_name, resolve));
                }
                resolve();
            })
        );
    });

    test("should run the entire file", (done) => {
        const logFilePath = path.join(
            vscode.workspace.workspaceFolders[0].uri.fsPath,
            "working_directory",
            "aview.log"
        );
        const logFileContent = fs.readFileSync(logFilePath, "utf8");
        const lastTwoLines = logFileContent.trim().split(/\r?\n/).slice(-2);
        const expectedLines = ["! this should be shown", "! this should ALSO be shown"];
        assert.deepStrictEqual(lastTwoLines, expectedLines);
        done();
    });
});

function logLine(line = "", done = () => {}) {
    const client = new net.Socket();
    client.connect(5002, "localhost", function () {
        client.write(`cmd var set var=.mdi.tmpstr str=(eval(str_print('! > ${line}')))`, done());
    });
}

async function checkForcheVscodeLib(lib_name, done = () => {}) {
    async function check(suffix, done) {
        const client = new net.Socket();
        let query = `query db_exists("${lib_name}${suffix}")`;
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

    let found = false;
    for (let suffix of ["", "_1", "_2", "_3", "_4", "_5", "_6", "_7", "_8", "_9"]) {
        await new Promise((resolve) => check(suffix, resolve)).then((result) => {
            if (result) {
                found = true;
            }
        });
    }
    done(found);
}

/**
 * Deletes the given library from Adams View.
 * @param {string} name
 * @returns {void}
 */
function deleteLibrary(name, done = () => {}) {
    // Create a tcp/ip socket and connect to 5002 on localhost
    const client = new net.Socket();
    client.on("error", function (err) {
        console.error("Error deleting library: " + err.toString());
        vscode.window.showErrorMessage("Error deleting library: " + err.toString());
        done();
    });
    client.connect(5002, "localhost", function () {
        client.write(`cmd library delete library=${name}`);
        client.on("data", function (cdata) {
            if (cdata.toString() != "cmd: 0") {
                console.error("Unexpected response from Adams View: " + cdata.toString());
                vscode.window.showErrorMessage(
                    `Unable to delete the temporary library for storing references to $_self: ${name}`
                );
            } else {
                console.log(
                    `Deleted the temporary library for storing references to $_self: ${name}`
                );
            }
            // kill client after server's response
            client.destroy();
            done();
        });
    });
}

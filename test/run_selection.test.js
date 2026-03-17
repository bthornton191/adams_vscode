const net = require("net");
const assert = require("assert");
const path = require("path");
const fs = require("fs");
const vscode = require("vscode");
const os = require("os");
const { run_selection, createLibIfNotExist, sub_lib_name, format_adams_cmd } = require("../src/run_selection.ts.js");
const { evaluate_exp, getPort } = require("../src/aview.ts.js");
const { waitForAdamsConnection } = require("./utils.js");
const { startAdamsView, killAdamsIfRunningInDir } = require("./global_fixture.cjs");

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
            }),
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
            }),
        );
    });

    test("should have a vscode library", async () => {
        await new Promise((resolve) => checkForcheVscodeLib(sub_lib_name, resolve)).then(
            (result) => {
                assert.strictEqual(result, true);
            },
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
            }),
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
                    run_selection(output_channel, false, null, resolve)(),
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
            }),
        );
    });

    test("Should only run the selection", (done) => {
        const logFilePath = path.join(
            vscode.workspace.workspaceFolders[0].uri.fsPath,
            "working_directory",
            "aview.log",
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
            },
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
            }),
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
                    run_selection(output_channel, true, null, resolve)(),
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
            }),
        );
    });

    test("should run the entire file", (done) => {
        const logFilePath = path.join(
            vscode.workspace.workspaceFolders[0].uri.fsPath,
            "working_directory",
            "aview.log",
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
            },
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
            }),
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
                    run_selection(output_channel, false, null, resolve)(),
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
            }),
        );
    });

    test("should only run the selection", (done) => {
        const logFilePath = path.join(
            vscode.workspace.workspaceFolders[0].uri.fsPath,
            "working_directory",
            "aview.log",
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
            },
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
            }),
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
                    run_selection(output_channel, false, null, resolve)(),
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
            }),
        );
    });

    test("aview.log should display 'this should be shown", (done) => {
        const logFilePath = path.join(
            vscode.workspace.workspaceFolders[0].uri.fsPath,
            "working_directory",
            "aview.log",
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
            },
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
            }),
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
                    run_selection(output_channel, true, null, resolve)(),
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
            }),
        );
    });

    test("should run the entire file", (done) => {
        const logFilePath = path.join(
            vscode.workspace.workspaceFolders[0].uri.fsPath,
            "working_directory",
            "aview.log",
        );
        const logFileContent = fs.readFileSync(logFilePath, "utf8");
        const lastTwoLines = logFileContent.trim().split(/\r?\n/).slice(-2);
        const expectedLines = ["! this should be shown", "! this should ALSO be shown"];
        assert.deepStrictEqual(lastTwoLines, expectedLines);
        done();
    });
});

suite("run_selection(entire_file = True) on cmd with macro parameters Test Suite", () => {
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
            }),
        );

        // Log a blank line to ensure the test doesn't use a previous result
        await new Promise((resolve) => logLine("run_selection_entire_file.cmd", resolve));

        // create a file in the user's temp directory
        const tempFilePath = path.join(os.tmpdir(), "run_selection_entire_file.cmd");
        const tempFileContent =
            "!$prefix:t=string:d=tes\n" +
            "var set var=$_self.test2 string=\"This is a $'prefix't\"\n" +
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
                    run_selection(output_channel, true, null, resolve)(),
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
            }),
        );
    });

    test("should run the entire file", (done) => {
        const logFilePath = path.join(
            vscode.workspace.workspaceFolders[0].uri.fsPath,
            "working_directory",
            "aview.log",
        );
        const logFileContent = fs.readFileSync(logFilePath, "utf8");
        const lastTwoLines = logFileContent.trim().split(/\r?\n/).slice(-2);
        const expectedLines = ["! this should be shown", "! this should ALSO be shown"];
        assert.deepStrictEqual(lastTwoLines, expectedLines);
        done();
    });

    test("format_adams_cmd should substitute $_self and macro parameters", (done) => {
        // Directly test the parameter substitution logic
        const input =
            "!$prefix:t=string:d=tes\n" +
            "var set var=$_self.test2 string=\"This is a $'prefix't\"";
        const result = format_adams_cmd(input, input, sub_lib_name);
        // $_self should be replaced with .vscode (sub_lib_name)
        assert.ok(result.includes("var set var=.vscode.test2"), "Expected $_self to be replaced with .vscode");
        // $'prefix't should become "test" (default "tes" + trailing "t")
        assert.ok(result.includes('string="This is a test"'), "Expected $\\'prefix\\'t to be replaced with test");
        done();
    });
});

suite("aviewPortNumber configuration Test Suite", () => {
    const alternatePort = 5003;
    const tempTestDir = path.join(os.tmpdir(), `adams_test_port_${alternatePort}`);

    suiteSetup(async () => {
        // Create temporary directory for alternate port server
        if (!fs.existsSync(tempTestDir)) {
            fs.mkdirSync(tempTestDir, { recursive: true });
        }

        // Update the configuration to use alternate port
        await vscode.workspace
            .getConfiguration("msc-adams")
            .update("aviewPortNumber", alternatePort, vscode.ConfigurationTarget.Workspace);

        // Start a new Adams View instance on the alternate port in temp directory
        await new Promise((resolve) => startAdamsView(resolve, alternatePort, tempTestDir));

        // Wait for adams view connection on default port to be ready
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
            }),
        );

        // Log a blank line to ensure the test doesn't use a previous result
        await new Promise((resolve) => logLine("port_config_test.py", resolve));

        const tempFilePath = path.join(os.tmpdir(), "port_config_test.py");
        const tempFileContent =
            "import os\n" +
            "port = os.environ.get('ADAMS_LISTENER_PORT', 'NOT_SET')\n" +
            "print(f'ADAMS_LISTENER_PORT is {port}')";
        fs.writeFileSync(tempFilePath, tempFileContent);

        // Open the file in the editor
        await vscode.workspace.openTextDocument(tempFilePath).then(async (document) => {
            await vscode.window.showTextDocument(document).then(async (editor) => {
                // Select the first character of the first line
                editor.selection = new vscode.Selection(0, 0, 0, 1);

                // Run the msc_adams.runSelection command
                await new Promise((resolve) =>
                    run_selection(output_channel, true, null, resolve)(),
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
            }),
        );

        // Kill the alternate port Adams View
        await new Promise((resolve) => killAdamsIfRunningInDir(tempTestDir, resolve));

        // Clean up temporary directory (retry to handle locked log files)
        for (let i = 0; i < 5; i++) {
            try {
                if (fs.existsSync(tempTestDir)) {
                    fs.rmSync(tempTestDir, { recursive: true, force: true });
                }
                break;
            } catch (e) {
                if (i < 4) {
                    await new Promise((r) => setTimeout(r, 1000));
                }
            }
        }

        // Reset the configuration back to default
        await vscode.workspace
            .getConfiguration("msc-adams")
            .update("aviewPortNumber", 5002, vscode.ConfigurationTarget.Workspace);
    });

    test("should connect to alternate port and print correct ADAMS_LISTENER_PORT", (done) => {
        const logFilePath = path.join(tempTestDir, "aview.log");
        const logFileContent = fs.readFileSync(logFilePath, "utf8");
        const lastLine = logFileContent.trim().split(/\r?\n/).pop();
        assert.strictEqual(lastLine, `! ADAMS_LISTENER_PORT is ${alternatePort}`);
        done();
    });

    test("getPort should return the configured alternate port", () => {
        const currentPort = getPort();
        assert.strictEqual(currentPort, alternatePort);
    });
});

function logLine(line = "", done = () => {}) {
    const client = new net.Socket();
    client.connect(getPort(), "localhost", function () {
        client.write(`cmd var set var=.mdi.tmpstr str=(eval(str_print('! > ${line}')))`, done());
    });
}

async function checkForcheVscodeLib(lib_name, done = () => {}) {
    async function check(suffix, done) {
        const client = new net.Socket();
        let query = `query db_exists("${lib_name}${suffix}")`;
        client.connect(getPort(), "localhost", function () {
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
    // Create a tcp/ip socket and connect to Adams View on configured port
    const client = new net.Socket();
    client.on("error", function (err) {
        console.error("Error deleting library: " + err.toString());
        vscode.window.showErrorMessage("Error deleting library: " + err.toString());
        done();
    });
    client.connect(getPort(), "localhost", function () {
        client.write(`cmd library delete library=${name}`);
        client.on("data", function (cdata) {
            if (cdata.toString() != "cmd: 0") {
                console.error("Unexpected response from Adams View: " + cdata.toString());
                vscode.window.showErrorMessage(
                    `Unable to delete the temporary library for storing references to $_self: ${name}`,
                );
            } else {
                console.log(
                    `Deleted the temporary library for storing references to $_self: ${name}`,
                );
            }
            // kill client after server's response
            client.destroy();
            done();
        });
    });
}

// =============================================================================
// Reporter telemetry tests — no Adams connection required
// =============================================================================

suite("run_selection reporter telemetry", () => {
    const os = require("os");
    const path = require("path");
    const { run_selection } = require("../src/run_selection.ts.js");

    function makeMockReporter() {
        const calls = { telemetry: [], errors: [] };
        return {
            sendTelemetryEvent: (...args) => calls.telemetry.push(args),
            sendTelemetryErrorEvent: (...args) => calls.errors.push(args),
            calls,
        };
    }

    test("sendAviewCommands sends error telemetry when Adams is not reachable", (done) => {
        // Use a port no server is listening on so the connection fails immediately
        const reporter = makeMockReporter();

        // Temporarily point to a port nothing is listening on
        const originalGet = vscode.workspace.getConfiguration;
        vscode.workspace.getConfiguration = (section) => ({
            get: (key) => (key === "aviewPortNumber" ? 19999 : null),
            update: () => Promise.resolve(),
        });

        const tempFilePath = path.join(os.tmpdir(), "reporter_test.py");
        fs.writeFileSync(tempFilePath, "print('hello')");

        vscode.workspace.openTextDocument(tempFilePath).then((document) => {
            vscode.window.showTextDocument(document).then(() => {
                run_selection(output_channel, false, reporter, () => {
                    vscode.workspace.getConfiguration = originalGet;
                    assert.strictEqual(reporter.calls.errors.length, 1);
                    assert.strictEqual(reporter.calls.errors[0][0], "sendAviewCommands");
                    done();
                })();
            });
        });
    });
});

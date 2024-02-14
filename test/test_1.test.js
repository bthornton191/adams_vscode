const net = require("net");
const assert = require("assert");
const path = require("path");
const fs = require("fs");
const vscode = require("vscode");
const os = require("os");
const { run_selection, createUniqueLibrary, tmp_lib_name } = require("../src/run_selection.ts.js");
// const { logBlankLine } = require('./utils.cjs');

output_channel = vscode.window.createOutputChannel("MSC Adams Testing");

suite("createUniqueLibrary Test Suite", () => {
    var lib_name = "";
    suiteSetup(async () => {
        await new Promise((resolve) => createUniqueLibrary(resolve)).then((result) => {
            lib_name = result;
        });
    });

    suiteTeardown(async () => {
        // Delete the temporary library
        const client = new net.Socket();
        client.connect(5002, "localhost", function () {
            client.write(`cmd library delete library=${lib_name}`);
        });
    });

    test("should return a library name", async () => {
        if (lib_name === undefined) {
            // Handle the undefined result here
            assert.fail("createUniqueLibrary returned undefined");
        } else {
            assert(lib_name.startsWith(tmp_lib_name));
        }
    });

    test("should have a temporary library", async () => {
        await new Promise((resolve) => checkForcheTmpLib(tmp_lib_name, resolve)).then((result) => {
            assert.strictEqual(result, true);
        });
    });
});

suite("run_selection(entire_file = False) on python Test Suite", () => {
    suiteSetup(async () => {
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
                await new Promise((resolve) => run_selection(output_channel, false, resolve)());
            });
        });
    });

    test("Should only run the selection", async () => {
        const logFilePath = path.join(
            vscode.workspace.workspaceFolders[0].uri.fsPath,
            "working_directory",
            "aview.log"
        );
        const logFileContent = fs.readFileSync(logFilePath, "utf8");
        const lastLine = logFileContent.trim().split("\n").pop();
        assert.strictEqual(lastLine, "! this should be shown");
    });

    test("should not have a temporary library", async () => {
        await new Promise((resolve) => checkForcheTmpLib(tmp_lib_name, resolve)).then((result) => {
            assert.strictEqual(result, false);
        });
    });
});

suite("run_selection(entire_file = True) on python Test Suite", () => {
    suiteSetup(async () => {
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
                await new Promise((resolve) => run_selection(output_channel, true, resolve)());
            });
        });
    });

    test("should run the entire file", async () => {
        const logFilePath = path.join(
            vscode.workspace.workspaceFolders[0].uri.fsPath,
            "working_directory",
            "aview.log"
        );
        const logFileContent = fs.readFileSync(logFilePath, "utf8");
        const lastTwoLines = logFileContent.trim().split(/\r?\n/).slice(-2);
        const expectedLines = ["! this should be shown", "! this should ALSO be shown"];
        assert.deepStrictEqual(lastTwoLines, expectedLines);
    });

    test("should not have a temporary library", async () => {
        await new Promise((resolve) => checkForcheTmpLib(tmp_lib_name, resolve)).then((result) => {
            assert.strictEqual(result, false);
        });
    });
});

suite("run_selection(entire_file = False) on cmd Test Suite", () => {
    suiteSetup(async () => {
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
                await new Promise((resolve) => run_selection(output_channel, false, resolve)());
            });
        });
    });

    test("should only run the selection", async () => {
        const logFilePath = path.join(
            vscode.workspace.workspaceFolders[0].uri.fsPath,
            "working_directory",
            "aview.log"
        );
        const logFileContent = fs.readFileSync(logFilePath, "utf8");
        const lastLine = logFileContent.trim().split("\n").pop();
        assert.strictEqual(lastLine, "! this should be shown");
    });

    test("should not have a temporary library", async () => {
        await new Promise((resolve) => checkForcheTmpLib(tmp_lib_name, resolve)).then((result) => {
            assert.strictEqual(result, false);
        });
    });
});

suite("run_selection(entire_file = False) on cmd when $_self is in the file Test Suite", () => {
    suiteSetup(async () => {
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
                await new Promise((resolve) => run_selection(output_channel, false, resolve)());
            });
        });
    });

    test("should work when $_self is in the file", async () => {
        const logFilePath = path.join(
            vscode.workspace.workspaceFolders[0].uri.fsPath,
            "working_directory",
            "aview.log"
        );
        const logFileContent = fs.readFileSync(logFilePath, "utf8");
        const lastLine = logFileContent.trim().split("\n").pop();
        assert.strictEqual(lastLine, "! this should be shown");
    });

    test("should delete the temporary library", async () => {
        await new Promise((resolve) => checkForcheTmpLib(tmp_lib_name, resolve)).then((result) => {
            assert.strictEqual(result, false);
        });
    });
});

suite("run_selection(entire_file = True) on cmd Test Suite", () => {
    suiteSetup(async () => {
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
                await new Promise((resolve) => run_selection(output_channel, true, resolve)());
            });
        });
    });

    test("should run the entire file", async () => {
        const logFilePath = path.join(
            vscode.workspace.workspaceFolders[0].uri.fsPath,
            "working_directory",
            "aview.log"
        );
        const logFileContent = fs.readFileSync(logFilePath, "utf8");
        const lastTwoLines = logFileContent.trim().split(/\r?\n/).slice(-2);
        const expectedLines = ["! this should be shown", "! this should ALSO be shown"];
        assert.deepStrictEqual(lastTwoLines, expectedLines);
    });
});

function logLine(line = "", done = () => {}) {
    const client = new net.Socket();
    client.connect(5002, "localhost", function () {
        client.write(`cmd var set var=.mdi.tmpstr str=(eval(str_print('! > ${line}')))`, done());
    });
}

async function checkForcheTmpLib(lib_name, done = () => {}) {
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

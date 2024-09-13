const assert = require("assert");
const path = require("path");
const vscode = require("vscode");
const { evaluate_exp } = require("../src/aview.ts.js");
const { waitForAdamsConnection } = require("./utils.js");
const { debug_in_adams } = require("../src/debug_in_adams.ts.js");
const { execute_cmd } = require("../src/aview.ts.js");

output_channel = vscode.window.createOutputChannel("MSC Adams Testing");

const testPythonScriptPath = path.normalize(path.join(__dirname, "files", "test_model.py"));

suite("debug_in_adams Test Suite", () => {
    suiteSetup(async () => {
        // Wait for adams view connection
        await new Promise((resolve) => {
            waitForAdamsConnection(resolve);
        });

        // Attach the debugger
        await new Promise((resolve) => debug_in_adams(output_channel, null, resolve)());

        // Open test_model.py in the editor
        await vscode.workspace.openTextDocument(testPythonScriptPath).then((document) => {
            vscode.window.showTextDocument(document);
        });

        // Remove all breakpoints in test_model.py
        vscode.debug.removeBreakpoints(vscode.debug.breakpoints);

        // Set a breakpoint in test_model.py
        console.log(`Setting breakpoint in ${testPythonScriptPath}`);
        const breakpoint = new vscode.SourceBreakpoint(
            new vscode.Location(vscode.Uri.file(testPythonScriptPath), new vscode.Position(7, 0))
        );
        vscode.debug.addBreakpoints([breakpoint]);

        // Run the model
        await new Promise((resolve) => {
            // Set a timeout
            let wait_time = 10;
            setTimeout(() => {
                resolve();
            }, wait_time * 1000);

            let cmd = `file python read file="${testPythonScriptPath}"`;
            console.log(`Running Adams View command: ${cmd}`);
            execute_cmd(cmd, console.log);
            console.log(`Waiting ${wait_time} seconds for the debugger to break...`);
        });

        console.log("Continuing. Hopefully the debugger broke. ¯\\_(ツ)_/¯");
    });

    suiteTeardown(async () => {
        // Terminate the debug session
        await vscode.debug.activeDebugSession?.customRequest("disconnect");
    });

    test("mass should be 1 before continue and 2 after continue", async () => {
        // Before continue
        await new Promise((resolve) => {
            const activeDebugSession = vscode.debug.activeDebugSession;
            activeDebugSession.customRequest("stackTrace", { threadId: 1 }).then((response) => {
                const frameId = response.stackFrames[0].id;
                activeDebugSession
                    .customRequest("evaluate", { expression: "part.mass", frameId: frameId })
                    .then(
                        (response) => {
                            mass = parseFloat(response.result);
                            console.log(`mass=${mass}`);
                            assert.strictEqual(
                                mass,
                                1,
                                "The mass of PART_2 is not 1. This means the breakpoint was not hit."
                            );
                            resolve();
                        },
                        (err) => {
                            throw new Error(err);
                        }
                    );
            });
        });

        // After continue
        await new Promise((resolve) => {
            // Continue the model
            vscode.debug.activeDebugSession?.customRequest("continue").then(() => {
                evaluate_exp("test_model.PART_2.mass", console.log, (mass) => {
                    console.log(`mass=${mass}`);
                    assert.strictEqual(
                        mass,
                        2,
                        "The mass of PART_2 is not 2. This may indicate that the debugger did not continue."
                    );
                    resolve();
                });
            });
        });
    });
});

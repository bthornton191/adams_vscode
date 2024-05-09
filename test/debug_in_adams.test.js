const assert = require("assert");
const path = require("path");
const fs = require("fs");
const vscode = require("vscode");
const { evaluate_exp } = require("../src/aview.ts.js");
const { waitForAdamsConnection, get_parents } = require("./utils.js");
const { debug_in_adams } = require("../src/debug_in_adams.ts.js");
const { execute_cmd } = require("../src/aview.ts.js");
const child_process = require("child_process");

output_channel = vscode.window.createOutputChannel("MSC Adams Testing");

const testPythonScriptPath = path.normalize(path.join(__dirname, "files", "test_model.py"));

suite("debug_in_adams Test Suite", () => {
    suiteSetup(async () => {
        let version = getAdamsVersionFromMdi(path.parse(process.env._ADAMS_LAUNCH_COMMAND));
        if (version == 2023) {
            console.log("Testing in Adams 2023. That means we need to set the debug adapter");
            set2023DebugAdapter();
        } else {
            console.log(
                "**NOT** Testing in Adams 2023. That means we can use the default debug adapter"
            );
            unsetDebugAdapter();
        }

        // Wait for adams view connection
        await new Promise((resolve) => {
            waitForAdamsConnection(resolve);
        });

        // Attach the debugger
        await new Promise((resolve) => debug_in_adams(output_channel, resolve)());

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
            let wait_time = 5;
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

/**
 * Get the version of Adams from the mdi file
 * @param {path.ParsedPath} adamsLaunchCommand
 * @returns {int}
 */
function getAdamsVersionFromMdi(adamsLaunchCommand) {
    return parseInt(get_parents(adamsLaunchCommand, 2).name.split("_")[0]);
}

/**
 * Set the the debug adapter path that should be used for Adams 2023
 */
function set2023DebugAdapter() {
    vscode.workspace.getConfiguration("msc-adams").update("debugOptions", {
        debugAdapterPath: get2023DebugAdapterPath(),
    });
}

/**
 * Unset the debug adapter path
 */
function unsetDebugAdapter() {
    vscode.workspace
        .getConfiguration("msc-adams")
        .update("debugOptions", { debugAdapterPath: undefined });
}

/**
 * This suite tests that a popup is shown when the user tries to debug in Adams 2023 without setting the debug adapter path
 */
suite("debug_in_adams in Adams 2023 without setting the debug adapter path", () => {
    suiteSetup(async () => {
        let version = getAdamsVersionFromMdi(path.parse(process.env._ADAMS_LAUNCH_COMMAND));

        if (version != 2023) {
            console.log("Not testing in Adams 2023. Skipping this test.");
            this.skip();
        }

        // Wait for adams view connection
        await new Promise((resolve) => {
            waitForAdamsConnection(resolve);
        });

        // Attach the debugger
        await new Promise((resolve) => debug_in_adams(output_channel, resolve)());

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
            let wait_time = 5;
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

    test("popup should be shown", async () => {
        // Before continue
        await new Promise((resolve) => {
            const activeDebugSession = vscode.debug.activeDebugSession;
            activeDebugSession.customRequest("stackTrace", { threadId: 1 }).then((response) => {
                const frameId = response.stackFrames[0].id;
                activeDebugSession
                    .customRequest("evaluate", { expression: "part.mass", frameId: frameId })
                    .then((response) => {
                        mass = parseFloat(response.result);
                        console.log(`mass=${mass}`);
                        assert.strictEqual(
                            mass,
                            1,
                            "The mass of PART_2 is not 1. This means the breakpoint was not hit."
                        );
                        resolve();
                    });
            });
        });
    });
});

/**
 * Get the path to the the debug.adapter module for the python 3.10
 * @returns {path.ParsedPath}
 */
function get2023DebugAdapterPath() {
    // List all installed python versions
    const python_exes = child_process.execSync("where python").toString().split("\n");
    // Get the python 3.10 path
    const python_310_path = python_exes.find((exe) => {
        const version = child_process.execSync(`${exe} --version`).toString();
        return version.includes("3.10");
    });

    // Raise an error if python 3.10 is not found
    if (!python_310_path) {
        throw new Error("Python 3.10 not found");
    }

    const text = child_process.execSync(`${python_310_path} -m pip show debugpy`).toString();

    if (text.includes("WARNING:")) {
        throw new Error("Debugpy not found. You may need to install debugpy in " + python_310_path);
    }

    // Get the location from the text
    const location = path.normalize(
        text
            .split("\r\n")
            .find((line) => line.startsWith("Location"))
            .split(": ")[1]
    );

    // Get the path to the debug adapter
    const debug_adapter_path = path.join(location, "debugpy", "adapter");

    // Raise an error if the debug adapter is not found
    if (!fs.existsSync(debug_adapter_path)) {
        throw new Error(
            `Debug adapter not found. You may need to install debugpy in ${python_310_path}`
        );
    }

    return path.normalize(debug_adapter_path);
}

async function wait(secs) {
    await new Promise((resolve) => {
        setTimeout(resolve, secs * 1000);
    });
}

const assert = require("assert");
const vscode = require("vscode");
const fs = require("fs");
const path = require("path");
const { load_stub_files } = require("../src/load_stub_files.ts.js");

output_channel = vscode.window.createOutputChannel("MSC Adams Testing");

suite("load_stub_files Test Suite", () => {
    const settingsPath = path.join(
        vscode.workspace.workspaceFolders[0].uri.fsPath,
        ".vscode",
        "settings.json"
    );

    suiteSetup(() => {
        // Clear workspace settings before tests
        if (fs.existsSync(settingsPath)) {
            fs.unlinkSync(settingsPath);
        }
    });

    suiteTeardown(() => {
        // Clear workspace settings after tests
        if (fs.existsSync(settingsPath)) {
            fs.unlinkSync(settingsPath);
        }
    });

    test("should add adams_stub_dir to python.analysis.extraPaths", async () => {
        const context = {
            asAbsolutePath: (relativePath) =>
                path.join(vscode.workspace.workspaceFolders[0].uri.fsPath, relativePath),
        };
        const reporter = {
            sendTelemetryEvent: () => {},
        };

        // Run load_stub_files
        await load_stub_files(context, output_channel, reporter)();

        // Wait up to 5 seconds for settings.json to be created
        const startTime = Date.now();
        const timeout = 5000; // 5 seconds
        while (!fs.existsSync(settingsPath) && Date.now() - startTime < timeout) {
            await new Promise((resolve) => setTimeout(resolve, 100)); // Wait for 100ms
        }

        // Verify settings.json exists
        if (!fs.existsSync(settingsPath)) {
            assert.fail(`settings.json does not exist at ${settingsPath}`);
        } else {
            // Verify settings.json contains the expected path
            const settings = JSON.parse(fs.readFileSync(settingsPath, "utf8"));
            const adamsStubDir = context.asAbsolutePath("resources/adamspy");
            assert(
                settings["python.analysis.extraPaths"].includes(adamsStubDir),
                "adams_stub_dir was not added to python.analysis.extraPaths"
            );
        }
    });

    test("should add adams_stub_dir to python.autoComplete.extraPaths", async () => {
        const context = {
            asAbsolutePath: (relativePath) =>
                path.join(vscode.workspace.workspaceFolders[0].uri.fsPath, relativePath),
        };
        const reporter = {
            sendTelemetryEvent: () => {},
        };

        // Run load_stub_files
        await load_stub_files(context, output_channel, reporter)();

        // Verify settings.json contains the expected path
        const settings = JSON.parse(fs.readFileSync(settingsPath, "utf8"));
        const adamsStubDir = context.asAbsolutePath("resources/adamspy");
        assert(
            settings["python.autoComplete.extraPaths"].includes(adamsStubDir),
            "adams_stub_dir was not added to python.autoComplete.extraPaths"
        );
    });
});

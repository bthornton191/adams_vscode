const assert = require("assert");
const vscode = require("vscode");
const fs = require("fs");
const path = require("path");
const { load_stub_files } = require("../src/load_stub_files.ts.js");

output_channel = vscode.window.createOutputChannel("MSC Adams Testing");

// Define module-level asAbsolutePath function
function asAbsolutePath(relativePath) {
    return path.join(path.dirname(vscode.workspace.workspaceFolders[0].uri.fsPath), relativePath);
}

// Define module-level context object
const context = { asAbsolutePath };

suite("load_stub_files Test Suite", () => {
    const settingsPath = path.join(
        vscode.workspace.workspaceFolders[0].uri.fsPath,
        ".vscode",
        "settings.json"
    );

    suiteSetup(() => {
        // Create .vscode directory if it doesn't exist
        const vscodeDir = path.dirname(settingsPath);
        if (!fs.existsSync(vscodeDir)) {
            fs.mkdirSync(vscodeDir, { recursive: true });
        }
    });

    setup(async () => {
        // Update Settings
        await vscode.workspace
            .getConfiguration("python")
            .update("analysis.extraPaths", [], vscode.ConfigurationTarget.Workspace);
        await vscode.workspace
            .getConfiguration("python")
            .update("autoComplete.extraPaths", [], vscode.ConfigurationTarget.Workspace);
    });

    teardown(() => {
        // Clear settings after each test
        if (fs.existsSync(settingsPath)) {
            fs.unlinkSync(settingsPath);
        }
    });

    test("should add adams_stub_dir to python.analysis.extraPaths", async () => {
        const adamsStubDir = asAbsolutePath("resources/adamspy");

        // Run load_stub_files with the module-level context
        await load_stub_files(context, output_channel)();

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
            assert(
                settings["python.analysis.extraPaths"].includes(adamsStubDir),
                "adams_stub_dir was not added to python.analysis.extraPaths"
            );
        }
    });

    test("should add adams_stub_dir to python.autoComplete.extraPaths", async () => {
        const adamsStubDir = asAbsolutePath("resources/adamspy");

        // Run load_stub_files with the module-level context
        await load_stub_files(context, output_channel)();

        // Wait a moment for settings to be updated
        await new Promise((resolve) => setTimeout(resolve, 100));

        // Read settings.json directly to verify changes
        const settings = JSON.parse(fs.readFileSync(settingsPath, "utf8"));

        // Verify adamsStubDir was added
        assert(
            settings["python.autoComplete.extraPaths"].includes(adamsStubDir),
            "adams_stub_dir was not added to python.autoComplete.extraPaths"
        );
    });

    test("should not duplicate paths in python.analysis.extraPaths", async () => {
        const adamsStubDir = asAbsolutePath("resources/adamspy");

        // Update Settings
        await vscode.workspace
            .getConfiguration("python")
            .update("analysis.extraPaths", [adamsStubDir], vscode.ConfigurationTarget.Workspace);
        await vscode.workspace
            .getConfiguration("python")
            .update("autoComplete.extraPaths", [], vscode.ConfigurationTarget.Workspace);

        // Run load_stub_files with the module-level context
        await load_stub_files(context, output_channel)();

        // Wait a moment for settings to be updated
        await new Promise((resolve) => setTimeout(resolve, 100));

        // Read settings.json directly to verify changes
        const settings = JSON.parse(fs.readFileSync(settingsPath, "utf8"));

        // Verify the path is only present once
        assert.strictEqual(
            settings["python.analysis.extraPaths"].filter((path) => path === adamsStubDir).length,
            1,
            "adams_stub_dir path was duplicated in python.analysis.extraPaths"
        );
    });
});

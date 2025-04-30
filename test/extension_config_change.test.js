const assert = require("assert");
const vscode = require("vscode");
const fs = require("fs");
const path = require("path");
const { activate } = require("../src/extension.ts");

output_channel = vscode.window.createOutputChannel("MSC Adams Testing");

// Define module-level asAbsolutePath function
function asAbsolutePath(relativePath) {
    return path.join(path.dirname(vscode.workspace.workspaceFolders[0].uri.fsPath), relativePath);
}

// Define module-level context object with subscriptions array
const context = {
    asAbsolutePath,
    subscriptions: [],
};

suite("Configuration Change Test Suite", () => {
    const settingsPath = path.join(
        vscode.workspace.workspaceFolders[0].uri.fsPath,
        ".vscode",
        "settings.json"
    );
    const mdiBat = path.resolve(process.env._ADAMS_LAUNCH_COMMAND);

    // Track executed commands
    let executedCommands = [];
    let originalExecuteCommand;

    suiteSetup(() => {
        // Create .vscode directory if it doesn't exist
        const vscodeDir = path.dirname(settingsPath);
        if (!fs.existsSync(vscodeDir)) {
            fs.mkdirSync(vscodeDir, { recursive: true });
        }

        // Store the original executeCommand function
        originalExecuteCommand = vscode.commands.executeCommand;

        // Replace executeCommand to track calls
        vscode.commands.executeCommand = function (command, ...args) {
            executedCommands.push({ command, args });
            return Promise.resolve();
        };

        activate(context, false, true);
    });

    setup(async () => {
        // Clear settings before each test
        if (fs.existsSync(settingsPath)) {
            fs.unlinkSync(settingsPath);
        }

        // Reset tracking of executed commands
        executedCommands = [];

        // Reset configuration to default values
        await vscode.workspace
            .getConfiguration("msc-adams")
            .update("adamsLaunchCommand", null, vscode.ConfigurationTarget.Workspace);
        await vscode.workspace
            .getConfiguration("msc-adams")
            .update(
                "runInAdams.autoLoadAdamsSitePackages",
                true,
                vscode.ConfigurationTarget.Workspace
            );

        // Wait for configuration to be applied
        await new Promise((resolve) => setTimeout(resolve, 500));
    });

    suiteTeardown(async () => {
        // Restore original executeCommand function
        vscode.commands.executeCommand = originalExecuteCommand;

        // Dispose all subscriptions
        for (const subscription of context.subscriptions) {
            try {
                if (subscription && typeof subscription.dispose === "function") {
                    subscription.dispose();
                }
            } catch (error) {
                console.error(`Error disposing subscription: ${error.message}`);
            }
        }
        // Clear the subscriptions array
        context.subscriptions.length = 0;

        // Clear workspace settings after tests
        if (fs.existsSync(settingsPath)) {
            fs.unlinkSync(settingsPath);
        }

        // Let any pending operations complete
        await new Promise((resolve) => setTimeout(resolve, 500));
    });

    test("should trigger loadAdamsSitePackages when adamsLaunchCommand changes and autoLoadAdamsSitePackages is enabled", async () => {
        // Set up initial condition - autoLoadAdamsSitePackages is enabled by default

        // Change the adamsLaunchCommand setting to trigger the configuration change handler
        await vscode.workspace
            .getConfiguration("msc-adams")
            .update("adamsLaunchCommand", mdiBat, vscode.ConfigurationTarget.Workspace);

        // Wait for configuration change event to be processed
        await new Promise((resolve) => setTimeout(resolve, 500));

        // Verify loadAdamsSitePackages was called
        const loadAdamsSitePackagesWasCalled = executedCommands.some(
            (cmd) => cmd.command === "msc_adams.loadAdamsSitePackages"
        );
        assert(
            loadAdamsSitePackagesWasCalled,
            "loadAdamsSitePackages should have been called when adamsLaunchCommand changed"
        );
    });

    test("should not trigger loadAdamsSitePackages when adamsLaunchCommand changes but autoLoadAdamsSitePackages is disabled", async () => {
        // Set up initial condition - disable autoLoadAdamsSitePackages
        await vscode.workspace
            .getConfiguration("msc-adams")
            .update(
                "runInAdams.autoLoadAdamsSitePackages",
                false,
                vscode.ConfigurationTarget.Workspace
            );

        // Wait for configuration to be applied
        await new Promise((resolve) => setTimeout(resolve, 500));

        // Clear the commands tracked so far
        executedCommands = [];

        // Change the adamsLaunchCommand setting to trigger the configuration change handler
        await vscode.workspace
            .getConfiguration("msc-adams")
            .update("adamsLaunchCommand", mdiBat, vscode.ConfigurationTarget.Workspace);

        // Wait for configuration change event to be processed
        await new Promise((resolve) => setTimeout(resolve, 1000));

        // Verify loadAdamsSitePackages was not called
        const loadAdamsSitePackagesWasCalled = executedCommands.some(
            (cmd) => cmd.command === "msc_adams.loadAdamsSitePackages"
        );
        assert(
            !loadAdamsSitePackagesWasCalled,
            "loadAdamsSitePackages should not have been called when autoLoadAdamsSitePackages is disabled"
        );
    });

    test("should not trigger loadAdamsSitePackages when adamsLaunchCommand is null", async () => {
        // Set up initial condition - set adamsLaunchCommand to a valid path
        await vscode.workspace
            .getConfiguration("msc-adams")
            .update("adamsLaunchCommand", mdiBat, vscode.ConfigurationTarget.Workspace);

        // Wait for configuration to be applied and initial commands to execute
        await new Promise((resolve) => setTimeout(resolve, 1000));

        // Clear the commands tracked so far
        executedCommands = [];

        // Change the adamsLaunchCommand setting to null
        await vscode.workspace
            .getConfiguration("msc-adams")
            .update("adamsLaunchCommand", null, vscode.ConfigurationTarget.Workspace);

        // Wait for configuration change event to be processed
        await new Promise((resolve) => setTimeout(resolve, 1000));

        // Verify loadAdamsSitePackages was not called
        const loadAdamsSitePackagesWasCalled = executedCommands.some(
            (cmd) => cmd.command === "msc_adams.loadAdamsSitePackages"
        );
        assert(
            !loadAdamsSitePackagesWasCalled,
            "loadAdamsSitePackages should not have been called when adamsLaunchCommand is null"
        );
    });

    test("should not trigger loadAdamsSitePackages when configuration change doesn't affect adamsLaunchCommand", async () => {
        // Set up initial conditions
        await vscode.workspace
            .getConfiguration("msc-adams")
            .update("adamsLaunchCommand", mdiBat, vscode.ConfigurationTarget.Workspace);

        // Wait for configuration to be applied and initial commands to execute
        await new Promise((resolve) => setTimeout(resolve, 1000));

        // Clear the commands tracked so far
        executedCommands = [];

        // Change some other setting
        await vscode.workspace
            .getConfiguration("msc-adams")
            .update("runInAdams.substituteSelf", "._vscode", vscode.ConfigurationTarget.Workspace);

        // Wait for configuration change event to be processed
        await new Promise((resolve) => setTimeout(resolve, 1000));

        // Verify loadAdamsSitePackages was not called
        const loadAdamsSitePackagesWasCalled = executedCommands.some(
            (cmd) => cmd.command === "msc_adams.loadAdamsSitePackages"
        );
        assert(
            !loadAdamsSitePackagesWasCalled,
            "loadAdamsSitePackages should not have been called when configuration change doesn't affect adamsLaunchCommand"
        );
    });
});

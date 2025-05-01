const assert = require("assert");
const vscode = require("vscode");
const fs = require("fs");
const path = require("path");
const { add_adams_site_packages } = require("../src/add_adams_site_packages.ts.js");

output_channel = vscode.window.createOutputChannel("MSC Adams Testing");

suite("add_adams_site_packages Test Suite", () => {
    const settingsPath = path.join(
        vscode.workspace.workspaceFolders[0].uri.fsPath,
        ".vscode",
        "settings.json"
    );

    // Mock configuration settings for msc-adams only
    const mdiBat = path.resolve(process.env._ADAMS_LAUNCH_COMMAND);
    const topDir = path.dirname(path.dirname(mdiBat));
    const sitePackages = path.join(topDir, "python", "win64", "Lib", "site-packages");

    suiteSetup(() => {
        // Create .vscode directory if it doesn't exist
        const vscodeDir = path.dirname(settingsPath);
        if (!fs.existsSync(vscodeDir)) {
            fs.mkdirSync(vscodeDir, { recursive: true });
        }
    });

    setup(async () => {
        // Clear settings
        if (fs.existsSync(settingsPath)) {
            fs.unlinkSync(settingsPath);
        }

        // Update Settings
        await vscode.workspace
            .getConfiguration("python")
            .update("analysis.extraPaths", [], vscode.ConfigurationTarget.Workspace);
        await vscode.workspace
            .getConfiguration("python")
            .update("autoComplete.extraPaths", [], vscode.ConfigurationTarget.Workspace);
        await vscode.workspace
            .getConfiguration("msc-adams")
            .update("adamsLaunchCommand", mdiBat, vscode.ConfigurationTarget.Workspace);

        // Give VS Code time to process the configuration changes
        await new Promise((resolve) => setTimeout(resolve, 500));
    });

    teardown(() => {
        // Clear settings after each test
        if (fs.existsSync(settingsPath)) {
            fs.unlinkSync(settingsPath);
        }
    });

    test("should add Adams site-packages to python.analysis.extraPaths", async () => {
        // Run add_adams_site_packages
        await add_adams_site_packages(output_channel)();

        // Wait a moment for settings to be updated
        await new Promise((resolve) => setTimeout(resolve, 100));

        // Read settings.json directly to verify changes
        const settings = JSON.parse(fs.readFileSync(settingsPath, "utf8"));

        // Verify the expected path was added to python.analysis.extraPaths
        assert(
            settings["python.analysis.extraPaths"].includes(sitePackages),
            "Adams site-packages was not added to python.analysis.extraPaths"
        );
    });

    test("should add Adams site-packages to python.autoComplete.extraPaths", async () => {
        // Run add_adams_site_packages
        await add_adams_site_packages(output_channel)();

        // Wait a moment for settings to be updated
        await new Promise((resolve) => setTimeout(resolve, 100));

        // Read settings.json directly to verify changes
        const settings = JSON.parse(fs.readFileSync(settingsPath, "utf8"));

        // Verify the expected path was added to python.autoComplete.extraPaths
        assert(
            settings["python.autoComplete.extraPaths"].includes(sitePackages),
            "Adams site-packages was not added to python.autoComplete.extraPaths"
        );
    });

    test("should not duplicate paths in python.analysis.extraPaths", async () => {
        // Set up initial settings.json with the path already present

        // Update Settings
        await vscode.workspace
            .getConfiguration("python")
            .update("analysis.extraPaths", [sitePackages], vscode.ConfigurationTarget.Workspace);
        await vscode.workspace
            .getConfiguration("python")
            .update("autoComplete.extraPaths", [], vscode.ConfigurationTarget.Workspace);
        await vscode.workspace
            .getConfiguration("msc-adams")
            .update("adamsLaunchCommand", mdiBat, vscode.ConfigurationTarget.Workspace);

        // Run add_adams_site_package
        await add_adams_site_packages(output_channel)();

        // Wait a moment for settings to be updated
        await new Promise((resolve) => setTimeout(resolve, 100));

        // Read settings.json directly to verify changes
        const settings = JSON.parse(fs.readFileSync(settingsPath, "utf8"));

        // Verify the path is only present once
        assert.strictEqual(
            settings["python.analysis.extraPaths"].filter((path) => path === sitePackages).length,
            1,
            "Adams site-packages path was duplicated in python.analysis.extraPaths"
        );
    });
    ("");
    test("should remove old Adams site-packages paths", async () => {
        // Create paths to an old Adams version's site-packages
        const adamsParentDir = path.dirname(topDir);
        const oldAdamsDir = path.join(adamsParentDir, "2022_1");
        const oldSitePackages = path.join(oldAdamsDir, "python", "win64", "Lib", "site-packages");

        // Set up initial settings with both current and old site-packages paths
        await vscode.workspace
            .getConfiguration("python")
            .update(
                "analysis.extraPaths",
                [sitePackages, oldSitePackages],
                vscode.ConfigurationTarget.Workspace
            );
        await vscode.workspace
            .getConfiguration("python")
            .update(
                "autoComplete.extraPaths",
                [sitePackages, oldSitePackages],
                vscode.ConfigurationTarget.Workspace
            );
        await vscode.workspace
            .getConfiguration("msc-adams")
            .update("adamsLaunchCommand", mdiBat, vscode.ConfigurationTarget.Workspace);

        // Run add_adams_site_packages
        await add_adams_site_packages(output_channel)();

        // Wait a moment for settings to be updated
        await new Promise((resolve) => setTimeout(resolve, 100));

        // Read settings.json directly to verify changes
        const settings = JSON.parse(fs.readFileSync(settingsPath, "utf8"));

        // Verify the old site-packages path was removed
        assert(
            !settings["python.analysis.extraPaths"].includes(oldSitePackages),
            "Old Adams site-packages was not removed from python.analysis.extraPaths"
        );
        assert(
            !settings["python.autoComplete.extraPaths"].includes(oldSitePackages),
            "Old Adams site-packages was not removed from python.autoComplete.extraPaths"
        );

        // Verify the current site-packages path is still there
        assert(
            settings["python.analysis.extraPaths"].includes(sitePackages),
            "Current Adams site-packages was incorrectly removed from python.analysis.extraPaths"
        );
        assert(
            settings["python.autoComplete.extraPaths"].includes(sitePackages),
            "Current Adams site-packages was incorrectly removed from python.autoComplete.extraPaths"
        );
    });
});

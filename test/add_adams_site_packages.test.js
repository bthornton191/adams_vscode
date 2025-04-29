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
    let mockMdiBat = path.join("C:", "MSC.Software", "Adams", "2023", "common", "mdi.bat");

    // Store original workspace.getConfiguration
    let originalGetConfiguration;

    // Mock Python analysis paths
    let mockExtraPaths = [];
    let mockAutoCompletePaths = [];

    // Create a mock reporter
    const mockReporter = {
        sendTelemetryEvent: (name, props) => {
            // Do nothing in test
        },
    };

    suiteSetup(() => {
        // Create .vscode directory if it doesn't exist
        const vscodeDir = path.dirname(settingsPath);
        if (!fs.existsSync(vscodeDir)) {
            fs.mkdirSync(vscodeDir, { recursive: true });
        }

        // Clear workspace settings before tests
        if (fs.existsSync(settingsPath)) {
            fs.unlinkSync(settingsPath);
        }

        // Create empty settings.json
        fs.writeFileSync(settingsPath, JSON.stringify({}), "utf8");

        // Store the original function
        originalGetConfiguration = vscode.workspace.getConfiguration;
    });

    setup(() => {
        // Reset mock paths before each test
        mockExtraPaths = [];
        mockAutoCompletePaths = [];

        // Create mock configuration function
        vscode.workspace.getConfiguration = function (section) {
            if (section === "msc-adams") {
                return {
                    get: (key, defaultValue) => {
                        if (key === "adamsLaunchCommand") {
                            return mockMdiBat;
                        }
                        return defaultValue;
                    },
                };
            } else if (section === "python") {
                return {
                    get: (key, defaultValue) => {
                        if (key === "analysis.extraPaths") {
                            return mockExtraPaths;
                        } else if (key === "autoComplete.extraPaths") {
                            return mockAutoCompletePaths;
                        }
                        return defaultValue;
                    },
                    update: (key, value, scope) => {
                        if (key === "analysis.extraPaths") {
                            mockExtraPaths = value;
                        } else if (key === "autoComplete.extraPaths") {
                            mockAutoCompletePaths = value;
                        }

                        // Update settings.json to match our mock
                        if (fs.existsSync(settingsPath)) {
                            const fileSettings = JSON.parse(fs.readFileSync(settingsPath, "utf8"));
                            fileSettings[`python.${key}`] = value;
                            fs.writeFileSync(
                                settingsPath,
                                JSON.stringify(fileSettings, null, 4),
                                "utf8"
                            );
                        }
                        return Promise.resolve();
                    },
                };
            }
            return originalGetConfiguration(section);
        };
    });

    teardown(() => {
        // Restore original function after each test to prevent test interference
        vscode.workspace.getConfiguration = originalGetConfiguration;
    });

    suiteTeardown(() => {
        // Ensure original function is restored
        vscode.workspace.getConfiguration = originalGetConfiguration;

        // Clear workspace settings after tests
        if (fs.existsSync(settingsPath)) {
            fs.unlinkSync(settingsPath);
        }
    });

    test("should add Adams site-packages to python.analysis.extraPaths", async () => {
        // Calculate the expected site-packages path based on the mock mdi.bat
        const mockAdamsDir = path.dirname(path.dirname(mockMdiBat));
        const mockSitePackages = path.join(mockAdamsDir, "python", "win64", "Lib", "site-packages");

        // Initial paths should be empty
        assert.deepStrictEqual(mockExtraPaths, [], "Initial extraPaths should be empty");

        const context = {
            asAbsolutePath: (relativePath) => relativePath,
        };

        // Run add_adams_site_packages
        await add_adams_site_packages(context, output_channel, mockReporter)();

        // Verify the expected path was added to python.analysis.extraPaths
        assert(
            mockExtraPaths.includes(mockSitePackages),
            "Adams site-packages was not added to python.analysis.extraPaths"
        );
    });

    test("should add Adams site-packages to python.autoComplete.extraPaths", async () => {
        // Calculate the expected site-packages path based on the mock mdi.bat
        const mockAdamsDir = path.dirname(path.dirname(mockMdiBat));
        const mockSitePackages = path.join(mockAdamsDir, "python", "win64", "Lib", "site-packages");

        // Initial paths should be empty
        assert.deepStrictEqual(
            mockAutoCompletePaths,
            [],
            "Initial autoCompletePaths should be empty"
        );

        const context = {
            asAbsolutePath: (relativePath) => relativePath,
        };

        // Run add_adams_site_packages
        await add_adams_site_packages(context, output_channel, mockReporter)();

        // Verify the expected path was added to python.autoComplete.extraPaths
        assert(
            mockAutoCompletePaths.includes(mockSitePackages),
            "Adams site-packages was not added to python.autoComplete.extraPaths"
        );
    });

    test("should not duplicate paths in python.analysis.extraPaths", async () => {
        // Calculate the expected site-packages path based on the mock mdi.bat
        const mockAdamsDir = path.dirname(path.dirname(mockMdiBat));
        const mockSitePackages = path.join(mockAdamsDir, "python", "win64", "Lib", "site-packages");

        // Set up the path as already present
        mockExtraPaths = [mockSitePackages];

        const context = {
            asAbsolutePath: (relativePath) => relativePath,
        };

        // Run add_adams_site_packages
        await add_adams_site_packages(context, output_channel, mockReporter)();

        // Verify the path is only present once
        assert.strictEqual(
            mockExtraPaths.filter((path) => path === mockSitePackages).length,
            1,
            "Adams site-packages path was duplicated in python.analysis.extraPaths"
        );
    });
});

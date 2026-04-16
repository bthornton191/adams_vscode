/**
 * Tests for src/mcp_server_provider.ts.js
 *
 * Verifies that provideMcpServerDefinitions() builds the correct argument
 * list for the Adams CMD Linter MCP server, in particular the new
 * --macro-base-dir flag that was added so the background workspace scan
 * targets the right directory.
 *
 * Requires VS Code 1.99+ for the lm.registerMcpServerDefinitionProvider API.
 * If the API is absent the suite skips automatically.
 */

const assert = require("assert");
const path = require("path");
const { registerMcpServerProvider } = require("../src/mcp_server_provider.ts.js");

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function makeMockContext() {
    return {
        asAbsolutePath: (p) => path.join(__dirname, "..", p),
        subscriptions: [],
        extension: { packageJSON: { version: "0.0.0-test" } },
    };
}

// ---------------------------------------------------------------------------
// Suite
// ---------------------------------------------------------------------------

suite("MCP Server Provider", () => {
    let capturedProvider = null;
    let originalRegister = null;
    let OriginalMcpClass = undefined;

    suiteSetup(function () {
        const vscode = require("vscode");

        // Skip the entire suite on older VS Code versions that don't have the
        // MCP provider API (pre-1.99).
        if (typeof vscode.lm?.registerMcpServerDefinitionProvider !== "function") {
            this.skip();
            return;
        }

        // Intercept registerMcpServerDefinitionProvider so we can get hold of
        // the provider object and call provideMcpServerDefinitions() directly.
        originalRegister = vscode.lm.registerMcpServerDefinitionProvider.bind(vscode.lm);
        vscode.lm.registerMcpServerDefinitionProvider = (_id, provider) => {
            capturedProvider = provider;
            return { dispose: () => {} };
        };

        // Replace McpStdioServerDefinition with a plain object factory so we
        // can inspect the constructor arguments without relying on internal
        // VS Code class internals.
        OriginalMcpClass = vscode.McpStdioServerDefinition;
        vscode.McpStdioServerDefinition = function (name, cmd, args, env, version) {
            this.name = name;
            this.cmd = cmd;
            this.args = args;
            this.env = env;
            this.version = version;
        };

        const ctx = makeMockContext();
        registerMcpServerProvider(ctx);
        ctx.subscriptions.length = 0; // clean up disposables

        // Hard-fail if the provider was not captured — catches regressions in
        // the registration path that would otherwise silently skip all tests.
        assert.ok(
            capturedProvider,
            "registerMcpServerProvider must invoke registerMcpServerDefinitionProvider",
        );
    });

    suiteTeardown(async () => {
        const vscode = require("vscode");
        if (originalRegister) {
            vscode.lm.registerMcpServerDefinitionProvider = originalRegister;
        }
        if (OriginalMcpClass !== undefined) {
            vscode.McpStdioServerDefinition = OriginalMcpClass;
        }
        // Reset workspace settings touched by these tests.
        const cfg = vscode.workspace.getConfiguration("msc-adams");
        await cfg.update("linter.enabled", undefined, vscode.ConfigurationTarget.Workspace);
        await cfg.update(
            "linter.scanWorkspaceMacros",
            undefined,
            vscode.ConfigurationTarget.Workspace,
        );
    });

    // -----------------------------------------------------------------------
    // --macro-base-dir
    // -----------------------------------------------------------------------

    test("passes --macro-base-dir equal to the first workspace folder when scanWorkspaceMacros is enabled", async function () {
        const vscode = require("vscode");
        const cfg = vscode.workspace.getConfiguration("msc-adams");
        await cfg.update("linter.enabled", true, vscode.ConfigurationTarget.Workspace);
        await cfg.update("linter.scanWorkspaceMacros", true, vscode.ConfigurationTarget.Workspace);

        const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspaceRoot) {
            // No workspace folder is open in this test environment.
            // When absent, --scan-workspace-macros is still emitted (the user
            // explicitly enabled it) but --macro-base-dir is omitted — the
            // Python server falls back to os.getcwd(). Skip the path-equality
            // check here; the no-folder behaviour is verified in the
            // 'omits --macro-base-dir when no workspace folder' test below.
            this.skip();
        }

        const defs = capturedProvider.provideMcpServerDefinitions();
        const linterDef = defs.find((d) => d.name === "Adams CMD Linter");

        assert.ok(linterDef, "Adams CMD Linter definition should be present");
        assert.ok(Array.isArray(linterDef.args), "args should be an array");

        const macroDirIdx = linterDef.args.indexOf("--macro-base-dir");
        assert.notStrictEqual(
            macroDirIdx,
            -1,
            "--macro-base-dir should be present in args when scanWorkspaceMacros is true",
        );
        assert.strictEqual(
            linterDef.args[macroDirIdx + 1],
            workspaceRoot,
            "--macro-base-dir value should equal the first workspace folder path",
        );
    });

    test("omits --macro-base-dir and --scan-workspace-macros when scanWorkspaceMacros is disabled", async function () {
        const vscode = require("vscode");
        const cfg = vscode.workspace.getConfiguration("msc-adams");
        await cfg.update("linter.enabled", true, vscode.ConfigurationTarget.Workspace);
        await cfg.update("linter.scanWorkspaceMacros", false, vscode.ConfigurationTarget.Workspace);

        const defs = capturedProvider.provideMcpServerDefinitions();
        const linterDef = defs.find((d) => d.name === "Adams CMD Linter");

        assert.ok(linterDef, "Adams CMD Linter definition should be present");
        assert.ok(
            !linterDef.args.includes("--scan-workspace-macros"),
            "--scan-workspace-macros should not be in args when disabled",
        );
        assert.ok(
            !linterDef.args.includes("--macro-base-dir"),
            "--macro-base-dir should not be in args when scanWorkspaceMacros is false",
        );
    });

    // -----------------------------------------------------------------------
    // ADAMS_LAUNCH_COMMAND env var forwarding
    // -----------------------------------------------------------------------

    test("forwards adamsLaunchCommand config to ADAMS_LAUNCH_COMMAND env var on Adams View definition", async function () {
        const vscode = require("vscode");
        const cfg = vscode.workspace.getConfiguration("msc-adams");
        await cfg.update(
            "adamsLaunchCommand",
            "C:\\Adams\\mdi.bat",
            vscode.ConfigurationTarget.Workspace,
        );

        try {
            const defs = capturedProvider.provideMcpServerDefinitions();
            const viewDef = defs.find((d) => d.name === "Adams View");

            assert.ok(viewDef, "Adams View definition should be present");
            assert.strictEqual(
                viewDef.env.ADAMS_LAUNCH_COMMAND,
                "C:\\Adams\\mdi.bat",
                "ADAMS_LAUNCH_COMMAND should match the adamsLaunchCommand config value",
            );
            assert.strictEqual(
                viewDef.env.ADAMS_LISTENER_PORT,
                String(cfg.get("aviewPortNumber", 5002)),
                "ADAMS_LISTENER_PORT should still be present",
            );
        } finally {
            await cfg.update("adamsLaunchCommand", undefined, vscode.ConfigurationTarget.Workspace);
        }
    });

    test("uses default adamsLaunchCommand value for ADAMS_LAUNCH_COMMAND when no explicit override is set", async function () {
        const vscode = require("vscode");
        const cfg = vscode.workspace.getConfiguration("msc-adams");
        await cfg.update("adamsLaunchCommand", undefined, vscode.ConfigurationTarget.Workspace);

        const defs = capturedProvider.provideMcpServerDefinitions();
        const viewDef = defs.find((d) => d.name === "Adams View");

        assert.ok(viewDef, "Adams View definition should be present");
        // The setting has a default of "mdi.bat" in package.json, so
        // ADAMS_LAUNCH_COMMAND is always populated.
        assert.strictEqual(
            viewDef.env.ADAMS_LAUNCH_COMMAND,
            cfg.get("adamsLaunchCommand"),
            "ADAMS_LAUNCH_COMMAND should match the effective config value (default or explicit)",
        );
    });

    // -----------------------------------------------------------------------
    // --macro-base-dir (no workspace folder)
    // -----------------------------------------------------------------------

    test("omits --macro-base-dir but keeps --scan-workspace-macros when no workspace folder is open", async function () {
        const vscode = require("vscode");

        // Temporarily stub workspaceFolders to simulate an empty workspace.
        // This is only possible if the property is configurable on vscode.workspace.
        const descriptor = Object.getOwnPropertyDescriptor(vscode.workspace, "workspaceFolders");
        let stubbed = false;
        try {
            Object.defineProperty(vscode.workspace, "workspaceFolders", {
                get: () => [],
                configurable: true,
            });
            stubbed = true;
        } catch (_) {
            // workspaceFolders is not configurable on this VS Code version — skip.
            this.skip();
        }

        try {
            const cfg = vscode.workspace.getConfiguration("msc-adams");
            await cfg.update("linter.enabled", true, vscode.ConfigurationTarget.Workspace);
            await cfg.update(
                "linter.scanWorkspaceMacros",
                true,
                vscode.ConfigurationTarget.Workspace,
            );

            const defs = capturedProvider.provideMcpServerDefinitions();
            const linterDef = defs.find((d) => d.name === "Adams CMD Linter");

            assert.ok(linterDef, "Adams CMD Linter definition should be present");
            // --scan-workspace-macros MUST be present: the user explicitly
            // enabled scanning; the server falls back to os.getcwd().
            assert.ok(
                linterDef.args.includes("--scan-workspace-macros"),
                "--scan-workspace-macros should be present even when no workspace folder",
            );
            // --macro-base-dir MUST be absent: there is no folder path to pass.
            assert.ok(
                !linterDef.args.includes("--macro-base-dir"),
                "--macro-base-dir should be absent when workspaceFolders is empty",
            );
        } finally {
            if (stubbed) {
                if (descriptor) {
                    Object.defineProperty(vscode.workspace, "workspaceFolders", descriptor);
                } else {
                    delete vscode.workspace.workspaceFolders;
                }
            }
        }
    });
});

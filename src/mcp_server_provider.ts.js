const path = require("path");

/**
 * Registers the Adams View MCP server definition provider with VS Code's language model API.
 * This allows agents (e.g. GitHub Copilot in agent mode) to discover and use the Adams View
 * MCP server automatically, without the user needing to manually configure .vscode/mcp.json.
 *
 * Requires VS Code 1.99+. Silently skips registration on older versions.
 *
 * @param {import("vscode").ExtensionContext} context
 */
function registerMcpServerProvider(context, reporter = null) {
    const vscode = require("vscode");
    if (typeof vscode.lm?.registerMcpServerDefinitionProvider !== "function") {
        if (reporter) {
            reporter.sendTelemetryEvent("mcp_version_unsupported");
        }
        return;
    }

    const provider = {
        provideMcpServerDefinitions() {
            const config = vscode.workspace.getConfiguration("msc-adams");
            const port = config.get("aviewPortNumber", 5002);
            const version = context.extension.packageJSON.version ?? "0.0.0";

            const adamsViewEnv = { ADAMS_LISTENER_PORT: String(port) };
            const launchCommand = config.get("adamsLaunchCommand");
            if (launchCommand) {
                adamsViewEnv.ADAMS_LAUNCH_COMMAND = launchCommand;
            }

            const definitions = [
                new vscode.McpStdioServerDefinition(
                    "Adams View",
                    "node",
                    [
                        context.asAbsolutePath(
                            path.join("adams-view-mcp-server", "dist", "index.js"),
                        ),
                    ],
                    adamsViewEnv,
                    version,
                ),
            ];

            if (config.get("linter.enabled")) {
                // Python path resolution: prefer explicit extension setting, fall back
                // to the Python extension's interpreter, then bare "python".
                // Note: bare "python" may not resolve correctly on all systems (e.g.
                // Windows Store stub). Users should set msc-adams.linter.pythonPath if
                // the server fails to start. This matches the same fallback used in
                // cmd_lsp_client.ts.js.
                const python_path =
                    config.get("linter.pythonPath") ||
                    vscode.workspace.getConfiguration("python").get("defaultInterpreterPath") ||
                    "python";

                const mcp_args = [
                    context.asAbsolutePath(path.join("bundled", "tool", "mcp_server.py")),
                ];

                if (config.get("linter.scanWorkspaceMacros")) {
                    mcp_args.push("--scan-workspace-macros");

                    // Tell the server which directory to scan. Use the first
                    // workspace folder so the scan targets project files rather
                    // than whatever directory the extension host happens to use
                    // as its cwd (which may be the extension install directory).
                    const workspace_root = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
                    if (workspace_root) {
                        mcp_args.push("--macro-base-dir", workspace_root);
                    }
                }

                const macro_paths = config.get("linter.macroPaths");
                if (Array.isArray(macro_paths) && macro_paths.length > 0) {
                    mcp_args.push("--macro-paths", ...macro_paths);
                }

                const macro_ignore_paths = config.get("linter.macroIgnorePaths");
                if (Array.isArray(macro_ignore_paths) && macro_ignore_paths.length > 0) {
                    mcp_args.push("--macro-ignore-paths", ...macro_ignore_paths);
                }

                if (config.get("linter.showMacroHint") === false) {
                    mcp_args.push("--no-show-macro-hint");
                }

                const ude_paths = config.get("linter.udePaths");
                if (Array.isArray(ude_paths) && ude_paths.length > 0) {
                    mcp_args.push("--ude-paths", ...ude_paths);
                }

                const ude_ignore_paths = config.get("linter.udeIgnorePaths");
                if (Array.isArray(ude_ignore_paths) && ude_ignore_paths.length > 0) {
                    mcp_args.push("--ude-ignore-paths", ...ude_ignore_paths);
                }

                definitions.push(
                    new vscode.McpStdioServerDefinition(
                        "Adams CMD Linter",
                        python_path,
                        mcp_args,
                        {},
                        version,
                    ),
                );
            }

            return definitions;
        },
    };

    context.subscriptions.push(
        vscode.lm.registerMcpServerDefinitionProvider("msc-adams.adamsViewMcp", provider),
    );

    if (reporter) {
        const config = vscode.workspace.getConfiguration("msc-adams");
        reporter.sendTelemetryEvent(
            "mcp_servers_registered",
            {
                cmd_linter_enabled: String(!!config.get("linter.enabled")),
            },
            {
                server_count: config.get("linter.enabled") ? 2 : 1,
            },
        );
    }
}

exports.registerMcpServerProvider = registerMcpServerProvider;

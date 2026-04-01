const vscode = require("vscode");
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
function registerMcpServerProvider(context) {
    if (typeof vscode.lm?.registerMcpServerDefinitionProvider !== "function") {
        return;
    }

    const provider = {
        provideMcpServerDefinitions() {
            const config = vscode.workspace.getConfiguration("msc-adams");
            const port = config.get("aviewPortNumber", 5002);
            const version = context.extension.packageJSON.version ?? "0.0.0";

            const definitions = [
                new vscode.McpStdioServerDefinition(
                    "Adams View",
                    "node",
                    [
                        context.asAbsolutePath(
                            path.join("adams-view-mcp-server", "dist", "index.js"),
                        ),
                    ],
                    { ADAMS_LISTENER_PORT: String(port) },
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
}

exports.registerMcpServerProvider = registerMcpServerProvider;

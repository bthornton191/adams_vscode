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
            const port = vscode.workspace
                .getConfiguration("msc-adams")
                .get("aviewPortNumber", 5002);

            return [
                new vscode.McpStdioServerDefinition(
                    "Adams View",
                    "node",
                    [context.asAbsolutePath(path.join("adams-view-mcp-server", "dist", "index.js"))],
                    { ADAMS_LISTENER_PORT: String(port) },
                    "0.1.0",
                ),
            ];
        },
    };

    context.subscriptions.push(
        vscode.lm.registerMcpServerDefinitionProvider("msc-adams.adamsViewMcp", provider),
    );
}

exports.registerMcpServerProvider = registerMcpServerProvider;

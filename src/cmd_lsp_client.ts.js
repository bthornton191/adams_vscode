/**
 * Creates and manages the Adams CMD LSP client.
 *
 * Follows the existing codebase conventions:
 * - Plain JavaScript with CommonJS (require / exports)
 * - .ts.js file extension
 * - Dependency injection (output_channel, reporter passed as parameters)
 * - const vscode = require("vscode") inside function bodies
 *
 * @param {import("vscode").OutputChannel} output_channel
 * @param {object|null} reporter
 * @returns {{ start: Function, stop: Function }}
 */
function cmd_lsp_client(output_channel, reporter) {
    const vscode = require("vscode");
    const path = require("path");
    const { LanguageClient, TransportKind } = require("vscode-languageclient/node");

    let client = null;

    function start(context) {
        const config = vscode.workspace.getConfiguration("msc-adams");
        if (!config.get("linter.enabled")) {
            output_channel.appendLine(
                `[${new Date().toLocaleTimeString()}] Adams CMD linter disabled (msc-adams.linter.enabled=false)`,
            );
            return;
        }

        // Find Python interpreter — prefer the extension setting, fall back to
        // the Python extension's default, then bare "python".
        const python_path =
            config.get("linter.pythonPath") ||
            vscode.workspace.getConfiguration("python").get("defaultInterpreterPath") ||
            "python";

        // Launch the bundled wrapper script — no user pip-install required.
        const server_script = path.join(context.extensionPath, "bundled", "tool", "lsp_server.py");

        // Build CLI args from VS Code settings
        const server_args = [server_script];

        if (config.get("linter.scanWorkspaceMacros")) {
            server_args.push("--scan-workspace-macros");
        }

        const macro_paths = config.get("linter.macroPaths");
        if (Array.isArray(macro_paths) && macro_paths.length > 0) {
            server_args.push("--macro-paths", ...macro_paths);
        }

        const macro_ignore_paths = config.get("linter.macroIgnorePaths");
        if (Array.isArray(macro_ignore_paths) && macro_ignore_paths.length > 0) {
            server_args.push("--macro-ignore-paths", ...macro_ignore_paths);
        }

        if (config.get("linter.showMacroHint") === false) {
            server_args.push("--no-show-macro-hint");
        }

        const server_options = {
            command: python_path,
            args: server_args,
            transport: TransportKind.stdio,
        };

        const client_options = {
            documentSelector: [{ scheme: "file", language: "adams_cmd" }],
            outputChannel: output_channel,
            // Synchronize settings so the server can read them if needed
            synchronize: {
                configurationSection: "msc-adams",
            },
        };

        client = new LanguageClient(
            "adams-cmd-lsp",
            "Adams CMD Language Server",
            server_options,
            client_options,
        );

        client.start().then(
            function () {
                output_channel.appendLine(
                    `[${new Date().toLocaleTimeString()}] Adams CMD Language Server started`,
                );
                if (reporter) {
                    reporter.sendTelemetryEvent("lsp_started");
                }
            },
            function (err) {
                // Don't block activation on LSP failure — the server is optional
                output_channel.appendLine(
                    `[${new Date().toLocaleTimeString()}] Failed to start Adams CMD Language Server: ${err.message}`,
                );
            },
        );

        context.subscriptions.push(client);
    }

    function stop() {
        if (client) {
            return client.stop();
        }
    }

    return { start: start, stop: stop };
}

exports.cmd_lsp_client = cmd_lsp_client;

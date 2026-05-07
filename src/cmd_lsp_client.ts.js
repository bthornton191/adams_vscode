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
    /** @type {import("vscode").Disposable[]} */
    let macro_watchers = [];
    /** @type {import("vscode").Disposable|null} */
    let config_listener = null;
    /** @type {boolean} */
    let initial_start = true;
    /** @type {number} Incremented on every restart. Lets earlier stop callbacks bail out
     *  when a newer restart has already taken over. */
    let restart_generation = 0;

    function _create_macro_watchers(macro_paths) {
        macro_watchers.forEach((w) => w.dispose());
        macro_watchers = [];
        if (!Array.isArray(macro_paths) || macro_paths.length === 0) {
            return;
        }
        // Convert glob patterns to VS Code RelativePatterns anchored to each
        // workspace folder so that watchers respect the configured paths.
        const workspace_folders = vscode.workspace.workspaceFolders || [];
        for (const pattern of macro_paths) {
            if (workspace_folders.length > 0) {
                for (const folder of workspace_folders) {
                    macro_watchers.push(
                        vscode.workspace.createFileSystemWatcher(
                            new vscode.RelativePattern(folder, pattern),
                        ),
                    );
                }
            } else {
                // Fallback when no workspace is open
                macro_watchers.push(vscode.workspace.createFileSystemWatcher(pattern));
            }
        }
    }

    function _restart(context) {
        // Claim ownership of this restart. Any earlier stop callback that resolves
        // later will see its generation is stale and skip starting a new client.
        const generation = ++restart_generation;
        const prev_client = client;
        client = null;

        const stop_promise = prev_client ? prev_client.stop() : Promise.resolve();
        stop_promise
            .catch(function () {}) // absorb stop errors; restart regardless
            .then(function () {
                // Only start if no newer restart has been requested since.
                if (generation === restart_generation) {
                    _start_client(context);
                }
            });
    }

    function _start_client(context) {
        const config = vscode.workspace.getConfiguration("msc-adams");
        if (!config.get("linter.enabled")) {
            output_channel.appendLine(
                `[${new Date().toLocaleTimeString()}] Adams CMD linter disabled (msc-adams.linter.enabled=false)`,
            );
            if (reporter) {
                reporter.sendTelemetryEvent("lsp_disabled");
            }
            return;
        }

        // Find Python interpreter — prefer the extension setting, fall back to
        // the Python extension's default, then bare "python".
        const explicit_python = config.get("linter.pythonPath");
        const extension_python = vscode.workspace
            .getConfiguration("python")
            .get("defaultInterpreterPath");
        const python_path = explicit_python || extension_python || "python";
        const python_path_source = explicit_python
            ? "explicit"
            : extension_python
              ? "python_extension"
              : "default";
        if (reporter) {
            reporter.sendTelemetryEvent("lsp_python_path_resolved", {
                source: python_path_source,
            });
        }

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

        const ude_paths = config.get("linter.udePaths");
        if (Array.isArray(ude_paths) && ude_paths.length > 0) {
            server_args.push("--ude-paths", ...ude_paths);
        }

        const ude_ignore_paths = config.get("linter.udeIgnorePaths");
        if (Array.isArray(ude_ignore_paths) && ude_ignore_paths.length > 0) {
            server_args.push("--ude-ignore-paths", ...ude_ignore_paths);
        }

        const server_options = {
            command: python_path,
            args: server_args,
            transport: TransportKind.stdio,
        };

        // Create file-system watchers from the same patterns used for scanning.
        // The vscode-languageclient library picks these up and sends
        // workspace/didChangeWatchedFiles notifications to the server automatically.
        _create_macro_watchers(
            Array.isArray(macro_paths) && macro_paths.length > 0 ? macro_paths : ["**/*.mac"],
        );

        const client_options = {
            documentSelector: [{ scheme: "file", language: "adams_cmd" }],
            outputChannel: output_channel,
            // Synchronize settings so the server receives didChangeConfiguration
            // and file-change events are forwarded via the registered watchers.
            synchronize: {
                configurationSection: "msc-adams",
                fileEvents: macro_watchers,
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
                if (reporter) {
                    reporter.sendTelemetryErrorEvent("lsp_start_failed", {
                        error_message: err.message,
                        python_path_source,
                    });
                }
            },
        );

        // Only push to subscriptions on first start so that VS Code properly
        // disposes the client on extension deactivation. Restarted clients are
        // managed manually via stop() and are not pushed again to avoid
        // accumulating stale entries in context.subscriptions.
        if (initial_start) {
            context.subscriptions.push(client);
            initial_start = false;
        }
    }

    function start(context) {
        _start_client(context);

        // Watch for changes to macro-related settings that require a client
        // restart (new CLI args and new file watcher patterns).
        const MACRO_RESTART_KEYS = [
            "msc-adams.linter.macroPaths",
            "msc-adams.linter.macroIgnorePaths",
            "msc-adams.linter.scanWorkspaceMacros",
            "msc-adams.linter.enabled",
            "msc-adams.linter.pythonPath",
        ];
        config_listener = vscode.workspace.onDidChangeConfiguration(function (event) {
            if (MACRO_RESTART_KEYS.some((k) => event.affectsConfiguration(k))) {
                output_channel.appendLine(
                    `[${new Date().toLocaleTimeString()}] Adams CMD linter settings changed — restarting language server`,
                );
                if (reporter) {
                    reporter.sendTelemetryEvent("lsp_restarted", { reason: "config_change" });
                }
                _restart(context);
            }
        });
        context.subscriptions.push(config_listener);
    }

    function stop() {
        macro_watchers.forEach((w) => w.dispose());
        macro_watchers = [];
        if (config_listener) {
            config_listener.dispose();
            config_listener = null;
        }
        if (client) {
            return client.stop();
        }
    }

    return { start: start, stop: stop };
}

exports.cmd_lsp_client = cmd_lsp_client;

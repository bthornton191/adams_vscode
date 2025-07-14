const path = require("path");
const vscode = require("vscode");
const TelemetryReporter = require("@vscode/extension-telemetry").default;
const fs = require("fs");
const { open_in_view } = require("./open_in_view.ts");
const { open_view_here } = require("./open_view_here.ts.js");
const { load_stub_files } = require("./load_stub_files.ts");
const { run_selection } = require("./run_selection.ts.js");
const { debug_in_adams } = require("./debug_in_adams.ts");
const { make_macro_header } = require("./make_macro_header.ts");
const { cmd_completion_provider } = require("./cmd_completion_provider.ts");
const { cmd_hover_provider } = require("./cmd_hover_provider.ts");
const { link_provider } = require("./link_provider.ts.js");
const { add_adams_site_packages } = require("../src/add_adams_site_packages.ts.js");

//Create output channel
const output_channel = vscode.window.createOutputChannel("MSC Adams");

// Connection string for Azure Application Insights
const connectionString =
    "InstrumentationKey=d1f9c873-6ad2-4566-8fe0-d694cda7000e;IngestionEndpoint=https://eastus-8.in.applicationinsights.azure.com/;LiveEndpoint=https://eastus.livediagnostics.monitor.azure.com/;ApplicationId=b993e79b-356a-466c-b53c-e51aa41f496a";

/**
 * Runs the currently selected text in Adams View.
 *
 * @param {vscode.ExtensionContext} context
 */
function activate(context, enableTelemetry = true, skipCommandRegistration = false) {
    // Telemetry
    let reporter = null;
    if (enableTelemetry) {
        reporter = new TelemetryReporter(connectionString);
        context.subscriptions.push(reporter);
    }

    const view_functions = new Map();
    const func_dir = context.asAbsolutePath("resources/adams_design_functions");
    const func_files = fs.readdirSync(func_dir);

    for (var file of func_files) {
        if (fs.lstatSync([func_dir, file].join("/")).isFile()) {
            let text = fs.readFileSync([func_dir, file].join("/"), "utf8");
            let function_name = path.parse(file).name;
            view_functions.set(function_name, text);
        }
    }

    // ---------------------------------------------------------------------------
    // Link Provider
    // ---------------------------------------------------------------------------
    vscode.languages.registerDocumentLinkProvider("adams_cmd", link_provider());
    vscode.languages.registerDocumentLinkProvider("adams_adm", link_provider());
    vscode.languages.registerDocumentLinkProvider("adams_acf", link_provider());
    vscode.languages.registerDocumentLinkProvider("adams_msg", link_provider());
    vscode.languages.registerDocumentLinkProvider("adams_log", link_provider());
    vscode.languages.registerDocumentLinkProvider("adams_to", link_provider());

    // ---------------------------------------------------------------------------
    // Hover Provider
    // ---------------------------------------------------------------------------
    vscode.languages.registerHoverProvider(
        "adams_cmd",
        cmd_hover_provider(view_functions, reporter)
    );

    // ---------------------------------------------------------------------------
    // Completion Provider
    // ---------------------------------------------------------------------------
    const cmd_files_json = context.asAbsolutePath("resources/adams_view_commands/structured.json");
    const view_commands = JSON.parse(fs.readFileSync(cmd_files_json));
    vscode.languages.registerCompletionItemProvider(
        "adams_cmd",
        cmd_completion_provider(view_functions, view_commands, reporter)
    );

    // ---------------------------------------------------------------------------
    // Commands
    // ---------------------------------------------------------------------------
    if (!skipCommandRegistration) {
        context.subscriptions.push(
            vscode.commands.registerCommand(
                "msc_adams.macros.makeHeader",
                make_macro_header(reporter)
            ),
            vscode.commands.registerCommand(
                "msc_adams.openInView",
                open_in_view(context, output_channel, reporter)
            ),
            vscode.commands.registerCommand(
                "msc_adams.openViewHere",
                open_view_here(output_channel, reporter)
            ),
            vscode.commands.registerCommand(
                "msc_adams.debugInAdams",
                debug_in_adams(output_channel, reporter)
            ),
            vscode.commands.registerCommand(
                "msc_adams.runSelection",
                run_selection(output_channel, false, reporter)
            ),
            vscode.commands.registerCommand(
                "msc_adams.runFile",
                run_selection(output_channel, true, reporter)
            ),
            vscode.commands.registerCommand(
                "msc_adams.loadStubFiles",
                load_stub_files(context, output_channel, reporter)
            ),
            vscode.commands.registerCommand(
                "msc_adams.loadAdamsSitePackages",
                add_adams_site_packages(output_channel, reporter)
            )
        );
    }

    // Set to run whenever the loadStubFiles setting is changed
    // vscode.workspace.onDidChangeConfiguration(load_stub_files(context, output_channel));

    if (vscode.workspace.getConfiguration().get("msc-adams.runInAdams.autoLoadAdamspyStubs")) {
        vscode.commands.executeCommand("msc_adams.loadStubFiles");
    }

    // Set to run whenever the adamsLaunchCommand setting is changed
    // Store the event listener so it can be disposed later
    const configChangeListener = vscode.workspace.onDidChangeConfiguration((event) => {
        if (event.affectsConfiguration("msc-adams.adamsLaunchCommand")) {
            const config = vscode.workspace.getConfiguration("msc-adams");
            const adamsLaunchPath = config.get("adamsLaunchCommand");
            const autoLoadEnabled = config.get("runInAdams.autoLoadAdamsSitePackages", true);

            if (adamsLaunchPath && autoLoadEnabled) {
                // Check if the file exists
                try {
                    if (fs.existsSync(adamsLaunchPath)) {
                        vscode.commands.executeCommand("msc_adams.loadAdamsSitePackages");
                    } else {
                        // Log warning if file doesn't exist (but don't break tests)
                        output_channel.appendLine(
                            `[${new Date().toLocaleTimeString()}]: Warning: Adams launch path does not exist: ${adamsLaunchPath}`
                        );
                    }
                } catch (error) {
                    // Log error but don't fail
                    output_channel.appendLine(
                        `[${new Date().toLocaleTimeString()}]: Error checking Adams launch path: ${
                            error.message
                        }`
                    );
                }
            }
        }
    });

    // Add the event listener to subscriptions so it's properly disposed
    context.subscriptions.push(configChangeListener);

    if (
        vscode.workspace.getConfiguration("msc-adams").get("runInAdams.autoLoadAdamsSitePackages")
    ) {
        vscode.commands.executeCommand("msc_adams.loadAdamsSitePackages");
    }

    vscode.window.showInformationMessage("MSC Adams Extension Activated");
    output_channel.appendLine(`[${new Date().toLocaleTimeString()}] MSC Adams Extension Activated`);
    if (enableTelemetry) {
        reporter.sendTelemetryEvent(
            "MSC Adams Extension Activated",
            vscode.workspace.getConfiguration().get("msc-adams")
        );
    }
}

function deactivate(context) {
    vscode.window.showInformationMessage("MSC Adams Extension Deactivated");
}

const command = "msc_adams.activate";
vscode.commands.registerCommand(command, () => {});

module.exports = {
    activate,
    deactivate,
};

const vscode = require("vscode");
const path = require("path");

function add_adams_site_packages(context, output_channel, reporter = null) {
    return async () => {
        if (process.platform !== "win32") {
            return;
        }

        // Get the path to the mdi.bat file
        const mdi_bat = vscode.workspace
            .getConfiguration("msc-adams")
            .get("adamsLaunchCommand", null);

        if (mdi_bat == null) {
            output_channel.appendLine(
                `[${new Date().toLocaleTimeString()}]: mdi.bat not found. Skipping site-packages addition.`
            );
            return;
        }

        const adams_dir = path.dirname(path.dirname(mdi_bat));

        // Get the path to site-packages. This should be adams_dir\python\Lib\site-packages
        const site_packages = path.join(adams_dir, "python", "win64", "Lib", "site-packages");

        // Get the current extra paths
        var extra_paths = vscode.workspace
            .getConfiguration("python")
            .get("analysis.extraPaths", null);

        // Get the current autocomplete paths
        var autocomp_paths = vscode.workspace
            .getConfiguration("python")
            .get("autoComplete.extraPaths", null);

        // =========================================================================================
        // If the site-packages directory is not already in the analysis.extraPaths, add it
        // =========================================================================================
        if (!extra_paths.includes(site_packages)) {
            extra_paths.push(site_packages);
            output_channel.appendLine(
                `[${new Date().toLocaleTimeString()}]: Adding "${site_packages}" to python.analysis.extraPaths`
            );
            reporter.sendTelemetryEvent("add_adams_site_packages_to_extraPaths", {
                path: site_packages,
                config: "analysis.extraPaths",
            });
        }

        if (vscode.workspace.workspaceFolders == undefined) {
            vscode.workspace
                .getConfiguration("python")
                .update("analysis.extraPaths", extra_paths, true);
        } else {
            vscode.workspace
                .getConfiguration("python")
                .update("analysis.extraPaths", extra_paths, null);
        }

        // =========================================================================================
        // If the stub directory is not already in the autoComplete.extra paths, add it
        // =========================================================================================
        if (!autocomp_paths.includes(site_packages)) {
            autocomp_paths.push(site_packages);
            output_channel.appendLine(
                `[${new Date().toLocaleTimeString()}]: Adding "${site_packages}" to python.autoComplete.extraPaths`
            );
            reporter.sendTelemetryEvent("add_adams_site_packages_to_autoComplete", {
                path: site_packages,
                config: "analysis.autoComplete.extraPaths",
            });
        }
        if (vscode.workspace.workspaceFolders == undefined) {
            vscode.workspace
                .getConfiguration("python")
                .update("autoComplete.extraPaths", autocomp_paths, true);
        } else {
            vscode.workspace
                .getConfiguration("python")
                .update("autoComplete.extraPaths", autocomp_paths, null);
        }
    };
}
exports.add_adams_site_packages = add_adams_site_packages;

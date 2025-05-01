const vscode = require("vscode");
const path = require("path");
const fs = require("fs");

function add_adams_site_packages(output_channel, reporter = null) {
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
                `[${new Date().toLocaleTimeString()}]: adamsLaunchCommand not set. Skipping site-packages addition.`
            );
            return;
        }

        if (!fs.existsSync(mdi_bat)) {
            output_channel.appendLine(
                `[${new Date().toLocaleTimeString()}]: adamsLaunchCommand set to ${mdi_bat}, but this path does not exist. Skipping site-packages addition.`
            );
            return;
        }

        const adams_dir = path.dirname(path.dirname(mdi_bat));

        // Get the path to site-packages. This should be adams_dir\python\Lib\site-packages
        const site_packages = path.join(adams_dir, "python", "win64", "Lib", "site-packages");

        // Get the current extra paths
        const extra_paths = vscode.workspace
            .getConfiguration("python")
            .get("analysis.extraPaths", null);

        // Get the current autocomplete paths
        const autocomp_paths = vscode.workspace
            .getConfiguration("python")
            .get("autoComplete.extraPaths", null);

        // Check to see if the site-packages directory exists for a *different* version of Adams
        // If it does, remove it.
        const adamsParentDir = path.dirname(adams_dir);

        // A regex to match `adams_dir\*\python\Lib\site-packages` where * is any version number
        // Let's assume that version numbers are any combination of digits and underscores
        const sitePackagesRegex = new RegExp(
            `${adamsParentDir.replace(/\\/g, '\\\\')}[\\\\/][\\d_]+[\\\\/]python[\\\\/]win64[\\\\/]Lib[\\\\/]site-packages`
        );

        // =========================================================================================
        // If the site-packages directory is not already in the analysis.extraPaths, add it
        // =========================================================================================

        // Remove any existing site-packages paths that match the regex from the extra paths
        let extraPathsToRemove = extra_paths.filter((path) => sitePackagesRegex.test(path));

        // Remove the site-packages directory that we actually want from `extraPathsToRemove`
        extraPathsToRemove = extraPathsToRemove.filter((path) => path !== site_packages);

        // Remove the paths from the extra paths
        var new_extra_paths = extra_paths.filter((path) => !extraPathsToRemove.includes(path));

        // Add the site-packages path to the extra paths if it is not already there
        if (!new_extra_paths.includes(site_packages)) {
            output_channel.appendLine(
                `[${new Date().toLocaleTimeString()}]: Adding "${site_packages}" to python.analysis.extraPaths`
            );
            if (reporter) {
                reporter.sendTelemetryEvent("add_adams_site_packages_to_extraPaths", {
                    path: site_packages,
                    config: "python.analysis.extraPaths",
                });
            }

            // Update the analysis.extraPaths setting
            new_extra_paths.push(site_packages);
        }

        if (new_extra_paths !== extra_paths) {
            await vscode.workspace
                .getConfiguration("python")
                .update(
                    "analysis.extraPaths",
                    new_extra_paths,
                    vscode.workspace.workspaceFolders === undefined ? true : null
                );
        }

        // =========================================================================================
        // If the site-packages directory is not already in the autoComplete.extra paths, add it
        // =========================================================================================

        // Remove any existing site-packages paths that match the regex from the autocomplete paths
        let autocompPathsToRemove = autocomp_paths.filter((path) => sitePackagesRegex.test(path));

        // Remove the site-packages that we actually want from `autocompPathsToRemove`
        autocompPathsToRemove = autocompPathsToRemove.filter((path) => path !== site_packages);

        // Remove the paths from the autocomp paths
        var new_autocomp_paths = autocomp_paths.filter(
            (path) => !autocompPathsToRemove.includes(path)
        );

        if (!new_autocomp_paths.includes(site_packages)) {
            output_channel.appendLine(
                `[${new Date().toLocaleTimeString()}]: Adding "${site_packages}" to python.autoComplete.extraPaths`
            );
            if (reporter) {
                reporter.sendTelemetryEvent("add_adams_site_packages_to_autoComplete", {
                    path: site_packages,
                    config: "python.autoComplete.extraPaths",
                });
            }

            // Update the autoComplete.extraPaths setting
            new_autocomp_paths.push(site_packages);
        }

        if (new_autocomp_paths != autocomp_paths) {
            await vscode.workspace
                .getConfiguration("python")
                .update(
                    "autoComplete.extraPaths",
                    new_autocomp_paths,
                    vscode.workspace.workspaceFolders === undefined ? true : null
                );
        }
    };
}
exports.add_adams_site_packages = add_adams_site_packages;

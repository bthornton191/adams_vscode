// .vscode-test.js
const { defineConfig } = require("@vscode/test-cli");
const { getLatestAdamsVersions } = require("./test/utils.js");
const path = require("path");

const adamsVersionDir = path.dirname(path.dirname(path.dirname(process.env.ADAMS_LAUNCH_COMMAND)));
const adamsLaunchCommands = [
    path.join(adamsVersionDir, "2023_2", "common", "mdi.bat"),
    path.join(adamsVersionDir, "2022_4_904865", "common", "mdi.bat"),
];
module.exports = defineConfig(
    adamsLaunchCommands.map((adamsLaunchCommand) => {
        return {
            files: "test/**/*.test.js",
            workspaceFolder: "test",
            env: {
                _ADAMS_LAUNCH_COMMAND: adamsLaunchCommand,
            },
            label: path.basename(path.dirname(path.dirname(adamsLaunchCommand))),
            mocha: {
                timeout: 300000,
                require: path.join(__dirname, "test", "global_fixture.cjs"),
            },
        };
    })
);

// BUG: Tries to run both versions of Adams in parallel

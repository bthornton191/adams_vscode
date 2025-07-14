// .vscode-test.js
const { defineConfig } = require("@vscode/test-cli");
const { getLatestAdamsVersions } = require("./test/utils.js");
const path = require("path");

const adamsLaunchCommand = getLatestAdamsVersions();
module.exports = defineConfig({
    files: "test/**/*.test.js",
    workspaceFolder: "test",
    env: {
        _ADAMS_LAUNCH_COMMAND: adamsLaunchCommand,
    },
    label: path.basename(path.dirname(path.dirname(adamsLaunchCommand))),
    mocha: {
        timeout: 300000,
        require: path.join(__dirname, "test", "global_fixture.cjs"),
        fullTrace: true,
    },
});

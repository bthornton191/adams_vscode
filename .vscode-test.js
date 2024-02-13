// .vscode-test.js
const { defineConfig } = require('@vscode/test-cli');

module.exports = defineConfig({
    files: 'test/**/*.test.js',
    workspaceFolder: 'test',
    mocha: {
        timeout: 60000,
    }
});
 
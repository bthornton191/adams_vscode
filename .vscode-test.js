// .vscode-test.js
const { defineConfig } = require('@vscode/test-cli');
const path = require('path');
module.exports = defineConfig({
    files: 'test/**/*.test.js',
    workspaceFolder: 'test',
    mocha: {
        timeout: 60000,
        require: path.join(__dirname, 'test', 'global_fixture.cjs'),
        preload: path.join(__dirname, 'test', 'global_fixture.cjs'),
    },

});

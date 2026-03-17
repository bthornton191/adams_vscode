const assert = require("assert");
const vscode = require("vscode");
const { make_macro_header } = require("../src/make_macro_header.ts.js");

function makeMockReporter() {
    const calls = { telemetry: [] };
    return {
        sendTelemetryEvent: (...args) => calls.telemetry.push(args),
        calls,
    };
}

suite("make_macro_header", () => {
    let originalExecuteCommand;
    let executedCommands;

    suiteSetup(() => {
        originalExecuteCommand = vscode.commands.executeCommand;
    });

    setup(() => {
        executedCommands = [];
        vscode.commands.executeCommand = (command, ...args) => {
            executedCommands.push({ command, args });
            return Promise.resolve();
        };
    });

    teardown(() => {
        vscode.commands.executeCommand = originalExecuteCommand;
    });

    test("should not crash when reporter is null", () => {
        assert.doesNotThrow(() => {
            make_macro_header(null)();
        });
    });

    test("should send telemetry when reporter is provided", () => {
        const reporter = makeMockReporter();

        make_macro_header(reporter)();

        assert.strictEqual(reporter.calls.telemetry.length, 1);
        assert.strictEqual(reporter.calls.telemetry[0][0], "make_macro_header");
    });

    test("should call executeCommand to insert snippet", () => {
        make_macro_header(null)();

        const insertSnippetCall = executedCommands.find(
            (c) => c.command === "editor.action.insertSnippet"
        );
        assert.ok(insertSnippetCall, "Expected editor.action.insertSnippet to be called");
        assert.strictEqual(insertSnippetCall.args[0].name, "Macro Header");
    });
});

const assert = require("assert");
const vscode = require("vscode");
const { cmd_hover_provider } = require("../src/cmd_hover_provider.ts.js");

function makeMockReporter() {
    const calls = { telemetry: [] };
    return {
        sendTelemetryEvent: (...args) => calls.telemetry.push(args),
        calls,
    };
}

function makeDocument(word, rangeUndefined = false) {
    const range = rangeUndefined ? undefined : { start: { line: 0, character: 0 } };
    return {
        getWordRangeAtPosition: () => range,
        getText: () => word,
    };
}

const position = new vscode.Position(0, 0);

suite("cmd_hover_provider", () => {
    test("should return a Hover when word is in view_functions", () => {
        const view_functions = new Map([["abs", "**abs**(x) — returns absolute value"]]);
        const provider = cmd_hover_provider(view_functions, null);

        const result = provider.provideHover(makeDocument("abs"), position, null);

        assert.ok(result instanceof vscode.Hover, "Expected a vscode.Hover instance");
    });

    test("should return undefined when word is not in view_functions", () => {
        const view_functions = new Map([["abs", "**abs**(x)"]]);
        const provider = cmd_hover_provider(view_functions, null);

        const result = provider.provideHover(makeDocument("unknownfunc"), position, null);

        assert.strictEqual(result, undefined);
    });

    test("should not crash when getWordRangeAtPosition returns undefined", () => {
        const view_functions = new Map([["abs", "**abs**(x)"]]);
        const provider = cmd_hover_provider(view_functions, null);

        // Cursor is at whitespace — range is undefined
        assert.doesNotThrow(() => {
            provider.provideHover(makeDocument("", true), position, null);
        });
    });

    test("should send telemetry when reporter is provided and word matches", () => {
        const view_functions = new Map([["abs", "**abs**(x)"]]);
        const reporter = makeMockReporter();
        const provider = cmd_hover_provider(view_functions, reporter);

        provider.provideHover(makeDocument("abs"), position, null);

        assert.strictEqual(reporter.calls.telemetry.length, 1);
        assert.strictEqual(reporter.calls.telemetry[0][0], "cmd_hover_provider");
        assert.strictEqual(reporter.calls.telemetry[0][1].word, "abs");
    });

    test("should not send telemetry when word does not match", () => {
        const view_functions = new Map([["abs", "**abs**(x)"]]);
        const reporter = makeMockReporter();
        const provider = cmd_hover_provider(view_functions, reporter);

        provider.provideHover(makeDocument("unknownfunc"), position, null);

        assert.strictEqual(reporter.calls.telemetry.length, 0);
    });

    test("should not crash when reporter is null and word matches", () => {
        const view_functions = new Map([["abs", "**abs**(x)"]]);
        const provider = cmd_hover_provider(view_functions, null);

        assert.doesNotThrow(() => {
            provider.provideHover(makeDocument("abs"), position, null);
        });
    });
});

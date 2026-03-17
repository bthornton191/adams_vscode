const assert = require("assert");
const vscode = require("vscode");
const { cmd_completion_provider } = require("../src/cmd_completion_provider.ts.js");

function makeMockReporter() {
    const calls = { telemetry: [] };
    return {
        sendTelemetryEvent: (...args) => calls.telemetry.push(args),
        calls,
    };
}

function makeDocument(word, lineText, rangeUndefined = false) {
    const range = rangeUndefined ? undefined : {};
    return {
        getWordRangeAtPosition: () => range,
        getText: () => word,
        lineAt: () => ({ text: lineText }),
    };
}

const position = new vscode.Position(0, 5);

suite("cmd_completion_provider", () => {
    test("should return function completions matching the typed word", () => {
        const function_names = new Map([
            ["abs", "abs doc"],
            ["acos", "acos doc"],
            ["sin", "sin doc"],
        ]);
        const commands = {};
        const provider = cmd_completion_provider(function_names, commands, null);

        const doc = makeDocument("a", "a");
        const completions = provider.provideCompletionItems(doc, position, null, {});

        const labels = completions.map((c) => c.label);
        assert.ok(labels.includes("abs"), "Expected 'abs' in completions");
        assert.ok(labels.includes("acos"), "Expected 'acos' in completions");
        assert.ok(!labels.includes("sin"), "'sin' should not match prefix 'a'");
    });

    test("should return argument completions when line exactly matches a command", () => {
        const function_names = new Map();
        const commands = { "model create": ["model_name", "type"] };
        const provider = cmd_completion_provider(function_names, commands, null);

        // Line exactly matches the command key (after stripping existing args)
        const doc = makeDocument("", "model create");
        const completions = provider.provideCompletionItems(doc, position, null, {});

        const labels = completions.map((c) => c.label);
        assert.ok(
            labels.some((l) => l.includes("model_name")),
            "Expected argument completion for 'model_name'"
        );
    });

    test("should return command word completions for partial command input", () => {
        const function_names = new Map();
        const commands = { "model create": [], "model delete": [] };
        const provider = cmd_completion_provider(function_names, commands, null);

        // Typing "model" — should get "create" and "delete" as next-word completions
        const doc = makeDocument("model", "model");
        const completions = provider.provideCompletionItems(doc, position, null, {});

        const labels = completions.map((c) => c.label);
        assert.ok(labels.some((l) => l.trim() === "create"), "Expected 'create' completion");
        assert.ok(labels.some((l) => l.trim() === "delete"), "Expected 'delete' completion");
    });

    test("should not crash when getWordRangeAtPosition returns undefined", () => {
        const function_names = new Map([["abs", "abs doc"]]);
        const commands = {};
        const provider = cmd_completion_provider(function_names, commands, null);

        const doc = makeDocument("", "  ", true); // whitespace position
        assert.doesNotThrow(() => {
            provider.provideCompletionItems(doc, position, null, {});
        });
    });

    test("should send telemetry when reporter is provided", () => {
        const function_names = new Map([["abs", "abs doc"]]);
        const commands = {};
        const reporter = makeMockReporter();
        const provider = cmd_completion_provider(function_names, commands, reporter);

        const doc = makeDocument("a", "a");
        provider.provideCompletionItems(doc, position, null, {});

        assert.strictEqual(reporter.calls.telemetry.length, 1);
        assert.strictEqual(reporter.calls.telemetry[0][0], "cmd_completion_provider");
    });

    test("should not crash when reporter is null", () => {
        const function_names = new Map([["abs", "abs doc"]]);
        const commands = {};
        const provider = cmd_completion_provider(function_names, commands, null);

        const doc = makeDocument("a", "a");
        assert.doesNotThrow(() => {
            provider.provideCompletionItems(doc, position, null, {});
        });
    });
});

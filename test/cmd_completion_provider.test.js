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

function makeDocument(word, lines, rangeUndefined = false) {
    const lineArray = Array.isArray(lines) ? lines : [lines];
    const range = rangeUndefined ? undefined : {};
    return {
        getWordRangeAtPosition: () => range,
        getText: () => word,
        lineAt: (lineOrPosition) => {
            const n = typeof lineOrPosition === "number" ? lineOrPosition : lineOrPosition.line;
            return { text: lineArray[n] !== undefined ? lineArray[n] : "" };
        },
        lineCount: lineArray.length,
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
        const provider = cmd_completion_provider(function_names, commands);

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
        const provider = cmd_completion_provider(function_names, commands);

        // Line exactly matches the command key (after stripping existing args)
        // Position must be at end of "model create" so line.substr(0, character) equals the full command
        const localPosition = new vscode.Position(0, 12);
        const doc = makeDocument("", "model create");
        const completions = provider.provideCompletionItems(doc, localPosition, null, {});

        const labels = completions.map((c) => c.label);
        assert.ok(
            labels.some((l) => l.includes("model_name")),
            "Expected argument completion for 'model_name'",
        );
    });

    test("should return command word completions for partial command input", () => {
        const function_names = new Map();
        const commands = { "model create": [], "model delete": [] };
        const provider = cmd_completion_provider(function_names, commands);

        // Typing "model " (with trailing space) — idx=2, so command.split(' ')[1] = "create"/"delete"
        const localPosition = new vscode.Position(0, 6);
        const doc = makeDocument("", "model ");
        const completions = provider.provideCompletionItems(doc, localPosition, null, {});

        const labels = completions.map((c) => c.label);
        assert.ok(
            labels.some((l) => l.trim() === "create"),
            "Expected 'create' completion",
        );
        assert.ok(
            labels.some((l) => l.trim() === "delete"),
            "Expected 'delete' completion",
        );
    });

    test("should not crash when getWordRangeAtPosition returns undefined", () => {
        const function_names = new Map([["abs", "abs doc"]]);
        const commands = {};
        const provider = cmd_completion_provider(function_names, commands);

        const doc = makeDocument("", "  ", true); // whitespace position
        assert.doesNotThrow(() => {
            provider.provideCompletionItems(doc, position, null, {});
        });
    });

    test("should send telemetry when reporter is provided", () => {
        const function_names = new Map([["abs", "abs doc"]]);
        const commands = {};
        const reporter = makeMockReporter();
        const provider = cmd_completion_provider(function_names, commands, {}, new Map(), reporter);

        const doc = makeDocument("a", "a");
        provider.provideCompletionItems(doc, position, null, {});

        assert.strictEqual(reporter.calls.telemetry.length, 1);
        assert.strictEqual(reporter.calls.telemetry[0][0], "cmd_completion_provider");
    });

    test("should not crash when reporter is null", () => {
        const function_names = new Map([["abs", "abs doc"]]);
        const commands = {};
        const provider = cmd_completion_provider(function_names, commands);

        const doc = makeDocument("a", "a");
        assert.doesNotThrow(() => {
            provider.provideCompletionItems(doc, position, null, {});
        });
    });

    test("should not suggest already-used arguments", () => {
        const function_names = new Map();
        const commands = { "model create": ["model_name", "type", "comments"] };
        const provider = cmd_completion_provider(function_names, commands);

        const lineText = "model create model_name=mymodel";
        const localPosition = new vscode.Position(0, lineText.length);
        const doc = makeDocument("", lineText);
        const completions = provider.provideCompletionItems(doc, localPosition, null, {});

        const labels = completions.map((c) => c.label);
        assert.ok(
            !labels.some((l) => l.includes("model_name")),
            "'model_name' should be excluded (already used)",
        );
        assert.ok(
            labels.some((l) => l.includes("type")),
            "Expected 'type' completion",
        );
        assert.ok(
            labels.some((l) => l.includes("comments")),
            "Expected 'comments' completion",
        );
    });

    test("should return argument completions on a continuation line", () => {
        const function_names = new Map();
        const commands = { "model create": ["model_name", "type", "comments"] };
        const provider = cmd_completion_provider(function_names, commands);

        const lines = ["model create &", "  "];
        const localPosition = new vscode.Position(1, lines[1].length);
        const doc = makeDocument("", lines);
        const completions = provider.provideCompletionItems(doc, localPosition, null, {});

        const labels = completions.map((c) => c.label);
        assert.ok(
            labels.some((l) => l.includes("model_name")),
            "Expected 'model_name' on continuation line",
        );
        assert.ok(
            labels.some((l) => l.includes("type")),
            "Expected 'type' on continuation line",
        );
    });

    test("should not suggest args already used on a previous continuation line", () => {
        const function_names = new Map();
        const commands = { "model create": ["model_name", "type", "comments"] };
        const provider = cmd_completion_provider(function_names, commands);

        const lines = ["model create model_name=mymodel &", "  "];
        const localPosition = new vscode.Position(1, lines[1].length);
        const doc = makeDocument("", lines);
        const completions = provider.provideCompletionItems(doc, localPosition, null, {});

        const labels = completions.map((c) => c.label);
        assert.ok(
            !labels.some((l) => l.includes("model_name")),
            "'model_name' should be excluded (used on previous line)",
        );
        assert.ok(
            labels.some((l) => l.includes("type")),
            "Expected 'type' completion",
        );
        assert.ok(
            labels.some((l) => l.includes("comments")),
            "Expected 'comments' completion",
        );
    });

    test("should not suggest command words on a continuation line", () => {
        const function_names = new Map();
        const commands = { "model create": [], "model delete": [] };
        const provider = cmd_completion_provider(function_names, commands);

        const lines = ["model &", "  "];
        const localPosition = new vscode.Position(1, lines[1].length);
        const doc = makeDocument("", lines);
        const completions = provider.provideCompletionItems(doc, localPosition, null, {});

        const labels = completions.map((c) => c.label);
        assert.ok(
            !labels.some((l) => l.trim() === "create"),
            "Should not suggest 'create' on continuation line",
        );
        assert.ok(
            !labels.some((l) => l.trim() === "delete"),
            "Should not suggest 'delete' on continuation line",
        );
    });

    test("should handle multi-level continuation lines", () => {
        const function_names = new Map();
        const commands = { "model create": ["model_name", "type", "comments", "title"] };
        const provider = cmd_completion_provider(function_names, commands);

        const lines = ["model create model_name=mymodel &", "  type=geometric &", "  "];
        const localPosition = new vscode.Position(2, lines[2].length);
        const doc = makeDocument("", lines);
        const completions = provider.provideCompletionItems(doc, localPosition, null, {});

        const labels = completions.map((c) => c.label);
        assert.ok(!labels.some((l) => l.includes("model_name")), "'model_name' should be excluded");
        assert.ok(!labels.some((l) => l.includes("type")), "'type' should be excluded");
        assert.ok(
            labels.some((l) => l.includes("comments")),
            "Expected 'comments'",
        );
        assert.ok(
            labels.some((l) => l.includes("title")),
            "Expected 'title'",
        );
    });

    test("should return argument value completions after arg=", () => {
        const function_names = new Map();
        const commands = { "model create": ["model_name", "fit_to_view"] };
        const arg_options = { "model create": { fit_to_view: ["yes", "no"] } };
        const provider = cmd_completion_provider(function_names, commands, arg_options);

        const lineText = "model create fit_to_view=";
        const localPosition = new vscode.Position(0, lineText.length);
        const doc = makeDocument("", lineText);
        const completions = provider.provideCompletionItems(doc, localPosition, null, {});

        const labels = completions.map((c) => c.label);
        assert.ok(labels.includes("yes"), "Expected 'yes' value completion");
        assert.ok(labels.includes("no"), "Expected 'no' value completion");
    });

    test("should filter argument value completions by partial input", () => {
        const function_names = new Map();
        const commands = { "simulation single_run transient": ["type", "initial_static"] };
        const arg_options = {
            "simulation single_run transient": {
                type: ["dynamic", "kinematic", "static", "auto_select"],
            },
        };
        const provider = cmd_completion_provider(function_names, commands, arg_options);

        const lineText = "simulation single_run transient type=dy";
        const localPosition = new vscode.Position(0, lineText.length);
        const doc = makeDocument("", lineText);
        const completions = provider.provideCompletionItems(doc, localPosition, null, {});

        const labels = completions.map((c) => c.label);
        assert.ok(labels.includes("dynamic"), "Expected 'dynamic'");
        assert.ok(!labels.includes("kinematic"), "'kinematic' should not match 'dy'");
        assert.ok(!labels.includes("static"), "'static' should not match 'dy'");
    });
});

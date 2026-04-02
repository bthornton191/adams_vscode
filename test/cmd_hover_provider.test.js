const assert = require("assert");
const vscode = require("vscode");
const { cmd_hover_provider } = require("../src/cmd_hover_provider.ts.js");

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function makeMockReporter() {
    const calls = { telemetry: [] };
    return {
        sendTelemetryEvent: (...args) => calls.telemetry.push(args),
        calls,
    };
}

/**
 * Builds a mock document with multiple lines.
 * lineAt accepts both a number and a Position-like object {line}.
 */
function makeDocument(lines, hoveredWord, rangeUndefined = false) {
    const lineArray = Array.isArray(lines) ? lines : [lines];
    const range = rangeUndefined ? undefined : { start: { line: 0, character: 0 } };
    return {
        getWordRangeAtPosition: () => range,
        getText: () => hoveredWord,
        lineAt: (arg) => {
            const ln = typeof arg === "number" ? arg : arg.line;
            return { text: lineArray[ln] !== undefined ? lineArray[ln] : "" };
        },
    };
}

const pos0 = new vscode.Position(0, 0);
const pos1 = new vscode.Position(1, 0);

// ---------------------------------------------------------------------------
// Shared fixtures
// ---------------------------------------------------------------------------

const VIEW_COMMANDS = {
    "marker create": ["marker_name", "location"],
    "view center": ["view_name", "screen_coords"],
    "simulation single_run transient": ["end_time", "steps"],
};
const COMMAND_DOCS = new Map([
    ["marker create", "# marker create\nCreates a marker."],
    ["view center", "# view center\nCenters the view."],
    [
        "simulation single_run transient",
        "# simulation single_run transient\nRuns transient simulation.",
    ],
]);

// ---------------------------------------------------------------------------
// Function hover tests
// ---------------------------------------------------------------------------

suite("cmd_hover_provider — function hover", () => {
    test("returns Hover when word is a design function", () => {
        const view_functions = new Map([["abs", "**abs**(x)"]]);
        const provider = cmd_hover_provider(view_functions, {}, new Map(), null);

        const result = provider.provideHover(makeDocument("abs", "abs"), pos0, null);

        assert.ok(result instanceof vscode.Hover);
    });

    test("returns undefined when word is not a function and no command context", () => {
        const view_functions = new Map([["abs", "**abs**(x)"]]);
        const provider = cmd_hover_provider(view_functions, {}, new Map(), null);

        const result = provider.provideHover(makeDocument("abs", "unknownfunc"), pos0, null);

        assert.strictEqual(result, undefined);
    });

    test("returns undefined when range is undefined (cursor at whitespace)", () => {
        const view_functions = new Map([["abs", "**abs**(x)"]]);
        const provider = cmd_hover_provider(view_functions, {}, new Map(), null);

        const result = provider.provideHover(makeDocument("", "", true), pos0, null);

        assert.strictEqual(result, undefined);
    });

    test("does not crash when reporter is null and word matches", () => {
        const view_functions = new Map([["abs", "**abs**(x)"]]);
        const provider = cmd_hover_provider(view_functions, {}, new Map(), null);

        assert.doesNotThrow(() => {
            provider.provideHover(makeDocument("abs", "abs"), pos0, null);
        });
    });

    test("sends telemetry with type=function when word is a design function", () => {
        const view_functions = new Map([["abs", "**abs**(x)"]]);
        const reporter = makeMockReporter();
        const provider = cmd_hover_provider(view_functions, {}, new Map(), reporter);

        provider.provideHover(makeDocument("abs", "abs"), pos0, null);

        assert.strictEqual(reporter.calls.telemetry.length, 1);
        assert.strictEqual(reporter.calls.telemetry[0][0], "cmd_hover_provider");
        assert.strictEqual(reporter.calls.telemetry[0][1].word, "abs");
        assert.strictEqual(reporter.calls.telemetry[0][1].type, "function");
    });

    test("does not send telemetry when word does not match", () => {
        const view_functions = new Map([["abs", "**abs**(x)"]]);
        const reporter = makeMockReporter();
        const provider = cmd_hover_provider(view_functions, {}, new Map(), reporter);

        provider.provideHover(makeDocument("noop", "noop"), pos0, null);

        assert.strictEqual(reporter.calls.telemetry.length, 0);
    });
});

// ---------------------------------------------------------------------------
// Command hover tests
// ---------------------------------------------------------------------------

suite("cmd_hover_provider — command hover", () => {
    test("returns command Hover when word is last keyword of a multi-word command", () => {
        const provider = cmd_hover_provider(new Map(), VIEW_COMMANDS, COMMAND_DOCS, null);

        // "marker create marker_name=.model.m1" — hover "create"
        const doc = makeDocument("marker create marker_name=.model.m1", "create");
        const result = provider.provideHover(doc, pos0, null);

        assert.ok(result instanceof vscode.Hover);
        assert.ok(result.contents[0].value.includes("marker create"));
    });

    test("returns command Hover when hovering the first keyword of a multi-word command", () => {
        const provider = cmd_hover_provider(new Map(), VIEW_COMMANDS, COMMAND_DOCS, null);

        // "marker create" — hover "marker"
        const doc = makeDocument("marker create", "marker");
        const result = provider.provideHover(doc, pos0, null);

        assert.ok(result instanceof vscode.Hover);
        assert.ok(result.contents[0].value.includes("marker create"));
    });

    test("resolves deeply nested 3-word command key", () => {
        const provider = cmd_hover_provider(new Map(), VIEW_COMMANDS, COMMAND_DOCS, null);

        const doc = makeDocument("simulation single_run transient end_time=5.0", "transient");
        const result = provider.provideHover(doc, pos0, null);

        assert.ok(result instanceof vscode.Hover);
        assert.ok(result.contents[0].value.includes("simulation single_run transient"));
    });

    test("clash: returns command Hover (not function) for 'center' in 'view center'", () => {
        const view_functions = new Map([["center", "# CENTER\nNon-statistical mean."]]);
        const provider = cmd_hover_provider(view_functions, VIEW_COMMANDS, COMMAND_DOCS, null);

        const doc = makeDocument("view center view_name=front", "center");
        const result = provider.provideHover(doc, pos0, null);

        assert.ok(result instanceof vscode.Hover);
        assert.ok(result.contents[0].value.includes("view center"), "Should show command doc");
        assert.ok(
            !result.contents[0].value.includes("non-statistical"),
            "Should NOT show function doc",
        );
    });

    test("function fallback: 'center' outside a command context returns function Hover", () => {
        const view_functions = new Map([["center", "# CENTER\nNon-statistical mean."]]);
        const provider = cmd_hover_provider(view_functions, VIEW_COMMANDS, COMMAND_DOCS, null);

        // Standalone expression (e.g. variable = center(arr)) — not a recognized command context
        const doc = makeDocument("x = center(arr)", "center");
        const result = provider.provideHover(doc, pos0, null);

        assert.ok(result instanceof vscode.Hover);
        assert.ok(result.contents[0].value.toLowerCase().includes("center"));
    });

    test("returns undefined for argument name (not part of command key)", () => {
        const provider = cmd_hover_provider(new Map(), VIEW_COMMANDS, COMMAND_DOCS, null);

        // "marker_name" is an argument, not part of the command key
        const doc = makeDocument("marker create marker_name=foo", "marker_name");
        const result = provider.provideHover(doc, pos0, null);

        assert.strictEqual(result, undefined);
    });

    test("returns undefined when command is recognised but has no doc file", () => {
        const commands = { "marker create": ["marker_name"] };
        const provider = cmd_hover_provider(new Map(), commands, new Map(), null); // empty command_docs

        const doc = makeDocument("marker create", "create");
        const result = provider.provideHover(doc, pos0, null);

        assert.strictEqual(result, undefined);
    });

    test("continuation lines: resolves command key across & lines", () => {
        const provider = cmd_hover_provider(new Map(), VIEW_COMMANDS, COMMAND_DOCS, null);

        // Line 0: "marker create &"  (continuation)
        // Line 1: "    marker_name=foo"  ← cursor here, hovering "marker_name"
        // The command key "marker create" is still resolved via backward walk,
        // but "marker_name" is not in the key words → undefined.
        const doc = makeDocument(["marker create &", "    marker_name=foo"], "marker_name");
        const result = provider.provideHover(doc, pos1, null);

        assert.strictEqual(result, undefined);
    });

    test("continuation lines: hovering command keyword on first line works", () => {
        const provider = cmd_hover_provider(new Map(), VIEW_COMMANDS, COMMAND_DOCS, null);

        // Line 0: "marker create &"  ← cursor here, hovering "create"
        const doc = makeDocument(["marker create &", "    marker_name=foo"], "create");
        const result = provider.provideHover(doc, pos0, null);

        assert.ok(result instanceof vscode.Hover);
        assert.ok(result.contents[0].value.includes("marker create"));
    });

    test("sends telemetry with type=command and matched key", () => {
        const reporter = makeMockReporter();
        const provider = cmd_hover_provider(new Map(), VIEW_COMMANDS, COMMAND_DOCS, reporter);

        const doc = makeDocument("marker create", "create");
        provider.provideHover(doc, pos0, null);

        assert.strictEqual(reporter.calls.telemetry.length, 1);
        assert.strictEqual(reporter.calls.telemetry[0][0], "cmd_hover_provider");
        assert.strictEqual(reporter.calls.telemetry[0][1].word, "marker create");
        assert.strictEqual(reporter.calls.telemetry[0][1].type, "command");
    });
});

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
    ["variable set", "# variable set\nSets a variable."],
]);

/**
 * Minimal command_tree fixture that mirrors the real schema structure.
 * Mirrors the entries in VIEW_COMMANDS plus variable set for abbreviation tests.
 *
 * min_prefix values chosen to match the real command_schema.json:
 *   variable → min_prefix 2  ("va..." unambiguous among siblings here)
 *   set      → min_prefix 2  ("se..." needed to avoid ambiguity)
 *   marker   → min_prefix 2
 *   create   → min_prefix 2
 *   view     → min_prefix 1  ("v" is unique in this fixture)
 *   center   → min_prefix 2
 *   simulation → min_prefix 2
 *   single_run → min_prefix 2
 *   transient  → min_prefix 2
 */
const COMMAND_TREE = {
    children: {
        marker: {
            min_prefix: 2,
            children: {
                create: { min_prefix: 2, children: {}, is_leaf: true },
            },
        },
        view: {
            min_prefix: 1,
            children: {
                center: { min_prefix: 2, children: {}, is_leaf: true },
            },
        },
        simulation: {
            min_prefix: 2,
            children: {
                single_run: {
                    min_prefix: 2,
                    children: {
                        transient: { min_prefix: 2, children: {}, is_leaf: true },
                    },
                },
            },
        },
        variable: {
            min_prefix: 2,
            children: {
                set: { min_prefix: 2, children: {}, is_leaf: true },
            },
        },
    },
};

// schema_commands mirrors the commands the tree can resolve
const SCHEMA_COMMANDS = {
    "marker create": {},
    "view center": {},
    "simulation single_run transient": {},
    "variable set": {},
};

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

    test("sends cmd_hover_miss telemetry when word does not match", () => {
        const view_functions = new Map([["abs", "**abs**(x)"]]);
        const reporter = makeMockReporter();
        const provider = cmd_hover_provider(view_functions, {}, new Map(), reporter);

        provider.provideHover(makeDocument("noop", "noop"), pos0, null);

        assert.strictEqual(reporter.calls.telemetry.length, 1);
        assert.strictEqual(reporter.calls.telemetry[0][0], "cmd_hover_miss");
        assert.strictEqual(reporter.calls.telemetry[0][1].word, "noop");
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

// ---------------------------------------------------------------------------
// Abbreviation-aware command hover tests (uses command_tree)
// ---------------------------------------------------------------------------

suite("cmd_hover_provider — abbreviation resolution", () => {
    function makeProvider() {
        return cmd_hover_provider(
            new Map(),
            VIEW_COMMANDS,
            COMMAND_DOCS,
            null,
            COMMAND_TREE,
            SCHEMA_COMMANDS,
        );
    }

    test("abbreviated first token resolves: 'mar create' → 'marker create'", () => {
        const provider = makeProvider();
        const doc = makeDocument("mar create marker_name=foo", "create");
        const result = provider.provideHover(doc, pos0, null);

        assert.ok(result instanceof vscode.Hover);
        assert.ok(result.contents[0].value.includes("marker create"));
    });

    test("abbreviated second token resolves: 'marker cr' → 'marker create'", () => {
        const provider = makeProvider();
        const doc = makeDocument("marker cr marker_name=foo", "cr");
        const result = provider.provideHover(doc, pos0, null);

        assert.ok(result instanceof vscode.Hover);
        assert.ok(result.contents[0].value.includes("marker create"));
    });

    test("'var set' → 'variable set'", () => {
        const provider = makeProvider();
        const doc = makeDocument("var set variable_name=x", "set");
        const result = provider.provideHover(doc, pos0, null);

        assert.ok(result instanceof vscode.Hover);
        assert.ok(result.contents[0].value.includes("variable set"));
    });

    test("hovering abbreviated first token of 'var set' works", () => {
        const provider = makeProvider();
        const doc = makeDocument("var set variable_name=x", "var");
        const result = provider.provideHover(doc, pos0, null);

        assert.ok(result instanceof vscode.Hover);
        assert.ok(result.contents[0].value.includes("variable set"));
    });

    test("too-short prefix (below min_prefix) returns undefined", () => {
        const provider = makeProvider();
        // "v" alone is fine (view min_prefix=1), but "v c" — "c" is ambiguous
        // or short depending on fixture; use "ma" which needs 2 chars — "m" fails
        const doc = makeDocument("m create", "create");
        const result = provider.provideHover(doc, pos0, null);

        assert.strictEqual(result, undefined);
    });

    test("ambiguous prefix returns undefined", () => {
        // "ma" matches both "marker" (min_prefix 2) and "macro" (min_prefix 2) → ambiguous
        const ambig_tree = {
            children: {
                marker: {
                    min_prefix: 2,
                    children: { create: { min_prefix: 2, children: {}, is_leaf: true } },
                },
                macro: {
                    min_prefix: 2,
                    children: { create: { min_prefix: 2, children: {}, is_leaf: true } },
                },
            },
        };
        const ambig_cmds = { "marker create": {}, "macro create": {} };
        const ambig_docs = new Map([
            ["marker create", "# marker create"],
            ["macro create", "# macro create"],
        ]);
        const provider = cmd_hover_provider(
            new Map(),
            {},
            ambig_docs,
            null,
            ambig_tree,
            ambig_cmds,
        );
        // "ma" is ambiguous between marker and macro
        const doc = makeDocument("ma create", "create");
        const result = provider.provideHover(doc, pos0, null);

        assert.strictEqual(result, undefined);
    });

    test("full-length token still works when command_tree is present", () => {
        const provider = makeProvider();
        const doc = makeDocument("variable set variable_name=x", "variable");
        const result = provider.provideHover(doc, pos0, null);

        assert.ok(result instanceof vscode.Hover);
        assert.ok(result.contents[0].value.includes("variable set"));
    });

    test("argument name is not matched (startsWith does not false-positive)", () => {
        const provider = makeProvider();
        // "marker_name" starts with "marker" but is an argument, stripped by strip_argument_pairs
        const doc = makeDocument("mar create marker_name=foo", "marker_name");
        const result = provider.provideHover(doc, pos0, null);

        assert.strictEqual(result, undefined);
    });

    test("cursor in inline ! comment does not trigger hover", () => {
        // Simulate range.start.character >= position of '!'
        const comment_line = "var set variable_name=foo ! var init";
        const comment_pos = comment_line.indexOf("!");
        // Cursor placed on the 'var' inside the comment (character >= comment_pos)
        const range = { start: { line: 0, character: comment_pos + 2 } };
        const doc = {
            getWordRangeAtPosition: () => range,
            getText: () => "var",
            lineAt: () => ({ text: comment_line }),
        };
        const provider = makeProvider();
        const result = provider.provideHover(doc, pos0, null);

        assert.strictEqual(result, undefined);
    });
});

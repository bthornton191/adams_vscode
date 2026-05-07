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

    test("should return argument completions when a previous arg has a parenthesized value", () => {
        const function_names = new Map();
        const commands = { "xy_plots curve create": ["curve", "curve_name", "x_variable"] };
        const provider = cmd_completion_provider(function_names, commands);

        const lines = [
            "    xy_plots curve create &",
            '        curve = (eval(.gui.main.gfx.page_1.views[$_self.idx].contents // ".my_curve")) &',
            "        ",
        ];
        const localPosition = new vscode.Position(2, lines[2].length);
        const doc = makeDocument("", lines);
        const completions = provider.provideCompletionItems(doc, localPosition, null, {});

        const labels = completions.map((c) => c.label);
        assert.ok(
            !labels.some((l) => l.includes("curve=")),
            "'curve' should be excluded (already used)",
        );
        assert.ok(
            labels.some((l) => l.includes("curve_name")),
            "Expected 'curve_name' completion",
        );
        assert.ok(
            labels.some((l) => l.includes("x_variable")),
            "Expected 'x_variable' completion",
        );
    });

    test("should handle tab-indented continuation lines", () => {
        const function_names = new Map();
        const commands = {
            "part modify rigid_body mass_properties": [
                "part_name",
                "mass",
                "density",
                "center_of_mass_marker",
            ],
        };
        const provider = cmd_completion_provider(function_names, commands);

        const lines = [
            "part modify rigid_body mass_properties &",
            "\tpart_name = .my_model.part_1 &",
            "\tmass = 10.5 &",
            "\t",
        ];
        const localPosition = new vscode.Position(3, lines[3].length);
        const doc = makeDocument("", lines);
        const completions = provider.provideCompletionItems(doc, localPosition, null, {});

        const labels = completions.map((c) => c.label);
        assert.ok(
            labels.some((l) => l.includes("density")),
            "Expected 'density' completion on tab-indented continuation",
        );
        assert.ok(
            labels.some((l) => l.includes("center_of_mass_marker")),
            "Expected 'center_of_mass_marker' completion on tab-indented continuation",
        );
    });

    test("should handle spaces around = in args", () => {
        const function_names = new Map();
        const commands = {
            "geometry create shape cylinder": ["cylinder", "length", "radius", "sides"],
        };
        const provider = cmd_completion_provider(function_names, commands);

        const lines = [
            "geometry create shape cylinder &",
            "    cylinder = $model.cyl_1 &",
            "    length = 10.0 &",
            "    ",
        ];
        const localPosition = new vscode.Position(3, lines[3].length);
        const doc = makeDocument("", lines);
        const completions = provider.provideCompletionItems(doc, localPosition, null, {});

        const labels = completions.map((c) => c.label);
        assert.ok(
            !labels.some((l) => l.includes("cylinder=")),
            "'cylinder' should be excluded (already used with spaces around =)",
        );
        assert.ok(
            !labels.some((l) => l.includes("length=")),
            "'length' should be excluded (already used with spaces around =)",
        );
        assert.ok(
            labels.some((l) => l.includes("radius")),
            "Expected 'radius' completion",
        );
    });

    test("should handle comma-separated parenthesized values", () => {
        const function_names = new Map();
        const commands = {
            "force create element_like bushing": [
                "bushing_name",
                "i_marker_name",
                "j_marker_name",
                "stiffness",
                "damping",
                "tstiffness",
                "tdamping",
            ],
        };
        const provider = cmd_completion_provider(function_names, commands);

        const lines = [
            "force create element_like bushing &",
            "    bushing_name = $model.bushing_1 &",
            "    i_marker_name = $model.ground.mkr_i &",
            "    j_marker_name = $model.part_1.mkr_j &",
            "    stiffness = ($model.k_val), ($model.k_val), 0 &",
            "    damping = ($model.d_val), ($model.d_val), 0 &",
            "    ",
        ];
        const localPosition = new vscode.Position(6, lines[6].length);
        const doc = makeDocument("", lines);
        const completions = provider.provideCompletionItems(doc, localPosition, null, {});

        const labels = completions.map((c) => c.label);
        assert.ok(
            !labels.some((l) => l.trim() === "stiffness="),
            "'stiffness' should be excluded (already used with comma-separated values)",
        );
        assert.ok(
            labels.some((l) => l.includes("tstiffness")),
            "Expected 'tstiffness' completion after comma-separated paren values",
        );
        assert.ok(
            labels.some((l) => l.includes("tdamping")),
            "Expected 'tdamping' completion after comma-separated paren values",
        );
    });

    test("should handle comma-separated quoted string values", () => {
        const function_names = new Map();
        const commands = {
            "force create direct force_vector": [
                "force_vector_name",
                "i_marker_name",
                "j_part_name",
                "ref_marker_name",
                "x_force_function",
                "y_force_function",
                "z_force_function",
            ],
        };
        const provider = cmd_completion_provider(function_names, commands);

        const lines = [
            "force create direct force_vector &",
            "    force_vector_name = $model.fv_1 &",
            "    i_marker_name = $model.part_1.mkr_i &",
            "    j_part_name = $model.ground &",
            "    ref_marker_name = $model.ground.ref_mkr &",
            '    x_force_function = "0" &',
            '    y_force_function = "IMPACT(DY(",          &',
            '                        "       0, ",         &',
            '                        "       $model.pen_depth)" &',
            "    ",
        ];
        const localPosition = new vscode.Position(9, lines[9].length);
        const doc = makeDocument("", lines);
        const completions = provider.provideCompletionItems(doc, localPosition, null, {});

        const labels = completions.map((c) => c.label);
        assert.ok(
            labels.some((l) => l.includes("z_force_function")),
            "Expected 'z_force_function' completion after comma-separated quoted values",
        );
        assert.ok(
            !labels.some((l) => l.trim() === "y_force_function="),
            "'y_force_function' should be excluded (already used)",
        );
    });

    test("should handle nested paren values with curly braces", () => {
        const function_names = new Map();
        const commands = {
            "marker create": ["marker", "location", "orientation", "relative_to"],
        };
        const provider = cmd_completion_provider(function_names, commands);

        const lines = [
            "marker create &",
            "    marker = $model.ground.mkr_1 &",
            "    location = (loc_relative_to({0, 0, 0}, $model.part_1.ref_mkr)) &",
            "    ",
        ];
        const localPosition = new vscode.Position(3, lines[3].length);
        const doc = makeDocument("", lines);
        const completions = provider.provideCompletionItems(doc, localPosition, null, {});

        const labels = completions.map((c) => c.label);
        assert.ok(
            labels.some((l) => l.includes("orientation")),
            "Expected 'orientation' completion after nested paren value with curly braces",
        );
        assert.ok(
            labels.some((l) => l.includes("relative_to")),
            "Expected 'relative_to' completion",
        );
        assert.ok(
            !labels.some((l) => l.includes("location=")),
            "'location' should be excluded (already used)",
        );
    });

    test("should handle quoted string values containing parens", () => {
        const function_names = new Map();
        const commands = {
            "constraint create motion_generator": [
                "motion_name",
                "i_marker_name",
                "j_marker_name",
                "axis",
                "time_derivative",
                "function",
            ],
        };
        const provider = cmd_completion_provider(function_names, commands);

        const lines = [
            "constraint create motion_generator &",
            "    motion_name = .my_model.motion_1 &",
            "    i_marker_name = .my_model.part_1.mkr_i &",
            "    j_marker_name = .my_model.ground.mkr_j &",
            '    function = "360d*(1-cos(2*pi*time))" &',
            "    ",
        ];
        const localPosition = new vscode.Position(5, lines[5].length);
        const doc = makeDocument("", lines);
        const completions = provider.provideCompletionItems(doc, localPosition, null, {});

        const labels = completions.map((c) => c.label);
        assert.ok(
            labels.some((l) => l.includes("axis")),
            "Expected 'axis' completion after quoted string with parens",
        );
        assert.ok(
            labels.some((l) => l.includes("time_derivative")),
            "Expected 'time_derivative' completion",
        );
        assert.ok(
            !labels.some((l) => l.includes("function=")),
            "'function' should be excluded (already used)",
        );
    });

    test("should handle comma-separated eval paren values for location args", () => {
        const function_names = new Map();
        const commands = {
            "marker create": ["marker_name", "location", "orientation"],
        };
        const provider = cmd_completion_provider(function_names, commands);

        const lines = [
            "marker create &",
            "    marker_name = $model.ground.stop_mkr &",
            "    location = (eval(loc_global({0,0,0}, $model.part_1.center_mkr)[1])), &",
            "               (eval(loc_global({0,0,0}, $model.part_2.ref_mkr)[2])), &",
            "               (eval(loc_global({0,0,0}, $model.part_1.center_mkr)[3])) &",
            "    ",
        ];
        const localPosition = new vscode.Position(5, lines[5].length);
        const doc = makeDocument("", lines);
        const completions = provider.provideCompletionItems(doc, localPosition, null, {});

        const labels = completions.map((c) => c.label);
        assert.ok(
            labels.some((l) => l.includes("orientation")),
            "Expected 'orientation' completion after comma-separated eval paren values",
        );
        assert.ok(
            !labels.some((l) => l.includes("marker_name=")),
            "'marker_name' should be excluded (already used)",
        );
    });

    test("should not add leading space to label when partial arg name is typed", () => {
        const function_names = new Map();
        const commands = {
            "marker create": ["marker_name", "location"],
        };
        const provider = cmd_completion_provider(function_names, commands);

        const lines = ["marker create &", "    marker_"];
        const localPosition = new vscode.Position(1, lines[1].length);
        const doc = makeDocument("marker_", lines);
        const completions = provider.provideCompletionItems(doc, localPosition, null, {});

        const match = completions.find((c) => c.label.includes("marker_name"));
        assert.ok(match, "Expected 'marker_name' completion");
        assert.ok(
            !String(match.label).startsWith(" "),
            "Label should not start with a space when partial arg is typed",
        );
    });

    test("should return filtered argument completions when typing partial arg name on continuation line", () => {
        const function_names = new Map([
            ["min", "min doc"],
            ["max", "max doc"],
        ]);
        const commands = {
            "marker create": ["marker_name", "marker", "location", "orientation", "relative_to"],
        };
        const provider = cmd_completion_provider(function_names, commands);

        // Simulates: "marker create &\n    m" (cursor after "m")
        const lines = ["marker create &", "    m"];
        const localPosition = new vscode.Position(1, lines[1].length);
        const doc = makeDocument("m", lines);
        const completions = provider.provideCompletionItems(doc, localPosition, null, {});

        const labels = completions.map((c) => c.label);
        assert.ok(
            labels.some((l) => l.includes("marker_name")),
            "Expected 'marker_name' (starts with 'm')",
        );
        assert.ok(
            labels.some((l) => l.includes("marker")),
            "Expected 'marker' (starts with 'm')",
        );
        assert.ok(
            !labels.some((l) => l.includes("location")),
            "'location' should be excluded (does not start with 'm')",
        );
        assert.ok(
            !labels.some((l) => l.includes("orientation")),
            "'orientation' should be excluded (does not start with 'm')",
        );
    });

    test("should not return function completions when typing partial arg name on continuation line", () => {
        const function_names = new Map([
            ["min", "min doc"],
            ["max", "max doc"],
        ]);
        const commands = {
            "marker create": ["marker_name", "location"],
        };
        const provider = cmd_completion_provider(function_names, commands);

        const lines = ["marker create &", "    m"];
        const localPosition = new vscode.Position(1, lines[1].length);
        const doc = makeDocument("m", lines);
        const completions = provider.provideCompletionItems(doc, localPosition, null, {});

        const kinds = completions.map((c) => c.kind);
        assert.ok(
            !kinds.includes(vscode.CompletionItemKind.Function),
            "Should not return function completions when typing arg name on continuation line",
        );
    });

    test("should not return function completions when typing partial arg name on first line", () => {
        const function_names = new Map([
            ["min", "min doc"],
            ["max", "max doc"],
        ]);
        const commands = {
            "marker create": ["marker_name", "location"],
        };
        const provider = cmd_completion_provider(function_names, commands);

        // Single line: "marker create m" (no continuation)
        const lineText = "marker create m";
        const localPosition = new vscode.Position(0, lineText.length);
        const doc = makeDocument("m", lineText);
        const completions = provider.provideCompletionItems(doc, localPosition, null, {});

        const kinds = completions.map((c) => c.kind);
        assert.ok(
            !kinds.includes(vscode.CompletionItemKind.Function),
            "Should not return function completions when typing arg name on first line",
        );
        const labels = completions.map((c) => c.label);
        assert.ok(
            labels.some((l) => l.includes("marker_name")),
            "Expected 'marker_name' argument completion",
        );
    });

    test("should not return function completions when on continuation line with no partial arg", () => {
        const function_names = new Map([["abs", "abs doc"]]);
        const commands = {
            "marker create": ["marker_name", "location"],
        };
        const provider = cmd_completion_provider(function_names, commands);

        const lines = ["marker create &", "    "];
        const localPosition = new vscode.Position(1, lines[1].length);
        const doc = makeDocument("", lines);
        const completions = provider.provideCompletionItems(doc, localPosition, null, {});

        const kinds = completions.map((c) => c.kind);
        assert.ok(
            !kinds.includes(vscode.CompletionItemKind.Function),
            "Should not return function completions when on continuation line (no partial)",
        );
    });

    test("should exclude already-used args when typing partial arg name on continuation line", () => {
        const function_names = new Map();
        const commands = {
            "marker create": ["marker_name", "marker", "location"],
        };
        const provider = cmd_completion_provider(function_names, commands);

        // marker_name already used; typing "m" — should get "marker" but not "marker_name"
        const lines = ["marker create marker_name=.model.part.mkr &", "    m"];
        const localPosition = new vscode.Position(1, lines[1].length);
        const doc = makeDocument("m", lines);
        const completions = provider.provideCompletionItems(doc, localPosition, null, {});

        const labels = completions.map((c) => c.label);
        assert.ok(
            labels.some((l) => l.includes("marker")),
            "Expected 'marker' completion",
        );
        assert.ok(
            !labels.some((l) => l.includes("marker_name")),
            "'marker_name' should be excluded (already used)",
        );
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

    test("should return no completions on macro parameter definition lines", () => {
        const function_names = new Map([["mod", "mod doc"], ["mode", "mode doc"]]);
        const commands = {};
        const provider = cmd_completion_provider(function_names, commands);

        // Typing 'm' after 't=' on a !$param definition line
        const lineText = "!$model:t=m";
        const localPosition = new vscode.Position(0, lineText.length);
        const doc = makeDocument("", lineText);
        const completions = provider.provideCompletionItems(doc, localPosition, null, {});

        assert.deepStrictEqual(completions, [], "Expected no completions on !$ lines");
    });

    // ── Abbreviation-aware completion via command_tree ────────────────────────

    const ABBREV_COMMAND_TREE = {
        children: {
            force: {
                min_prefix: 4,
                children: {
                    create: {
                        min_prefix: 2,
                        children: {
                            element_like: {
                                min_prefix: 1,
                                children: {
                                    translational_spring_damper: {
                                        min_prefix: 1,
                                        children: {},
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    };

    const TSD_COMMANDS = {
        "force create element_like translational_spring_damper": [
            "spring_damper_name",
            "damping",
            "stiffness",
            "displacement_at_preload",
            "i_marker_name",
            "j_marker_name",
        ],
    };

    test("should return argument completions for abbreviated command on continuation line", () => {
        const function_names = new Map([
            ["displacement", "displacement doc"],
            ["damping_coeff", "damping_coeff doc"],
        ]);
        const provider = cmd_completion_provider(
            function_names,
            TSD_COMMANDS,
            {},
            new Map(),
            null,
            ABBREV_COMMAND_TREE,
        );

        // Mirrors linked_refs.mac: 'element' is an abbreviation of 'element_like'.
        // Several args already used; cursor is at bare 'd' on the last continuation line.
        const lines = [
            "force create element translational_spring_damper  &",
            "    spring_damper_name = $model.tsd1  &",
            "    i_marker_name = $model.arm1.tip  &",
            "    j_marker_name = $model.arm2.spring_J  &",
            "    stiffness = (eval($model.stiffness))  &",
            "    damping = (eval($model.damping))  &",
            "    d",
        ];
        const localPosition = new vscode.Position(6, lines[6].length);
        const doc = makeDocument("d", lines);
        const completions = provider.provideCompletionItems(doc, localPosition, null, {});

        const kinds = completions.map((c) => c.kind);
        const labels = completions.map((c) => c.label);
        assert.ok(
            !kinds.includes(vscode.CompletionItemKind.Function),
            "Should not return function completions when typing arg name for abbreviated command",
        );
        assert.ok(
            labels.some((l) => l.includes("displacement_at_preload")),
            "Expected 'displacement_at_preload' argument completion for partial 'd'",
        );
        assert.ok(
            !labels.some((l) => l.includes("damping")),
            "'damping' should be excluded (already used on a previous line)",
        );
    });

    test("should fall back to function completions when command_tree is null for abbreviated command", () => {
        const function_names = new Map([["displacement", "displacement doc"]]);
        // No command_tree passed — abbreviated 'element' won't resolve
        const provider = cmd_completion_provider(function_names, TSD_COMMANDS);

        const lines = [
            "force create element translational_spring_damper  &",
            "    spring_damper_name = $model.tsd1  &",
            "    d",
        ];
        const localPosition = new vscode.Position(2, lines[2].length);
        const doc = makeDocument("d", lines);
        const completions = provider.provideCompletionItems(doc, localPosition, null, {});

        const kinds = completions.map((c) => c.kind);
        assert.ok(
            kinds.includes(vscode.CompletionItemKind.Function),
            "Without command_tree, abbreviated command should fall back to function completions",
        );
    });
});

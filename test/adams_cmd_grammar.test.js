/**
 * Tests for the Adams CMD TextMate grammar (syntaxes/adams_cmd.tmLanguage.json).
 *
 * Uses vscode-textmate + vscode-oniguruma to tokenize text offline — no Adams
 * View process or VS Code extension host required.
 */

const assert = require("assert");
const fs = require("fs");
const path = require("path");
const { Registry, INITIAL } = require("vscode-textmate");
const { loadWASM, createOnigScanner, createOnigString } = require("vscode-oniguruma");

const GRAMMAR_FILE = path.join(__dirname, "..", "syntaxes", "adams_cmd.tmLanguage.json");
const WASM_FILE = path.join(path.dirname(require.resolve("vscode-oniguruma")), "onig.wasm");

/**
 * Set up the vscode-textmate Registry backed by vscode-oniguruma.
 * Returns a Promise that resolves to a loaded IGrammar.
 */
async function loadGrammar() {
    const wasmBin = fs.readFileSync(WASM_FILE).buffer;
    await loadWASM(wasmBin);

    const registry = new Registry({
        onigLib: Promise.resolve({ createOnigScanner, createOnigString }),
        loadGrammar: (scopeName) => {
            if (scopeName === "source.adams_cmd") {
                const raw = fs.readFileSync(GRAMMAR_FILE, "utf-8");
                const { parseRawGrammar } = require("vscode-textmate");
                return parseRawGrammar(raw, GRAMMAR_FILE);
            }
            return null;
        },
    });

    return registry.loadGrammar("source.adams_cmd");
}

/**
 * Tokenize an array of lines.
 * Returns an array (one entry per line) of arrays of { text, scopes } objects.
 */
function tokenizeLines(grammar, lines) {
    let ruleStack = INITIAL;
    return lines.map((line) => {
        const result = grammar.tokenizeLine(line, ruleStack);
        ruleStack = result.ruleStack;
        return result.tokens.map((token) => ({
            text: line.slice(token.startIndex, token.endIndex),
            scopes: token.scopes,
        }));
    });
}

/**
 * Return true if any token on a line has the given scope.
 */
function lineHasScope(lineTokens, scope) {
    return lineTokens.some((t) => t.scopes.includes(scope));
}

// ---------------------------------------------------------------------------

suite("adams_cmd grammar", () => {
    let grammar;

    suiteSetup(async () => {
        grammar = await loadGrammar();
    });

    // -----------------------------------------------------------------------
    // Sanity / baseline tests
    // -----------------------------------------------------------------------

    test("grammar loads successfully", () => {
        assert.ok(grammar, "grammar should not be null");
    });

    test("simple double-quoted string is tokenised as string", () => {
        const tokens = tokenizeLines(grammar, ['variable set variable=foo string="hello"']);
        const allScopes = tokens[0].flatMap((t) => t.scopes);
        assert.ok(
            allScopes.includes("string.quoted.double.adams_cmd"),
            "expected string.quoted.double.adams_cmd scope",
        );
    });

    test("line after a closed double-quoted string is not a string", () => {
        const lines = [
            'variable set variable=foo string="hello"',
            "variable set variable=bar real=1.0",
        ];
        const tokens = tokenizeLines(grammar, lines);
        assert.ok(
            !lineHasScope(tokens[1], "string.quoted.double.adams_cmd"),
            "line after closed string should not carry string scope",
        );
    });

    // -----------------------------------------------------------------------
    // Regression: issue #11 — complex quoted expression with nested/escaped
    // quotes should NOT leave a string scope open for subsequent lines.
    // -----------------------------------------------------------------------

    test("issue #11: complex nested-quote expression does not bleed string scope onto next line", () => {
        // This is the exact problematic expression reported in issue #11.
        const lines = [
            "variable set variable=$_self.pyExe integer= &",
            '(eval(run_python_code("execute_cmd(\'variable set variable=$_self.fileList string=(eval(STR_SPLIT(STR_REPLACE_ALL(STR_SUBSTR(\'+repr(str(files))+\',2,STR_LENGTH(\'+repr(str(files))+\')-2),"\\\'", ""),",")))\')")))',
            "",
            "variable set variable=after_expr real=1.0",
        ];

        const tokens = tokenizeLines(grammar, lines);

        // The line after the complex expression should NOT be inside any string scope.
        assert.ok(
            !lineHasScope(tokens[3], "string.quoted.double.adams_cmd"),
            "line following complex expression should not have double-string scope (issue #11)",
        );
        assert.ok(
            !lineHasScope(tokens[3], "string.quoted.single.adams_cmd"),
            "line following complex expression should not have single-string scope (issue #11)",
        );
    });

    test("issue #11: comment line after complex expression is tokenised as a comment, not a string", () => {
        const lines = [
            "variable set variable=$_self.pyExe integer= &",
            '(eval(run_python_code("execute_cmd(\'variable set variable=$_self.fileList string=(eval(STR_SPLIT(STR_REPLACE_ALL(STR_SUBSTR(\'+repr(str(files))+\',2,STR_LENGTH(\'+repr(str(files))+\')-2),"\\\'", ""),",")))\')")))',
            "! this is a comment",
        ];

        const tokens = tokenizeLines(grammar, lines);

        assert.ok(
            lineHasScope(tokens[2], "comment"),
            "line starting with ! should be tokenised as a comment",
        );
        assert.ok(
            !lineHasScope(tokens[2], "string.quoted.double.adams_cmd"),
            "comment line should not be inside a double-string scope",
        );
        assert.ok(
            !lineHasScope(tokens[2], "string.quoted.single.adams_cmd"),
            "comment line should not be inside a single-string scope",
        );
    });
});

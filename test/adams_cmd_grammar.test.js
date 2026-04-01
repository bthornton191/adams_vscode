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

    // -----------------------------------------------------------------------
    // String preservation tests — correct highlighting we must not break
    // -----------------------------------------------------------------------

    test("single-quoted string is tokenised as string", () => {
        const tokens = tokenizeLines(grammar, ["variable set variable=sep string_value='.'"])[0];
        assert.ok(
            tokens.some((t) => t.scopes.includes("string.quoted.single.adams_cmd")),
            "expected string.quoted.single.adams_cmd scope",
        );
    });

    test("line after a closed single-quoted string is not a string", () => {
        const lines = [
            "variable set variable=sep string_value='.'",
            "variable set variable=bar real=1.0",
        ];
        const tokens = tokenizeLines(grammar, lines);
        assert.ok(
            !lineHasScope(tokens[1], "string.quoted.single.adams_cmd"),
            "line after closed single-quoted string should not carry string scope",
        );
    });

    test("double-quoted string containing single-quotes does not bleed onto next line", () => {
        // A single quote INSIDE a double-quoted string is a literal character —
        // it must NOT open a nested string scope that breaks subsequent lines.
        const lines = [
            'variable set variable=x string_value="it\'s fine"',
            "variable set variable=after real=1.0",
        ];
        const tokens = tokenizeLines(grammar, lines);
        assert.ok(
            !lineHasScope(tokens[1], "string.quoted.double.adams_cmd"),
            'line after "it\'s fine" should not carry double-string scope',
        );
        assert.ok(
            !lineHasScope(tokens[1], "string.quoted.single.adams_cmd"),
            'line after "it\'s fine" should not carry single-string scope',
        );
    });

    test("single-quoted string containing double-quotes does not bleed onto next line", () => {
        // A double quote INSIDE a single-quoted string is a literal character —
        // it must NOT open a nested string scope that breaks subsequent lines.
        const lines = [
            "variable set variable=x string_value='say \"hello\"'",
            "variable set variable=after real=1.0",
        ];
        const tokens = tokenizeLines(grammar, lines);
        assert.ok(
            !lineHasScope(tokens[1], "string.quoted.double.adams_cmd"),
            "line after 'say \"hello\"' should not carry double-string scope",
        );
        assert.ok(
            !lineHasScope(tokens[1], "string.quoted.single.adams_cmd"),
            "line after 'say \"hello\"' should not carry single-string scope",
        );
    });

    // -----------------------------------------------------------------------
    // Bug: string // concatenation expression incorrectly highlighted as string
    //
    // Pattern: "prefix_text'" // expression // "'suffix_text"
    //   The middle `expression` is NOT inside any string — it is a plain Adams
    //   expression between two string literals joined with the // operator.
    //   The BROKEN grammar treated the ' at the end of the first literal as
    //   opening a nested single-quoted string, causing `expression` and the
    //   // operators to be coloured as string content.
    // -----------------------------------------------------------------------

    test("string // concat: expression between strings is not highlighted as string", () => {
        // From lsp_demo.cmd line 379.
        // The line uses Adams' // string-concatenation operator to build a
        // runtime expression like:  "prefix['" // $var // "']"
        // The two // operators and the variable between them are NOT inside
        // any string literal; only the "prefix['" and "']" segments are.
        const line =
            "var set var=$_self.py_str str=(eval($_self.py_str)), " +
            '(eval("mod = Adams.Models[\'" // $_self.model.object_value.name // "\']"))';

        const tokens = tokenizeLines(grammar, [line])[0];

        // Every token whose text contains one of the // operators must NOT
        // carry a string scope.  Before the fix the // tokens were inside the
        // nested single-string scope opened by the ' character at the end of
        // the first double-quoted string.
        const concatTokens = tokens.filter((t) => t.text.includes("//"));
        assert.ok(concatTokens.length > 0, "expected to find at least one token containing //");
        for (const t of concatTokens) {
            assert.ok(
                !t.scopes.includes("string.quoted.double.adams_cmd"),
                `// operator token must NOT be inside a double-string scope (was: ${t.scopes})`,
            );
            assert.ok(
                !t.scopes.includes("string.quoted.single.adams_cmd"),
                `// operator token must NOT be inside a single-string scope (was: ${t.scopes})`,
            );
        }
    });

    test("string // concat: line after concatenation expression is not a string", () => {
        const lines = [
            "var set var=$_self.py_str str=(eval($_self.py_str)), " +
                '(eval("mod = Adams.Models[\'" // $_self.model.object_value.name // "\']"))',
            "variable set variable=after real=1.0",
        ];
        const tokens = tokenizeLines(grammar, lines);
        assert.ok(
            !lineHasScope(tokens[1], "string.quoted.double.adams_cmd"),
            "line after concat expression should not carry double-string scope",
        );
        assert.ok(
            !lineHasScope(tokens[1], "string.quoted.single.adams_cmd"),
            "line after concat expression should not carry single-string scope",
        );
    });
});

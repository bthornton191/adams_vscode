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

    // -----------------------------------------------------------------------
    // Inline comments — ! after code on the same line
    // -----------------------------------------------------------------------

    test("inline comment is tokenised as a comment", () => {
        const line = "simulation single transient end_time = 1.0  ! run for 1 second";
        const tokens = tokenizeLines(grammar, [line])[0];
        const commentTokens = tokens.filter((t) => t.scopes.includes("comment"));
        assert.ok(commentTokens.length > 0, "expected at least one token with comment scope");
        assert.ok(
            commentTokens.some((t) => t.text === "!"),
            "the ! marker should be tokenised as a comment",
        );
        assert.ok(
            commentTokens.some((t) => t.text.includes("run")),
            "text after ! should be tokenised as a comment",
        );
    });

    test("code before inline comment is not a comment", () => {
        const line = "simulation single transient end_time = 1.0  ! run for 1 second";
        const tokens = tokenizeLines(grammar, [line])[0];
        const nonCommentTokens = tokens.filter((t) => !t.scopes.includes("comment"));
        assert.ok(
            nonCommentTokens.some((t) => t.text === "1.0"),
            "numeric token before the comment should not carry comment scope",
        );
    });

    test("full-line comment still tokenised as a comment (regression)", () => {
        const line = "! this is a full-line comment";
        const tokens = tokenizeLines(grammar, [line])[0];
        assert.ok(lineHasScope(tokens, "comment"), "full-line ! comment should have comment scope");
    });

    test("! as NOT operator inside parens is not a comment", () => {
        const line = "if condition = (!DB_EXISTS(.model.PART_1))";
        const tokens = tokenizeLines(grammar, [line])[0];
        assert.ok(
            !lineHasScope(tokens, "comment"),
            "no token on a line using ! as NOT operator should have comment scope",
        );
    });

    test("! as NOT operator inside parens with leading space is not a comment", () => {
        const line = "if condition = ( !DB_EXISTS(.model.PART_1))";
        const tokens = tokenizeLines(grammar, [line])[0];
        assert.ok(
            !lineHasScope(tokens, "comment"),
            "no token on a line using ! as NOT operator with leading space should have comment scope",
        );
    });

    test("! inside a double-quoted string is not a comment", () => {
        const line = 'variable set variable=foo string="hello ! world"';
        const tokens = tokenizeLines(grammar, [line])[0];
        const bangToken = tokens.find((t) => t.text.includes("!"));
        assert.ok(bangToken !== undefined, "expected to find a token containing !");
        assert.ok(
            !bangToken.scopes.includes("comment"),
            "! inside a double-quoted string must NOT be a comment",
        );
        assert.ok(
            bangToken.scopes.includes("string.quoted.double.adams_cmd"),
            "! inside a double-quoted string should retain string scope",
        );
    });

    test("inline comment with no space after ! is still a comment", () => {
        // !run — no whitespace between ! and the comment text
        const line = "simulation single transient end_time = 1.0  !run for 1 second";
        const tokens = tokenizeLines(grammar, [line])[0];
        assert.ok(lineHasScope(tokens, "comment"), "!run should be tokenised as a comment");
        const commentTokens = tokens.filter((t) => t.scopes.includes("comment"));
        assert.ok(
            commentTokens.some((t) => t.text.includes("run")),
            "text after ! should be inside the comment scope",
        );
    });

    test("! as NOT operator with spaces on both sides inside parens is not a comment", () => {
        // ( ! DB_EXISTS(...)) — ! is inside parens so it is the NOT operator
        const line = "if condition = ( ! DB_EXISTS(.model.PART_1))";
        const tokens = tokenizeLines(grammar, [line])[0];
        assert.ok(
            !lineHasScope(tokens, "comment"),
            "! as NOT operator with surrounding spaces inside parens must NOT be a comment",
        );
    });

    test("!= inequality operator inside parens is not a comment", () => {
        const line = "if condition = ($_self.var != 10)";
        const tokens = tokenizeLines(grammar, [line])[0];
        assert.ok(
            !lineHasScope(tokens, "comment"),
            "!= inequality operator inside parens must NOT be a comment",
        );
    });
});

// ---------------------------------------------------------------------------
// Macro frontmatter highlighting
// ---------------------------------------------------------------------------

suite("adams_cmd grammar — macro frontmatter", () => {
    let grammar;

    suiteSetup(async () => {
        grammar = await loadGrammar();
    });

    // Helpers that return the tokens for a specific line index
    function tokenizeMacro(lines) {
        return tokenizeLines(grammar, lines);
    }

    function tokenOnLine(lineTokens, text) {
        return lineTokens.find((t) => t.text === text);
    }

    // -----------------------------------------------------------------------
    // USER_ENTERED_COMMAND
    // -----------------------------------------------------------------------

    test("!USER_ENTERED_COMMAND: keyword is selfParameter", () => {
        const tokens = tokenizeMacro(["!USER_ENTERED_COMMAND  cdm wear"])[0];
        const kw = tokenOnLine(tokens, "USER_ENTERED_COMMAND");
        assert.ok(kw, "expected to find USER_ENTERED_COMMAND token");
        assert.ok(kw.scopes.includes("selfParameter"), `expected selfParameter, got: ${kw.scopes}`);
    });

    test("!USER_ENTERED_COMMAND: command text is command.command", () => {
        const tokens = tokenizeMacro(["!USER_ENTERED_COMMAND  cdm wear"])[0];
        const cmd = tokens.find((t) => t.text.includes("cdm wear"));
        assert.ok(cmd, "expected to find command text token");
        assert.ok(
            cmd.scopes.includes("command.command"),
            `expected command.command, got: ${cmd.scopes}`,
        );
    });

    test("!USER_ENTERED_COMMAND: ! prefix is comment", () => {
        const tokens = tokenizeMacro(["!USER_ENTERED_COMMAND  cdm wear"])[0];
        const bang = tokenOnLine(tokens, "!");
        assert.ok(bang, "expected to find ! token");
        assert.ok(
            bang.scopes.includes("comment"),
            `expected comment scope on !, got: ${bang.scopes}`,
        );
    });

    // -----------------------------------------------------------------------
    // END_OF_PARAMETERS
    // -----------------------------------------------------------------------

    test("!END_OF_PARAMETERS: keyword is selfParameter", () => {
        const lines = ["!USER_ENTERED_COMMAND  cdm wear", "!END_OF_PARAMETERS"];
        const tokens = tokenizeMacro(lines);
        const kw = tokenOnLine(tokens[1], "END_OF_PARAMETERS");
        assert.ok(kw, "expected to find END_OF_PARAMETERS token");
        assert.ok(kw.scopes.includes("selfParameter"), `expected selfParameter, got: ${kw.scopes}`);
    });

    test("lines after END_OF_PARAMETERS are not in the frontmatter block", () => {
        const lines = [
            "!USER_ENTERED_COMMAND  cdm wear",
            "!END_OF_PARAMETERS",
            "variable set variable=foo real=1.0",
        ];
        const tokens = tokenizeMacro(lines);
        // The variable line should have command.command or command.control scope, not selfParameter
        assert.ok(
            !lineHasScope(tokens[2], "selfParameter"),
            "code after END_OF_PARAMETERS should not be in frontmatter scope",
        );
    });

    // -----------------------------------------------------------------------
    // HELP_STRING
    // -----------------------------------------------------------------------

    test("HELP_STRING: keyword is selfParameter", () => {
        const lines = [
            "!USER_ENTERED_COMMAND  cdm wear",
            "! HELP_STRING:  A description of the macro.",
        ];
        const tokens = tokenizeMacro(lines);
        const kw = tokenOnLine(tokens[1], "HELP_STRING");
        assert.ok(kw, "expected to find HELP_STRING token");
        assert.ok(kw.scopes.includes("selfParameter"), `expected selfParameter, got: ${kw.scopes}`);
    });

    test("DESCRIPTION: keyword is selfParameter", () => {
        const lines = [
            "!USER_ENTERED_COMMAND  cdm wear",
            "! DESCRIPTION:  A description using the alias.",
        ];
        const tokens = tokenizeMacro(lines);
        const kw = tokenOnLine(tokens[1], "DESCRIPTION");
        assert.ok(kw, "expected to find DESCRIPTION token");
        assert.ok(
            kw.scopes.includes("selfParameter"),
            `expected selfParameter on DESCRIPTION keyword, got: ${kw.scopes}`,
        );
    });

    test("DESCRIPTION: text on same line is string.unquoted.adams_cmd", () => {
        const lines = [
            "!USER_ENTERED_COMMAND  cdm wear",
            "! DESCRIPTION:  A description using the alias.",
        ];
        const tokens = tokenizeMacro(lines);
        const strToken = tokens[1].find((t) => t.text.includes("A description using the alias"));
        assert.ok(strToken, "expected to find description text token");
        assert.ok(
            strToken.scopes.includes("string.unquoted.adams_cmd"),
            `expected string.unquoted.adams_cmd on DESCRIPTION value, got: ${strToken.scopes}`,
        );
    });

    test("HELP_STRING: text on same line is string.unquoted.adams_cmd", () => {
        const lines = [
            "!USER_ENTERED_COMMAND  cdm wear",
            "! HELP_STRING:  A description of the macro.",
        ];
        const tokens = tokenizeMacro(lines);
        const strToken = tokens[1].find((t) => t.text.includes("A description"));
        assert.ok(strToken, "expected to find description text token");
        assert.ok(
            strToken.scopes.includes("string.unquoted.adams_cmd"),
            `expected string.unquoted.adams_cmd, got: ${strToken.scopes}`,
        );
    });

    test("HELP_STRING: continuation lines are string.unquoted.adams_cmd", () => {
        const lines = [
            "!USER_ENTERED_COMMAND  cdm wear",
            "! HELP_STRING:  First line.",
            "!               Second line.",
            "!               Third line.",
        ];
        const tokens = tokenizeMacro(lines);
        assert.ok(
            lineHasScope(tokens[2], "string.unquoted.adams_cmd"),
            "HELP_STRING continuation line 2 should be string.unquoted.adams_cmd",
        );
        assert.ok(
            lineHasScope(tokens[3], "string.unquoted.adams_cmd"),
            "HELP_STRING continuation line 3 should be string.unquoted.adams_cmd",
        );
    });

    test("HELP_STRING: string does not bleed past a subsequent keyword line", () => {
        const lines = [
            "!USER_ENTERED_COMMAND  cdm wear",
            "! HELP_STRING:  First line.",
            "!               Continuation.",
            "! AUTHOR:       Ben Thornton",
        ];
        const tokens = tokenizeMacro(lines);
        assert.ok(
            !lineHasScope(tokens[3], "string.unquoted.adams_cmd"),
            "AUTHOR line should not carry string.unquoted.adams_cmd scope",
        );
    });

    // -----------------------------------------------------------------------
    // Non-parsed keywords (AUTHOR, DATE, MACRO NAME, etc.)
    // -----------------------------------------------------------------------

    test("AUTHOR: keyword is selfParameter", () => {
        const lines = ["!USER_ENTERED_COMMAND  cdm wear", "! AUTHOR:  Ben Thornton"];
        const tokens = tokenizeMacro(lines);
        const kw = tokenOnLine(tokens[1], "AUTHOR");
        assert.ok(kw, "expected to find AUTHOR token");
        assert.ok(kw.scopes.includes("selfParameter"), `expected selfParameter, got: ${kw.scopes}`);
    });

    test("AUTHOR: value text is comment (not a parsed field)", () => {
        const lines = ["!USER_ENTERED_COMMAND  cdm wear", "! AUTHOR:  Ben Thornton"];
        const tokens = tokenizeMacro(lines);
        const val = tokens[1].find((t) => t.text.includes("Ben Thornton"));
        assert.ok(val, "expected to find author value token");
        assert.ok(
            val.scopes.includes("comment"),
            `expected comment scope on author value, got: ${val.scopes}`,
        );
    });

    test("MACRO NAME: keyword is selfParameter", () => {
        const lines = ["!USER_ENTERED_COMMAND  cdm wear", "! MACRO NAME:  test.mac"];
        const tokens = tokenizeMacro(lines);
        // The keyword token may be "MACRO NAME" or "MACRO" depending on how it's captured
        const kw = tokens[1].find(
            (t) => t.text.includes("MACRO") && t.scopes.includes("selfParameter"),
        );
        assert.ok(kw, "expected MACRO NAME keyword to have selfParameter scope");
    });

    test("MACRO_NAME (underscore variant): keyword is selfParameter", () => {
        const lines = ["!USER_ENTERED_COMMAND  cdm wear", "! MACRO_NAME:  test.mac"];
        const tokens = tokenizeMacro(lines);
        const kw = tokens[1].find(
            (t) => t.text.includes("MACRO") && t.scopes.includes("selfParameter"),
        );
        assert.ok(kw, "expected MACRO_NAME (underscore) keyword to have selfParameter scope");
    });

    // -----------------------------------------------------------------------
    // Parameter definitions: qualifier highlighting
    // -----------------------------------------------------------------------

    test("$param_name: parameter token is parameter.reference", () => {
        const lines = ["!USER_ENTERED_COMMAND  cdm wear", "!$param1:t=int:d=100"];
        const tokens = tokenizeMacro(lines);
        const param = tokenOnLine(tokens[1], "$param1");
        assert.ok(param, "expected to find $param1 token");
        assert.ok(
            param.scopes.includes("parameter.reference"),
            `expected parameter.reference, got: ${param.scopes}`,
        );
    });

    test("qualifier key 't' is command.argument", () => {
        const lines = ["!USER_ENTERED_COMMAND  cdm wear", "!$param1:t=int:d=100"];
        const tokens = tokenizeMacro(lines);
        const key = tokenOnLine(tokens[1], "t");
        assert.ok(key, "expected to find 't' qualifier key token");
        assert.ok(
            key.scopes.includes("command.argument"),
            `expected command.argument on qualifier key 't', got: ${key.scopes}`,
        );
    });

    test("qualifier colon separator is keyword.operator", () => {
        const lines = ["!USER_ENTERED_COMMAND  cdm wear", "!$param1:t=int:d=100"];
        const tokens = tokenizeMacro(lines);
        const colons = tokens[1].filter(
            (t) => t.text === ":" && t.scopes.includes("keyword.operator"),
        );
        assert.ok(colons.length > 0, "expected at least one : token with keyword.operator scope");
    });

    test("qualifier unquoted value is constant.other.qualifier.adams_cmd", () => {
        const lines = ["!USER_ENTERED_COMMAND  cdm wear", "!$param1:t=int:d=100"];
        const tokens = tokenizeMacro(lines);
        const val = tokens[1].find(
            (t) => t.text === "int" && t.scopes.includes("constant.other.qualifier.adams_cmd"),
        );
        assert.ok(
            val,
            "expected qualifier value 'int' to have constant.other.qualifier.adams_cmd scope",
        );
    });

    test("qualifier double-quoted value is string.quoted.double.adams_cmd", () => {
        const lines = ["!USER_ENTERED_COMMAND  cdm wear", '!$part_name:t=str:d="part"'];
        const tokens = tokenizeMacro(lines);
        const val = tokens[1].find(
            (t) => t.text.includes("part") && t.scopes.includes("string.quoted.double.adams_cmd"),
        );
        assert.ok(val, 'expected :d="part" to have string.quoted.double.adams_cmd scope');
    });

    // -----------------------------------------------------------------------
    // Parameter docstrings
    // -----------------------------------------------------------------------

    test("docstring line after $param is string.unquoted.adams_cmd", () => {
        const lines = [
            "!USER_ENTERED_COMMAND  cdm wear",
            "!$param1:t=int:d=100",
            "! The first parameter — an integer count.",
        ];
        const tokens = tokenizeMacro(lines);
        assert.ok(
            lineHasScope(tokens[2], "string.unquoted.adams_cmd"),
            "docstring line after $param should be string.unquoted.adams_cmd",
        );
    });

    test("docstring does not bleed past the next $param definition", () => {
        const lines = [
            "!USER_ENTERED_COMMAND  cdm wear",
            "!$param1:t=int:d=100",
            "! Docstring for param1.",
            "!$param2:t=str:d=foo",
        ];
        const tokens = tokenizeMacro(lines);
        // The !$param2 line: $param2 should be parameter.reference, not string
        const param2 = tokens[3].find((t) => t.text.includes("param2"));
        assert.ok(param2, "expected to find $param2 token");
        assert.ok(
            param2.scopes.includes("parameter.reference"),
            `expected parameter.reference on $param2, got: ${param2.scopes}`,
        );
        assert.ok(
            !param2.scopes.includes("string.unquoted.adams_cmd"),
            "$param2 token should not be inside a string scope",
        );
    });

    // -----------------------------------------------------------------------
    // Safety: frontmatter block ends at first non-comment line
    // -----------------------------------------------------------------------

    test("code line immediately after !USER_ENTERED_COMMAND (no END_OF_PARAMETERS) is not frontmatter", () => {
        const lines = ["!USER_ENTERED_COMMAND  cdm wear", "variable set variable=foo real=1.0"];
        const tokens = tokenizeMacro(lines);
        assert.ok(
            !lineHasScope(tokens[1], "selfParameter"),
            "code line without END_OF_PARAMETERS should not carry selfParameter scope",
        );
    });

    test("! $foo (space between ! and $) inside frontmatter is a comment, not a parameter", () => {
        // Parameter definitions must be !$name (no space). A comment like
        // "! $variable is the answer" must not be mistaken for a param definition.
        const lines = [
            "!USER_ENTERED_COMMAND  cdm wear",
            "! $foo is used for something",
            "!END_OF_PARAMETERS",
        ];
        const tokens = tokenizeMacro(lines);
        const dollarToken = tokens[1].find((t) => t.text.includes("$foo"));
        assert.ok(dollarToken, "expected to find $foo token");
        assert.ok(
            !dollarToken.scopes.includes("parameter.reference"),
            "! $foo (with space) should NOT be treated as a parameter definition",
        );
        assert.ok(
            lineHasScope(tokens[1], "comment"),
            "! $foo (with space) line should be treated as a comment",
        );
    });

    test("HELP_STRING: string does not bleed onto !END_OF_PARAMETERS line", () => {
        const lines = [
            "!USER_ENTERED_COMMAND  cdm wear",
            "! HELP_STRING:  Description text.",
            "!END_OF_PARAMETERS",
        ];
        const tokens = tokenizeMacro(lines);
        assert.ok(
            !lineHasScope(tokens[2], "string.unquoted.adams_cmd"),
            "END_OF_PARAMETERS line should not carry string scope",
        );
        assert.ok(
            lineHasScope(tokens[2], "selfParameter"),
            "END_OF_PARAMETERS keyword should have selfParameter scope",
        );
    });

    // -----------------------------------------------------------------------
    // Separator / other comment lines inside frontmatter
    // -----------------------------------------------------------------------

    test("separator line (! ---) inside frontmatter is a comment", () => {
        const lines = [
            "!USER_ENTERED_COMMAND  cdm wear",
            "! -----------------------------------------------------------------",
            "!END_OF_PARAMETERS",
        ];
        const tokens = tokenizeMacro(lines);
        assert.ok(
            lineHasScope(tokens[1], "comment"),
            "separator line inside frontmatter should have comment scope",
        );
    });

    test("! $foo (space before $) inside HELP_STRING block terminates the string and is a comment", () => {
        // The HELP_STRING end lookahead fires on ![ \t]*$ so "! $foo" stops the block.
        const lines = [
            "!USER_ENTERED_COMMAND  cdm wear",
            "! HELP_STRING:  Description.",
            "! $param is a variable",
            "!END_OF_PARAMETERS",
        ];
        const tokens = tokenizeMacro(lines);
        assert.ok(
            lineHasScope(tokens[2], "comment"),
            "! $foo line (space before $) inside frontmatter should be scoped as comment, not string",
        );
        assert.ok(
            !lineHasScope(tokens[2], "string.unquoted.adams_cmd"),
            "! $foo line should not carry string.unquoted.adams_cmd scope",
        );
    });
});

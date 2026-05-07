const vscode = require("vscode");
const { strip_argument_pairs } = require("./cmd_completion_provider.ts.js");

/**
 * Walks backward through & continuation lines and returns the FULL current line
 * joined with any preceding continuation lines. Unlike get_full_command_context,
 * this includes the entire current line (not truncated at the cursor position) so
 * that the first keyword of a multi-word command is always visible in the context.
 * Inline Adams ! comments are stripped from each line before joining.
 * @param {object} document
 * @param {object} position
 * @returns {string}
 */
function get_full_command_text(document, position) {
    const strip_comment = (text) => text.replace(/\s*!.*$/, "");
    const parts = [strip_comment(document.lineAt(position.line).text)];
    let line_no = position.line - 1;
    while (line_no >= 0) {
        const prev_text = document.lineAt(line_no).text;
        if (/&[ \t]*(!.*)?$/.test(prev_text)) {
            parts.unshift(prev_text.replace(/&[ \t]*(!.*)?$/, "").trimEnd());
            line_no--;
        } else {
            break;
        }
    }
    return parts.join(" ");
}

/**
 * Match a single token against a node's children, honouring min_prefix and
 * ambiguity rules. Port of Schema._match_token() from adams_cmd_lsp/schema.py.
 *
 * @param {string} token
 * @param {Object} children  — command_tree node.children
 * @returns {string|null}    canonical child name, or null on no-match / ambiguity
 */
function _match_token(token, children) {
    const t = token.toLowerCase();

    // Exact match takes priority
    for (const name of Object.keys(children)) {
        if (name.toLowerCase() === t) return name;
    }

    // Prefix match — must be unambiguous and at least min_prefix chars
    const matches = [];
    for (const [name, node_data] of Object.entries(children)) {
        const min_prefix = node_data.min_prefix !== undefined ? node_data.min_prefix : name.length;
        if (t.length >= min_prefix && name.toLowerCase().startsWith(t)) {
            matches.push(name);
        }
    }
    return matches.length === 1 ? matches[0] : null;
}

/**
 * Resolve a list of (possibly abbreviated) command tokens to a canonical key.
 * Port of Schema.resolve_command_key() from adams_cmd_lsp/schema.py.
 *
 * @param {string[]} tokens        — e.g. ["var", "set"]
 * @param {Object}   command_tree  — the "command_tree" object from command_schema.json
 * @param {Object}   commands      — the "commands" object from command_schema.json (for leaf check)
 * @returns {string|null}          canonical key (e.g. "variable set"), or null on failure
 */
function resolve_command_key(tokens, command_tree, commands) {
    let node = command_tree;
    const resolved = [];

    for (const token of tokens) {
        const children = node.children || {};
        if (Object.keys(children).length === 0) return null;

        const match = _match_token(token, children);
        if (match === null) return null;

        resolved.push(match);
        node = children[match];
    }

    const key = resolved.join(" ");
    return Object.prototype.hasOwnProperty.call(commands, key) ? key : null;
}

/**
 * @param {Map<string, string>} view_functions  function name → markdown doc
 * @param {Object} view_commands                structured.json (command key → arg[])
 * @param {Map<string, string>} command_docs    command key → markdown doc
 * @param {object|null} reporter
 * @param {Object|null} command_tree            command_schema.json "command_tree" (enables abbreviation)
 * @param {Object|null} schema_commands         command_schema.json "commands" (needed for leaf check)
 */
function cmd_hover_provider(
    view_functions,
    view_commands = {},
    command_docs = new Map(),
    reporter = null,
    command_tree = null,
    schema_commands = null,
) {
    return {
        provideHover(document, position, token) {
            const range = document.getWordRangeAtPosition(position);
            if (!range) return undefined;

            // If the cursor is inside an inline Adams ! comment, no hover.
            const raw_line = document.lineAt(position.line).text;
            const comment_pos = raw_line.indexOf("!");
            if (comment_pos !== -1 && range.start.character >= comment_pos) {
                return undefined;
            }

            const word = document.getText(range).toLowerCase();

            // --- Command hover ---
            // Use the FULL current line (plus any & continuation lines before it) so
            // that hovering the first keyword of a multi-word command works correctly.
            const full_text = get_full_command_text(document, position);
            const command_context = strip_argument_pairs(full_text).toLowerCase();
            const context_words = command_context.trim().split(/\s+/).filter(Boolean);

            let matched_key = null;
            let matched_was_abbreviation = false;

            if (command_tree && schema_commands) {
                // --- Abbreviation-aware resolution via command_tree ---
                // Try progressively shorter token prefixes so we don't include
                // argument values that weren't fully stripped (defensive).
                for (let len = context_words.length; len >= 1; len--) {
                    const tokens = context_words.slice(0, len);
                    const key = resolve_command_key(tokens, command_tree, schema_commands);
                    if (key !== null) {
                        // Show hover when the hovered word is one of the abbreviated
                        // input tokens that produced this key (not a canonical key word
                        // check, which would false-positive on canonical prefixes).
                        if (tokens.includes(word)) {
                            matched_key = key;
                            const canonical_words = key.split(" ");
                            matched_was_abbreviation = tokens.some(
                                (t, i) =>
                                    canonical_words[i] !== undefined && t !== canonical_words[i],
                            );
                        }
                        break; // Stop at the longest resolved key regardless
                    }
                }
            } else {
                // --- Exact-match fallback (used in tests without schema) ---
                for (let len = context_words.length; len >= 1; len--) {
                    const candidate = context_words.slice(0, len).join(" ");
                    if (Object.prototype.hasOwnProperty.call(view_commands, candidate)) {
                        if (candidate.split(" ").some((kw) => kw === word)) {
                            matched_key = candidate;
                        }
                        break;
                    }
                }
            }

            if (matched_key !== null) {
                const doc_text = command_docs.get(matched_key);
                if (doc_text) {
                    if (reporter) {
                        reporter.sendTelemetryEvent("cmd_hover_provider", {
                            word: matched_key,
                            type: "command",
                            was_abbreviation: String(matched_was_abbreviation),
                        });
                    }
                    return new vscode.Hover(new vscode.MarkdownString(doc_text), range);
                }
                // Command recognised but no doc file yet — don't fall through to function hover.
                return undefined;
            }

            // --- Function hover (fallback) ---
            if (view_functions.has(word)) {
                const text = view_functions.get(word);
                if (reporter) {
                    reporter.sendTelemetryEvent("cmd_hover_provider", {
                        word: word,
                        type: "function",
                        was_abbreviation: "false",
                    });
                }
                return new vscode.Hover(new vscode.MarkdownString(text), range);
            }

            if (reporter) {
                reporter.sendTelemetryEvent("cmd_hover_miss", { word });
            }
            return undefined;
        },
    };
}
exports.cmd_hover_provider = cmd_hover_provider;

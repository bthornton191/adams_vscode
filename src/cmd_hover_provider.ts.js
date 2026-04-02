const vscode = require("vscode");
const { strip_argument_pairs } = require("./cmd_completion_provider.ts.js");

/**
 * Walks backward through & continuation lines and returns the FULL current line
 * joined with any preceding continuation lines. Unlike get_full_command_context,
 * this includes the entire current line (not truncated at the cursor position) so
 * that the first keyword of a multi-word command is always visible in the context.
 * @param {object} document
 * @param {object} position
 * @returns {string}
 */
function get_full_command_text(document, position) {
    const parts = [document.lineAt(position.line).text];
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
 * @param {Map<string, string>} view_functions  function name → markdown doc
 * @param {Object} view_commands                structured.json (command key → arg[])
 * @param {Map<string, string>} command_docs    command key → markdown doc
 * @param {object|null} reporter
 */
function cmd_hover_provider(
    view_functions,
    view_commands = {},
    command_docs = new Map(),
    reporter = null,
) {
    return {
        provideHover(document, position, token) {
            const range = document.getWordRangeAtPosition(position);
            if (!range) return undefined;

            const word = document.getText(range).toLowerCase();

            // --- Command hover ---
            // Use the FULL current line (plus any & continuation lines before it) so
            // that hovering the first keyword of a multi-word command works correctly.
            const full_text = get_full_command_text(document, position);
            const command_context = strip_argument_pairs(full_text).toLowerCase();
            const context_words = command_context.trim().split(/\s+/).filter(Boolean);

            // Longest-match: try progressively shorter left-side prefixes so that
            // e.g. "view center view_name=..." resolves to "view center".
            let matched_key = null;
            for (let len = context_words.length; len >= 1; len--) {
                const candidate = context_words.slice(0, len).join(" ");
                if (view_commands.hasOwnProperty(candidate)) {
                    // Only show command hover if the hovered word is actually one of
                    // the tokens that make up this command key (not an argument value).
                    if (candidate.split(" ").some((kw) => kw === word)) {
                        matched_key = candidate;
                    }
                    break; // Stop at the longest recognised command key regardless
                }
            }

            if (matched_key !== null) {
                const doc_text = command_docs.get(matched_key);
                if (doc_text) {
                    if (reporter) {
                        reporter.sendTelemetryEvent("cmd_hover_provider", {
                            word: matched_key,
                            type: "command",
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
                    });
                }
                return new vscode.Hover(new vscode.MarkdownString(text), range);
            }

            return undefined;
        },
    };
}
exports.cmd_hover_provider = cmd_hover_provider;

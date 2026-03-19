const vscode = require("vscode");

/**
 * @param {Map<string, string>} function_names
 * @param {Object} commands         command → string[]              (structured.json)
 * @param {Object} arg_options      command → {argName: string[]}   (argument_options.json)
 * @param {Map<string, string>} command_docs  command → markdown doc string
 * @param {object|null} reporter
 * @returns {vscode.CompletionItemProvider}
 */
function cmd_completion_provider(
    function_names,
    commands,
    arg_options = {},
    command_docs = new Map(),
    reporter = null,
) {
    return {
        provideCompletionItems(document, position, token, context) {
            let completions = [];
            const range = document.getWordRangeAtPosition(position);
            const word = document.getText(range).toLowerCase();
            const current_line = document.lineAt(position).text.substr(0, position.character);

            // Reconstruct the full command text across & continuation lines
            const full_text = get_full_command_context(document, position);

            // Strip all argument=value pairs (including the incomplete trailing one)
            // to isolate the command name.
            const command_key = full_text
                .replace(/\s+\w+\s*=\s*([^\s]+|"[^"]*")/g, "") // complete pairs
                .replace(/\s+\w+\s*=\s*\S*$/, "") // trailing incomplete
                .trim();

            // Functions
            for (var [name, doc] of function_names.entries()) {
                if (name.startsWith(word)) {
                    let completion = new vscode.CompletionItem(name);
                    completion.kind = vscode.CompletionItemKind.Function;
                    completion.command = { command: "editor.action.showHover" };
                    completion.documentation = new vscode.MarkdownString(doc);
                    completions.push(completion);
                }
            }

            // Arguments
            // If the stripped full text exactly matches a command, we are in the arguments section
            if (commands.hasOwnProperty(command_key)) {
                // Collect argument names already used across all continuation lines
                const used_args = new Set();
                for (const m of full_text.matchAll(/(\w+)\s*=/g)) {
                    used_args.add(m[1]);
                }

                // Get the indentation
                if (vscode.workspace.getConfiguration("editor").get("insertSpaces")) {
                    let n_spaces = vscode.workspace.getConfiguration("editor").get("tabSize");
                    var indent_type = " ".repeat(n_spaces);
                } else {
                    var indent_type = "\t";
                }
                var indent = indent_type.repeat(get_indent_level(current_line, indent_type) + 1);

                const cmd_doc = command_docs.get(command_key);

                for (let arg of commands[command_key]) {
                    if (used_args.has(arg)) continue;
                    let label = current_line.endsWith(" ") ? arg : " " + arg;
                    let completion = new vscode.CompletionItem(label + "=");
                    completion.kind = vscode.CompletionItemKind.Field;
                    if (cmd_doc) {
                        completion.documentation = new vscode.MarkdownString(cmd_doc);
                    }
                    completions.push(completion);
                }
            }

            // Argument Values
            // Detect when the cursor is right after `arg_name=` or `arg_name=partial`
            // Pattern: some text ending in  word= or word=partial  (no space after =)
            const arg_value_match = current_line.match(/(\w+)=(\w*)$/);
            if (arg_value_match && commands.hasOwnProperty(command_key)) {
                const arg_name = arg_value_match[1];
                const partial = arg_value_match[2].toLowerCase();
                const cmd_options = (arg_options || {})[command_key];
                const values = cmd_options && cmd_options[arg_name];
                if (values) {
                    const value_completions = [];
                    for (const val of values) {
                        if (!partial || val.toLowerCase().startsWith(partial)) {
                            let completion = new vscode.CompletionItem(val);
                            completion.kind = vscode.CompletionItemKind.EnumMember;
                            value_completions.push(completion);
                        }
                    }
                    if (value_completions.length > 0) {
                        return value_completions;
                    }
                }
            }

            // Commands — only suggest on the first (non-continuation) line
            const on_continuation =
                position.line > 0 && /&[ \t]*(!.*)?$/.test(document.lineAt(position.line - 1).text);

            if (!on_continuation) {
                for (let [command, args] of Object.entries(commands)) {
                    if (
                        command.startsWith(current_line.trim()) &&
                        command.split(" ").length >= current_line.trimStart().split(" ").length &&
                        command.toLowerCase() !== current_line.trim().toLowerCase()
                    ) {
                        let idx = current_line.trimStart().split(" ").length;
                        let next_word = command.split(" ")[idx - 1];
                        let completion = new vscode.CompletionItem(next_word + " ");
                        completion.kind = vscode.CompletionItemKind.Interface;
                        completion.command = {
                            command: "editor.action.triggerSuggest",
                            title: "Re-trigger completions...",
                        };
                        const doc = command_docs.get(command);
                        if (doc) {
                            completion.documentation = new vscode.MarkdownString(doc);
                        }
                        if (!completions.some((c) => c.label === next_word + " ")) {
                            completions.push(completion);
                        }
                    }
                }
            }

            // Report telemetry
            if (reporter) {
                reporter.sendTelemetryEvent("cmd_completion_provider");
            }

            return completions;
        },
    };
}
exports.cmd_completion_provider = cmd_completion_provider;

/**
 * Walks backward through & continuation lines to reconstruct the full command text
 * up to (but not including) the position of the cursor.
 * @param {object} document
 * @param {object} position
 * @returns {string}
 */
function get_full_command_context(document, position) {
    const current_text = document.lineAt(position).text.substr(0, position.character);
    const parts = [current_text];
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

function get_indent_level(line, indent_type) {
    var indent_count = 0;
    for (let char of line) {
        if (char === indent_type) {
            indent_count++;
        } else {
            break;
        }
    }
    return indent_count;
}

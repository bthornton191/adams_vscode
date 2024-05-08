const vscode = require("vscode");
const path = require("path");
const fs = require("fs");

/**
 * @returns {vscode.DocumentLinkProvider}
 */
function link_provider() {
    return {
        /**
         * Provide links for all windows and linux file paths. Paths with spaces will need to be
         * enclosed in single or double quotes.
         * @param {vscode.TextDocument} document
         * @param {vscode.CancellationToken} token
         * @returns {vscode.DocumentLink[]}
         */
        provideDocumentLinks(document, token) {
            const links = [];
            const text = document.getText().replace(/\\/g, "/");

            // Regex to match filepaths on windows and linux
            const regex_quoted =
                /(?<="|')(?:[A-Za-z]:)?(?:\/+)[^"'<>|:\n\r*?]+\.[a-zA-Z0-9]+(?="|')/g;
            const regex_unquoted = /((?:[A-Za-z]:)?(?:\/+)[^"'<>|:\n\r*? ]+\.[a-zA-Z0-9]+)/g;
            const regex_local = /[^"'<>|:\n\r*? ]+\.[a-zA-Z0-9]+/g;
            let match;

            while ((match = regex_quoted.exec(text)) || (match = regex_unquoted.exec(text))) {
                const file = path.normalize(match[0]);

                // Add the link if the file exists and isn't already in the links
                if (fs.existsSync(file) && !links.some((link) => link.target.fsPath === file)) {
                    const range = new vscode.Range(
                        document.positionAt(match.index),
                        document.positionAt(match.index + match[0].length)
                    );
                    links.push(new vscode.DocumentLink(range, vscode.Uri.file(file)));
                }
            }

            // Local paths
            while ((match = regex_local.exec(text))) {
                // Append the file to the current file parent directory
                var file = path.join(path.dirname(document.uri.fsPath), match[0]);

                // Add the link if the file exists
                if (fs.existsSync(file)) {
                    const range = new vscode.Range(
                        document.positionAt(match.index),
                        document.positionAt(match.index + match[0].length)
                    );
                    links.push(new vscode.DocumentLink(range, vscode.Uri.file(file)));
                }
            }
            return links;
        },
    };
}

exports.link_provider = link_provider;

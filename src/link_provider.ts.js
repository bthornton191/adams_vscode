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
            const regex =
                // /(?<quoted>(?<="|')(?:[A-Za-z]:)?(?:\/+)[^"'<>|:\n\r*?]+\.[a-zA-Z0-9]+(?="|'))|(?<unquoted>((?:[A-Za-z]:)?(?:\/+)[^"'<>|:\n\r*? ]+\.[a-zA-Z0-9]+))(?<pos>(, line \d+)|(:\d+(:\d+)?))?/g;
                /(?:(?:(?:"|')(?<quoted>(?:[A-Za-z]:)?(?:\/+)[^"'<>|:\n\r*?]+\.[a-zA-Z0-9]+)(?:"|'))|(?<unquoted>((?:[A-Za-z]:)?(?:\/+)[^"'<>|:\n\r*? ]+\.[a-zA-Z0-9]+)))(?<line>, line \d+)?/g;
            let match;

            while ((match = regex.exec(text))) {
                var file = path.normalize(match.groups?.quoted || match.groups?.unquoted);

                const range = new vscode.Range(
                    document.positionAt(match.index),
                    document.positionAt(match.index + match[0].length)
                );

                // Add the link if the file exists and isn't already in the links
                if (
                    fs.existsSync(file) &&
                    !links.some(
                        (link) =>
                            link.range.isEqual(range) ||
                            link.range.contains(range) ||
                            range.contains(link.range)
                    )
                ) {
                    var uri = vscode.Uri.file(file);
                    // Get the position
                    if (match.groups?.line) {
                        // Get the line number
                        const line = parseInt(match.groups.line.replace(", line ", ""));
                        uri = uri.with({ fragment: `L${line}` });
                    }
                    links.push(new vscode.DocumentLink(range, uri));
                }
            }

            return links;
        },
    };
}

/**
 * Add a link to the links array if the file exists and isn't already in the links
 * @param {vscode.TextDocument} document
 * @param {RegExpExecArray} match
 * @param {string} file
 * @param {vscode.DocumentLink[]} links
 **/
function addLink(document, match, file, links) {
    const range = new vscode.Range(
        document.positionAt(match.index),
        document.positionAt(match.index + match[0].length)
    );

    // Add the link if the file exists and isn't already in the links
    if (
        fs.existsSync(file) &&
        !links.some(
            (link) =>
                link.range.isEqual(range) ||
                link.range.contains(range) ||
                range.contains(link.range)
        )
    ) {
        links.push(new vscode.DocumentLink(range, vscode.Uri.file(file)));
    }
}

exports.link_provider = link_provider;

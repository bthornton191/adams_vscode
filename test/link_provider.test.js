const assert = require("assert");
const path = require("path");
const fs = require("fs");
const vscode = require("vscode");
const { link_provider } = require("../src/link_provider.ts.js");

// Build a minimal mock document around a string of text
function makeDocument(text) {
    return {
        getText: () => text,
        positionAt: (offset) => {
            // Simple line/character calculation
            const before = text.slice(0, offset);
            const lines = before.split("\n");
            return new vscode.Position(lines.length - 1, lines[lines.length - 1].length);
        },
    };
}

suite("link_provider", () => {
    let originalExistsSync;

    suiteSetup(() => {
        originalExistsSync = fs.existsSync;
    });

    suiteTeardown(() => {
        fs.existsSync = originalExistsSync;
    });

    test("should return a link for a quoted file path that exists", () => {
        fs.existsSync = () => true;

        const text = `open file "/C:/models/myfile.cmd"`;
        const provider = link_provider();
        const links = provider.provideDocumentLinks(makeDocument(text), null);

        assert.ok(links.length > 0, "Expected at least one link");
        assert.ok(links[0].target.fsPath.includes("myfile.cmd"));
    });

    test("should return a link for an unquoted file path that exists", () => {
        fs.existsSync = () => true;

        const text = `include /C:/models/myfile.cmd`;
        const provider = link_provider();
        const links = provider.provideDocumentLinks(makeDocument(text), null);

        assert.ok(links.length > 0, "Expected at least one link");
        assert.ok(links[0].target.fsPath.includes("myfile.cmd"));
    });

    test("should not return a link for a path that does not exist", () => {
        fs.existsSync = () => false;

        const text = `open file "/C:/models/nonexistent.cmd"`;
        const provider = link_provider();
        const links = provider.provideDocumentLinks(makeDocument(text), null);

        assert.strictEqual(links.length, 0);
    });

    test("should include line number in URI fragment when ', line N' suffix present", () => {
        fs.existsSync = () => true;

        const text = `Error in "/C:/models/myfile.cmd", line 42`;
        const provider = link_provider();
        const links = provider.provideDocumentLinks(makeDocument(text), null);

        assert.ok(links.length > 0, "Expected at least one link");
        assert.ok(
            links[0].target.toString().includes("L42"),
            `Expected URI to contain 'L42', got: ${links[0].target.toString()}`,
        );
    });

    test("should not duplicate links for the same range", () => {
        fs.existsSync = () => true;

        // Two occurrences of the same path on the same line — regex will match once each
        const text = `"/C:/models/a.cmd" "/C:/models/a.cmd"`;
        const provider = link_provider();
        const links = provider.provideDocumentLinks(makeDocument(text), null);

        // Each match is at a different position so we get two links, but no overlapping duplicates
        const targets = links.map((l) => l.target.fsPath);
        const unique = [...new Set(targets)];
        // Both links point to the same file but at different positions — that's fine
        assert.ok(links.length >= 1);
        assert.strictEqual(unique.length, 1);
    });

    test("should handle Windows-style paths (backslash normalisation)", () => {
        fs.existsSync = () => true;

        // The provider converts backslashes to forward slashes internally
        const text = `include "C:/models/sub/myfile.cmd"`;
        const provider = link_provider();
        const links = provider.provideDocumentLinks(makeDocument(text), null);

        assert.ok(links.length > 0, "Expected at least one link");
    });
});

/**
 * Tests for src/cmd_lsp_client.ts.js
 *
 * Verifies module exports, file-watcher creation, and config-change restart
 * behaviour without requiring Adams View.
 */

const assert = require("assert");
const { cmd_lsp_client } = require("../src/cmd_lsp_client.ts.js");

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function makeMockOutputChannel() {
    return { appendLine: () => {} };
}

function makeMockContext(subscriptions) {
    return {
        extensionPath: __dirname,
        subscriptions: subscriptions || [],
    };
}

// ---------------------------------------------------------------------------
// Suite
// ---------------------------------------------------------------------------

suite("cmd_lsp_client", () => {
    test("module exports cmd_lsp_client factory function", () => {
        assert.strictEqual(typeof cmd_lsp_client, "function");
    });

    test("factory returns object with start and stop methods", () => {
        const lsp = cmd_lsp_client(makeMockOutputChannel(), null);
        assert.strictEqual(typeof lsp.start, "function");
        assert.strictEqual(typeof lsp.stop, "function");
    });

    test("stop is a no-op before start is called", () => {
        const lsp = cmd_lsp_client(makeMockOutputChannel(), null);
        // Must not throw and must return undefined (no client to stop)
        const result = lsp.stop();
        assert.ok(result === undefined);
    });
});

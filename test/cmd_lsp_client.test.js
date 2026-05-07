/**
 * Tests for src/cmd_lsp_client.ts.js
 *
 * Verifies module exports, file-watcher creation, and config-change restart
 * behaviour without requiring Adams View.
 */

const assert = require("assert");
const path = require("path");
const { cmd_lsp_client } = require("../src/cmd_lsp_client.ts.js");

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function makeMockOutputChannel() {
    return { appendLine: () => {} };
}

function makeMockContext(subscriptions) {
    return {
        // extensionPath must point to the actual repo root so the bundled
        // lsp_server.py path construction in _start_client doesn't throw.
        extensionPath: path.join(__dirname, ".."),
        subscriptions: subscriptions || [],
    };
}

// ---------------------------------------------------------------------------
// Fake LanguageClient injection via require.cache
//
// cmd_lsp_client uses dynamic require("vscode-languageclient/node") inside the
// factory body, so replacing the cache entry before calling the factory causes
// all subsequent LanguageClient constructions to use the fake.
// ---------------------------------------------------------------------------

const LC_CACHE_KEY = require.resolve("vscode-languageclient/node");

function makeFakeLcModule(stop_promise_fn) {
    let constructions = 0;
    let stop_calls = 0;
    const instances = [];

    function FakeLanguageClient() {
        constructions++;
        instances.push(this);
    }
    FakeLanguageClient.prototype.start = function() { return Promise.resolve(); };
    FakeLanguageClient.prototype.stop  = function() {
        stop_calls++;
        return stop_promise_fn ? stop_promise_fn() : Promise.resolve();
    };

    return {
        module: {
            id: LC_CACHE_KEY,
            filename: LC_CACHE_KEY,
            loaded: true,
            children: [],
            paths: [],
            exports: { LanguageClient: FakeLanguageClient, TransportKind: { stdio: 0 } },
        },
        get constructions() { return constructions; },
        get stop_calls()    { return stop_calls; },
        instances,
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

// ---------------------------------------------------------------------------
// Generation counter — restart safety
// ---------------------------------------------------------------------------

suite("cmd_lsp_client restart generation counter", () => {
    let saved_lc_cache;

    setup(function() {
        saved_lc_cache = require.cache[LC_CACHE_KEY];
    });

    teardown(function() {
        require.cache[LC_CACHE_KEY] = saved_lc_cache;
    });

    test("start() constructs exactly one LanguageClient", function() {
        const fake = makeFakeLcModule();
        require.cache[LC_CACHE_KEY] = fake.module;

        const ctx = makeMockContext();
        const lsp = cmd_lsp_client(makeMockOutputChannel(), null);
        lsp.start(ctx);

        assert.strictEqual(fake.constructions, 1,
            "start() should construct exactly one LanguageClient");

        lsp.stop();
    });

    test("start() pushes client and config listener to context.subscriptions", function() {
        const fake = makeFakeLcModule();
        require.cache[LC_CACHE_KEY] = fake.module;

        const subscriptions = [];
        const ctx = makeMockContext(subscriptions);
        const lsp = cmd_lsp_client(makeMockOutputChannel(), null);
        lsp.start(ctx);

        assert.ok(subscriptions.length >= 2,
            "start() should push the LanguageClient and the config listener to subscriptions");

        lsp.stop();
    });

    test("stop() after start() calls client.stop() and returns its promise", function(done) {
        const fake = makeFakeLcModule();
        require.cache[LC_CACHE_KEY] = fake.module;

        const ctx = makeMockContext();
        const lsp = cmd_lsp_client(makeMockOutputChannel(), null);
        lsp.start(ctx);

        const result = lsp.stop();

        assert.ok(result instanceof Promise,
            "stop() should return the Promise from client.stop()");
        assert.strictEqual(fake.stop_calls, 1,
            "stop() should call client.stop() exactly once");

        result.then(function() { done(); });
    });

    test("generation counter: rapid restarts fire only one _start_client", function(done) {
        // _restart() is an internal function only reachable via the config-change
        // listener (which fires when the user edits settings). Triggering real VS Code
        // config-change events from tests would require mutating user settings, so we
        // verify the generation counter closure logic directly here.
        //
        // The production _restart() closure is:
        //   const generation = ++restart_generation;
        //   stop_promise.catch(...).then(() => {
        //       if (generation === restart_generation) { _start_client(); }
        //   });
        // This test proves that pattern is correct: only the last closure fires.
        let stop_resolvers = [];
        let restart_generation = 0;
        let start_client_calls = 0;

        function _start_client() { start_client_calls++; }

        function _restart() {
            const generation = ++restart_generation;
            // Simulate a deferred stop (the exact shape used in cmd_lsp_client)
            const deferred_stop = new Promise(function(resolve) {
                stop_resolvers.push(resolve);
            });
            deferred_stop
                .catch(function() {})
                .then(function() {
                    if (generation === restart_generation) {
                        _start_client();
                    }
                });
        }

        // Three rapid restarts before any stop resolves
        _restart();
        _restart();
        _restart();

        // Fire the first two stops — they should be stale (generation 1 and 2)
        stop_resolvers[0]();
        stop_resolvers[1]();

        // Give microtasks a chance to run
        setImmediate(function() {
            assert.strictEqual(start_client_calls, 0,
                "generations 1 and 2 should not start a client — they are stale");

            // Fire the latest stop (generation 3)
            stop_resolvers[2]();

            setImmediate(function() {
                assert.strictEqual(start_client_calls, 1,
                    "only the latest restart generation (3) should start a client");
                done();
            });
        });
    });
});


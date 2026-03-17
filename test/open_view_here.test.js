const assert = require("assert");
const path = require("path");
const child_process = require("child_process");
const { open_view_here } = require("../src/open_view_here.ts.js");

// Minimal fakes
const output_channel = { appendLine: () => {} };

function makeUri(fsPath) {
    return { fsPath };
}

function makeMockReporter() {
    const calls = { telemetry: [], errors: [] };
    return {
        sendTelemetryEvent: (...args) => calls.telemetry.push(args),
        sendTelemetryErrorEvent: (...args) => calls.errors.push(args),
        calls,
    };
}

suite("open_view_here", () => {
    let originalExecFile;

    suiteSetup(() => {
        originalExecFile = child_process.execFile;
    });

    suiteTeardown(() => {
        child_process.execFile = originalExecFile;
    });

    test("should call execFile with correct arguments", (done) => {
        const capturedArgs = {};
        child_process.execFile = (file, args, opts, cb) => {
            capturedArgs.file = file;
            capturedArgs.args = args;
            capturedArgs.opts = opts;
            cb(null, "", "");
        };

        const uri = makeUri("C:/projects/mymodel");
        open_view_here(output_channel, null)(uri);

        // adams_launch_command comes from vscode config (null in test env)
        assert.deepStrictEqual(capturedArgs.args, ["aview", "ru-s", "i"]);
        assert.strictEqual(capturedArgs.opts.cwd, uri.fsPath);
        done();
    });

    test("should not crash when reporter is null", (done) => {
        child_process.execFile = (file, args, opts, cb) => cb(null, "", "");

        const uri = makeUri("C:/projects/mymodel");

        assert.doesNotThrow(() => {
            open_view_here(output_channel, null)(uri);
        });
        done();
    });

    test("should send telemetry event when reporter is provided", (done) => {
        child_process.execFile = (file, args, opts, cb) => cb(null, "", "");

        const reporter = makeMockReporter();
        const uri = makeUri("C:/projects/mymodel");

        open_view_here(output_channel, reporter)(uri);

        assert.strictEqual(reporter.calls.telemetry.length, 1);
        assert.strictEqual(reporter.calls.telemetry[0][0], "open_view_here");
        done();
    });

    test("should send error telemetry when execFile returns an error", (done) => {
        const err = new Error("spawn failed");
        child_process.execFile = (file, args, opts, cb) => cb(err, "", "");

        const reporter = makeMockReporter();
        const uri = makeUri("C:/projects/mymodel");

        open_view_here(output_channel, reporter)(uri);

        assert.strictEqual(reporter.calls.errors.length, 1);
        assert.strictEqual(reporter.calls.errors[0][0], "open_view_here");
        assert.strictEqual(reporter.calls.errors[0][1].error, err.message);
        done();
    });

    test("should send error telemetry when execFile returns stderr", (done) => {
        child_process.execFile = (file, args, opts, cb) => cb(null, "", "some stderr output");

        const reporter = makeMockReporter();
        const uri = makeUri("C:/projects/mymodel");

        open_view_here(output_channel, reporter)(uri);

        assert.strictEqual(reporter.calls.errors.length, 1);
        assert.strictEqual(reporter.calls.errors[0][0], "open_view_here");
        done();
    });

    test("should not crash when reporter is null and execFile errors", (done) => {
        const err = new Error("spawn failed");
        child_process.execFile = (file, args, opts, cb) => cb(err, "", "");

        const uri = makeUri("C:/projects/mymodel");

        assert.doesNotThrow(() => {
            open_view_here(output_channel, null)(uri);
        });
        done();
    });
});

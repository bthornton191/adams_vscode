const assert = require("assert");
const path = require("path");
const child_process = require("child_process");
const fs = require("fs");
const vscode = require("vscode");
const { open_in_view } = require("../src/open_in_view.ts.js");

// Minimal fakes
const output_channel = { appendLine: () => {} };

function makeContext(viewLauncherPath) {
    return { asAbsolutePath: () => viewLauncherPath };
}

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

function makeMockChild() {
    const listeners = {};
    return {
        unref: function () { this.unrefCalled = true; },
        on: function (event, cb) { listeners[event] = cb; },
        unrefCalled: false,
        listeners,
    };
}

suite("open_in_view", () => {
    let originalSpawn;
    let originalExistsSync;
    const FAKE_LAUNCH_CMD = "C:/fake/mdi.bat";

    suiteSetup(async () => {
        await vscode.workspace
            .getConfiguration("msc-adams")
            .update("adamsLaunchCommand", FAKE_LAUNCH_CMD, vscode.ConfigurationTarget.Workspace);
        originalSpawn = child_process.spawn;
        originalExistsSync = fs.existsSync;
    });

    suiteTeardown(async () => {
        child_process.spawn = originalSpawn;
        fs.existsSync = originalExistsSync;
        await vscode.workspace
            .getConfiguration("msc-adams")
            .update("adamsLaunchCommand", null, vscode.ConfigurationTarget.Workspace);
    });

    setup(() => {
        // By default, pretend the launch command exists on disk
        fs.existsSync = (p) => p === FAKE_LAUNCH_CMD ? true : originalExistsSync(p);
    });

    teardown(() => {
        fs.existsSync = originalExistsSync;
    });

    test("should not spawn when launch command path does not exist", (done) => {
        let spawnCalled = false;
        child_process.spawn = () => { spawnCalled = true; return makeMockChild(); };
        fs.existsSync = () => false;

        const context = makeContext("C:/fake/launcher.bat");
        const uri = makeUri("C:/models/mymodel.cmd");
        open_in_view(context, output_channel, null)(uri);

        assert.strictEqual(spawnCalled, false,
            "spawn should not be called when the launch command does not exist");
        done();
    });

    test("should send config_missing telemetry when launch command does not exist", (done) => {
        child_process.spawn = () => makeMockChild();
        fs.existsSync = () => false;

        const reporter = makeMockReporter();
        const context = makeContext("C:/fake/launcher.bat");
        const uri = makeUri("C:/models/mymodel.cmd");
        open_in_view(context, output_channel, reporter)(uri);

        assert.strictEqual(reporter.calls.errors.length, 1);
        assert.strictEqual(reporter.calls.errors[0][0], "open_in_view");
        assert.strictEqual(reporter.calls.errors[0][1].error_type, "config_missing");
        done();
    });

    test("should call spawn with correct arguments", (done) => {
        const capturedArgs = {};
        child_process.spawn = (file, args, opts) => {
            capturedArgs.file = file;
            capturedArgs.args = args;
            capturedArgs.opts = opts;
            return makeMockChild();
        };

        const launcher = "C:/fake/launcher.bat";
        const context = makeContext(launcher);
        const uri = makeUri("C:/models/mymodel.cmd");
        const handler = open_in_view(context, output_channel, null);

        handler(uri);

        assert.strictEqual(capturedArgs.file, launcher);
        assert.strictEqual(capturedArgs.args[0], path.basename(uri.fsPath));
        assert.strictEqual(capturedArgs.args[1], FAKE_LAUNCH_CMD);
        assert.strictEqual(capturedArgs.opts.cwd, path.dirname(uri.fsPath));
        done();
    });

    test("should spawn with detached:true so the process gets its own window", (done) => {
        const capturedArgs = {};
        child_process.spawn = (file, args, opts) => {
            capturedArgs.opts = opts;
            return makeMockChild();
        };

        const launcher = "C:/fake/launcher.bat";
        const context = makeContext(launcher);
        const uri = makeUri("C:/models/mymodel.cmd");

        open_in_view(context, output_channel, null)(uri);

        assert.strictEqual(capturedArgs.opts.detached, true,
            "Process must be detached to get its own window on Windows");
        done();
    });

    test("should spawn with shell:true so .bat files are handled correctly", (done) => {
        const capturedArgs = {};
        child_process.spawn = (file, args, opts) => {
            capturedArgs.opts = opts;
            return makeMockChild();
        };

        const launcher = "C:/fake/launcher.bat";
        const context = makeContext(launcher);
        const uri = makeUri("C:/models/mymodel.cmd");

        open_in_view(context, output_channel, null)(uri);

        assert.strictEqual(capturedArgs.opts.shell, true,
            "shell:true is required for .bat file execution on Windows");
        done();
    });

    test("should call unref so extension host does not wait for Adams to exit", (done) => {
        let mockChild;
        child_process.spawn = (file, args, opts) => {
            mockChild = makeMockChild();
            return mockChild;
        };

        const launcher = "C:/fake/launcher.bat";
        const context = makeContext(launcher);
        const uri = makeUri("C:/models/mymodel.cmd");

        open_in_view(context, output_channel, null)(uri);

        assert.strictEqual(mockChild.unrefCalled, true,
            "unref() must be called so the extension host can exit independently");
        done();
    });

    test("should not crash when reporter is null", (done) => {
        child_process.spawn = (file, args, opts) => makeMockChild();

        const context = makeContext("C:/fake/launcher.bat");
        const uri = makeUri("C:/models/mymodel.cmd");

        assert.doesNotThrow(() => {
            open_in_view(context, output_channel, null)(uri);
        });
        done();
    });

    test("should send telemetry event when reporter is provided", (done) => {
        child_process.spawn = (file, args, opts) => makeMockChild();

        const reporter = makeMockReporter();
        const context = makeContext("C:/fake/launcher.bat");
        const uri = makeUri("C:/models/mymodel.cmd");

        open_in_view(context, output_channel, reporter)(uri);

        assert.strictEqual(reporter.calls.telemetry.length, 1);
        assert.strictEqual(reporter.calls.telemetry[0][0], "open_in_view");
        done();
    });

    test("should send error telemetry when spawn emits an error", (done) => {
        let mockChild;
        child_process.spawn = (file, args, opts) => {
            mockChild = makeMockChild();
            return mockChild;
        };

        const reporter = makeMockReporter();
        const context = makeContext("C:/fake/launcher.bat");
        const uri = makeUri("C:/models/mymodel.cmd");

        open_in_view(context, output_channel, reporter)(uri);

        // Simulate error event
        const err = new Error("spawn failed");
        mockChild.listeners.error(err);

        assert.strictEqual(reporter.calls.errors.length, 1);
        assert.strictEqual(reporter.calls.errors[0][0], "open_in_view");
        assert.strictEqual(reporter.calls.errors[0][1].error_type, "process_error");
        assert.strictEqual(reporter.calls.errors[0][1].error_message, err.message);
        done();
    });

    test("should not crash when reporter is null and spawn emits an error", (done) => {
        let mockChild;
        child_process.spawn = (file, args, opts) => {
            mockChild = makeMockChild();
            return mockChild;
        };

        const context = makeContext("C:/fake/launcher.bat");
        const uri = makeUri("C:/models/mymodel.cmd");
        open_in_view(context, output_channel, null)(uri);

        assert.doesNotThrow(() => {
            mockChild.listeners.error(new Error("spawn failed"));
        });
        done();
    });
});

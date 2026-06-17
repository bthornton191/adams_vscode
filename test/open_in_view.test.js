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

/**
 * Capture a child_process.exec call: exec(command, options, callback).
 * The launcher is fire-and-forget, so the return value is unused.
 */
function captureExec() {
    const c = {};
    child_process.exec = (command, options, callback) => {
        c.command = command;
        c.options = options;
        c.callback = callback;
        return {};
    };
    return c;
}

suite("open_in_view", () => {
    let originalExec;
    let originalExistsSync;
    // Use a path with spaces â€” this is the regression case that broke repeatedly
    const FAKE_LAUNCH_CMD = "C:/Program Files/fake/mdi.bat";

    suiteSetup(async () => {
        await vscode.workspace
            .getConfiguration("msc-adams")
            .update("adamsLaunchCommand", FAKE_LAUNCH_CMD, vscode.ConfigurationTarget.Workspace);
        originalExec = child_process.exec;
        originalExistsSync = fs.existsSync;
    });

    suiteTeardown(async () => {
        child_process.exec = originalExec;
        fs.existsSync = originalExistsSync;
        await vscode.workspace
            .getConfiguration("msc-adams")
            .update("adamsLaunchCommand", null, vscode.ConfigurationTarget.Workspace);
    });

    setup(() => {
        fs.existsSync = (p) => p === FAKE_LAUNCH_CMD ? true : originalExistsSync(p);
    });

    teardown(() => {
        child_process.exec = originalExec;
        fs.existsSync = originalExistsSync;
    });

    test("should not exec when launch command path does not exist", (done) => {
        let execCalled = false;
        child_process.exec = () => { execCalled = true; return {}; };
        fs.existsSync = () => false;

        const context = makeContext("C:/fake/launcher.bat");
        open_in_view(context, output_channel, null)(makeUri("C:/models/mymodel.cmd"));

        assert.strictEqual(execCalled, false,
            "exec should not be called when the launch command does not exist");
        done();
    });

    test("should send config_missing telemetry when launch command does not exist", (done) => {
        child_process.exec = () => ({});
        fs.existsSync = () => false;

        const reporter = makeMockReporter();
        open_in_view(makeContext("C:/fake/launcher.bat"), output_channel, reporter)(makeUri("C:/models/mymodel.cmd"));

        assert.strictEqual(reporter.calls.errors.length, 1);
        assert.strictEqual(reporter.calls.errors[0][0], "open_in_view");
        assert.strictEqual(reporter.calls.errors[0][1].error_type, "config_missing");
        done();
    });

    test("should exec a command containing launcher, filename, and Adams launch path", (done) => {
        const launcher = "C:/fake/launcher.bat";
        const c = captureExec();

        const uri = makeUri("C:/models/mymodel.cmd");
        open_in_view(makeContext(launcher), output_channel, null)(uri);

        assert.strictEqual(typeof c.command, "string", "exec must be called with a command string");
        assert.ok(c.command.includes(launcher), "command must contain the launcher path");
        assert.ok(c.command.includes(path.basename(uri.fsPath)), "command must contain the model filename");
        assert.ok(c.command.includes(FAKE_LAUNCH_CMD), "command must contain the Adams launch path");
        done();
    });

    test("should quote the launcher, filename, and launch path so spaces survive", (done) => {
        // open_in_view wraps each token in quotes; the Adams launch path
        // ("C:/Program Files/...") contains spaces and must stay one token.
        const launcher = "C:/fake/launcher.bat";
        const c = captureExec();

        const uri = makeUri("C:/models/mymodel.cmd");
        open_in_view(makeContext(launcher), output_channel, null)(uri);

        assert.ok(c.command.includes(`"${launcher}"`), "launcher must be quoted");
        assert.ok(c.command.includes(`"${path.basename(uri.fsPath)}"`), "filename must be quoted");
        assert.ok(c.command.includes(`"${FAKE_LAUNCH_CMD}"`), "launch path must be quoted");
        done();
    });

    test("should pass cwd as the directory containing the model file", (done) => {
        const c = captureExec();

        const uri = makeUri("C:/models/mymodel.cmd");
        open_in_view(makeContext("C:/fake/launcher.bat"), output_channel, null)(uri);

        assert.strictEqual(c.options.cwd, path.dirname(uri.fsPath));
        done();
    });

    test("should not crash when reporter is null", (done) => {
        child_process.exec = () => ({});

        assert.doesNotThrow(() => {
            open_in_view(makeContext("C:/fake/launcher.bat"), output_channel, null)(makeUri("C:/models/mymodel.cmd"));
        });
        done();
    });

    test("should send telemetry event when reporter is provided", (done) => {
        child_process.exec = () => ({});

        const reporter = makeMockReporter();
        open_in_view(makeContext("C:/fake/launcher.bat"), output_channel, reporter)(makeUri("C:/models/mymodel.cmd"));

        assert.strictEqual(reporter.calls.telemetry.length, 1);
        assert.strictEqual(reporter.calls.telemetry[0][0], "open_in_view");
        done();
    });

    test("should send error telemetry when the exec callback receives an error", (done) => {
        const c = captureExec();

        const reporter = makeMockReporter();
        open_in_view(makeContext("C:/fake/launcher.bat"), output_channel, reporter)(makeUri("C:/models/mymodel.cmd"));

        const err = new Error("launch failed");
        c.callback(err);

        assert.strictEqual(reporter.calls.errors.length, 1);
        assert.strictEqual(reporter.calls.errors[0][0], "open_in_view");
        assert.strictEqual(reporter.calls.errors[0][1].error_type, "process_error");
        assert.strictEqual(reporter.calls.errors[0][1].error_message, err.message);
        done();
    });

    test("should not crash when reporter is null and the exec callback errors", (done) => {
        const c = captureExec();

        open_in_view(makeContext("C:/fake/launcher.bat"), output_channel, null)(makeUri("C:/models/mymodel.cmd"));

        assert.doesNotThrow(() => {
            c.callback(new Error("launch failed"));
        });
        done();
    });
});

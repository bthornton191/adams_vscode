const assert = require("assert");
const path = require("path");
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
 * Stub vscode.window.createTerminal and capture the options + sendText calls.
 * Returns a fake Terminal. Set `throwOnCreate` to simulate a creation failure.
 */
function captureTerminal(throwOnCreate = false) {
    const c = { created: false, sendTextCalls: [] };
    vscode.window.createTerminal = (options) => {
        if (throwOnCreate) throw new Error("terminal failed");
        c.created = true;
        c.options = options;
        return {
            sendText: (text, addNewLine) => c.sendTextCalls.push({ text, addNewLine }),
            show() {},
            hide() {},
            dispose() { c.disposed = true; },
        };
    };
    return c;
}

suite("open_in_view", () => {
    let originalCreateTerminal;
    let originalExistsSync;
    // Use a path with spaces â€” this is the regression case that broke repeatedly
    const FAKE_LAUNCH_CMD = "C:/Program Files/fake/mdi.bat";

    suiteSetup(async () => {
        await vscode.workspace
            .getConfiguration("msc-adams")
            .update("adamsLaunchCommand", FAKE_LAUNCH_CMD, vscode.ConfigurationTarget.Workspace);
        originalCreateTerminal = vscode.window.createTerminal;
        originalExistsSync = fs.existsSync;
    });

    suiteTeardown(async () => {
        vscode.window.createTerminal = originalCreateTerminal;
        fs.existsSync = originalExistsSync;
        await vscode.workspace
            .getConfiguration("msc-adams")
            .update("adamsLaunchCommand", null, vscode.ConfigurationTarget.Workspace);
    });

    setup(() => {
        fs.existsSync = (p) => p === FAKE_LAUNCH_CMD ? true : originalExistsSync(p);
    });

    teardown(() => {
        vscode.window.createTerminal = originalCreateTerminal;
        fs.existsSync = originalExistsSync;
    });

    test("should not create a terminal when launch command path does not exist", (done) => {
        const c = captureTerminal();
        fs.existsSync = () => false;

        const context = makeContext("C:/fake/launcher.bat");
        open_in_view(context, output_channel, null)(makeUri("C:/models/mymodel.cmd"));

        assert.strictEqual(c.created, false,
            "a terminal should not be created when the launch command does not exist");
        done();
    });

    test("should send config_missing telemetry when launch command does not exist", (done) => {
        captureTerminal();
        fs.existsSync = () => false;

        const reporter = makeMockReporter();
        open_in_view(makeContext("C:/fake/launcher.bat"), output_channel, reporter)(makeUri("C:/models/mymodel.cmd"));

        assert.strictEqual(reporter.calls.errors.length, 1);
        assert.strictEqual(reporter.calls.errors[0][0], "open_in_view");
        assert.strictEqual(reporter.calls.errors[0][1].error_type, "config_missing");
        done();
    });

    test("should send a command containing launcher, filename, and Adams launch path", (done) => {
        const launcher = "C:/fake/launcher.bat";
        const c = captureTerminal();

        const uri = makeUri("C:/models/mymodel.cmd");
        open_in_view(makeContext(launcher), output_channel, null)(uri);

        assert.strictEqual(c.created, true, "a terminal must be created to launch Adams");
        assert.strictEqual(c.sendTextCalls.length, 1, "the launch command must be sent once");
        const sent = c.sendTextCalls[0].text;
        assert.ok(sent.includes(launcher), "command must contain the launcher path");
        assert.ok(sent.includes(path.basename(uri.fsPath)), "command must contain the model filename");
        assert.ok(sent.includes(FAKE_LAUNCH_CMD), "command must contain the Adams launch path");
        done();
    });

    test("should quote the launcher, filename, and launch path so spaces survive", (done) => {
        // open_in_view wraps each token in quotes; the Adams launch path
        // ("C:/Program Files/...") contains spaces and must stay one token.
        const launcher = "C:/fake/launcher.bat";
        const c = captureTerminal();

        const uri = makeUri("C:/models/mymodel.cmd");
        open_in_view(makeContext(launcher), output_channel, null)(uri);

        const sent = c.sendTextCalls[0].text;
        assert.ok(sent.includes(`"${launcher}"`), "launcher must be quoted");
        assert.ok(sent.includes(`"${path.basename(uri.fsPath)}"`), "filename must be quoted");
        assert.ok(sent.includes(`"${FAKE_LAUNCH_CMD}"`), "launch path must be quoted");
        done();
    });

    test("should use a hidden cmd terminal with cwd = the model file's directory", (done) => {
        const c = captureTerminal();

        const uri = makeUri("C:/models/mymodel.cmd");
        open_in_view(makeContext("C:/fake/launcher.bat"), output_channel, null)(uri);

        assert.strictEqual(c.options.cwd, path.dirname(uri.fsPath));
        assert.strictEqual(c.options.hideFromUser, true, "the terminal must be hidden from the user");
        assert.ok(/cmd\.exe$/i.test(c.options.shellPath || ""), "the terminal must use cmd.exe");
        done();
    });

    test("should not crash when reporter is null", (done) => {
        captureTerminal();

        assert.doesNotThrow(() => {
            open_in_view(makeContext("C:/fake/launcher.bat"), output_channel, null)(makeUri("C:/models/mymodel.cmd"));
        });
        done();
    });

    test("should send telemetry event when reporter is provided", (done) => {
        captureTerminal();

        const reporter = makeMockReporter();
        open_in_view(makeContext("C:/fake/launcher.bat"), output_channel, reporter)(makeUri("C:/models/mymodel.cmd"));

        assert.strictEqual(reporter.calls.telemetry.length, 1);
        assert.strictEqual(reporter.calls.telemetry[0][0], "open_in_view");
        done();
    });

    test("should send terminal_error telemetry when createTerminal throws", (done) => {
        captureTerminal(true);

        const reporter = makeMockReporter();
        open_in_view(makeContext("C:/fake/launcher.bat"), output_channel, reporter)(makeUri("C:/models/mymodel.cmd"));

        assert.strictEqual(reporter.calls.errors.length, 1);
        assert.strictEqual(reporter.calls.errors[0][0], "open_in_view");
        assert.strictEqual(reporter.calls.errors[0][1].error_type, "terminal_error");
        done();
    });

    test("should not crash when reporter is null and createTerminal throws", (done) => {
        captureTerminal(true);

        assert.doesNotThrow(() => {
            open_in_view(makeContext("C:/fake/launcher.bat"), output_channel, null)(makeUri("C:/models/mymodel.cmd"));
        });
        done();
    });
});

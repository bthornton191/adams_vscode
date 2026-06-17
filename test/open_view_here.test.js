const assert = require("assert");
const child_process = require("child_process");
const fs = require("fs");
const path = require("path");
const os = require("os");
const vscode = require("vscode");
const { open_view_here } = require("../src/open_view_here.ts.js");
const { killAdamsIfRunningInDir } = require("./global_fixture.cjs");

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

suite("open_view_here", () => {
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

        open_view_here(output_channel, null)(makeUri("C:/projects/mymodel"));

        assert.strictEqual(execCalled, false,
            "exec should not be called when the launch command does not exist");
        done();
    });

    test("should send config_missing telemetry when launch command does not exist", (done) => {
        child_process.exec = () => ({});
        fs.existsSync = () => false;

        const reporter = makeMockReporter();
        open_view_here(output_channel, reporter)(makeUri("C:/projects/mymodel"));

        assert.strictEqual(reporter.calls.errors.length, 1);
        assert.strictEqual(reporter.calls.errors[0][0], "open_view_here");
        assert.strictEqual(reporter.calls.errors[0][1].error_type, "config_missing");
        done();
    });

    test("should launch via child_process.exec (hidden cmd.exe), not spawn/wscript", (done) => {
        // Regression: the spawn({detached})/wscript launch flashed console windows
        // and then silently broke MSC's launcher chain. exec runs the launcher
        // through a hidden cmd.exe in a real console, which is what works.
        const c = captureExec();
        open_view_here(output_channel, null)(makeUri("C:/projects/mymodel"));

        assert.strictEqual(typeof c.command, "string", "exec must be called with a command string");
        assert.ok(c.command.includes("aview"), "command must contain 'aview'");
        assert.ok(c.command.includes("ru-s"), "command must contain 'ru-s'");
        done();
    });

    test("should quote the launch path so spaces are parsed as one token", (done) => {
        // Regression: paths like C:\Program Files\...\mdi.bat must be quoted in
        // the command string or cmd.exe splits them on the space.
        const c = captureExec();
        open_view_here(output_channel, null)(makeUri("C:/projects/mymodel"));

        assert.ok(c.command.includes(`"${FAKE_LAUNCH_CMD}"`),
            "the launch path must appear quoted in the exec command string");
        done();
    });

    test("should pass cwd as the right-clicked folder so Adams starts there", (done) => {
        const c = captureExec();

        const uri = makeUri("C:/projects/mymodel");
        open_view_here(output_channel, null)(uri);

        assert.strictEqual(c.options.cwd, uri.fsPath,
            "Adams must be launched with the right-clicked folder as its working directory");
        done();
    });

    test("should not crash when reporter is null", (done) => {
        child_process.exec = () => ({});

        assert.doesNotThrow(() => {
            open_view_here(output_channel, null)(makeUri("C:/projects/mymodel"));
        });
        done();
    });

    test("should send telemetry event when reporter is provided", (done) => {
        child_process.exec = () => ({});

        const reporter = makeMockReporter();
        open_view_here(output_channel, reporter)(makeUri("C:/projects/mymodel"));

        assert.strictEqual(reporter.calls.telemetry.length, 1);
        assert.strictEqual(reporter.calls.telemetry[0][0], "open_view_here");
        done();
    });

    test("should send error telemetry when the exec callback receives an error", (done) => {
        const c = captureExec();

        const reporter = makeMockReporter();
        open_view_here(output_channel, reporter)(makeUri("C:/projects/mymodel"));

        const err = new Error("launch failed");
        c.callback(err);

        assert.strictEqual(reporter.calls.errors.length, 1);
        assert.strictEqual(reporter.calls.errors[0][0], "open_view_here");
        assert.strictEqual(reporter.calls.errors[0][1].error_type, "process_error");
        assert.strictEqual(reporter.calls.errors[0][1].error_message, err.message);
        done();
    });

    test("should not crash when reporter is null and the exec callback errors", (done) => {
        const c = captureExec();

        open_view_here(output_channel, null)(makeUri("C:/projects/mymodel"));

        assert.doesNotThrow(() => {
            c.callback(new Error("launch failed"));
        });
        done();
    });
});

suite("open_view_here (integration)", () => {
    // This suite exercises the full VS Code command registration path:
    // vscode.commands.executeCommand -> registered handler -> child_process.exec -> Adams View
    // Requires Adams to be installed (env var _ADAMS_LAUNCH_COMMAND set).
    const adamsLaunchCmd = process.env._ADAMS_LAUNCH_COMMAND;
    const testDir = path.join(os.tmpdir(), "adams_open_view_here_test_" + process.pid);

    suiteSetup(async function () {
        if (!adamsLaunchCmd || !fs.existsSync(adamsLaunchCmd)) {
            this.skip();
            return;
        }
        if (!fs.existsSync(testDir)) {
            fs.mkdirSync(testDir, { recursive: true });
        }
        // Point the config at the real Adams launch command
        await vscode.workspace
            .getConfiguration("msc-adams")
            .update("adamsLaunchCommand", adamsLaunchCmd, vscode.ConfigurationTarget.Workspace);
    });

    suiteTeardown(async function () {
        if (!adamsLaunchCmd || !fs.existsSync(adamsLaunchCmd)) return;
        // Kill Adams launched by this test
        await new Promise((resolve) => killAdamsIfRunningInDir(testDir, resolve));
        // Restore config
        await vscode.workspace
            .getConfiguration("msc-adams")
            .update("adamsLaunchCommand", null, vscode.ConfigurationTarget.Workspace);
        // Clean up temp dir
        try { fs.rmSync(testDir, { recursive: true, force: true }); } catch { /* ignore */ }
    });

    test("executeCommand msc_adams.openViewHere launches Adams View", function (done) {
        if (!adamsLaunchCmd || !fs.existsSync(adamsLaunchCmd)) { this.skip(); return; }
        this.timeout(90000); // Adams can take a while to start

        // Write a startup script so Adams produces a log file we can detect
        fs.writeFileSync(path.join(testDir, "aviewBS.cmd"), "");
        fs.writeFileSync(path.join(testDir, "aview.cmd"), "command_server start");
        fs.writeFileSync(path.join(testDir, "aviewAS.cmd"), "");

        const logFile = path.join(testDir, "aview.log");
        if (fs.existsSync(logFile)) fs.unlinkSync(logFile);

        // Execute the VS Code command (goes through the full registration path)
        vscode.commands.executeCommand("msc_adams.openViewHere", { fsPath: testDir });

        // Poll for the log file to appear, proving Adams actually launched
        let attempts = 0;
        const maxAttempts = 120;
        const interval = 500;

        function poll() {
            attempts++;
            try {
                if (fs.existsSync(logFile) && fs.readFileSync(logFile, "utf8").includes("command_server start")) {
                    done();
                    return;
                }
            } catch { /* file may be locked */ }

            if (attempts >= maxAttempts) {
                done(new Error("Adams View did not start within timeout (log file never appeared)"));
                return;
            }
            setTimeout(poll, interval);
        }
        setTimeout(poll, 1000); // initial delay before first check
    });
});

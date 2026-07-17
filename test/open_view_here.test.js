const assert = require("assert");
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

suite("open_view_here", () => {
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

        open_view_here(output_channel, null)(makeUri("C:/projects/mymodel"));

        assert.strictEqual(c.created, false,
            "a terminal should not be created when the launch command does not exist");
        done();
    });

    test("should send config_missing telemetry when launch command does not exist", (done) => {
        captureTerminal();
        fs.existsSync = () => false;

        const reporter = makeMockReporter();
        open_view_here(output_channel, reporter)(makeUri("C:/projects/mymodel"));

        assert.strictEqual(reporter.calls.errors.length, 1);
        assert.strictEqual(reporter.calls.errors[0][0], "open_view_here");
        assert.strictEqual(reporter.calls.errors[0][1].error_type, "config_missing");
        done();
    });

    test("should launch via a hidden cmd integrated terminal (real console), not exec/spawn", (done) => {
        // The extension host has no real console, so child_process.exec runs the
        // mdi.bat chain console-less and it silently fails. A hidden integrated
        // terminal runs cmd in a ConPTY (real console) with no flashing window.
        const c = captureTerminal();
        open_view_here(output_channel, null)(makeUri("C:/projects/mymodel"));

        assert.strictEqual(c.created, true, "a terminal must be created to launch Adams");
        assert.strictEqual(c.options.hideFromUser, true, "the terminal must be hidden from the user");
        assert.ok(/cmd\.exe$/i.test(c.options.shellPath || ""),
            "the terminal must use cmd.exe so the sent command syntax is correct");
        assert.strictEqual(c.sendTextCalls.length, 1, "the launch command must be sent once");
        const sent = c.sendTextCalls[0].text;
        assert.ok(sent.includes("aview"), "command must contain 'aview'");
        assert.ok(sent.includes("ru-s"), "command must contain 'ru-s'");
        done();
    });

    test("should quote the launch path so spaces are parsed as one token", (done) => {
        // Regression: paths like C:\Program Files\...\mdi.bat must be quoted in
        // the command or cmd.exe splits them on the space.
        const c = captureTerminal();
        open_view_here(output_channel, null)(makeUri("C:/projects/mymodel"));

        assert.ok(c.sendTextCalls[0].text.includes(`"${FAKE_LAUNCH_CMD}"`),
            "the launch path must appear quoted in the sent command");
        done();
    });

    test("should set terminal cwd to the right-clicked folder so Adams starts there", (done) => {
        const c = captureTerminal();

        const uri = makeUri("C:/projects/mymodel");
        open_view_here(output_channel, null)(uri);

        assert.strictEqual(c.options.cwd, uri.fsPath,
            "Adams must be launched with the right-clicked folder as the terminal cwd");
        done();
    });

    test("should not crash when reporter is null", (done) => {
        captureTerminal();

        assert.doesNotThrow(() => {
            open_view_here(output_channel, null)(makeUri("C:/projects/mymodel"));
        });
        done();
    });

    test("should send telemetry event when reporter is provided", (done) => {
        captureTerminal();

        const reporter = makeMockReporter();
        open_view_here(output_channel, reporter)(makeUri("C:/projects/mymodel"));

        assert.strictEqual(reporter.calls.telemetry.length, 1);
        assert.strictEqual(reporter.calls.telemetry[0][0], "open_view_here");
        done();
    });

    test("should send terminal_error telemetry when createTerminal throws", (done) => {
        captureTerminal(true); // throw on create

        const reporter = makeMockReporter();
        open_view_here(output_channel, reporter)(makeUri("C:/projects/mymodel"));

        assert.strictEqual(reporter.calls.errors.length, 1);
        assert.strictEqual(reporter.calls.errors[0][0], "open_view_here");
        assert.strictEqual(reporter.calls.errors[0][1].error_type, "terminal_error");
        done();
    });

    test("should not crash when reporter is null and createTerminal throws", (done) => {
        captureTerminal(true);

        assert.doesNotThrow(() => {
            open_view_here(output_channel, null)(makeUri("C:/projects/mymodel"));
        });
        done();
    });
});

suite("open_view_here (integration)", () => {
    // This suite exercises the full VS Code command registration path:
    // vscode.commands.executeCommand -> registered handler -> integrated terminal -> Adams View
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

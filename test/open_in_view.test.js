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

/** Read the VBS file written by spawnDetached, clean it up, return content. */
function captureVbs(capturedSpawn) {
    const vbsPath = capturedSpawn.args[1];
    const content = fs.readFileSync(vbsPath, "utf8");
    try { fs.unlinkSync(vbsPath); } catch { /* ignore */ }
    return content;
}

suite("open_in_view", () => {
    let originalSpawn;
    let originalExistsSync;
    // Use a path with spaces â€” this is the regression case that broke repeatedly
    const FAKE_LAUNCH_CMD = "C:/Program Files/fake/mdi.bat";

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
        open_in_view(context, output_channel, null)(makeUri("C:/models/mymodel.cmd"));

        assert.strictEqual(spawnCalled, false,
            "spawn should not be called when the launch command does not exist");
        done();
    });

    test("should send config_missing telemetry when launch command does not exist", (done) => {
        child_process.spawn = () => makeMockChild();
        fs.existsSync = () => false;

        const reporter = makeMockReporter();
        open_in_view(makeContext("C:/fake/launcher.bat"), output_channel, reporter)(makeUri("C:/models/mymodel.cmd"));

        assert.strictEqual(reporter.calls.errors.length, 1);
        assert.strictEqual(reporter.calls.errors[0][0], "open_in_view");
        assert.strictEqual(reporter.calls.errors[0][1].error_type, "config_missing");
        done();
    });

    test("should spawn via wscript.exe (not the .bat directly) to suppress console windows", (done) => {
        if (process.platform !== "win32") { done(); return; }

        const capturedSpawn = {};
        child_process.spawn = (file, args, opts) => {
            capturedSpawn.file = file;
            capturedSpawn.args = args;
            capturedSpawn.opts = opts;
            return makeMockChild();
        };

        open_in_view(makeContext("C:/fake/launcher.bat"), output_channel, null)(makeUri("C:/models/mymodel.cmd"));

        assert.strictEqual(capturedSpawn.file, "wscript.exe",
            "wscript.exe must be used â€” not the .bat directly â€” to suppress child console windows");
        assert.strictEqual(capturedSpawn.args[0], "/nologo");
        assert.match(capturedSpawn.args[1], /adams-spawn-.*\.vbs$/,
            "Second arg must be a temp VBS file");
        done();
    });

    test("should write VBS containing launcher, filename, and Adams launch path", (done) => {
        if (process.platform !== "win32") { done(); return; }

        const launcher = "C:/fake/launcher.bat";
        const capturedSpawn = {};
        child_process.spawn = (file, args, opts) => {
            capturedSpawn.args = args;
            return makeMockChild();
        };

        const uri = makeUri("C:/models/mymodel.cmd");
        open_in_view(makeContext(launcher), output_channel, null)(uri);

        const vbsContent = captureVbs(capturedSpawn);
        assert.ok(vbsContent.includes("WScript.Shell"), "VBS must use WScript.Shell");
        assert.ok(vbsContent.includes(launcher), "VBS must contain the launcher path");
        assert.ok(vbsContent.includes(path.basename(uri.fsPath)), "VBS must contain the model filename");
        assert.ok(vbsContent.includes(FAKE_LAUNCH_CMD), "VBS must contain the Adams launch path");
        done();
    });

    test("should use Shell.Run style=0 to suppress console windows for the full process tree", (done) => {
        if (process.platform !== "win32") { done(); return; }

        const capturedSpawn = {};
        child_process.spawn = (file, args, opts) => {
            capturedSpawn.args = args;
            return makeMockChild();
        };

        open_in_view(makeContext("C:/fake/launcher.bat"), output_channel, null)(makeUri("C:/models/mymodel.cmd"));

        const vbsContent = captureVbs(capturedSpawn);
        assert.match(vbsContent, /, 0, (True|False)$/,
            "Shell.Run must use window style 0 to suppress console windows");
        done();
    });

    test("should use Chr(34) quoting so paths with spaces are safe in VBS", (done) => {
        // Regression: doubled-quote escaping in VBS string literals breaks when the
        // path starts immediately after the opening quote: ""path"" is parsed as
        // empty-string + identifier, not a quoted path. Chr(34) is unambiguous.
        if (process.platform !== "win32") { done(); return; }

        const launcher = "C:/Program Files/fake/launcher.bat";
        const capturedSpawn = {};
        child_process.spawn = (file, args, opts) => {
            capturedSpawn.args = args;
            return makeMockChild();
        };

        open_in_view(makeContext(launcher), output_channel, null)(makeUri("C:/models/my model.cmd"));

        const vbsContent = captureVbs(capturedSpawn);
        assert.ok(vbsContent.includes("Chr(34)"),
            "VBS must use Chr(34) â€” not doubled-quote escaping â€” for path quoting");
        assert.ok(vbsContent.includes(`"${launcher}"`),
            "Launcher path with spaces must appear verbatim inside a VBS string literal");
        assert.ok(vbsContent.includes(`"${FAKE_LAUNCH_CMD}"`),
            "Adams launch path with spaces must appear verbatim inside a VBS string literal");
        done();
    });

    test("should spawn with detached:true so Adams gets its own window station", (done) => {
        const capturedOpts = {};
        child_process.spawn = (file, args, opts) => {
            capturedOpts.value = opts;
            return makeMockChild();
        };

        open_in_view(makeContext("C:/fake/launcher.bat"), output_channel, null)(makeUri("C:/models/mymodel.cmd"));

        assert.strictEqual(capturedOpts.value.detached, true,
            "Process must be detached to get its own window station on Windows");
        done();
    });

    test("should call unref so extension host does not wait for Adams to exit", (done) => {
        let mockChild;
        child_process.spawn = () => {
            mockChild = makeMockChild();
            return mockChild;
        };

        open_in_view(makeContext("C:/fake/launcher.bat"), output_channel, null)(makeUri("C:/models/mymodel.cmd"));

        assert.strictEqual(mockChild.unrefCalled, true,
            "unref() must be called so the extension host can exit independently");
        done();
    });

    test("should pass cwd as the directory containing the model file", (done) => {
        const capturedOpts = {};
        child_process.spawn = (file, args, opts) => {
            capturedOpts.value = opts;
            return makeMockChild();
        };

        const uri = makeUri("C:/models/mymodel.cmd");
        open_in_view(makeContext("C:/fake/launcher.bat"), output_channel, null)(uri);

        assert.strictEqual(capturedOpts.value.cwd, path.dirname(uri.fsPath));
        done();
    });

    test("should not crash when reporter is null", (done) => {
        child_process.spawn = () => makeMockChild();

        assert.doesNotThrow(() => {
            open_in_view(makeContext("C:/fake/launcher.bat"), output_channel, null)(makeUri("C:/models/mymodel.cmd"));
        });
        done();
    });

    test("should send telemetry event when reporter is provided", (done) => {
        child_process.spawn = () => makeMockChild();

        const reporter = makeMockReporter();
        open_in_view(makeContext("C:/fake/launcher.bat"), output_channel, reporter)(makeUri("C:/models/mymodel.cmd"));

        assert.strictEqual(reporter.calls.telemetry.length, 1);
        assert.strictEqual(reporter.calls.telemetry[0][0], "open_in_view");
        done();
    });

    test("should send error telemetry when spawn emits an error", (done) => {
        let mockChild;
        child_process.spawn = () => {
            mockChild = makeMockChild();
            return mockChild;
        };

        const reporter = makeMockReporter();
        open_in_view(makeContext("C:/fake/launcher.bat"), output_channel, reporter)(makeUri("C:/models/mymodel.cmd"));

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
        child_process.spawn = () => {
            mockChild = makeMockChild();
            return mockChild;
        };

        open_in_view(makeContext("C:/fake/launcher.bat"), output_channel, null)(makeUri("C:/models/mymodel.cmd"));

        assert.doesNotThrow(() => {
            mockChild.listeners.error(new Error("spawn failed"));
        });
        done();
    });
});

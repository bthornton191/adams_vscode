const assert = require("assert");
const fs = require("fs");
const path = require("path");
const os = require("os");
const vscode = require("vscode");
const { generateWrapperScript, open_adams_terminal } = require("../src/open_adams_terminal.ts.js");

// Minimal fakes
const output_channel = { appendLine: () => {} };

function makeMockReporter() {
    const calls = { telemetry: [], errors: [] };
    return {
        sendTelemetryEvent: (...args) => calls.telemetry.push(args),
        sendTelemetryErrorEvent: (...args) => calls.errors.push(args),
        calls,
    };
}

/**
 * Stub vscode.window.createTerminal and capture the options.
 * Returns a fake Terminal. Set `throwOnCreate` to simulate a creation failure.
 */
function captureTerminal(throwOnCreate) {
    const c = { created: false, showCalls: 0 };
    vscode.window.createTerminal = (options) => {
        if (throwOnCreate) throw new Error("terminal failed");
        c.created = true;
        c.options = options;
        return {
            show() { c.showCalls++; },
            hide() {},
            dispose() { c.disposed = true; },
        };
    };
    return c;
}

/**
 * Create a fake ExtensionContext with a writable globalStorageUri.
 */
function makeFakeContext() {
    const storageDir = path.join(os.tmpdir(), "adams_terminal_test_" + process.pid);
    if (!fs.existsSync(storageDir)) {
        fs.mkdirSync(storageDir, { recursive: true });
    }
    return {
        globalStorageUri: { fsPath: storageDir },
    };
}

/**
 * Create a minimal AdamsSetup.bat in a temp directory that mimics the
 * structure of the real file.  Uses CRLF line endings.
 */
function makeFakeAdamsSetupBat(dir, version) {
    if (!version) version = "2024_2";
    const setupDir = path.join(dir, "common");
    if (!fs.existsSync(setupDir)) {
        fs.mkdirSync(setupDir, { recursive: true });
    }
    const setupBatPath = path.join(setupDir, "AdamsSetup.bat");
    // Mimic the real AdamsSetup.bat structure with CRLF
    const content = [
        "@echo off",
        "set VERSION=" + version,
        "::",
        "call:ExpandPath",
        "::",
        "if \"%~1\" NEQ \"-nc\" call:setupVS",
        "::",
        "echo.",
        "echo To run Adams products type \"adams" + version + "\"",
        "echo.",
        "::",
        "call:setWorkingDir",
        "::",
        "call:CleanUp",
        "::",
        "%windir%\\system32\\cmd.exe /K",
        "goto :EOF",
        "::",
        ":ExpandPath",
        "set topdir=%~dsp0%",
        "set topdir=%topdir:~0,-7%",
        "set \"PATH=%PATH%;%topdir%bin;\"",
        "for /F \"usebackq delims==\" %%i in (`type \"%topdir%common\\plat\"`) DO @set MDI_CPU=%%i",
        "set X64=",
        "if \"%MDI_CPU%\" == \"win64\" set X64=_x64",
        "goto :EOF",
        ":setupVS",
        "goto :EOF",
        ":CleanUp",
        "set VERSION=",
        "set topdir=",
        "set MDI_CPU=",
        "set X64=",
        "goto :EOF",
        ":setWorkingDir",
        "goto:EOF",
    ].join("\r\n") + "\r\n";
    fs.writeFileSync(setupBatPath, content, "utf8");
    return setupBatPath;
}

// ---------------------------------------------------------------------------
// generateWrapperScript (pure function, no vscode dependency)
// ---------------------------------------------------------------------------
suite("generateWrapperScript", () => {
    let tmpDir;

    setup(() => {
        tmpDir = path.join(os.tmpdir(), "adams_wrapper_test_" + process.pid + "_" + Date.now());
        fs.mkdirSync(tmpDir, { recursive: true });
    });

    teardown(() => {
        try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch { /* ignore */ }
    });

    test("should replace the topdir self-discovery line with the literal path", () => {
        const setupBatPath = makeFakeAdamsSetupBat(tmpDir);
        const storageDir = path.join(tmpDir, "storage");
        const wrapperPath = generateWrapperScript(setupBatPath, storageDir);

        const content = fs.readFileSync(wrapperPath, "utf8");
        const expectedCommonDir = path.dirname(setupBatPath) + path.sep;
        const topdirLine = content.split(/\r?\n/).find((l) => l.startsWith('set "topdir='));
        assert.ok(topdirLine, "a set \"topdir=...\" line must exist in the wrapper");
        assert.ok(topdirLine.includes(expectedCommonDir),
            "the topdir value must be the common directory with trailing separator");
    });

    test("should remove the %windir%\\system32\\cmd.exe /K line", () => {
        const setupBatPath = makeFakeAdamsSetupBat(tmpDir);
        const storageDir = path.join(tmpDir, "storage");
        const wrapperPath = generateWrapperScript(setupBatPath, storageDir);

        const content = fs.readFileSync(wrapperPath, "utf8");
        assert.ok(!content.match(/^%windir%\\system32\\cmd\.exe\s+\/K/im),
            "the cmd.exe /K line must be removed from the wrapper");
    });

    test("should preserve CRLF line endings", () => {
        const setupBatPath = makeFakeAdamsSetupBat(tmpDir);
        const storageDir = path.join(tmpDir, "storage");
        const wrapperPath = generateWrapperScript(setupBatPath, storageDir);

        const content = fs.readFileSync(wrapperPath, "utf8");
        const lines = content.split("\n");
        for (let i = 0; i < lines.length - 1; i++) {
            assert.ok(lines[i].endsWith("\r"),
                "line " + i + " must end with \\r (CRLF preserved): '" + lines[i].slice(0, 30) + "...'");
        }
    });

    test("should preserve the existing `set topdir=%topdir:~0,-7%` line", () => {
        const setupBatPath = makeFakeAdamsSetupBat(tmpDir);
        const storageDir = path.join(tmpDir, "storage");
        const wrapperPath = generateWrapperScript(setupBatPath, storageDir);

        const content = fs.readFileSync(wrapperPath, "utf8");
        assert.ok(content.includes("set topdir=%topdir:~0,-7%"),
            "the substring-stripping line must be preserved so topdir derivation still works");
    });

    test("should throw if the topdir self-discovery line is not found", () => {
        const setupDir = path.join(tmpDir, "common");
        fs.mkdirSync(setupDir, { recursive: true });
        const setupBatPath = path.join(setupDir, "AdamsSetup.bat");
        // Write a batch file without the topdir line
        fs.writeFileSync(setupBatPath, "@echo off\r\necho hello\r\n", "utf8");
        const storageDir = path.join(tmpDir, "storage");

        assert.throws(
            () => generateWrapperScript(setupBatPath, storageDir),
            /set topdir/,
            "should throw with a message mentioning 'set topdir'"
        );
    });

    test("should handle paths with spaces", () => {
        const dirWithSpaces = path.join(tmpDir, "Program Files");
        const setupBatPath = makeFakeAdamsSetupBat(dirWithSpaces);
        const storageDir = path.join(tmpDir, "storage");
        const wrapperPath = generateWrapperScript(setupBatPath, storageDir);

        const content = fs.readFileSync(wrapperPath, "utf8");
        const topdirLine = content.split(/\r?\n/).find((l) => l.startsWith('set "topdir='));
        assert.ok(topdirLine.includes("Program Files"),
            "the topdir value must include the spaces-containing path");
    });

    test("should create the storage directory if it does not exist", () => {
        const setupBatPath = makeFakeAdamsSetupBat(tmpDir);
        const storageDir = path.join(tmpDir, "nested", "storage");
        assert.ok(!fs.existsSync(storageDir), "storage dir must not exist before call");
        const wrapperPath = generateWrapperScript(setupBatPath, storageDir);
        assert.ok(fs.existsSync(wrapperPath), "wrapper script must be written");
    });
});

// ---------------------------------------------------------------------------
// open_adams_terminal (command handler, requires vscode stub)
// ---------------------------------------------------------------------------
suite("open_adams_terminal", () => {
    let originalCreateTerminal;
    let originalExistsSync;
    let originalPlatform;
    let originalGetConfiguration;
    let originalShowWarningMessage;
    let tmpDir;
    let fakeContext;
    let fakeMdiBat;

    suiteSetup(() => {
        originalCreateTerminal = vscode.window.createTerminal;
        originalExistsSync = fs.existsSync;
        originalPlatform = process.platform;
        originalGetConfiguration = vscode.workspace.getConfiguration;
        originalShowErrorMessage = vscode.window.showErrorMessage;
        originalShowWarningMessage = vscode.window.showWarningMessage;
    });

    suiteTeardown(() => {
        vscode.window.createTerminal = originalCreateTerminal;
        fs.existsSync = originalExistsSync;
        vscode.workspace.getConfiguration = originalGetConfiguration;
        vscode.window.showErrorMessage = originalShowErrorMessage;
        vscode.window.showWarningMessage = originalShowWarningMessage;
        Object.defineProperty(process, "platform", { value: originalPlatform, writable: true });
    });

    setup(() => {
        tmpDir = path.join(os.tmpdir(), "adams_terminal_cmd_test_" + process.pid + "_" + Date.now());
        fs.mkdirSync(tmpDir, { recursive: true });

        // Create a fake Adams installation structure
        const commonDir = path.join(tmpDir, "common");
        fs.mkdirSync(commonDir, { recursive: true });
        fakeMdiBat = path.join(commonDir, "mdi.bat");
        fs.writeFileSync(fakeMdiBat, "@echo off\r\n", "utf8");
        makeFakeAdamsSetupBat(tmpDir);

        fakeContext = makeFakeContext();

        // Stub getConfiguration so tests don't depend on real VS Code settings
        vscode.workspace.getConfiguration = () => ({
            get() { return fakeMdiBat; },
            has() { return true; },
            inspect() { return undefined; },
            update() { return Promise.resolve(); },
        });

        // Force platform to win32 for these tests
        Object.defineProperty(process, "platform", { value: "win32", writable: true });
    });

    teardown(() => {
        vscode.window.createTerminal = originalCreateTerminal;
        fs.existsSync = originalExistsSync;
        vscode.workspace.getConfiguration = originalGetConfiguration;
        vscode.window.showErrorMessage = originalShowErrorMessage;
        vscode.window.showWarningMessage = originalShowWarningMessage;
        Object.defineProperty(process, "platform", { value: originalPlatform, writable: true });
        try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch { /* ignore */ }
        try { fs.rmSync(fakeContext.globalStorageUri.fsPath, { recursive: true, force: true }); } catch { /* ignore */ }
    });

    test("should not create a terminal when launch command path does not exist", () => {
        const c = captureTerminal();
        fs.existsSync = () => false;

        open_adams_terminal(fakeContext, output_channel, null)();

        assert.strictEqual(c.created, false,
            "a terminal should not be created when the launch command does not exist");
    });

    test("should send config_missing telemetry when launch command does not exist", () => {
        captureTerminal();
        fs.existsSync = () => false;

        const reporter = makeMockReporter();
        open_adams_terminal(fakeContext, output_channel, reporter)();

        assert.strictEqual(reporter.calls.errors.length, 1);
        assert.strictEqual(reporter.calls.errors[0][0], "open_adams_terminal");
        assert.strictEqual(reporter.calls.errors[0][1].error_type, "config_missing");
    });

    test("should show error when AdamsSetup.bat is not found", () => {
        const c = captureTerminal();
        let errorMsg = null;
        vscode.window.showErrorMessage = (msg) => { errorMsg = msg; return Promise.resolve(); };

        // mdi.bat exists, but AdamsSetup.bat does not
        fs.existsSync = (p) => p === fakeMdiBat ? true : false;

        open_adams_terminal(fakeContext, output_channel, null)();

        assert.strictEqual(c.created, false, "no terminal should be created");
        assert.ok(errorMsg && errorMsg.includes("AdamsSetup.bat"),
            "error message should mention AdamsSetup.bat");
    });

    test("should send setup_bat_missing telemetry when AdamsSetup.bat is not found", () => {
        captureTerminal();
        vscode.window.showErrorMessage = () => Promise.resolve();
        fs.existsSync = (p) => p === fakeMdiBat ? true : false;

        const reporter = makeMockReporter();
        open_adams_terminal(fakeContext, output_channel, reporter)();

        assert.strictEqual(reporter.calls.errors.length, 1);
        assert.strictEqual(reporter.calls.errors[0][1].error_type, "setup_bat_missing");
    });

    test("should create terminal with correct name, shell, and cwd", () => {
        const c = captureTerminal();
        // All paths exist
        fs.existsSync = (p) => true;

        open_adams_terminal(fakeContext, output_channel, null)();

        assert.strictEqual(c.created, true, "a terminal must be created");
        assert.strictEqual(c.options.name, "Adams CMD", "terminal name must be 'Adams CMD'");
        assert.ok(/cmd\.exe$/i.test(c.options.shellPath || ""),
            "shellPath must be cmd.exe");
        assert.ok(Array.isArray(c.options.shellArgs),
            "shellArgs must be an array");
        assert.strictEqual(c.options.shellArgs[0], "/K",
            "first shell arg must be /K");
        assert.ok(c.options.shellArgs[1] && c.options.shellArgs[1].endsWith("adams_terminal_setup.bat"),
            "second shell arg must point to the wrapper script");
        assert.strictEqual(c.showCalls, 1, "terminal.show() must be called once");
    });

    test("should send telemetry event on success", () => {
        captureTerminal();
        fs.existsSync = () => true;

        const reporter = makeMockReporter();
        open_adams_terminal(fakeContext, output_channel, reporter)();

        assert.strictEqual(reporter.calls.telemetry.length, 1);
        assert.strictEqual(reporter.calls.telemetry[0][0], "open_adams_terminal");
    });

    test("should not crash when reporter is null", () => {
        captureTerminal();
        fs.existsSync = () => true;

        assert.doesNotThrow(() => {
            open_adams_terminal(fakeContext, output_channel, null)();
        });
    });

    test("should send terminal_error telemetry when createTerminal throws", () => {
        captureTerminal(true);
        fs.existsSync = () => true;

        const reporter = makeMockReporter();
        open_adams_terminal(fakeContext, output_channel, reporter)();

        assert.strictEqual(reporter.calls.errors.length, 1);
        assert.strictEqual(reporter.calls.errors[0][0], "open_adams_terminal");
        assert.strictEqual(reporter.calls.errors[0][1].error_type, "terminal_error");
    });

    test("should not crash when reporter is null and createTerminal throws", () => {
        captureTerminal(true);
        fs.existsSync = () => true;

        assert.doesNotThrow(() => {
            open_adams_terminal(fakeContext, output_channel, null)();
        });
    });

    test("should not create a terminal on non-Windows platforms", () => {
        const c = captureTerminal();
        vscode.window.showWarningMessage = () => Promise.resolve();
        Object.defineProperty(process, "platform", { value: "linux", writable: true });
        fs.existsSync = () => true;

        open_adams_terminal(fakeContext, output_channel, null)();

        assert.strictEqual(c.created, false,
            "no terminal should be created on non-Windows platforms");
    });
});
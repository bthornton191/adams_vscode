/**
 * tests/batch.test.ts — Unit tests for batch tool helpers.
 *
 * Tests log parsing, status determination, and file extension validation.
 * No real Adams View process or TCP server needed.
 */

import * as crypto from "crypto";
import { EventEmitter } from "events";
import { describe, it, expect, beforeEach, afterEach } from "vitest";
import {
  BATCH_FINISH_MARKER,
  hasFinishMarker,
  extractErrors,
  determineCompletedStatus,
  tailLines,
  buildBatchSpawnArgs,
  _clearJobs,
  _registerJob,
  _jobRegistry,
  BatchJob,
  BatchJobStatus,
} from "../src/tools/batch.js";

// ── Helper: build a minimal fake BatchJob ─────────────────────────────────────

function fakeJob(overrides: Partial<BatchJob> = {}): BatchJob {
  const proc = new EventEmitter() as any;
  proc.pid = 12345;
  proc.exitCode = null;
  proc.killed = false;
  proc.unref = () => undefined;
  return {
    id: crypto.randomUUID(),
    file: "C:/work/test.cmd",
    workingDirectory: "C:/work",
    logPath: "C:/work/aview.log",
    pid: 12345,
    startTime: new Date().toISOString(),
    exitCode: null,
    process: proc,
    ...overrides,
  };
}

// ── hasFinishMarker ───────────────────────────────────────────────────────────

describe("hasFinishMarker", () => {
  it("returns true when the finish marker is present", () => {
    const log = `Some output\n${BATCH_FINISH_MARKER}\nMore output`;
    expect(hasFinishMarker(log)).toBe(true);
  });

  it("returns false when the finish marker is absent", () => {
    expect(hasFinishMarker("Some output\nAdams is running")).toBe(false);
  });

  it("returns false for an empty log", () => {
    expect(hasFinishMarker("")).toBe(false);
  });

  it("returns true when marker is at the very start", () => {
    expect(hasFinishMarker(BATCH_FINISH_MARKER)).toBe(true);
  });
});

// ── extractErrors ─────────────────────────────────────────────────────────────

describe("extractErrors — Adams ERROR: lines", () => {
  it("extracts a single ERROR: line", () => {
    const log = "INFO: loading\nERROR: bad part name\nINFO: done";
    const errors = extractErrors(log);
    expect(errors).toHaveLength(1);
    expect(errors[0]).toContain("ERROR: bad part name");
  });

  it("extracts multiple ERROR: lines", () => {
    const log = "ERROR: first\nWARNING: skipped\nERROR: second";
    expect(extractErrors(log)).toHaveLength(2);
  });

  it("returns empty array when no errors", () => {
    const log = "INFO: all good\n! Command file is exhausted";
    expect(extractErrors(log)).toHaveLength(0);
  });

  it("does not match lines containing 'error' in lowercase mid-word", () => {
    const log = "some_error_value = 5";
    expect(extractErrors(log)).toHaveLength(0);
  });

  it("deduplicates repeated identical error lines", () => {
    const log = "ERROR: duplicate\nERROR: duplicate\nERROR: duplicate";
    expect(extractErrors(log)).toHaveLength(1);
  });
});

describe("extractErrors — Python traceback lines", () => {
  it("detects 'Traceback (most recent call last)'", () => {
    const log = "Running script\nTraceback (most recent call last):\n  File x, line 1";
    const errors = extractErrors(log);
    expect(errors.some((e) => e.includes("Traceback"))).toBe(true);
  });

  it("detects named exception lines matching XxxError:", () => {
    const log = "AttributeError: 'NoneType' object has no attribute 'x'";
    const errors = extractErrors(log);
    expect(errors.some((e) => e.includes("AttributeError"))).toBe(true);
  });

  it("prefixes Python errors with [Python]", () => {
    const log = "Traceback (most recent call last):";
    const errors = extractErrors(log);
    expect(errors[0]).toMatch(/^\[Python\]/);
  });

  it("does not match generic lowercase patterns", () => {
    const log = "some value: error occurred";
    expect(extractErrors(log)).toHaveLength(0);
  });
});

// ── tailLines ─────────────────────────────────────────────────────────────────

describe("tailLines", () => {
  it("returns last n non-empty lines", () => {
    const text = "line1\nline2\nline3\nline4\nline5";
    expect(tailLines(text, 3)).toBe("line3\nline4\nline5");
  });

  it("returns all lines when fewer than n", () => {
    const text = "a\nb";
    expect(tailLines(text, 10)).toBe("a\nb");
  });

  it("skips blank lines", () => {
    const text = "a\n\nb\n\nc";
    expect(tailLines(text, 2)).toBe("b\nc");
  });

  it("returns empty string for empty input", () => {
    expect(tailLines("", 10)).toBe("");
  });

  it("handles Windows CRLF line endings (normalises to LF on rejoin)", () => {
    const text = "line1\r\nline2\r\nline3";
    // Split strips \r; rejoined with \n
    expect(tailLines(text, 2)).toBe("line2\nline3");
  });
});

// ── determineCompletedStatus ──────────────────────────────────────────────────

describe("determineCompletedStatus", () => {
  const logWithMarker = `Adams output\n${BATCH_FINISH_MARKER}\n`;
  const logWithoutMarker = "Adams output\nAdams crashed unexpectedly";

  it("returns 'completed' when finish marker is present regardless of exit code", () => {
    expect(determineCompletedStatus(logWithMarker, 0)).toBe("completed");
    expect(determineCompletedStatus(logWithMarker, 1)).toBe("completed");
  });

  it("returns 'failed' when process exited non-zero and no finish marker", () => {
    expect(determineCompletedStatus(logWithoutMarker, 1)).toBe("failed");
    expect(determineCompletedStatus(logWithoutMarker, 2)).toBe("failed");
  });

  it("returns 'crashed' when exit code is 0 but no finish marker", () => {
    expect(determineCompletedStatus(logWithoutMarker, 0)).toBe("crashed");
  });

  it("returns 'crashed' when exit code is null and no finish marker", () => {
    expect(determineCompletedStatus(logWithoutMarker, null)).toBe("crashed");
  });

  it("returns 'completed' even when errors are present alongside finish marker", () => {
    const log = `ERROR: bad param\n${BATCH_FINISH_MARKER}\n`;
    expect(determineCompletedStatus(log, 0)).toBe("completed");
  });
});

// ── Job registry ─────────────────────────────────────────────────────────────

describe("job registry", () => {
  beforeEach(() => {
    _clearJobs();
  });

  it("starts empty after clear", () => {
    expect(_jobRegistry.size).toBe(0);
  });

  it("stores a registered job", () => {
    const job = fakeJob();
    _registerJob(job);
    expect(_jobRegistry.has(job.id)).toBe(true);
  });

  it("retrieves a registered job by ID", () => {
    const job = fakeJob();
    _registerJob(job);
    const retrieved = _jobRegistry.get(job.id);
    expect(retrieved).toBeDefined();
    expect(retrieved!.file).toBe(job.file);
  });

  it("is cleared by _clearJobs", () => {
    _registerJob(fakeJob());
    _registerJob(fakeJob());
    _clearJobs();
    expect(_jobRegistry.size).toBe(0);
  });
});

// ── buildBatchSpawnArgs ───────────────────────────────────────────────────────

describe("buildBatchSpawnArgs (Windows)", () => {
  const originalPlatform = Object.getOwnPropertyDescriptor(process, "platform");

  beforeEach(() => {
    // Override process.platform to "win32" for these tests
    Object.defineProperty(process, "platform", { value: "win32", configurable: true });
  });

  it("uses cmd.exe as the spawn command on Windows", () => {
    const { cmd } = buildBatchSpawnArgs("C:\\Adams\\mdi.bat", "model.cmd");
    expect(cmd).toBe("cmd.exe");
  });

  it("prefixes args with /c on Windows", () => {
    const { args } = buildBatchSpawnArgs("C:\\Adams\\mdi.bat", "model.cmd");
    expect(args[0]).toBe("/c");
  });

  it("includes the mdi path as second arg on Windows", () => {
    const { args } = buildBatchSpawnArgs("C:\\Adams\\mdi.bat", "model.cmd");
    expect(args[1]).toBe("C:\\Adams\\mdi.bat");
  });

  it("passes aview ru-s -b and the filename on Windows", () => {
    const { args } = buildBatchSpawnArgs("C:\\Adams\\mdi.bat", "model.cmd");
    expect(args).toContain("aview");
    expect(args).toContain("ru-s");
    expect(args).toContain("-b");
    expect(args[args.length - 1]).toBe("model.cmd");
  });

  afterEach(() => {
    if (originalPlatform) {
      Object.defineProperty(process, "platform", originalPlatform);
    }
  });
});

describe("buildBatchSpawnArgs (Linux)", () => {
  const originalPlatform = Object.getOwnPropertyDescriptor(process, "platform");

  beforeEach(() => {
    Object.defineProperty(process, "platform", { value: "linux", configurable: true });
  });

  it("uses the mdi executable directly as the spawn command on Linux", () => {
    const { cmd } = buildBatchSpawnArgs("/opt/adams/mdi", "model.cmd");
    expect(cmd).toBe("/opt/adams/mdi");
  });

  it("does NOT include cmd.exe or /c on Linux", () => {
    const { args } = buildBatchSpawnArgs("/opt/adams/mdi", "model.cmd");
    expect(args).not.toContain("cmd.exe");
    expect(args).not.toContain("/c");
  });

  it("does NOT include -c or exit on Linux (batch mode exits itself)", () => {
    const { args } = buildBatchSpawnArgs("/opt/adams/mdi", "model.cmd");
    expect(args).not.toContain("-c");
    expect(args).not.toContain("exit");
  });

  it("passes aview ru-s -b and the filename on Linux", () => {
    const { args } = buildBatchSpawnArgs("/opt/adams/mdi", "model.cmd");
    expect(args).toContain("aview");
    expect(args).toContain("ru-s");
    expect(args).toContain("-b");
    expect(args[args.length - 1]).toBe("model.cmd");
  });

  afterEach(() => {
    if (originalPlatform) {
      Object.defineProperty(process, "platform", originalPlatform);
    }
  });
});

// ── File extension validation (mirrors tool input validation logic) ────────────

describe("file extension validation", () => {
  function validateExtension(filePath: string): boolean {
    const ext = require("path").extname(filePath).toLowerCase();
    return ext === ".cmd" || ext === ".py";
  }

  it("accepts .cmd files", () => {
    expect(validateExtension("/work/my_model.cmd")).toBe(true);
  });

  it("accepts .py files", () => {
    expect(validateExtension("/work/my_script.py")).toBe(true);
  });

  it("rejects .txt files", () => {
    expect(validateExtension("/work/notes.txt")).toBe(false);
  });

  it("rejects files with no extension", () => {
    expect(validateExtension("/work/my_model")).toBe(false);
  });

  it("accepts .CMD uppercase (case-insensitive)", () => {
    expect(validateExtension("/work/MY_MODEL.CMD")).toBe(true);
  });

  it("accepts .PY uppercase (case-insensitive)", () => {
    expect(validateExtension("/work/SCRIPT.PY")).toBe(true);
  });
});

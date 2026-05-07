/**
 * tests/hidden-spawn.test.ts — Unit tests for the spawnHidden helper.
 *
 * Tests VBScript content and spawn argument generation on Windows and
 * direct spawn behaviour on non-Windows. No real processes are launched.
 */

import * as os from "os";
import * as path from "path";
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";

// ── Mocks ─────────────────────────────────────────────────────────────────────

const mockChild = vi.hoisted(() => ({
  pid: 99999,
  unref: vi.fn(),
  once: vi.fn(),
}));

// We mock fs/promises so no files are written to disk.
vi.mock("fs/promises", () => ({
  writeFile: vi.fn().mockResolvedValue(undefined),
  unlink: vi.fn().mockResolvedValue(undefined),
}));

// We mock the fs sync module used for cleanup.
vi.mock("fs", () => ({
  unlinkSync: vi.fn(),
}));

// We mock child_process.spawn to avoid launching real processes.
vi.mock("child_process", () => ({
  spawn: vi.fn().mockReturnValue(mockChild),
}));

import * as fsMock from "fs/promises";
import { spawn as spawnMock } from "child_process";
import { spawnHidden } from "../src/hidden-spawn.js";

// ── Helpers ───────────────────────────────────────────────────────────────────

function setPlatform(platform: string) {
  Object.defineProperty(process, "platform", { value: platform, configurable: true });
}

// ── Windows tests ─────────────────────────────────────────────────────────────

describe("spawnHidden — Windows", () => {
  const originalPlatform = Object.getOwnPropertyDescriptor(process, "platform");

  beforeEach(() => {
    setPlatform("win32");
    vi.clearAllMocks();
  });

  afterEach(() => {
    if (originalPlatform) {
      Object.defineProperty(process, "platform", originalPlatform);
    }
  });

  it("writes a VBS file to the temp directory", async () => {
    await spawnHidden("C:\\Adams\\mdi.bat", ["aview", "ru-s", "-b", "model.cmd"], {
      cwd: "C:\\work",
      detached: true,
      wait: true,
    });

    expect(fsMock.writeFile).toHaveBeenCalledOnce();
    const [filePath] = (fsMock.writeFile as ReturnType<typeof vi.fn>).mock.calls[0] as [string, ...unknown[]];
    expect(filePath).toContain(os.tmpdir());
    expect(filePath).toMatch(/adams-spawn-.*\.vbs$/);
  });

  it("VBS content uses window style 0", async () => {
    await spawnHidden("C:\\Adams\\mdi.bat", ["aview", "ru-s", "-b", "model.cmd"], {
      cwd: "C:\\work",
      detached: true,
      wait: true,
    });

    const [, vbsContent] = (fsMock.writeFile as ReturnType<typeof vi.fn>).mock.calls[0] as [string, string, ...unknown[]];
    expect(vbsContent).toContain(", 0, ");
  });

  it("VBS content uses True when wait=true", async () => {
    await spawnHidden("C:\\Adams\\mdi.bat", ["aview", "ru-s", "-b", "model.cmd"], {
      cwd: "C:\\work",
      detached: true,
      wait: true,
    });

    const [, vbsContent] = (fsMock.writeFile as ReturnType<typeof vi.fn>).mock.calls[0] as [string, string, ...unknown[]];
    expect(vbsContent).toContain(", 0, True");
  });

  it("VBS content uses False when wait=false", async () => {
    await spawnHidden("C:\\Adams\\mdi.bat", ["aview", "ru-s", "i"], {
      cwd: "C:\\work",
      detached: true,
      wait: false,
    });

    const [, vbsContent] = (fsMock.writeFile as ReturnType<typeof vi.fn>).mock.calls[0] as [string, string, ...unknown[]];
    expect(vbsContent).toContain(", 0, False");
  });

  it("VBS content includes the command and args", async () => {
    await spawnHidden("C:\\Adams\\mdi.bat", ["aview", "ru-s", "-b", "model.cmd"], {
      cwd: "C:\\work",
      detached: true,
      wait: true,
    });

    const [, vbsContent] = (fsMock.writeFile as ReturnType<typeof vi.fn>).mock.calls[0] as [string, string, ...unknown[]];
    expect(vbsContent).toContain("C:\\Adams\\mdi.bat");
    expect(vbsContent).toContain("aview");
    expect(vbsContent).toContain("ru-s");
    expect(vbsContent).toContain("-b");
    expect(vbsContent).toContain("model.cmd");
  });

  it("spawns wscript.exe with /nologo and the VBS path", async () => {
    await spawnHidden("C:\\Adams\\mdi.bat", ["aview", "ru-s", "-b", "model.cmd"], {
      cwd: "C:\\work",
      detached: true,
      wait: true,
    });

    expect(spawnMock).toHaveBeenCalledOnce();
    const [cmd, args] = (spawnMock as ReturnType<typeof vi.fn>).mock.calls[0] as [string, string[], ...unknown[]];
    expect(cmd).toBe("wscript.exe");
    expect(args[0]).toBe("/nologo");
    expect(args[1]).toMatch(/adams-spawn-.*\.vbs$/);
  });

  it("passes cwd and detached through to spawn", async () => {
    await spawnHidden("C:\\Adams\\mdi.bat", ["aview", "ru-s", "-b", "model.cmd"], {
      cwd: "C:\\work",
      detached: true,
      wait: true,
    });

    const [, , opts] = (spawnMock as ReturnType<typeof vi.fn>).mock.calls[0] as [string, string[], Record<string, unknown>];
    expect(opts.cwd).toBe("C:\\work");
    expect(opts.detached).toBe(true);
  });

  it("escapes double-quotes in the command path inside VBS", async () => {
    await spawnHidden(`C:\\Adams "2024"\\mdi.bat`, ["aview"], {
      cwd: "C:\\work",
      detached: true,
      wait: true,
    });

    const [, vbsContent] = (fsMock.writeFile as ReturnType<typeof vi.fn>).mock.calls[0] as [string, string, ...unknown[]];
    // Double-quotes in the path should be escaped by doubling them
    expect(vbsContent).toContain('""');
  });

  it("escapes quotes in space-containing args so they do not break the VBS string", async () => {
    // Regression: batch mode passes cmd="cmd.exe" with args=["/c", "C:\Program Files\...\mdi.bat", ...]
    // The path arg contains a space, so it gets wrapped in quotes. Those quotes
    // MUST be doubled ("") to avoid prematurely terminating the VBS string literal.
    await spawnHidden("cmd.exe", ["/c", "C:\\Program Files\\MSC.Software\\Adams\\2023_4_1\\common\\mdi.bat", "aview", "ru-s", "-b", "model.cmd"], {
      cwd: "C:\\work",
      detached: true,
      wait: true,
    });

    const [, vbsContent] = (fsMock.writeFile as ReturnType<typeof vi.fn>).mock.calls[0] as [string, string, ...unknown[]];
    // The VBS string is delimited by the outer quotes in the template.
    // Any inner quotes must be doubled. Verify no bare (unescaped) quotes appear
    // inside the Shell.Run string argument by checking the structure:
    // - Strip the known outer pattern: CreateObject(...).Run "...", 0, X
    // - Everything between the first " after .Run and the last " before , 0 must
    //   contain only "" (escaped) quotes, never a lone ".
    const match = vbsContent.match(/\.Run "(.*)", 0, (True|False)$/);
    expect(match).not.toBeNull();
    const innerStr = match![1];
    // Replace all "" (escaped quotes) then check no lone " remains
    const afterEscape = innerStr.replace(/""/g, "");
    expect(afterEscape).not.toContain('"');
  });

  it("VBS content for batch mode (cmd.exe + mdi path with spaces) is syntactically valid", async () => {
    await spawnHidden("cmd.exe", ["/c", "C:\\Program Files\\MSC.Software\\Adams\\2023_4_1\\common\\mdi.bat", "aview", "ru-s", "-b", "model.cmd"], {
      cwd: "C:\\work",
      detached: true,
      wait: true,
    });

    const [, vbsContent] = (fsMock.writeFile as ReturnType<typeof vi.fn>).mock.calls[0] as [string, string, ...unknown[]];
    // Verify the generated VBS passes the Shell.Run the full cmd including the path
    expect(vbsContent).toContain("cmd.exe");
    expect(vbsContent).toContain("Program Files");
    expect(vbsContent).toContain("mdi.bat");
    expect(vbsContent).toContain("model.cmd");
    // Verify the outer VBS string delimiter structure: .Run "...", 0, True/False
    expect(vbsContent).toMatch(/\.Run ".*", 0, (True|False)$/);
  });

  it("returns the child process from spawn", async () => {
    const { child } = await spawnHidden("C:\\Adams\\mdi.bat", ["aview"], {
      cwd: "C:\\work",
      detached: true,
      wait: true,
    });
    expect(child).toBe(mockChild);
  });
});

// ── Non-Windows tests ─────────────────────────────────────────────────────────

describe("spawnHidden — non-Windows (Linux)", () => {
  const originalPlatform = Object.getOwnPropertyDescriptor(process, "platform");

  beforeEach(() => {
    setPlatform("linux");
    vi.clearAllMocks();
  });

  afterEach(() => {
    if (originalPlatform) {
      Object.defineProperty(process, "platform", originalPlatform);
    }
  });

  it("does NOT write a VBS file", async () => {
    await spawnHidden("/opt/adams/mdi", ["aview", "ru-s", "-b", "model.cmd"], {
      cwd: "/work",
      detached: true,
      wait: true,
    });

    expect(fsMock.writeFile).not.toHaveBeenCalled();
  });

  it("spawns the command directly (not wscript.exe)", async () => {
    await spawnHidden("/opt/adams/mdi", ["aview", "ru-s", "-b", "model.cmd"], {
      cwd: "/work",
      detached: true,
      wait: true,
    });

    const [cmd] = (spawnMock as ReturnType<typeof vi.fn>).mock.calls[0] as [string, ...unknown[]];
    expect(cmd).toBe("/opt/adams/mdi");
    expect(cmd).not.toBe("wscript.exe");
  });

  it("passes args directly to spawn", async () => {
    await spawnHidden("/opt/adams/mdi", ["aview", "ru-s", "-b", "model.cmd"], {
      cwd: "/work",
      detached: true,
      wait: true,
    });

    const [, args] = (spawnMock as ReturnType<typeof vi.fn>).mock.calls[0] as [string, string[], ...unknown[]];
    expect(args).toEqual(["aview", "ru-s", "-b", "model.cmd"]);
  });

  it("returns the child process from spawn", async () => {
    const { child } = await spawnHidden("/opt/adams/mdi", ["aview"], {
      cwd: "/work",
      detached: true,
      wait: false,
    });
    expect(child).toBe(mockChild);
  });
});

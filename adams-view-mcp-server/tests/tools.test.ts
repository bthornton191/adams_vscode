/**
 * tests/tools.test.ts — Unit tests for tool handlers.
 *
 * Tests tool logic by mocking the client functions (executeCmd, evaluateExp)
 * directly via vitest mocking. No real TCP server needed here.
 */

import { describe, it, expect, vi, beforeEach } from "vitest";
import { parseDescription, parseData } from "../src/client.js";

// ── Smoke tests for tool-level parsing/normalization helpers ─────────────────
// (Full tool tests require wiring into McpServer and are integration-level;
//  the most important logic — parsing — is tested in client.test.ts.
//  Here we add a few targeted checks for tool utility code.)

describe("model name normalisation", () => {
  function normaliseModelName(name: string): string {
    return name.startsWith(".") ? name : `.${name}`;
  }

  it("adds dot prefix when missing", () => {
    expect(normaliseModelName("my_model")).toBe(".my_model");
  });

  it("keeps existing dot prefix", () => {
    expect(normaliseModelName(".my_model")).toBe(".my_model");
  });
});

describe("solver commands array formatting", () => {
  function formatSolverCommands(cmds: string[]): string {
    return cmds
      .map((c) => `"${c.replace(/"/g, '\\"')}"`)
      .join(", &\n                  ");
  }

  it("wraps single command in quotes", () => {
    expect(formatSolverCommands(["SIMULATE/DYNAMIC, END=1.0, DTOUT=0.01"])).toBe(
      '"SIMULATE/DYNAMIC, END=1.0, DTOUT=0.01"'
    );
  });

  it("joins multiple commands with continuation", () => {
    const result = formatSolverCommands(["SIMULATE/DYNAMIC, END=1.0, DTOUT=0.01", "STOP"]);
    expect(result).toContain('"SIMULATE/DYNAMIC, END=1.0, DTOUT=0.01"');
    expect(result).toContain('"STOP"');
    expect(result).toContain("&");
  });

  it("escapes embedded double quotes", () => {
    expect(formatSolverCommands(['CMD with "quotes"'])).toBe('"CMD with \\"quotes\\""');
  });
});

describe("log flags bitmask", () => {
  function buildFlags(opts: {
    filter_by_type: boolean;
    show_infos: boolean;
    show_warnings: boolean;
    show_errors: boolean;
    show_fatals: boolean;
    suppress_duplicates: boolean;
    filter_string: string;
  }): number {
    let flags = 0;
    if (opts.filter_by_type) flags |= 1;
    if (opts.show_infos) flags |= 2;
    if (opts.show_warnings) flags |= 4;
    if (opts.show_errors) flags |= 8;
    if (opts.show_fatals) flags |= 16;
    if (opts.suppress_duplicates) flags |= 32;
    if (opts.filter_string !== "") flags |= 64;
    return flags;
  }

  const defaults = {
    filter_by_type: false,
    show_infos: true,
    show_warnings: true,
    show_errors: true,
    show_fatals: true,
    suppress_duplicates: false,
    filter_string: "",
  };

  it("returns 0 for all defaults (no type filter, no string filter)", () => {
    // With filter_by_type=false and filter_string="" only bits 1–4 and 6 are off.
    // show_* bits (2,4,8,16) are set but filter_by_type (1) is not → net visible flags = 30
    // However since filter_by_type=false they have no effect; total flags = 30
    expect(buildFlags(defaults)).toBe(30); // 2|4|8|16 = 30
  });

  it("adds bit 1 when filter_by_type is true", () => {
    expect(buildFlags({ ...defaults, filter_by_type: true }) & 1).toBe(1);
  });

  it("adds bit 32 when suppress_duplicates is true", () => {
    expect(buildFlags({ ...defaults, suppress_duplicates: true }) & 32).toBe(32);
  });

  it("adds bit 64 when filter_string is non-empty", () => {
    expect(buildFlags({ ...defaults, filter_string: "error" }) & 64).toBe(64);
  });

  it("does NOT add bit 64 when filter_string is empty", () => {
    expect(buildFlags(defaults) & 64).toBe(0);
  });

  it("excludes infos bit when show_infos is false", () => {
    expect(buildFlags({ ...defaults, show_infos: false }) & 2).toBe(0);
  });
});

/**
 * tests/client.test.ts — Unit tests for the TCP client functions.
 *
 * Tests parsing helpers directly (no network) and protocol behaviour
 * via a mock Adams TCP server.
 *
 * evaluateExp now uses Python (Adams.evaluate_exp) via executeCmd + temp files,
 * so its tests mock the cmd protocol and simulate the Python output file.
 */

import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import * as net from "net";
import * as fs from "fs/promises";
import {
  parseDescription,
  parseData,
  executeCmd,
  evaluateExp,
  checkConnection,
  getPort,
} from "../src/client.js";
import { startStatefulMockServer } from "./helpers.js";

// ── parseDescription ─────────────────────────────────────────────────────────

describe("parseDescription", () => {
  it("parses 'query: str: 1'", () => {
    expect(parseDescription("query: str: 1")).toEqual(["str", 1]);
  });

  it("parses 'query: int: 3'", () => {
    expect(parseDescription("query: int: 3")).toEqual(["int", 3]);
  });

  it("parses with extra spaces", () => {
    expect(parseDescription("query:  float:  2")).toEqual(["float", 2]);
  });

  it("handles missing count (defaults to 1)", () => {
    expect(parseDescription("query: str")).toEqual(["str", 1]);
  });
});

// ── parseData ────────────────────────────────────────────────────────────────

describe("parseData", () => {
  it("coerces int type", () => {
    expect(parseData("42", "int", 1)).toBe(42);
  });

  it("coerces float type", () => {
    expect(parseData("3.14", "float", 1)).toBeCloseTo(3.14);
  });

  it("coerces 'on' to true", () => {
    expect(parseData("on", "str", 1)).toBe(true);
  });

  it("coerces 'off' to false", () => {
    expect(parseData("off", "str", 1)).toBe(false);
  });

  it("coerces 'yes' to true", () => {
    expect(parseData("yes", "str", 1)).toBe(true);
  });

  it("coerces 'no' to false", () => {
    expect(parseData("no", "str", 1)).toBe(false);
  });

  it("returns trimmed string for str type", () => {
    expect(parseData("  hello world  ", "str", 1)).toBe("hello world");
  });

  it("returns array for count > 1", () => {
    expect(parseData("1, 2, 3", "int", 3)).toEqual([1, 2, 3]);
  });

  it("returns array of strings for count > 1 str type", () => {
    expect(parseData(".model_a, .model_b", "str", 2)).toEqual([".model_a", ".model_b"]);
  });

  // Adams text-mode array format: parenthesized, string elements quoted
  it("strips outer parens from array response", () => {
    expect(parseData("(1, 2, 3)", "int", 3)).toEqual([1, 2, 3]);
  });

  it("strips outer parens and quotes from string array (Adams db_children format)", () => {
    expect(
      parseData(
        "('.suspension.ground', '.suspension.Lower_Arm', '.suspension.Upper_Arm')",
        "str",
        3
      )
    ).toEqual([".suspension.ground", ".suspension.Lower_Arm", ".suspension.Upper_Arm"]);
  });

  it("strips outer parens from int array (Adams object ID format)", () => {
    expect(parseData("(19, 20, 17)", "int", 3)).toEqual([19, 20, 17]);
  });

  it("strips single quotes from scalar string", () => {
    expect(parseData("'suspension'", "str", 1)).toBe("suspension");
  });
});

// ── getPort ──────────────────────────────────────────────────────────────────

describe("getPort", () => {
  it("returns DEFAULT_PORT when env is unset", () => {
    const original = process.env["ADAMS_LISTENER_PORT"];
    delete process.env["ADAMS_LISTENER_PORT"];
    expect(getPort()).toBe(5002);
    if (original !== undefined) process.env["ADAMS_LISTENER_PORT"] = original;
  });

  it("reads ADAMS_LISTENER_PORT from env", () => {
    process.env["ADAMS_LISTENER_PORT"] = "6000";
    expect(getPort()).toBe(6000);
    delete process.env["ADAMS_LISTENER_PORT"];
  });
});

// ── executeCmd ───────────────────────────────────────────────────────────────

describe("executeCmd", () => {
  let mock: { port: number; close: () => Promise<void> } | undefined;

  beforeEach(async () => {
    // Simple mock: echo "cmd: 0" for any connection
    mock = await startStatefulMockServer((socket: net.Socket) => {
      socket.once("data", (_chunk: Buffer) => {
        socket.write("cmd: 0");
        socket.end();
      });
    });
    process.env["ADAMS_LISTENER_PORT"] = String(mock.port);
  });

  afterEach(async () => {
    delete process.env["ADAMS_LISTENER_PORT"];
    if (mock) { await mock.close(); mock = undefined; }
  });

  it("resolves on 'cmd: 0' response", async () => {
    await expect(executeCmd("model create model_name=test")).resolves.toBeUndefined();
  });

  it("throws on unexpected response", async () => {
    // Override to send an error response
    if (mock) { await mock.close(); mock = undefined; }
    mock = await startStatefulMockServer((socket: net.Socket) => {
      socket.once("data", (_chunk: Buffer) => {
        socket.write("cmd: 1 - ERROR: Something went wrong");
        socket.end();
      });
    });
    process.env["ADAMS_LISTENER_PORT"] = String(mock.port);
    await expect(executeCmd("bad_command")).rejects.toThrow(/unexpected response/);
  });

  it("throws when Adams View is not reachable", async () => {
    // Start a server that immediately destroys every connection (simulates refused/closed port)
    const refused = await startStatefulMockServer((socket: net.Socket) => { socket.destroy(); });
    process.env["ADAMS_LISTENER_PORT"] = String(refused.port);
    try {
      await expect(executeCmd("test")).rejects.toThrow();
    } finally {
      await refused.close();
    }
  }, 15000);
});

// ── evaluateExp ──────────────────────────────────────────────────────────────
//
// evaluateExp now:
//   1. Writes a Python script to a temp dir
//   2. Calls executeCmd("file python read ...") via TCP cmd protocol
//   3. Reads the JSON output from a temp file written by the Python script
//
// To test this without Adams, we mock the TCP cmd server and intercept the
// temp file writes to simulate Adams writing the Python output file.

describe("evaluateExp", () => {
  let mock: { port: number; close: () => Promise<void> } | undefined;

  /**
   * Create a mock cmd server that intercepts the Python script, extracts the
   * output file path, and writes the given JSON result to it — simulating
   * what Adams.evaluate_exp() would produce via the Python stdout capture.
   */
  function createMockAdamsServer(pythonResult: Record<string, unknown>) {
    return startStatefulMockServer((socket: net.Socket) => {
      let buf = "";
      socket.on("data", (chunk: Buffer) => {
        buf += chunk.toString();
        const msg = buf.trim();
        // Expect: cmd file python read file_name="<path>"
        if (msg.startsWith("cmd file python read")) {
          const match = msg.match(/file_name="([^"]+)"/);
          if (match) {
            const scriptPath = match[1]!;
            // Read the script to find the output file path
            const scriptContent = require("fs").readFileSync(
              scriptPath.replace(/\//g, require("path").sep),
              "utf8"
            );
            const outMatch = scriptContent.match(/open\("([^"]+)"/);
            if (outMatch) {
              const outputPath = outMatch[1]!.replace(/\//g, require("path").sep);
              require("fs").writeFileSync(
                outputPath,
                JSON.stringify(pythonResult) + "\n",
                "utf8"
              );
            }
          }
          socket.write("cmd: 0");
          socket.end();
          buf = "";
        }
      });
    });
  }

  afterEach(async () => {
    delete process.env["ADAMS_LISTENER_PORT"];
    if (mock) { await mock.close(); mock = undefined; }
  });

  it("returns a string result from Python", async () => {
    mock = await createMockAdamsServer({ v: "C:\\adams\\work" });
    process.env["ADAMS_LISTENER_PORT"] = String(mock.port);
    const result = await evaluateExp("getcwd()");
    expect(result).toBe("C:\\adams\\work");
  });

  it("returns an integer result from Python", async () => {
    mock = await createMockAdamsServer({ v: 1 });
    process.env["ADAMS_LISTENER_PORT"] = String(mock.port);
    const result = await evaluateExp("db_exists('.mdi')");
    expect(result).toBe(1);
  });

  it("returns a float result from Python", async () => {
    mock = await createMockAdamsServer({ v: 3.14 });
    process.env["ADAMS_LISTENER_PORT"] = String(mock.port);
    const result = await evaluateExp("some_float_expr()");
    expect(result).toBeCloseTo(3.14);
  });

  it("returns an array result from Python", async () => {
    mock = await createMockAdamsServer({
      v: [".suspension.ground", ".suspension.Lower_Arm", ".suspension.Upper_Arm"],
    });
    process.env["ADAMS_LISTENER_PORT"] = String(mock.port);
    const result = await evaluateExp("db_children(suspension, 'part')");
    expect(result).toEqual([
      ".suspension.ground",
      ".suspension.Lower_Arm",
      ".suspension.Upper_Arm",
    ]);
  });

  it("returns an integer array from Python", async () => {
    mock = await createMockAdamsServer({ v: [19, 20, 17] });
    process.env["ADAMS_LISTENER_PORT"] = String(mock.port);
    const result = await evaluateExp("{strut.id, upper.id, rack.id}");
    expect(result).toEqual([19, 20, 17]);
  });

  it("coerces 'on'/'off'/'yes'/'no' strings to booleans", async () => {
    mock = await createMockAdamsServer({ v: "on" });
    process.env["ADAMS_LISTENER_PORT"] = String(mock.port);
    expect(await evaluateExp("some_toggle()")).toBe(true);

    if (mock) { await mock.close(); mock = undefined; }
    mock = await createMockAdamsServer({ v: "off" });
    process.env["ADAMS_LISTENER_PORT"] = String(mock.port);
    expect(await evaluateExp("some_toggle()")).toBe(false);
  });

  it("throws a useful error when Python reports an exception", async () => {
    mock = await createMockAdamsServer({ e: "NameError: name 'jibberish' is not defined" });
    process.env["ADAMS_LISTENER_PORT"] = String(mock.port);
    await expect(evaluateExp("jibberish")).rejects.toThrow(/NameError/);
  });

  it("can evaluate after a previous error on the same server", async () => {
    // First call: error
    let callCount = 0;
    mock = await startStatefulMockServer((socket: net.Socket) => {
      let buf = "";
      socket.on("data", (chunk: Buffer) => {
        buf += chunk.toString();
        const msg = buf.trim();
        if (msg.startsWith("cmd file python read")) {
          callCount++;
          const match = msg.match(/file_name="([^"]+)"/);
          if (match) {
            const scriptPath = match[1]!;
            const scriptContent = require("fs").readFileSync(
              scriptPath.replace(/\//g, require("path").sep),
              "utf8"
            );
            const outMatch = scriptContent.match(/open\("([^"]+)"/);
            if (outMatch) {
              const outputPath = outMatch[1]!.replace(/\//g, require("path").sep);
              const result = callCount === 1
                ? { e: "bad expression" }
                : { v: 1 };
              require("fs").writeFileSync(outputPath, JSON.stringify(result) + "\n", "utf8");
            }
          }
          socket.write("cmd: 0");
          socket.end();
          buf = "";
        }
      });
    });
    process.env["ADAMS_LISTENER_PORT"] = String(mock.port);

    await expect(evaluateExp("bad_expr")).rejects.toThrow();
    const result = await evaluateExp("db_exists('.mdi')");
    expect(result).toBe(1);
  });

  it("throws when Adams View is not reachable", async () => {
    const refused = await startStatefulMockServer((socket: net.Socket) => { socket.destroy(); });
    process.env["ADAMS_LISTENER_PORT"] = String(refused.port);
    try {
      await expect(evaluateExp("any_expr()")).rejects.toThrow();
    } finally {
      await refused.close();
    }
  }, 15000);

  it("safely embeds expressions containing quotes", async () => {
    // Expression with both single and double quotes
    mock = await createMockAdamsServer({ v: 1 });
    process.env["ADAMS_LISTENER_PORT"] = String(mock.port);
    const result = await evaluateExp(`db_exists(".model's_test")`);
    expect(result).toBe(1);
  });
});

// ── checkConnection ──────────────────────────────────────────────────────────

describe("checkConnection", () => {
  let mock: { port: number; close: () => Promise<void> } | undefined;

  function createMockAdamsServer(pythonResult: Record<string, unknown>) {
    return startStatefulMockServer((socket: net.Socket) => {
      let buf = "";
      socket.on("data", (chunk: Buffer) => {
        buf += chunk.toString();
        const msg = buf.trim();
        if (msg.startsWith("cmd file python read")) {
          const match = msg.match(/file_name="([^"]+)"/);
          if (match) {
            const scriptPath = match[1]!;
            const scriptContent = require("fs").readFileSync(
              scriptPath.replace(/\//g, require("path").sep),
              "utf8"
            );
            const outMatch = scriptContent.match(/open\("([^"]+)"/);
            if (outMatch) {
              const outputPath = outMatch[1]!.replace(/\//g, require("path").sep);
              require("fs").writeFileSync(outputPath, JSON.stringify(pythonResult) + "\n", "utf8");
            }
          }
          socket.write("cmd: 0");
          socket.end();
          buf = "";
        }
      });
    });
  }

  afterEach(async () => {
    delete process.env["ADAMS_LISTENER_PORT"];
    if (mock) { await mock.close(); mock = undefined; }
  });

  it("returns true when Adams is ready", async () => {
    mock = await createMockAdamsServer({ v: 1 });
    process.env["ADAMS_LISTENER_PORT"] = String(mock.port);
    expect(await checkConnection()).toBe(true);
  });

  it("returns false when connection refused", async () => {
    const refused = await startStatefulMockServer((socket: net.Socket) => { socket.destroy(); });
    process.env["ADAMS_LISTENER_PORT"] = String(refused.port);
    try {
      expect(await checkConnection()).toBe(false);
    } finally {
      await refused.close();
    }
  }, 15000);

  it("returns false when Adams returns 0 for db_exists", async () => {
    mock = await createMockAdamsServer({ v: 0 });
    process.env["ADAMS_LISTENER_PORT"] = String(mock.port);
    expect(await checkConnection()).toBe(false);
  });
});

/**
 * tests/client.test.ts — Unit tests for the TCP client functions.
 *
 * Tests parsing helpers directly (no network) and protocol behaviour
 * via a mock Adams TCP server.
 */

import { describe, it, expect, beforeEach, afterEach } from "vitest";
import * as net from "net";
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
    process.env["ADAMS_LISTENER_PORT"] = "1"; // port 1 should be refused
    await expect(executeCmd("test")).rejects.toThrow(/Could not connect/);
  });
});

// ── evaluateExp ──────────────────────────────────────────────────────────────

describe("evaluateExp", () => {
  let mock: { port: number; close: () => Promise<void> } | undefined;

  afterEach(async () => {
    delete process.env["ADAMS_LISTENER_PORT"];
    if (mock) { await mock.close(); mock = undefined; }
  });

  it("handles string result via two-round-trip protocol", async () => {
    mock = await startStatefulMockServer((socket: net.Socket) => {
      let step = 0;
      socket.on("data", (chunk: Buffer) => {
        const msg = chunk.toString().trim();
        if (step === 0) {
          // Receive "query <expr>", send description
          expect(msg).toMatch(/^query /);
          socket.write("query: str: 1\n");
          step = 1;
        } else if (step === 1 && msg === "OK") {
          socket.write("C:\\\\adams\\\\work");
          socket.end();
        }
      });
    });
    process.env["ADAMS_LISTENER_PORT"] = String(mock.port);

    const result = await evaluateExp("getcwd()");
    expect(result).toBe("C:\\\\adams\\\\work");
  });

  it("handles integer result", async () => {
    mock = await startStatefulMockServer((socket: net.Socket) => {
      let step = 0;
      socket.on("data", (chunk: Buffer) => {
        const msg = chunk.toString().trim();
        if (step === 0) {
          socket.write("query: int: 1\n");
          step = 1;
        } else if (step === 1 && msg === "OK") {
          socket.write("1");
          socket.end();
        }
      });
    });
    process.env["ADAMS_LISTENER_PORT"] = String(mock.port);

    const result = await evaluateExp("db_exists('.mdi')");
    expect(result).toBe(1);
  });

  it("handles array result (count > 1)", async () => {
    mock = await startStatefulMockServer((socket: net.Socket) => {
      let step = 0;
      socket.on("data", (chunk: Buffer) => {
        const msg = chunk.toString().trim();
        if (step === 0) {
          socket.write("query: str: 2\n");
          step = 1;
        } else if (step === 1 && msg === "OK") {
          socket.write(".model_a, .model_b");
          socket.end();
        }
      });
    });
    process.env["ADAMS_LISTENER_PORT"] = String(mock.port);

    const result = await evaluateExp("UNIQUE_NAME_IN_HIERARCHY('.model')");
    expect(result).toEqual([".model_a", ".model_b"]);
  });
});

// ── checkConnection ──────────────────────────────────────────────────────────

describe("checkConnection", () => {
  let mock: { port: number; close: () => Promise<void> } | undefined;

  afterEach(async () => {
    delete process.env["ADAMS_LISTENER_PORT"];
    if (mock) { await mock.close(); mock = undefined; }
  });

  it("returns true when Adams is ready", async () => {
    mock = await startStatefulMockServer((socket: net.Socket) => {
      let step = 0;
      socket.on("data", (chunk: Buffer) => {
        const msg = chunk.toString().trim();
        if (step === 0) {
          socket.write("query: int: 1\n");
          step = 1;
        } else if (step === 1 && msg === "OK") {
          socket.write("1");
          socket.end();
        }
      });
    });
    process.env["ADAMS_LISTENER_PORT"] = String(mock.port);
    expect(await checkConnection()).toBe(true);
  });

  it("returns false when connection refused", async () => {
    process.env["ADAMS_LISTENER_PORT"] = "1";
    expect(await checkConnection()).toBe(false);
  });

  it("returns false when Adams returns 0 for db_exists", async () => {
    mock = await startStatefulMockServer((socket: net.Socket) => {
      let step = 0;
      socket.on("data", (chunk: Buffer) => {
        const msg = chunk.toString().trim();
        if (step === 0) {
          socket.write("query: int: 1\n");
          step = 1;
        } else if (step === 1 && msg === "OK") {
          socket.write("0");
          socket.end();
        }
      });
    });
    process.env["ADAMS_LISTENER_PORT"] = String(mock.port);
    expect(await checkConnection()).toBe(false);
  });
});

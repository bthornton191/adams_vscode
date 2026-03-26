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

  it("handles Adams parenthesized string array (db_children format)", async () => {
    mock = await startStatefulMockServer((socket: net.Socket) => {
      let step = 0;
      socket.on("data", (chunk: Buffer) => {
        const msg = chunk.toString().trim();
        if (step === 0) {
          socket.write("query: str: 4: 0");
          step = 1;
        } else if (step === 1 && msg === "OK") {
          socket.write("('.suspension.ground', '.suspension.Lower_Arm', '.suspension.Upper_Arm', '.suspension.Spindle_Wheel')");
          socket.end();
        }
      });
    });
    process.env["ADAMS_LISTENER_PORT"] = String(mock.port);

    const result = await evaluateExp("db_children(suspension, 'part')");
    expect(result).toEqual([
      ".suspension.ground",
      ".suspension.Lower_Arm",
      ".suspension.Upper_Arm",
      ".suspension.Spindle_Wheel",
    ]);
  });

  it("handles Adams parenthesized int array (object ID format)", async () => {
    mock = await startStatefulMockServer((socket: net.Socket) => {
      let step = 0;
      socket.on("data", (chunk: Buffer) => {
        const msg = chunk.toString().trim();
        if (step === 0) {
          socket.write("query: int: 3: 12");
          step = 1;
        } else if (step === 1 && msg === "OK") {
          socket.write("(19, 20, 17)");
          socket.end();
        }
      });
    });
    process.env["ADAMS_LISTENER_PORT"] = String(mock.port);

    const result = await evaluateExp("{strut_lower.id, strut_upper.id, steering_rack.id}");
    expect(result).toEqual([19, 20, 17]);
  });

  it("throws a useful error on SERVER_ERROR and completes the protocol", async () => {
    // Track that Adams received "OK" after sending SERVER_ERROR — this ensures
    // the command server is not left in a stuck state.
    let receivedOkAfterError = false;
    let errorDataSent = false;

    mock = await startStatefulMockServer((socket: net.Socket) => {
      let step = 0;
      socket.on("data", (chunk: Buffer) => {
        const msg = chunk.toString().trim();
        if (step === 0) {
          // Adams sends SERVER_ERROR for invalid expression
          socket.write("SERVER_ERROR");
          step = 1;
        } else if (step === 1 && msg === "OK") {
          receivedOkAfterError = true;
          // Adams sends a generic error string as the data payload
          socket.write("Cannot evaluate expression: jibberish");
          errorDataSent = true;
          socket.end();
        }
      });
    });
    process.env["ADAMS_LISTENER_PORT"] = String(mock.port);

    await expect(evaluateExp("jibberish")).rejects.toThrow(/Cannot evaluate expression: jibberish/);
    expect(receivedOkAfterError).toBe(true);
    expect(errorDataSent).toBe(true);
  });

  it("can make a successful query after a SERVER_ERROR on the same server", async () => {
    // Simulates the real-world scenario: one invalid query, then a valid one —
    // each on its own connection. The server should handle both correctly.
    let callCount = 0;
    mock = await startStatefulMockServer((socket: net.Socket) => {
      callCount++;
      const isFirstCall = callCount === 1;
      let step = 0;
      socket.on("data", (chunk: Buffer) => {
        const msg = chunk.toString().trim();
        if (step === 0) {
          socket.write(isFirstCall ? "SERVER_ERROR" : "query: int: 1");
          step = 1;
        } else if (step === 1 && msg === "OK") {
          socket.write(isFirstCall ? "Error: bad expression" : "1");
          socket.end();
        }
      });
    });
    process.env["ADAMS_LISTENER_PORT"] = String(mock.port);

    await expect(evaluateExp("bad_expr")).rejects.toThrow();
    const result = await evaluateExp("db_exists('.mdi')");
    expect(result).toBe(1);
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
    // Start a server that immediately destroys every connection
    const refused = await startStatefulMockServer((socket: net.Socket) => { socket.destroy(); });
    process.env["ADAMS_LISTENER_PORT"] = String(refused.port);
    try {
      expect(await checkConnection()).toBe(false);
    } finally {
      await refused.close();
    }
  }, 15000);

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

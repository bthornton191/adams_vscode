/**
 * client.ts — Promise-based TCP client for Adams View command server.
 *
 * Re-implements the wire protocol from src/aview.ts.js with:
 *   - No vscode dependency
 *   - Proper response buffering
 *   - 10-second timeout on all operations
 *   - Promise-based API (no callbacks)
 */

import * as net from "net";
import { DEFAULT_PORT, TIMEOUT_MS } from "./constants.js";

export type AdamsValue = string | number | boolean;

/** Resolve the Adams View command server port from the environment. */
export function getPort(): number {
  const env = process.env["ADAMS_LISTENER_PORT"];
  if (env !== undefined && env !== "") {
    const parsed = parseInt(env, 10);
    if (!isNaN(parsed)) return parsed;
  }
  return DEFAULT_PORT;
}

/**
 * Parse the description line returned by Adams View for a query request.
 * Adams returns e.g. "query: str: 1" — split on one-or-more spaces/colons.
 *
 * @returns [type, count]
 */
export function parseDescription(response: string): [string, number] {
  const parts = response.trim().split(/[ :]+/);
  const type = parts[1] ?? "str";
  const count = parseInt(parts[2] ?? "1", 10);
  return [type, isNaN(count) ? 1 : count];
}

/**
 * Parse the data line returned by Adams View for a query response.
 * Coerces values according to type: int→number, float→number,
 * str "on/off/yes/no"→boolean, str otherwise→string.
 * Multiple values (count > 1) are returned as an array.
 */
export function parseData(
  response: string,
  type: string,
  count: number
): AdamsValue | AdamsValue[] {
  const raw = response.trim();
  const items: string[] = count > 1 ? raw.split(/,\s*/) : [raw];

  function coerce(s: string): AdamsValue {
    const v = s.trim();
    if (type === "int") return parseInt(v, 10);
    if (type === "float") return parseFloat(v);
    // str type: boolean-like strings
    const lower = v.toLowerCase();
    if (lower === "on" || lower === "yes") return true;
    if (lower === "off" || lower === "no") return false;
    return v;
  }

  const coerced = items.map(coerce);
  return count > 1 ? coerced : coerced[0]!;
}

/** Receive all data from a socket until it closes or emits an error. */
function receiveAll(socket: net.Socket): Promise<string> {
  return new Promise((resolve, reject) => {
    let buf = "";
    socket.on("data", (chunk: Buffer) => {
      buf += chunk.toString();
    });
    socket.once("end", () => resolve(buf));
    socket.once("error", reject);
  });
}

/** Open a TCP connection to Adams View and return the socket. */
function connect(port: number): Promise<net.Socket> {
  return new Promise((resolve, reject) => {
    const socket = net.createConnection({ host: "127.0.0.1", port });
    socket.once("connect", () => resolve(socket));
    socket.once("error", reject);
  });
}

/** Wrap a promise with a timeout. */
function withTimeout<T>(promise: Promise<T>, ms: number, message: string): Promise<T> {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error(message)), ms);
    promise.then(
      (v) => { clearTimeout(timer); resolve(v); },
      (e) => { clearTimeout(timer); reject(e); }
    );
  });
}

function connectionErrorMessage(port: number): string {
  return (
    `Could not connect to Adams View on port ${port}.\n` +
    `Make sure Adams View is open and the Command Server is running.\n` +
    `In Adams View: Tools > Command Server > Start`
  );
}

/**
 * Execute an Adams View command. Throws on error or unexpected response.
 * Adams View returns "cmd: 0" on success.
 */
export async function executeCmd(cmd: string): Promise<void> {
  const port = getPort();
  const socket = await withTimeout(
    connect(port),
    TIMEOUT_MS,
    connectionErrorMessage(port)
  ).catch((e: Error) => {
    throw new Error(connectionErrorMessage(port) + (e.message ? `\n(${e.message})` : ""));
  });

  socket.setNoDelay(true);
  socket.write(`cmd ${cmd}`);

  const response = await withTimeout(
    receiveAll(socket),
    TIMEOUT_MS,
    `Timed out waiting for Adams View response to command.`
  );
  socket.destroy();

  const trimmed = response.trim();
  if (trimmed !== "cmd: 0") {
    throw new Error(
      `Adams View returned an unexpected response: "${trimmed}"\n` +
      `Expected "cmd: 0" for success.`
    );
  }
}

/**
 * Evaluate an Adams View expression and return its typed value.
 * Uses the two-round-trip query protocol.
 */
export async function evaluateExp(exp: string): Promise<AdamsValue | AdamsValue[]> {
  const port = getPort();
  const socket = await withTimeout(
    connect(port),
    TIMEOUT_MS,
    connectionErrorMessage(port)
  ).catch((e: Error) => {
    throw new Error(connectionErrorMessage(port) + (e.message ? `\n(${e.message})` : ""));
  });

  socket.setNoDelay(true);

  try {
    // Round-trip 1: send query, receive description line
    socket.write(`query ${exp}`);

    const desc = await withTimeout(
      new Promise<string>((resolve, reject) => {
        let buf = "";
        function onData(chunk: Buffer) {
          buf += chunk.toString();
          // Adams sends description line then waits for "OK"
          // The line ends with a newline or the socket remains open
          if (buf.includes("\n") || buf.trim().length > 0) {
            socket.removeListener("data", onData);
            resolve(buf);
          }
        }
        socket.on("data", onData);
        socket.once("error", reject);
      }),
      TIMEOUT_MS,
      `Timed out waiting for Adams View query description.`
    );

    const [type, count] = parseDescription(desc);

    // Round-trip 2: send OK, receive data line
    socket.write("OK");

    const dataLine = await withTimeout(
      receiveAll(socket),
      TIMEOUT_MS,
      `Timed out waiting for Adams View query data.`
    );
    socket.destroy();

    return parseData(dataLine, type, count);
  } catch (e) {
    socket.destroy();
    throw e;
  }
}

/**
 * Check whether Adams View is running and its session is ready.
 * Returns true if the TCP port is reachable and `db_exists('.mdi')` returns 1.
 */
export async function checkConnection(): Promise<boolean> {
  try {
    const result = await evaluateExp("db_exists('.mdi')");
    return result === 1 || result === true;
  } catch {
    return false;
  }
}

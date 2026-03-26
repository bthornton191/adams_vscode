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
import { DEFAULT_PORT, TIMEOUT_MS, QUERY_DESC_TIMEOUT_MS } from "./constants.js";

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
 *
 * Adams wraps array responses in parentheses and string elements in single
 * quotes, e.g. `('.item1', '.item2')` or `(19, 20, 17)`. These are stripped.
 */
export function parseData(
  response: string,
  type: string,
  count: number
): AdamsValue | AdamsValue[] {
  // Strip outer parentheses (Adams wraps arrays in parens in text mode)
  let raw = response.trim();
  if (raw.startsWith("(") && raw.endsWith(")")) {
    raw = raw.slice(1, -1).trim();
  }

  const items: string[] = count > 1 ? raw.split(/,\s*/) : [raw];

  function coerce(s: string): AdamsValue {
    let v = s.trim();
    // Strip surrounding single or double quotes (Adams wraps string elements)
    if (
      (v.startsWith("'") && v.endsWith("'")) ||
      (v.startsWith('"') && v.endsWith('"'))
    ) {
      v = v.slice(1, -1);
    }
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

  // Track whether Adams sent us a description (round-trip 1 complete).
  // We must send "OK" to acknowledge the description — but ONLY if Adams
  // actually sent one. Sending a spurious "OK" when Adams sent nothing
  // (e.g. invalid expression → silence → timeout) corrupts the command
  // server state and breaks subsequent connections.
  let descriptionReceived = false;
  let sentOK = false;

  /**
   * Gracefully close the socket.
   * Sends "OK" first only if Adams sent us a description and we haven't
   * acknowledged it yet — completing the protocol so Adams can reset.
   * Uses FIN (socket.end) rather than RST (socket.destroy) so Adams gets
   * a clean close signal.
   */
  function closeSocket() {
    if (descriptionReceived && !sentOK) {
      try { socket.write("OK"); sentOK = true; } catch { /* ignore */ }
    }
    socket.end();
    // Safety net: force-destroy after 2 s if Adams doesn't close its end.
    const t = setTimeout(() => { try { socket.destroy(); } catch { /* ignore */ } }, 2000);
    if (t.unref) t.unref();
  }

  try {
    // Round-trip 1: send query, receive description line.
    // Adams sends the description in a single packet (no trailing newline in
    // the protocol), so we resolve as soon as any data arrives.
    socket.write(`query ${exp}`);

    const desc = await withTimeout(
      new Promise<string>((resolve, reject) => {
        let buf = "";
        function onData(chunk: Buffer) {
          buf += chunk.toString();
          if (buf.trim().length > 0) {
            socket.removeListener("data", onData);
            socket.removeListener("end", onEnd);
            resolve(buf);
          }
        }
        function onEnd() {
          socket.removeListener("data", onData);
          if (buf.trim().length > 0) {
            resolve(buf);
          } else {
            reject(new Error(
              `Adams View closed the connection without responding to query "${exp}". ` +
              `The expression may be invalid or Adams may not be ready.`
            ));
          }
        }
        socket.on("data", onData);
        socket.once("end", onEnd);
        socket.once("error", reject);
      }),
      QUERY_DESC_TIMEOUT_MS,
      `Adams View did not respond to query "${exp}". ` +
      `The expression may be invalid — check the Adams View message window for details.`
    );

    // Adams sent a description — we are now obligated to send "OK"
    descriptionReceived = true;
    const trimmedDesc = desc.trim();

    // Per Adams docs: for an invalid expression Adams sends "SERVER_ERROR" as
    // the description. The client MUST still send "OK", then Adams sends a
    // generic error string as the data payload. We read that string and throw.
    if (trimmedDesc.startsWith("SERVER_ERROR")) {
      socket.write("OK");
      sentOK = true;
      const errData = await withTimeout(
        new Promise<string>((resolve, reject) => {
          let buf = "";
          function onData(chunk: Buffer) {
            buf += chunk.toString();
            if (buf.trim().length > 0) {
              socket.removeListener("data", onData);
              resolve(buf);
            }
          }
          socket.on("data", onData);
          socket.once("end", () => resolve(buf));
          socket.once("error", reject);
        }),
        TIMEOUT_MS,
        `Timed out waiting for Adams View error details for "${exp}".`
      );
      closeSocket();
      throw new Error(
        `Adams View could not evaluate "${exp}": ${errData.trim() || "unknown error"}. ` +
        `Check the Adams View message window for details.`
      );
    }

    // If Adams returned a command-level error (e.g. "cmd: 1") instead of
    // entering the query protocol, surface it immediately.
    if (trimmedDesc.startsWith("cmd:")) {
      closeSocket();
      const code = trimmedDesc.split(/[ :]+/)[1] ?? "?";
      throw new Error(
        `Adams View rejected the expression "${exp}" (Adams error code ${code}). ` +
        `Check the Adams View message window for details.`
      );
    }

    const [type, count] = parseDescription(desc);

    // Round-trip 2: send OK, receive data line.
    // Use a data-handler (not receiveAll) so we don't hang if Adams sends the
    // data but doesn't close the socket.
    socket.write("OK");
    sentOK = true;

    const dataLine = await withTimeout(
      new Promise<string>((resolve, reject) => {
        let buf = "";
        function onData(chunk: Buffer) {
          buf += chunk.toString();
          if (buf.trim().length > 0) {
            socket.removeListener("data", onData);
            resolve(buf);
          }
        }
        socket.on("data", onData);
        socket.once("end", () => resolve(buf));
        socket.once("error", reject);
      }),
      TIMEOUT_MS,
      `Timed out waiting for Adams View query data for "${exp}".`
    );
    socket.destroy();

    return parseData(dataLine, type, count);
  } catch (e) {
    closeSocket();
    throw e;
  }
}

/**
 * Check whether Adams View is running and its session is ready.
 * Returns true if the TCP port is reachable and `db_exists('.mdi')` returns 1.
 * Retries once after a short delay to handle transient connection resets.
 */
export async function checkConnection(): Promise<boolean> {
  for (let attempt = 0; attempt < 2; attempt++) {
    try {
      const result = await evaluateExp("db_exists('.mdi')");
      if (result === 1 || result === true) return true;
    } catch {
      // Not ready yet
    }
    if (attempt === 0) {
      await new Promise((r) => setTimeout(r, 1000));
    }
  }
  return false;
}

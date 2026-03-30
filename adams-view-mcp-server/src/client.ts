/**
 * client.ts — Promise-based TCP client for Adams View command server.
 *
 * Uses the "cmd" protocol for commands and Python-based evaluation for
 * expressions. The raw TCP "query" protocol is avoided because Adams
 * versions before 2025.2 hang indefinitely for invalid expressions.
 * Instead, evaluateExp() runs Adams.evaluate_exp() via a Python script
 * and reads the result from a temp file.
 */

import * as crypto from "crypto";
import * as fs from "fs/promises";
import * as net from "net";
import * as os from "os";
import * as path from "path";
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
 *
 * @param cmd The command string to send.
 * @param timeoutMs Response timeout in milliseconds (default: TIMEOUT_MS).
 *                  Use a larger value for long-running commands.
 */
export async function executeCmd(cmd: string, timeoutMs?: number): Promise<void> {
  const ms = timeoutMs ?? TIMEOUT_MS;
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
    ms,
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
 * Send an Adams View command without waiting for a response (fire-and-forget).
 *
 * Connects, writes the command, and closes the socket immediately without
 * waiting for "cmd: 0". Adams View will still execute the command.
 * Use this when a command may run for minutes or hours and blocking the
 * caller is impractical.
 *
 * Callers receive no confirmation of success or failure. Use
 * checkConnection() to poll until Adams View is responsive again, which
 * indicates the command has finished.
 */
export async function sendCmd(cmd: string): Promise<void> {
  const port = getPort();
  const socket = await withTimeout(
    connect(port),
    TIMEOUT_MS,
    connectionErrorMessage(port)
  ).catch((e: Error) => {
    throw new Error(connectionErrorMessage(port) + (e.message ? `\n(${e.message})` : ""));
  });

  socket.setNoDelay(true);
  await new Promise<void>((resolve, reject) => {
    socket.write(`cmd ${cmd}`, (err) => {
      socket.destroy();
      if (err) reject(err); else resolve();
    });
  });
}

/**
 * Evaluate an Adams View expression and return its typed value.
 *
 * Runs Adams.evaluate_exp() via a Python script to avoid the known bug in
 * Adams versions before 2025.2 where the TCP "query" protocol hangs
 * indefinitely for invalid expressions.
 */
export async function evaluateExp(exp: string): Promise<AdamsValue | AdamsValue[]> {
  const tmpDir = await fs.mkdtemp(path.join(os.tmpdir(), "adams-mcp-eval-"));
  const scriptFile = path.join(tmpDir, "eval.py");
  const outputFile = path.join(tmpDir, `out-${crypto.randomUUID()}.txt`);
  const outputFileAdams = outputFile.replace(/\\/g, "/");

  // Safely embed the expression as a JSON-encoded Python string literal.
  const expJson = JSON.stringify(exp);

  const script = [
    `import Adams, sys as _mcp_sys, io as _mcp_io, json as _mcp_json`,
    `_mcp_buf = _mcp_io.StringIO()`,
    `_mcp_old = _mcp_sys.stdout`,
    `_mcp_sys.stdout = _mcp_buf`,
    `try:`,
    `    _mcp_result = Adams.evaluate_exp(${expJson})`,
    `    print(_mcp_json.dumps({"v": _mcp_result}))`,
    `except Exception as _mcp_e:`,
    `    print(_mcp_json.dumps({"e": str(_mcp_e)}))`,
    `finally:`,
    `    _mcp_sys.stdout = _mcp_old`,
    `    with open(${JSON.stringify(outputFileAdams)}, "w", encoding="utf-8") as _mcp_f:`,
    `        _mcp_f.write(_mcp_buf.getvalue())`,
  ].join("\n");

  try {
    await fs.writeFile(scriptFile, script, "utf8");
    await executeCmd(
      `file python read file_name="${scriptFile.replace(/\\/g, "/")}"`
    );

    let raw: string;
    try {
      raw = (await fs.readFile(outputFile, "utf8")).trim();
    } catch {
      throw new Error(
        `Adams View did not produce output for expression "${exp}". ` +
        `Check the Adams View message window for details.`
      );
    }

    if (!raw) {
      throw new Error(
        `Adams View returned empty output for expression "${exp}". ` +
        `Check the Adams View message window for details.`
      );
    }

    const parsed = JSON.parse(raw);

    if (parsed.e !== undefined) {
      throw new Error(
        `Adams View could not evaluate "${exp}": ${parsed.e}. ` +
        `Check the Adams View message window for details.`
      );
    }

    return coerceValue(parsed.v);
  } catch (e) {
    if (e instanceof SyntaxError) {
      throw new Error(
        `Adams View returned invalid output for expression "${exp}". ` +
        `Check the Adams View message window for details.`
      );
    }
    throw e;
  } finally {
    await fs.unlink(scriptFile).catch(() => undefined);
    await fs.unlink(outputFile).catch(() => undefined);
    await fs.rmdir(tmpDir).catch(() => undefined);
  }
}

/**
 * Coerce a value returned by Adams.evaluate_exp() (via JSON) into the
 * AdamsValue types expected by callers. JSON preserves ints, floats,
 * strings, booleans, and arrays natively. The only extra coercion needed
 * is Adams' boolean-like strings ("on"/"off"/"yes"/"no").
 */
function coerceValue(v: unknown): AdamsValue | AdamsValue[] {
  if (Array.isArray(v)) {
    return v.map((item) => coerceSingle(item));
  }
  return coerceSingle(v);
}

function coerceSingle(v: unknown): AdamsValue {
  if (typeof v === "number" || typeof v === "boolean") return v;
  if (typeof v === "string") {
    const lower = v.toLowerCase();
    if (lower === "on" || lower === "yes") return true;
    if (lower === "off" || lower === "no") return false;
    return v;
  }
  return String(v);
}

/**
 * Check whether Adams View is running and its session is ready.
 * Returns true if Adams can execute a command and db_exists('.mdi') returns 1.
 */
export async function checkConnection(): Promise<boolean> {
  try {
    const result = await evaluateExp("db_exists('.mdi')");
    return result === 1 || result === true;
  } catch {
    return false;
  }
}

/**
 * tests/e2e.test.ts — End-to-end tests against a live Adams View instance.
 *
 * Adams View is auto-launched if not already running (requires ADAMS_LAUNCH_COMMAND
 * or ADAMS_INSTALL_DIR env var, or Adams installed in the default location).
 * All tests are automatically skipped when Adams cannot be started, so these
 * are safe to run in CI where Adams is not installed.
 *
 * Run with:
 *   npm run test:e2e
 */

import { describe, it, expect, beforeAll, afterAll } from "vitest";
import { checkConnection, evaluateExp, executeCmd } from "../src/client.js";
import { setupAdams, teardownAdams } from "./adams-fixtures.js";

// ── Lifecycle ─────────────────────────────────────────────────────────────────

beforeAll(setupAdams, 180_000);
afterAll(teardownAdams, 30_000);

// ── Test helper ───────────────────────────────────────────────────────────────

function e2e(name: string, fn: () => Promise<void>, timeoutMs = 15_000) {
  it(name, async () => {
    if (!await checkConnection()) {
      console.log(`[e2e] Adams not reachable — skipping: ${name}`);
      return;
    }
    await fn();
  }, timeoutMs);
}

// ── Basic connectivity ────────────────────────────────────────────────────────

describe("E2E: checkConnection", () => {
  e2e("returns true when Adams is running", async () => {
    const result = await checkConnection();
    expect(result).toBe(true);
  });
});

// ── Valid expressions ─────────────────────────────────────────────────────────

describe("E2E: evaluateExp — valid expressions", () => {
  e2e("evaluates db_exists('.mdi') as truthy", async () => {
    const result = await evaluateExp("db_exists('.mdi')");
    // Returns 1 or true depending on Adams version
    expect(result === 1 || result === true).toBe(true);
  });

  e2e("evaluates getcwd() and returns a non-empty string", async () => {
    const result = await evaluateExp("getcwd()");
    expect(typeof result).toBe("string");
    expect((result as string).length).toBeGreaterThan(0);
  });

  e2e("can make a second query after a successful first query", async () => {
    const first = await evaluateExp("db_exists('.mdi')");
    expect(first === 1 || first === true).toBe(true);
    const second = await evaluateExp("getcwd()");
    expect(typeof second).toBe("string");
  });
});

// ── Invalid expressions ───────────────────────────────────────────────────────

describe("E2E: evaluateExp — invalid expressions", () => {
  e2e(
    "throws an error (not a timeout) for an invalid expression",
    async () => {
      const start = Date.now();
      let threw = false;
      let errorMessage = "";
      try {
        await evaluateExp("this_function_does_not_exist_xyz()");
      } catch (e: unknown) {
        threw = true;
        errorMessage = e instanceof Error ? e.message : String(e);
      }
      const elapsed = Date.now() - start;

      // Must throw, not silently succeed
      expect(threw).toBe(true);

      // Must NOT hit the 10-second timeout — should fail fast (within 3s + buffer)
      expect(elapsed).toBeLessThan(6_000);

      console.log(`[e2e] Invalid expression error (${elapsed}ms): ${errorMessage}`);
    },
    20_000
  );

  e2e(
    "connection is still usable after an invalid expression",
    async () => {
      // This is the key regression test — previously Adams got stuck waiting
      // for "OK" and subsequent connections would fail.
      try {
        await evaluateExp("this_function_does_not_exist_xyz()");
      } catch {
        // Expected — ignore the error
      }

      // The command server must still be reachable
      const stillConnected = await checkConnection();
      if (!stillConnected) {
        throw new Error(
          "Adams View command server is no longer reachable after an invalid expression. " +
          "The protocol cleanup (sending OK before closing) may be broken."
        );
      }
    },
    20_000
  );

  e2e(
    "can evaluate a valid expression after a previous invalid one",
    async () => {
      try {
        await evaluateExp("this_function_does_not_exist_xyz()");
      } catch {
        // Expected
      }

      // Must be able to evaluate a valid expression on the same connection
      const result = await evaluateExp("db_exists('.mdi')");
      expect(result === 1 || result === true).toBe(true);
    },
    20_000
  );

  e2e(
    "logs what Adams actually sends for an invalid expression",
    async () => {
      // This test always passes — it just prints the raw error so we know
      // exactly what Adams sends. Useful for debugging the wire protocol.
      try {
        await evaluateExp("jibberish_xyz_abc");
      } catch (e: unknown) {
        const msg = e instanceof Error ? e.message : String(e);
        console.log(`[e2e] Adams error message for 'jibberish_xyz_abc': ${msg}`);
      }
    },
    20_000
  );
});

// ── executeCmd ────────────────────────────────────────────────────────────────

describe("E2E: executeCmd", () => {
  e2e("succeeds with a valid no-op command", async () => {
    // A comment-only command (!) is a safe no-op in Adams CMD syntax
    await expect(executeCmd("! e2e test ping")).resolves.toBeUndefined();
  });

  e2e("connection is still usable after a failed command", async () => {
    try {
      await executeCmd("this_is_not_a_valid_command_xyz");
    } catch {
      // Expected
    }
    const stillConnected = await checkConnection();
    expect(stillConnected).toBe(true);
  });
});

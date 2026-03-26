/** Default TCP port for Adams View command server */
export const DEFAULT_PORT = 5002;

/** Maximum response size in characters before truncation */
export const CHARACTER_LIMIT = 25000;

/** Timeout for Adams View TCP operations in milliseconds */
export const TIMEOUT_MS = 10000;

/**
 * Timeout for the query description round-trip (round-trip 1 of evaluateExp).
 * Adams either responds to a query immediately (single packet) or not at all
 * (when the expression is invalid). A short timeout lets us surface the error
 * quickly without waiting the full TIMEOUT_MS.
 */
export const QUERY_DESC_TIMEOUT_MS = 3000;

/**
 * tests/helpers.ts — Mock Adams View TCP server for unit tests.
 *
 * Creates a real TCP server on a random OS-assigned port. Each test can
 * configure response behaviour via the handler callback.
 */

import * as net from "net";

export type RequestHandler = (request: string) => string | null;

export interface MockAdamsServer {
  port: number;
  close: () => Promise<void>;
  /**
   * Set the handler for the next (or all) requests.
   * Return a string to send as the response.
   * Return null to send no response (useful for testing timeouts).
   */
  setHandler: (handler: RequestHandler) => void;
}

/**
 * Start a mock Adams View TCP server on a random port.
 * The server handles one request per connection, using the current handler.
 *
 * For query requests (two round-trips), the handler is called twice per
 * connection: once for the initial "query ..." request (return the description
 * line), and once for the "OK" acknowledgement (return the data line).
 */
export async function startMockServer(): Promise<MockAdamsServer> {
  let handler: RequestHandler = () => "cmd: 0";

  const server = net.createServer((socket) => {
    let buf = "";
    socket.on("data", (chunk: Buffer) => {
      buf += chunk.toString();
      const response = handler(buf.trim());
      if (response !== null) {
        socket.write(response);
        buf = "";
        // For cmd responses, close the socket so the client sees end-of-stream
        // For query responses that need two round-trips, the handler keeps the
        // socket open by not destroying it — the client will send "OK" next.
        // We destroy after writing unless this looks like a query description.
        if (!buf.startsWith("query ") && response.includes(": ")) {
          // Might be a query description — wait for "OK"
        } else {
          socket.end();
        }
      }
    });
    socket.on("error", () => socket.destroy());
  });

  await new Promise<void>((resolve) => server.listen(0, "127.0.0.1", resolve));

  const address = server.address() as net.AddressInfo;

  return {
    port: address.port,
    setHandler(h: RequestHandler) {
      handler = h;
    },
    close() {
      return new Promise<void>((resolve, reject) => {
        server.close((err) => (err ? reject(err) : resolve()));
      });
    },
  };
}

/**
 * A stateful handler factory for the two-round-trip query protocol.
 * Returns a handler that processes the first request (sends description),
 * then processes the "OK" acknowledgement (sends data), then ends the socket.
 *
 * Usage: set as the server handler before triggering a query.
 */
export function makeQueryHandler(
  description: string,
  data: string
): (socket: net.Socket) => void {
  return (socket: net.Socket) => {
    let step = 0;
    socket.on("data", (chunk: Buffer) => {
      const msg = chunk.toString().trim();
      if (step === 0 && msg.startsWith("query ")) {
        socket.write(description);
        step = 1;
      } else if (step === 1 && msg === "OK") {
        socket.write(data);
        socket.end();
      }
    });
  };
}

/**
 * Start a mock server with fine-grained per-connection control.
 * Calls connectionHandler for each new connection.
 *
 * All open sockets are force-closed when close() is called, so server.close()
 * always resolves promptly even if a handler leaves a socket open.
 */
export async function startStatefulMockServer(
  connectionHandler: (socket: net.Socket) => void
): Promise<{ port: number; close: () => Promise<void> }> {
  const openSockets = new Set<net.Socket>();
  const server = net.createServer((socket) => {
    openSockets.add(socket);
    socket.once("close", () => openSockets.delete(socket));
    connectionHandler(socket);
  });
  await new Promise<void>((resolve) => server.listen(0, "127.0.0.1", resolve));
  const address = server.address() as net.AddressInfo;
  return {
    port: address.port,
    close() {
      for (const s of openSockets) s.destroy();
      return new Promise<void>((resolve, reject) => {
        server.close((err) => (err ? reject(err) : resolve()));
      });
    },
  };
}

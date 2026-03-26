#!/usr/bin/env node
/**
 * Adams View MCP Server
 *
 * Exposes Adams View operations as MCP tools consumable by any MCP-compatible
 * agent harness. Communicates with Adams View over its TCP command server
 * protocol (default port 5002).
 *
 * Transport: stdio (V1)
 * No VS Code dependency.
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

import { registerQueryTools } from "./tools/query.js";
import { registerCmdTools } from "./tools/cmd.js";
import { registerModelTools } from "./tools/model.js";
import { registerLogTools } from "./tools/log.js";
import { registerSimulationTools } from "./tools/simulation.js";
import { registerSessionTools } from "./tools/session.js";

const server = new McpServer({
  name: "adams-view-mcp-server",
  version: "0.1.0",
});

registerQueryTools(server);
registerCmdTools(server);
registerModelTools(server);
registerLogTools(server);
registerSimulationTools(server);
registerSessionTools(server);

async function main(): Promise<void> {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Adams View MCP server running via stdio");
}

main().catch((error: unknown) => {
  console.error("Fatal error:", error);
  process.exit(1);
});

/**
 * tools/model.ts — Model management tools: adams_delete_model
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { executeCmd } from "../client.js";

function errorResult(message: string) {
  return {
    content: [{ type: "text" as const, text: message }],
    isError: true,
  };
}

/** Normalise a model name to always have a leading dot. */
function normaliseModelName(name: string): string {
  return name.startsWith(".") ? name : `.${name}`;
}

export function registerModelTools(server: McpServer): void {
  // ── adams_delete_model ───────────────────────────────────────────────────
  server.registerTool(
    "adams_delete_model",
    {
      title: "Delete Adams View Model",
      description: `Deletes the named model from the Adams View session.

Accepts either bare name ('my_model') or dot-prefixed path ('.my_model') —
both are normalised internally to the dot-prefixed form that Adams requires.

Args:
  - model_name (string): Model name, e.g. 'my_model' or '.my_model'

Returns:
  Success message, or an error if the model does not exist or deletion fails.

Warning: This operation is irreversible. Unsaved changes to the model will
be lost.`,
      inputSchema: z
        .object({
          model_name: z
            .string()
            .min(1)
            .describe("Model name, e.g. 'my_model' or '.my_model'"),
        })
        .strict(),
      annotations: {
        readOnlyHint: false,
        destructiveHint: true,
        idempotentHint: false,
        openWorldHint: false,
      },
    },
    async ({ model_name }) => {
      const dotName = normaliseModelName(model_name);
      try {
        await executeCmd(`model delete model=${dotName}`);
        return {
          content: [
            {
              type: "text" as const,
              text: `Model ${dotName} deleted successfully.`,
            },
          ],
        };
      } catch (e: unknown) {
        return errorResult(
          `Error deleting model ${dotName}: ${e instanceof Error ? e.message : String(e)}`
        );
      }
    }
  );
}

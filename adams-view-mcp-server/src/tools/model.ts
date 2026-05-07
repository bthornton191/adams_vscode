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

  // ── adams_export_model_cmd ───────────────────────────────────────────────
  server.registerTool(
    "adams_export_model_cmd",
    {
      title: "Export Adams View Model as CMD File",
      description: `Exports the named model to a .cmd file on disk.

Uses 'file command write entity_name=.<model_name> file_name=<file_name>' to
write the full model definition as an Adams CMD script. The resulting file can
be loaded back into Adams View with adams_load_file or shared with others.

Args:
  - model_name (string): Model name, e.g. 'my_model' or '.my_model'
  - file_name (string): Absolute path for the output .cmd file,
    e.g. 'C:/models/my_model.cmd'

Returns:
  Success message with the file path written, or an error.`,
      inputSchema: z
        .object({
          model_name: z
            .string()
            .min(1)
            .describe("Model name, e.g. 'my_model' or '.my_model'"),
          file_name: z
            .string()
            .min(1)
            .describe("Absolute path for the output .cmd file, e.g. 'C:/models/my_model.cmd'"),
        })
        .strict(),
      annotations: {
        readOnlyHint: false,
        destructiveHint: false,
        idempotentHint: true,
        openWorldHint: false,
      },
    },
    async ({ model_name, file_name }) => {
      const dotName = normaliseModelName(model_name);
      const filePath = file_name.replace(/\\/g, "/");
      try {
        await executeCmd(
          `file command write entity_name=${dotName} file_name="${filePath}"`
        );
        return {
          content: [
            {
              type: "text" as const,
              text: `Model ${dotName} exported to: ${filePath}`,
            },
          ],
        };
      } catch (e: unknown) {
        return errorResult(
          `Error exporting model ${dotName}: ${e instanceof Error ? e.message : String(e)}`
        );
      }
    }
  );
}

/**
 * tools/simulation.ts — Simulation tools:
 *   adams_create_simulation_script, adams_submit_simulation
 */

import * as fs from "fs/promises";
import * as path from "path";
import { spawn } from "child_process";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { evaluateExp, executeCmd } from "../client.js";

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

/** Strip the leading dot from a model name to get the bare name. */
function bareModelName(dotName: string): string {
  return dotName.startsWith(".") ? dotName.slice(1) : dotName;
}

export function registerSimulationTools(server: McpServer): void {
  // ── adams_create_simulation_script ────────────────────────────────────────
  server.registerTool(
    "adams_create_simulation_script",
    {
      title: "Create Adams Simulation Script",
      description: `Creates a solver simulation script in Adams View and exports the model and
command files to a directory.

Steps:
  1. Creates a simulation script object in Adams View from an array of Adams
     Solver commands (e.g. SIMULATE/DYNAMIC, STOP).
  2. Exports the model dataset (.adm) to output_directory/<model_name>.adm
  3. Writes the solver command file (.acf) to output_directory/<model_name>.acf

The script remains in the Adams View model for reuse. The returned acf_path
can be passed directly to adams_submit_simulation.

Args:
  - model_name (string): Model name, e.g. 'my_model' or '.my_model'
  - solver_commands (string[]): Adams Solver commands, e.g.
    ["SIMULATE/DYNAMIC, END=1.0, DTOUT=0.01", "STOP"]
  - script_name (string, optional): Name for the script object within the
    model. Defaults to 'mcp_sim_script'.
  - output_directory (string): Absolute path to directory for .adm/.acf output

Returns:
  { "adm_path": string, "acf_path": string, "script_name": string }`,
      inputSchema: z
        .object({
          model_name: z.string().min(1).describe("Model name, e.g. 'my_model' or '.my_model'"),
          solver_commands: z
            .array(z.string().min(1))
            .min(1)
            .describe(
              "Array of Adams Solver commands, e.g. [\"SIMULATE/DYNAMIC, END=1.0, DTOUT=0.01\", \"STOP\"]"
            ),
          script_name: z
            .string()
            .optional()
            .describe(
              "Name for the simulation script object within the model. Defaults to 'mcp_sim_script'."
            ),
          output_directory: z
            .string()
            .min(1)
            .describe(
              "Absolute path to the directory where .adm and .acf files will be written"
            ),
        })
        .strict(),
      annotations: {
        readOnlyHint: false,
        destructiveHint: false,
        idempotentHint: false,
        openWorldHint: false,
      },
    },
    async ({ model_name, solver_commands, script_name, output_directory }) => {
      // Validate output directory exists
      try {
        await fs.access(output_directory);
      } catch {
        return errorResult(`Output directory not found: ${output_directory}`);
      }

      const dotModel = normaliseModelName(model_name);
      const bare = bareModelName(dotModel);
      const scriptBaseName = script_name ?? "mcp_sim_script";
      const fullScriptName = `${dotModel}.${scriptBaseName}`;

      // Format solver commands as Adams CMD array syntax
      const solverCommandsArg = solver_commands
        .map((c) => `"${c.replace(/"/g, '\\"')}"`)
        .join(", &\n                  ");

      const admPath = path.join(output_directory, `${bare}.adm`).replace(/\\/g, "/");
      const acfPath = path.join(output_directory, `${bare}.acf`).replace(/\\/g, "/");

      // Step 1: Create simulation script
      try {
        await executeCmd(
          `simulation script create &\n` +
          `  sim_script_name=${fullScriptName} &\n` +
          `  solver_commands=${solverCommandsArg}`
        );
      } catch (e: unknown) {
        return errorResult(
          `Error creating simulation script: ${e instanceof Error ? e.message : String(e)}`
        );
      }

      // Step 2: Export .adm dataset
      try {
        await executeCmd(
          `file adams_data_set write &\n` +
          `  model_name=${dotModel} &\n` +
          `  file_name="${admPath}"`
        );
      } catch (e: unknown) {
        // Best-effort cleanup: delete the script
        await executeCmd(`simulation script delete sim_script_name=${fullScriptName}`).catch(
          () => undefined
        );
        return errorResult(
          `Error exporting .adm file: ${e instanceof Error ? e.message : String(e)}`
        );
      }

      // Step 3: Write .acf command file
      try {
        await executeCmd(
          `simulation script write_acf &\n` +
          `  sim_script_name=${fullScriptName} &\n` +
          `  file_name="${acfPath}"`
        );
      } catch (e: unknown) {
        await executeCmd(`simulation script delete sim_script_name=${fullScriptName}`).catch(
          () => undefined
        );
        return errorResult(
          `Error writing .acf file: ${e instanceof Error ? e.message : String(e)}`
        );
      }

      const result = {
        adm_path: admPath,
        acf_path: acfPath,
        script_name: fullScriptName,
      };
      return {
        content: [{ type: "text" as const, text: JSON.stringify(result, null, 2) }],
      };
    }
  );

  // ── adams_submit_simulation ───────────────────────────────────────────────
  server.registerTool(
    "adams_submit_simulation",
    {
      title: "Submit Adams Simulation",
      description: `Runs Adams Solver standalone on an existing .acf file.

The solver is launched as a detached background process and this tool returns
immediately with the expected output file paths. The solver runs in the same
directory as the .acf file.

After submitting, read the .msg file to monitor progress. The simulation is
complete when the .msg file contains 'Simulation complete' or shows an error.

Args:
  - acf_path (string): Absolute path to the .acf (Adams Command File) to run.
    The .adm file must be in the same directory.

Returns:
  {
    "pid": number,
    "working_directory": string,
    "acf_path": string,
    "adm_path": string,
    "msg_path": string,
    "res_path": string,
    "req_path": string,
    "gra_path": string,
    "message": string
  }

Errors:
  - ACF file not found
  - Adams View not connected (can't resolve TOPDIR)
  - Adams Solver executable not found at resolved path
  - Spawn failure`,
      inputSchema: z
        .object({
          acf_path: z
            .string()
            .min(1)
            .describe(
              "Absolute path to the .acf (Adams Command File) to run. The .adm must be in the same directory."
            ),
        })
        .strict(),
      annotations: {
        readOnlyHint: false,
        destructiveHint: false,
        idempotentHint: false,
        openWorldHint: false,
      },
    },
    async ({ acf_path }) => {
      // Validate .acf file exists
      try {
        await fs.access(acf_path);
      } catch {
        return errorResult(`ACF file not found: ${acf_path}`);
      }

      const workingDir = path.dirname(acf_path);
      const acfFilename = path.basename(acf_path);
      const modelBase = path.basename(acf_path, ".acf");

      // Get Adams installation root from Adams View
      let topdir: string;
      try {
        const raw = await evaluateExp(`GETENV("TOPDIR")`);
        topdir = String(raw).trim();
        if (!topdir) {
          return errorResult(
            `Could not determine Adams installation directory. Is Adams View running? Run adams_check_connection first.`
          );
        }
      } catch {
        return errorResult(
          `Could not determine Adams installation directory. Is Adams View running? Run adams_check_connection first.`
        );
      }

      // Resolve solver executable
      const isWindows = process.platform === "win32";
      const mdiPath = isWindows
        ? path.join(topdir, "common", "mdi.bat")
        : path.join(topdir, "mdi");
      const args = isWindows
        ? ["ru-s", acfFilename]
        : ["-c", "ru-s", acfFilename, "exit"];

      // Validate executable exists
      try {
        await fs.access(mdiPath);
      } catch {
        return errorResult(
          `Adams Solver executable not found at: ${mdiPath}. Verify your Adams installation.`
        );
      }

      // Spawn detached solver
      let pid: number | undefined;
      try {
        const solver = spawn(mdiPath, args, {
          cwd: workingDir,
          detached: true,
          stdio: "ignore",
        });
        solver.unref();
        pid = solver.pid;
      } catch (e: unknown) {
        return errorResult(
          `Failed to launch Adams Solver: ${e instanceof Error ? e.message : String(e)}`
        );
      }

      const result = {
        pid: pid ?? null,
        working_directory: workingDir,
        acf_path,
        adm_path: path.join(workingDir, `${modelBase}.adm`),
        msg_path: path.join(workingDir, `${modelBase}.msg`),
        res_path: path.join(workingDir, `${modelBase}.res`),
        req_path: path.join(workingDir, `${modelBase}.req`),
        gra_path: path.join(workingDir, `${modelBase}.gra`),
        message: `Adams Solver started (PID ${pid ?? "unknown"}). Monitor progress by reading the .msg file. The simulation is complete when the .msg file contains 'Simulation complete' or the process exits.`,
      };

      return {
        content: [{ type: "text" as const, text: JSON.stringify(result, null, 2) }],
      };
    }
  );
}

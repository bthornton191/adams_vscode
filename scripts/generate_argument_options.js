#!/usr/bin/env node
/**
 * generate_argument_options.js  (v2 — with @macro_reference expansion)
 *
 * Parses the Adams View command language definition file and generates a JSON
 * file (argument_options.json) mapping command arguments to their allowed
 * string values.
 *
 * Usage:
 *   node scripts/generate_argument_options.js <path/to/cmd_language_def_file>
 *   or set the CMD_LANG_SRC environment variable.
 *
 */

"use strict";

const fs = require("fs");
const path = require("path");

const LANGUAGE_SRC = process.argv[2] || process.env.CMD_LANG_SRC;

if (!LANGUAGE_SRC) {
    console.error(
        "Usage: node scripts/generate_argument_options.js <path/to/cmd_language_def_file>",
    );
    console.error("   or: CMD_LANG_SRC=<path> node scripts/generate_argument_options.js");
    console.error("");
    process.exit(1);
}

const STRUCTURED_JSON = path.resolve(__dirname, "../resources/adams_view_commands/structured.json");
const OUTPUT_JSON = path.resolve(
    __dirname,
    "../resources/adams_view_commands/argument_options.json",
);

// ---------------------------------------------------------------------------
// Step 1 – Parse %OPTION_TYPE [val1, val2, ...]; definitions
// ---------------------------------------------------------------------------

/**
 * Returns a Map<string, string[]> where keys are type names (UPPERCASE) and
 * values are the allowed string values for that type.
 */
function parseOptionTypes(src) {
    const types = new Map();
    const lines = src.split("\n");
    let i = 0;
    while (i < lines.length) {
        // Match leading %NAME [ possibly with leading whitespace
        const m = lines[i].match(/^\s*%(\w+)\s*\[(.*)/);
        if (m) {
            const typeName = m[1].toUpperCase();
            let text = m[2];

            // Collect continuation lines until we find the closing bracket
            while (!text.includes("]") && i + 1 < lines.length) {
                i++;
                // Strip leading "!" comment marker (used for multi-line options)
                const cont = lines[i].replace(/^\s*!\s*/, " ");
                text += cont;
            }

            const closeIdx = text.indexOf("]");
            const valuesPart = closeIdx >= 0 ? text.substring(0, closeIdx) : text;

            const values = valuesPart
                .split(/[,\n]/)
                .map((v) => v.trim())
                .filter((v) => v.length > 0 && v !== ";");

            if (values.length > 0) {
                types.set(typeName, values);
            }
        }
        i++;
    }
    return types;
}

// ---------------------------------------------------------------------------
// Step 2 – Parse leaf macro blocks (#name <func> arg=TYPE ...; ) into a map
//           macros: Map<string, Map<string, string>>
//           where: macroName -> (argName -> typeName)
// ---------------------------------------------------------------------------

/**
 * Split the source into macro blocks.
 *
 * Each block starts at a line beginning with '#' (not '#page' comment or
 * similar comment-only lines) and ends at the next such block or end of file.
 */
function splitIntoMacros(lines) {
    const blocks = [];
    let current = null;

    for (const line of lines) {
        const macroStart = line.match(/^#(\w+)/);
        if (macroStart) {
            if (current) blocks.push(current);
            current = { name: macroStart[1], lines: [line] };
        } else if (current) {
            current.lines.push(line);
        }
    }
    if (current) blocks.push(current);
    return blocks;
}

/**
 * Parse a single block and return:
 *   { isLeaf: bool, args: Map<argName, typeName>, refs: string[] }
 *
 * isLeaf is true when the block contains a <cmd_xxx> function call.
 * args contains directly defined argument→type pairs.
 * refs lists @macro_name references to expand later.
 */
function parseBlock(block) {
    const isLeaf = block.lines.some((l) => /^\s*<\w+>/.test(l));
    const args = new Map();
    const refs = [];

    for (const line of block.lines) {
        const trimmed = line.trim();
        if (!trimmed) continue;

        // @macro_reference — capture for expansion
        const refMatch = trimmed.match(/^@(\w+)/);
        if (refMatch) {
            refs.push(refMatch[1]);
            continue;
        }

        // Skip structural / comment / other non-arg lines
        if (
            trimmed.startsWith("!") ||
            trimmed.startsWith("#") ||
            trimmed.startsWith("%") ||
            trimmed.startsWith("<") ||
            trimmed.startsWith("{") ||
            trimmed.startsWith("}") ||
            trimmed.startsWith("[") ||
            trimmed.startsWith("]") ||
            trimmed.startsWith(":")
        ) {
            continue;
        }

        // Match: arg_name[?helpHint] = TYPE_NAME[(constraints)][=default][*]
        const m = trimmed.match(/^([a-z_]\w*)(?:\?\w+)?\s*=\s*([A-Za-z][A-Za-z0-9_]*)/);
        if (m) {
            const argName = m[1];
            const typeName = m[2].toUpperCase();
            if (!args.has(argName)) {
                args.set(argName, typeName);
            }
        }
    }

    return { isLeaf, args, refs };
}

/**
 * Parse all blocks, expand @references recursively, and return only leaf
 * macros with their fully-expanded arg→type maps.
 *
 * @param {string} src
 * @returns {Map<string, Map<string, string>>}
 */
function parseAndExpandMacros(src) {
    const lines = src.split("\n");
    const blocks = splitIntoMacros(lines);

    // Raw parse for every block
    const raw = new Map();
    for (const block of blocks) {
        raw.set(block.name, parseBlock(block));
    }

    // Expand references recursively (depth-first, cycle-safe)
    const expanded = new Map();
    const inProgress = new Set();

    function expand(name) {
        if (expanded.has(name)) return expanded.get(name);
        if (inProgress.has(name)) return new Map(); // cycle guard

        inProgress.add(name);
        const macro = raw.get(name);
        if (!macro) {
            expanded.set(name, new Map());
            inProgress.delete(name);
            return new Map();
        }

        const result = new Map(macro.args); // start with own direct args
        for (const refName of macro.refs) {
            const refArgs = expand(refName);
            for (const [k, v] of refArgs) {
                if (!result.has(k)) result.set(k, v); // first occurrence wins
            }
        }

        expanded.set(name, result);
        inProgress.delete(name);
        return result;
    }

    for (const name of raw.keys()) {
        expand(name);
    }

    // Return only leaf macros with fully-expanded args
    const leafMacros = new Map();
    for (const [name, macro] of raw) {
        if (macro.isLeaf) {
            leafMacros.set(name, expanded.get(name) || new Map());
        }
    }

    return leafMacros;
}

// ---------------------------------------------------------------------------
// Step 3 – For each structured.json command find the best-matching leaf macro
//           by counting how many of the command's args appear in the macro.
// ---------------------------------------------------------------------------

function matchCommandsToMacros(structured, leafMacros) {
    const result = new Map();

    for (const [cmd, args] of Object.entries(structured)) {
        if (!Array.isArray(args) || args.length === 0) continue;
        const argSet = new Set(args.map((a) => a.toLowerCase()));

        let bestMacro = null;
        let bestScore = -1;

        for (const [, macroArgs] of leafMacros) {
            if (macroArgs.size === 0) continue;
            let overlap = 0;
            for (const a of argSet) {
                if (macroArgs.has(a)) overlap++;
            }
            // Score: overlap count + tiebreaker favouring smaller macros
            const score = overlap + overlap / macroArgs.size;
            if (score > bestScore) {
                bestScore = score;
                bestMacro = macroArgs;
            }
        }

        if (bestMacro && bestScore > 0) {
            result.set(cmd, bestMacro);
        }
    }

    return result;
}

// ---------------------------------------------------------------------------
// Step 4 – Build the output JSON
// ---------------------------------------------------------------------------

function main() {
    console.log("Reading command language definition file…");
    const src = fs.readFileSync(LANGUAGE_SRC, "utf8");

    console.log("Parsing option type definitions…");
    const optionTypes = parseOptionTypes(src);
    console.log(`  Found ${optionTypes.size} option types.`);

    console.log("Parsing and expanding macro blocks…");
    const leafMacros = parseAndExpandMacros(src);
    console.log(`  Found ${leafMacros.size} expanded leaf macros.`);

    console.log("Reading structured.json…");
    const structured = JSON.parse(fs.readFileSync(STRUCTURED_JSON, "utf8"));
    console.log(`  Found ${Object.keys(structured).length} commands.`);

    console.log("Matching commands to macros…");
    const commandMacroMap = matchCommandsToMacros(structured, leafMacros);

    console.log("Building argument_options.json…");
    const output = {};
    let commandCount = 0;
    let argCount = 0;

    for (const [cmd, args] of Object.entries(structured)) {
        if (!Array.isArray(args) || args.length === 0) continue;

        const macroArgs = commandMacroMap.get(cmd);
        if (!macroArgs) continue;

        const cmdOptions = {};

        for (const arg of args) {
            const typeName = macroArgs.get(arg.toLowerCase());
            if (!typeName) continue;

            const values = optionTypes.get(typeName);
            if (!values || values.length === 0) continue;

            cmdOptions[arg] = values;
            argCount++;
        }

        if (Object.keys(cmdOptions).length > 0) {
            output[cmd] = cmdOptions;
            commandCount++;
        }
    }

    fs.writeFileSync(OUTPUT_JSON, JSON.stringify(output, null, 2));

    console.log(`\nDone!`);
    console.log(`  Commands with argument options : ${commandCount}`);
    console.log(`  Total arg→values entries       : ${argCount}`);
    console.log(`  Output written to              : ${OUTPUT_JSON}`);
}

main();

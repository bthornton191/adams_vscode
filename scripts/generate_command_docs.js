#!/usr/bin/env node
/**
 * generate_command_docs.js
 *
 * Parses the Adams View command HTML help files and produces one Markdown
 * file per command under resources/adams_view_commands/command_docs/.
 *
 * Only commands that exist in structured.json are written to disk.
 *
 * Usage:
 *   node scripts/generate_command_docs.js [path/to/help/dir]
 *
 * The help dir defaults to the well-known Adams 2023_1 install location.
 */

"use strict";

const fs = require("fs");
const path = require("path");

const HELP_DIR = process.argv[2] || process.env.ADAMS_HELP_DIR;

if (!HELP_DIR) {
    console.error("Usage: node scripts/generate_command_docs.js <path/to/adams_view_cmd/help/dir>");
    console.error("   or: ADAMS_HELP_DIR=<path> node scripts/generate_command_docs.js");
    console.error("");
    console.error("The help dir is typically:");
    console.error("  C:\\Program Files\\MSC.Software\\Adams\\<version>\\help\\adams_view_cmd");
    process.exit(1);
}

const STRUCTURED_JSON = path.resolve(__dirname, "../resources/adams_view_commands/structured.json");
const OUT_DIR = path.resolve(__dirname, "../resources/adams_view_commands/command_docs");

// ---------------------------------------------------------------------------
// Simple HTML helpers (no external deps required)
// ---------------------------------------------------------------------------

/** Strip all HTML tags and decode common entities, returning plain text. */
function innerText(html) {
    return html
        .replace(/<[^>]+>/g, "")
        .replace(/&amp;/g, "&")
        .replace(/&lt;/g, "<")
        .replace(/&gt;/g, ">")
        .replace(/&nbsp;/g, " ")
        .replace(/&#\d+;/g, "")
        .replace(/\s+/g, " ")
        .trim();
}

/** Extract the first match of a regex from html, returning plain innerText. */
function extractText(html, re) {
    const m = html.match(re);
    return m ? innerText(m[1] || "") : "";
}

// ---------------------------------------------------------------------------
// Parsers
// ---------------------------------------------------------------------------

/**
 * Extract the command name from the <h1> element.
 */
function parseCommandName(html) {
    return extractText(html, /<h1[^>]*>([\s\S]*?)<\/h1>/i);
}

/**
 * Extract the first description paragraph — the <div class="body"> that
 * immediately follows the <h1>.
 */
function parseDescription(html) {
    const m = html.match(/<h1[\s\S]*?<\/h1>([\s\S]*?)(?:<h[23]|<table)/i);
    if (!m) return "";
    // Pick the first div with class="body" inside that region
    const region = m[1];
    const dm = region.match(/<div[^>]*class="body"[^>]*>([\s\S]*?)<\/div>/i);
    return dm ? innerText(dm[1]) : "";
}

/**
 * Parse the first <table class="bordered"> and return an array of row arrays,
 * where each row is an array of cell text strings.
 *
 * The first row (header) is skipped.
 */
function parseParamTable(html) {
    // Find the first bordered table
    const tableMatch = html.match(/<table[^>]*class="bordered"[^>]*>([\s\S]*?)<\/table>/i);
    if (!tableMatch) return [];

    const tableHtml = tableMatch[1];
    const rows = [];

    // Split by <tr
    const trParts = tableHtml.split(/<tr[\s>]/i);

    for (const trChunk of trParts) {
        // Get all <td> cells (skip <th> header row)
        const tdMatches = [...trChunk.matchAll(/<td[^>]*>([\s\S]*?)<\/td>/gi)];
        if (tdMatches.length === 0) continue;

        // Each cell may contain nested <div class="cellbody10"> or similar
        const cells = tdMatches.map((m) => {
            const cellHtml = m[1];
            // Try to pull text from the first div inside the cell
            const divMatch = cellHtml.match(/<div[^>]*>([\s\S]*?)<\/div>/i);
            return divMatch ? innerText(divMatch[1]) : innerText(cellHtml);
        });

        if (cells.length >= 2) {
            rows.push(cells);
        }
    }

    return rows;
}

// ---------------------------------------------------------------------------
// Markdown generation
// ---------------------------------------------------------------------------

function escapeMarkdown(text) {
    return text.replace(/\|/g, "\\|");
}

function generateMarkdown(commandName, description, rows) {
    const lines = [];

    lines.push(`# ${commandName}`);
    lines.push("");

    if (description) {
        lines.push(description);
        lines.push("");
    }

    if (rows.length > 0) {
        lines.push("## Parameters");
        lines.push("");
        lines.push("| Parameter | Type | Description |");
        lines.push("|---|---|---|");

        for (const row of rows) {
            const param = row[0] ? `\`${row[0].toLowerCase()}\`` : "";
            const type = escapeMarkdown(row[1] || "");
            const desc = escapeMarkdown(row[2] || row[1] || "");
            lines.push(`| ${param} | ${type} | ${desc} |`);
        }
        lines.push("");
    }

    return lines.join("\n");
}

// ---------------------------------------------------------------------------
// File naming: command key → filename (spaces and slashes → underscores)
// ---------------------------------------------------------------------------

function commandKeyToFilename(key) {
    return key.replace(/\s+/g, "_") + ".md";
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

function main() {
    if (!fs.existsSync(STRUCTURED_JSON)) {
        console.error(`ERROR: structured.json not found:\n  ${STRUCTURED_JSON}`);
        process.exit(1);
    }

    // Load the command key set for filtering
    const structured = JSON.parse(fs.readFileSync(STRUCTURED_JSON, "utf8"));
    const commandKeys = new Set(Object.keys(structured).map((k) => k.toLowerCase()));

    // Ensure output directory exists
    if (!fs.existsSync(OUT_DIR)) {
        fs.mkdirSync(OUT_DIR, { recursive: true });
    }

    const htmlFiles = fs.readdirSync(HELP_DIR).filter((f) => f.endsWith(".html"));
    console.log(`Found ${htmlFiles.length} HTML files.`);

    let written = 0;
    let skipped = 0;
    let noName = 0;

    for (const htmlFile of htmlFiles) {
        const html = fs.readFileSync(path.join(HELP_DIR, htmlFile), "utf8");

        const commandName = parseCommandName(html);
        if (!commandName) {
            noName++;
            continue;
        }

        // Only write docs for commands that exist in structured.json
        if (!commandKeys.has(commandName.toLowerCase())) {
            skipped++;
            continue;
        }

        const description = parseDescription(html);
        const rows = parseParamTable(html);
        const markdown = generateMarkdown(commandName, description, rows);

        // Use the exact structured.json key casing for the filename
        // (find it case-insensitively)
        const structuredKey = Object.keys(structured).find(
            (k) => k.toLowerCase() === commandName.toLowerCase(),
        );
        const filename = commandKeyToFilename(structuredKey || commandName);
        fs.writeFileSync(path.join(OUT_DIR, filename), markdown, "utf8");
        written++;
    }

    console.log(`\nDone!`);
    console.log(`  Written  : ${written}`);
    console.log(`  Skipped (not in structured.json) : ${skipped}`);
    console.log(`  No <h1> found : ${noName}`);
    console.log(`  Output dir : ${OUT_DIR}`);
}

main();

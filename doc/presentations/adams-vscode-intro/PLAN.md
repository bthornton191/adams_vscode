# Adams VS Code Extension — Conference Presentation Plan

## Overview

| Item            | Detail                                                     |
| --------------- | ---------------------------------------------------------- |
| **Format**      | Conference talk, ~25 minutes                               |
| **Platform**    | [Slidev](https://sli.dev/) (Markdown-first slide framework)|
| **Recordings**  | [OpenScreen](https://github.com/siddharthvaddem/openscreen) (free, open-source screen recorder with auto-zoom and annotations) |
| **Audience**    | Adams power users (CMD scripters, Python scripters) and Adams internal development team — mixed technical level |
| **Delivery**    | Recorded screen demos embedded in slides (not live) for reliability |
| **Theme**       | Modern, clean Slidev theme with smooth animations/transitions. Will need to accommodate corporate logos/branding. |

## Goal

Convince Adams users who write CMD or Python scripts to switch from Notepad++ or the Adams GUI macro editor to VS Code with this extension. For users already on VS Code, show them what they're missing in recent features (linter, autocomplete, macro management).

## Core Message

> **"What if your editor actually understood Adams?"**

The Adams GUI macro editor gives you a text box and an Apply button. Notepad++ gives you colors. This extension gives you an editor that *knows* Adams — it reads the docs so you don't have to, catches errors before you run, and manages your macro libraries.

## Audience Segments

| Segment | What they need to see |
| ------- | --------------------- |
| **CMD scripters on Notepad++** | Side-by-side comparison that makes switching undeniable. Hover docs, linting, and autocomplete are the killers. |
| **CMD scripters already on the extension** | The new LSP features: linter, macro scanner, semantic highlighting. Things they may not know exist yet. |
| **Adams internal developers** | Architecture overview, MCP integration, contribution opportunities. |
| **Beginners / GUI-only users** | Plant the seed that learning CMD is easier with this tool. Extension lowers the barrier — autocomplete and docs teach you the language as you type. |

## Narrative Arc: Pain → Solution → Wow → Future → CTA

### Opening — "The Editor Gap" (~3 min)

| Slide | Content | Visual |
| ----- | ------- | ------ |
| **Title** | "Your Editor Should Work As Hard As You Do" — Adams VS Code Extension | Clean title with extension logo, corporate branding |
| **The problem** | The Adams GUI macro editor: a text box and an Apply button. This is what we've accepted as a scripting environment. | Screenshot of the Adams GUI macro editor |
| **The Notepad++ standard** | This was the upgrade. Custom syntax highlighting, nothing else. | Screenshot of Notepad++ with Adams .cmd file |
| **The gap** | What these tools don't give you: no error checking, no docs, no code navigation, no debugging. Every syntax error costs a round-trip to Adams View. | Bullet list with ✗ marks, maybe a "time wasted" visual |

### Act 1 — "Your Editor Knows Adams" (~8 min)

*Focus: Everyday workflow improvements that save time on every script.*

| Slide | Content | Demo Recording |
| ----- | ------- | -------------- |
| **Syntax highlighting** | Quick baseline comparison — Notepad++ vs VS Code with semantic tokens. Not the selling point, but sets the stage. | ~15s: Open a .cmd file, scroll through showing colors and semantic token differentiation |
| **Autocomplete** | Start typing a command, see completions with argument signatures. Tab-complete into a full command template. | ~30s: Type partial commands ("variable cre", "marker mod"), show completion popup with argument lists, tab-complete |
| **Hover documentation** | Hover over ANY Adams function or command to see docs inline. "You never have to leave your editor to look up syntax." | ~30s: Hover over DX(), STEP(), IMPACT(), hover over "marker create" to show argument docs |
| **Real-time linting** | The safety net. Errors caught while you type, not when you run. "Every red squiggle is a round-trip to Adams View you saved." | ~45s: Type a CMD script with intentional errors (unknown command → E001, invalid argument → E003), show Problems panel, fix in real-time |
| **Abbreviated commands** | Extension understands Adams abbreviations — "var set" resolves to "variable set". Hover and autocomplete both work. | ~20s: Show hover/autocomplete working with abbreviated commands |

### Act 2 — "Beyond a Text Editor" (~8 min)

*Focus: Features that fundamentally change how you work with Adams scripts.*

| Slide | Content | Demo Recording |
| ----- | ------- | -------------- |
| **Run in Adams View** | Execute code directly from VS Code. No copy-paste, no window switching. "Your editor IS your Adams console." | ~30s: Select CMD code, Ctrl+K Ctrl+R, show execution in Adams View, show result |
| **Python debugging** | Set breakpoints and debug Python scripts running inside Adams View. Full debugging, inside Adams. | ~45s: Open Python script, set breakpoint, click "Debug in Adams", show pause at breakpoint, inspect variables, step through |
| **Macro library management** | Go-to-definition, find-references, hover docs across your entire macro library. "Your macros are now first-class citizens." | ~45s: Enable macro scanning, go-to-definition on a macro call, find-references, hover showing help string |
| **Semantic highlighting** | Valid vs invalid arguments distinguished by color — errors visible before the linter even fires. | ~20s: Show correct vs incorrect commands side-by-side, colors making errors obvious |

### Act 3 — "What's Coming" (~3 min)

*Focus: MCP / AI integration — plant seeds for future capabilities.*

| Slide | Content | Demo Recording |
| ----- | ------- | -------------- |
| **AI agents + Adams** | MCP servers let AI assistants interact with Adams — lint CMD, look up command syntax, query models. Brief demo or screenshot of Copilot using Adams MCP tools. | ~30s (optional): Show Copilot agent using `adams_lint_cmd_text` or `adams_lookup_command` |
| **Vision** | "The scripting experience Adams users deserve." Community contributions welcome, the extension keeps improving. | Statement slide, clean and bold |

### Closing — "Get Started" (~3 min)

| Slide | Content | Visual |
| ----- | ------- | ------ |
| **Installation** | One-click from VS Code Marketplace. | QR code to Marketplace listing, brief recording of search → install |
| **Configuration** | Key settings: point to Adams installation, enable linter, enable macro scanning. | Config snippet or screenshot of settings |
| **Call to action** | "Install it today. Open your next .cmd file in VS Code. Let me know what breaks." | Contact info, GitHub link, QR code |

## Screen Recordings Checklist (OpenScreen)

Record these clips after installing OpenScreen. Each should be a polished, focused demo of a single feature. Use auto-zoom to keep the action area visible.

| # | Feature | ~Duration | Key Actions |
|---|---------|-----------|-------------|
| 1 | Syntax highlighting | 15s | Open .cmd file, scroll through, show semantic token colors |
| 2 | Autocomplete | 30s | Type partial commands, show completions with argument lists, tab-complete |
| 3 | Hover documentation | 30s | Hover over functions (DX, STEP, IMPACT), hover over commands (marker create) |
| 4 | Real-time linting | 45s | Type errors (E001, E003), show Problems panel, fix in real-time |
| 5 | Abbreviated commands | 20s | Hover and complete abbreviated forms (var set, mar cre) |
| 6 | Run in Adams View | 30s | Select code → Ctrl+K Ctrl+R → execution in Adams View |
| 7 | Python debugging | 45s | Set breakpoint → Debug in Adams → pause → inspect → step |
| 8 | Macro library | 45s | Go-to-definition, find-references, hover on macro call |
| 9 | Semantic highlighting | 20s | Valid vs invalid argument colors side-by-side |
| 10 | MCP / AI demo | 30s | Copilot using Adams MCP tools (optional) |

## Tooling Setup

### Slidev

```bash
# Initialize project (run from doc/presentations/adams-vscode-intro/)
npm init slidev@latest

# Development
npm run dev          # http://localhost:3030

# Export
npm run export       # PDF (needs playwright-chromium)
npm run build        # Static SPA
```

**Theme:** Will select a modern, clean theme with smooth transitions. Candidates:
- `slidev-theme-seriph` — clean, professional
- `slidev-theme-apple-basic` — minimal, modern
- Custom theme possible if corporate branding requires it

**Animations:** Slidev supports `v-click` step reveals, slide transitions (`transition: slide-left`), Magic Move for code animations, and `v-mark` for hand-drawn annotation effects.

**Corporate branding:** Logos and brand colors can be integrated via global CSS overrides and `global-top.vue` / `global-bottom.vue` layer components (persistent header/footer on all slides).

### OpenScreen

Download from [GitHub Releases](https://github.com/siddharthvaddem/openscreen/releases). Windows — works out of the box.

Features to use:
- **Auto-zoom** on click targets (keeps focus on the action)
- **Annotations** (arrows, text) for callouts if needed
- **Trim** to cut dead time
- **Custom background** to match slide aesthetic

### Copilot Skill

The official [Slidev skill](https://github.com/slidevjs/slidev/tree/main/skills/slidev) will be installed to `.agents/skills/slidev/` to enable AI-assisted slide authoring. This gives the agent knowledge of Slidev syntax, layouts, animations, code features, and export options.

## Next Steps

1. ~~Create `doc/presentations/` folder and update `.vscodeignore`~~ ✅
2. ~~Write this plan document~~ ✅
3. Install Slidev skill to `.agents/skills/slidev/`
4. Initialize Slidev project in this folder (`npm init slidev`)
5. Select and configure theme
6. Build slides (iterative — outline → content → animations → polish)
7. Record screen demos with OpenScreen
8. Embed recordings in slides
9. Test full presentation flow
10. Export to PDF as backup

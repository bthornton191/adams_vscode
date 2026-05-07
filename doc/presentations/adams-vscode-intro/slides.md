---
theme: seriph
title: "Streamlining Adams Scripting with the Adams Extension for VS Code"
info: |
  Adams VS Code Extension — Conference Presentation

  Bringing modern editor intelligence to Adams scripting.
author: Ben Thornton
transition: slide-left
defaults:
  transition: fade
fonts:
  sans: Inter
  mono: Fira Code
highlighter: shiki
lineNumbers: false
drawings:
  enabled: false
aspectRatio: 16/9
canvasWidth: 980
download: true
colorSchema: dark
themeConfig:
  primary: '#6366f1'
---

<style>
/* ─── Global gradient background ─────────────────────────── */
.slidev-layout {
  background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 40%, #24243e 100%) !important;
}

/* ─── Section divider slides ─────────────────────────────── */
.slidev-layout.section {
  background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%) !important;
}

/* ─── Cover / title slide ────────────────────────────────── */
.slidev-layout.cover {
  background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%) !important;
}

/* ─── Subtle card / box styling ──────────────────────────── */
.feature-card {
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  backdrop-filter: blur(4px);
}
</style>

# Streamlining Adams Scripting

The Adams VS Code Extension

<div class="pt-10 flex items-center justify-center gap-4">
  <img src="/adams-logo.png" class="h-10 opacity-90" alt="Adams Logo" />
  <div class="w-px h-8 bg-white opacity-20" />
  <img src="/logo.svg" class="h-6 opacity-70" style="filter: brightness(0) invert(1)" alt="Cadence" />
</div>

<div class="mt-6 text-sm text-white/50">Ben Thornton</div>

<!--
Welcome everyone. I'm going to show you something that I think will change how you write Adams scripts. Whether you're a CMD power user or just getting started with scripting, this extension brings modern editor intelligence to Adams.
-->

---

# Agenda

<div class="mt-8 flex flex-col gap-4">

<div class="agenda-item" style="--i:1">
  <span class="agenda-num">01</span>
  <div>
    <div class="agenda-title">The Editor Gap</div>
    <div class="agenda-sub">Where Adams scripting tools are today</div>
  </div>
</div>

<div class="agenda-item" style="--i:2">
  <span class="agenda-num">02</span>
  <div>
    <div class="agenda-title">Code Editing</div>
    <div class="agenda-sub">Syntax highlighting, autocomplete, hover docs, linting, code navigation</div>
  </div>
</div>

<div class="agenda-item" style="--i:3">
  <span class="agenda-num">03</span>
  <div>
    <div class="agenda-title">Adams Integration</div>
    <div class="agenda-sub">Run in Adams, Python debugging</div>
  </div>
</div>

<div class="agenda-item" style="--i:4">
  <span class="agenda-num">04</span>
  <div>
    <div class="agenda-title">What's Coming</div>
    <div class="agenda-sub">Teaching AI agents to use Adams</div>
  </div>
</div>

<div class="agenda-item" style="--i:5">
  <span class="agenda-num">05</span>
  <div>
    <div class="agenda-title">Get Started</div>
    <div class="agenda-sub">Two-minute install</div>
  </div>
</div>

</div>

<style>
@keyframes agendaFadeUp {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}
.agenda-item {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  padding: 0.6rem 1rem;
  border-radius: 8px;
  border: 1px solid rgba(255,255,255,0.07);
  background: rgba(255,255,255,0.03);
  opacity: 0;
  animation: agendaFadeUp 0.25s ease forwards;
  animation-delay: calc(0.15s + var(--i) * 0.2s);
}
.agenda-num {
  font-size: 1.4rem;
  font-weight: 700;
  color: #6366f1;
  min-width: 2.5rem;
  font-variant-numeric: tabular-nums;
}
.agenda-title {
  font-size: 1rem;
  font-weight: 600;
  color: #e2e8f0;
}
.agenda-sub {
  font-size: 0.78rem;
  color: rgba(255,255,255,0.4);
  margin-top: 0.1rem;
}
</style>

<!--
Here's what we'll cover. We'll start with the current state — what we've all been working with. Then I'll walk through the everyday improvements: autocomplete, hover docs, linting. Then the bigger workflow changes: running code in Adams, Python debugging, navigating your macro library. A quick look at what's coming with AI. And then we'll get you installed.
-->

---
layout: section
---

# The Editor Gap

Where Adams scripting tools are today

<!--
Let's start by talking about what we've all been working with.
-->

---
layout: center
---

# The Adams GUI Macro Editor

<div class="text-center mt-8">
  <img src="/aview_macro_editor.png" class="rounded-lg shadow-xl mx-auto" style="max-height: 380px" alt="Adams GUI Macro Editor" />
</div>

<!--
This is the Adams macro editor. It's a text box. And an Apply button. That's it. No highlighting, no error checking, no docs. If you misspell an argument, you find out when you run it.
-->

---
layout: center
---

# The Notepad++ Upgrade

<div class="text-center mt-8">
  <img src="/notepadpp.png" class="rounded-lg shadow-xl mx-auto" style="max-height: 380px" alt="Notepad++ with Adams CMD file" />
</div>


<!--
If you wanted better, you moved to Notepad++ with a custom syntax file. You got colors. That's it. No completions, no docs, no linting. Every syntax error still costs you a round-trip to Adams View.
-->

---

# What's Missing?

<div class="mt-8"></div>

<v-clicks>

- <mdi-close-circle class="text-red-500" /> **No error checking** — syntax errors found at runtime, not while writing
- <mdi-close-circle class="text-red-500" /> **No documentation** — constant tab-switching to the Adams help
- <mdi-close-circle class="text-red-500" /> **No autocomplete** — memorize every command and argument name
- <mdi-close-circle class="text-red-500" /> **No code navigation** — find your macros by searching directories
- <mdi-close-circle class="text-red-500" /> **No debugging** — `print` statements

</v-clicks>

<v-click>

<div class="mt-8 p-4 rounded-lg" style="background: rgba(99, 102, 241, 0.08); border: 1px solid rgba(99,102,241,0.2)">
  <p class="text-lg text-center text-white/70">
    Every modern language has all of this.
  </p>
</div>

</v-click>

<v-click>

<div class="p-4 rounded-lg text-center" style="background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(99,102,241,0.4)">
  <span class="text-xl text-indigo-300 font-semibold">Now Adams does too!</span>
</div>

</v-click>

<!--
Let's be honest about what's missing. No error checking — you find typos at runtime. No docs — you're constantly switching to the help browser. No autocomplete — you have to memorize command names and argument lists. No navigation — finding a macro means searching folders. And debugging? Print statements and prayer.

Every single syntax error costs you a round-trip to Adams View. Write, run, fail, fix, repeat. What if your editor could catch those problems before you ever hit run?
-->

---
layout: section
---

# Code Editing

How the MSC Adams extension for VS Code helps you *read* and *write* code

<!--
Let's see what changes when your editor actually understands Adams.

[click] These are the features that save you time on every single script.
-->

---

# Syntax Highlighting

<div class="mt-6 grid grid-cols-2 gap-6">

<div>
  <div class="text-sm text-white/50 mb-2 text-center">Dark theme</div>
  <img src="/syntax_highlighting.png" class="rounded-lg shadow-xl" style="width: 85%; height: auto; display: block; margin: 0 auto" alt="VS Code Adams syntax highlighting — dark" />
</div>

<div>
  <div class="text-sm text-white/50 mb-2 text-center">Light theme</div>
  <img src="/syntax_highlighting-light.png" class="rounded-lg shadow-xl" style="width: 85%; height: auto; display: block; margin: 0 auto" alt="VS Code Adams syntax highlighting — light" />
</div>

</div>

<!--
VS Code with semantic token highlighting — the editor distinguishes commands, arguments, values, and even valid vs invalid names with different colors. Works in both dark and light themes.

This is just the starting point.
-->

---

# Autocomplete

Adams CMD

<div class="mt-4" style="height: calc(100% - 5rem)">
  <video src="/cmd_autocomplete.mp4" autoplay loop muted controls style="max-height: 100%; max-width: 100%; display: block; margin: 0 auto" />
</div>

<!--
Start typing a command name, and the editor shows you completions with the full argument list. Tab-complete into a template. You don't need to memorize argument names — the editor knows them.

This works for Adams functions too — DX, STEP, IMPACT — they all have completion with argument signatures.

And it works for your custom macros. The extension discovers them in your workspace and offers them in the completion list alongside built-in commands.
-->

---

# Autocomplete

Python

<div class="mt-4" style="height: calc(100% - 5rem)">
  <video src="/python_autocomplete.mp4" autoplay loop muted controls style="max-height: 100%; max-width: 100%; display: block; margin: 0 auto" />
</div>

<!--
The same experience for Adams Python scripts. Full autocomplete for the Adams Python API — every class, method, and argument.
-->

---

# Hover Documentation 

Adams CMD

<div class="mt-4" style="height: calc(100% - 5rem)">
  <video src="/hover_cmd.mp4" autoplay loop muted controls style="max-height: 100%; max-width: 100%; display: block; margin: 0 auto" />
</div>

<!--
Hover over any Adams function — DX, STEP, IMPACT — and you get the full documentation inline. Arguments, format, examples.

Hover over a command keyword and you see every argument with its type and description.

Works for built-in commands, custom macros, and abbreviated forms.
-->

---

# Hover Documentation

Python

<div class="mt-4" style="height: calc(100% - 5rem)">
  <video src="/hover_python.mp4" autoplay loop muted controls style="max-height: 100%; max-width: 100%; display: block; margin: 0 auto" />
</div>

<!--
The same hover docs experience for Adams Python scripts. Hover over any Adams Python API method and you get the full docstring inline.
-->

---
layout: center
clicksStart: 1
---

# Linting

Spellcheck for code

<div class="sem-block mt-12 mx-auto" style="max-width: 560px">
<v-switch>
<template #1>
<pre class="sem-code"><code><span class="cmd">marker</span> <span class="cmd">create</span>  &amp;
   <span class="arg">marker_name</span> = <span class="val">.model.PART_1.cm</span>  &amp;
   <span class="arg">locaton</span> = <span class="num">0, 0, 0</span>  &amp;
   <span class="arg">orientation</span> = <span class="num">0, 0, 0</span></code></pre>
</template>
<template #2>
<pre class="sem-code"><code><span class="cmd">marker</span> <span class="cmd">create</span>  &amp;
   <span class="arg">marker_name</span> = <span class="val">.model.PART_1.cm</span>  &amp;
   <span class="arg-bad">locaton</span> = <span class="num">0, 0, 0</span>  &amp;
   <span class="arg">orientation</span> = <span class="num">0, 0, 0</span></code></pre>
</template>
</v-switch>
</div>

<style>
.sem-block {
  background: #1e1e2e;
  border-radius: 8px;
  padding: 20px 24px;
  border: 1px solid rgba(255,255,255,0.08);
}
.sem-code {
  margin: 0;
  font-family: 'Fira Code', monospace;
  font-size: 0.95em;
  line-height: 1.8;
  white-space: pre;
  color: #cdd6f4;
}
.sem-code .cmd     { color: #89b4fa; }
.sem-code .arg     { color: #89dceb; }
.sem-code .arg-bad {
  color: #89dceb;
  text-decoration: underline wavy #f38ba8;
  text-underline-offset: 3px;
}
.sem-code .val     { color: #a6e3a1; }
.sem-code .num     { color: #fab387; }
</style>

<!--
The editor uses semantic tokens to color valid and invalid argument names differently. On the left, everything is correct — clean colors. On the right, "locaton" is misspelled. Before the linter even runs, the color difference makes the error obvious at a glance. The wavy red underline is the linter kicking in too.
-->

---

# Linting

Adams CMD

<div class="mt-4 flex gap-4 items-center" style="height: calc(100% - 4rem)">
  <video src="/linting.mp4" autoplay loop muted controls style="flex: 1; min-width: 0; max-height: 100%" />

  <div class="flex flex-col gap-3 text-center text-sm" style="width: 180px; flex-shrink: 0">
    <div class="p-3 rounded-lg bg-red-50 dark:bg-red-900/20">
      <div class="font-bold text-red-600">Error</div>
      <div>E000</div>
      <div class="text-xs opacity-60">(e.g. unknown command)</div>
    </div>
    <div class="p-3 rounded-lg bg-yellow-50 dark:bg-yellow-900/20">
      <div class="font-bold text-yellow-600">Warning</div>
      <div>W000</div>
      <div class="text-xs opacity-60">(e.g. object name omitted)</div>
    </div>
    <div class="p-3 rounded-lg bg-blue-50 dark:bg-blue-900/20">
      <div class="font-bold text-blue-600">Information</div>
      <div>I000</div>
      <div class="text-xs opacity-60">(e.g. hardcoded adams id)</div>
    </div>
  </div>
</div>

<!--
The linter checks your code as you type. Unknown command? Red squiggle. Invalid argument name? Error immediately. You see the problem before you ever hit run.

Every red squiggle is a round-trip to Adams View you just saved.
-->

---

# Linting

Python

<div class="mt-4" style="height: calc(100% - 4rem)">
  <video src="/python_linting.mp4" autoplay loop muted controls style="max-height: 100%; max-width: 100%; display: block; margin: 0 auto" />
</div>

<!--
Python scripts get the same treatment via Pylance — type errors, missing attributes, and invalid API usage surfaced as you write.
-->

---

# Code Navigation

Adams CMD

<div class="mt-4" style="height: calc(100% - 5rem)">
  <video src="/cmd_linked_refs.mp4" autoplay loop muted controls style="max-height: 100%; max-width: 100%; display: block; margin: 0 auto" />
</div>

<!--
Click on any name — a part, a marker, a variable, a macro — and Go to Definition jumps straight to where it's defined. Find All References shows every place it's used across the entire workspace.

The extension indexes everything: macros, variables, parts, markers, constraints, and UDEs.
-->


---

# Compatible with Custom Macros

<div class="custom-macro-slide">

<div class="custom-macro-video">
  <video src="/works_with_custom_macros.mp4" autoplay loop muted class="w-full h-full rounded-xl object-contain" />
</div>

<div class="custom-macro-chips">
  <span class="chip" style="--i:0"><mdi-check class="text-green-400" /> Autocomplete</span>
  <span class="chip" style="--i:1"><mdi-check class="text-green-400" /> Hover docs</span>
  <span class="chip" style="--i:2"><mdi-check class="text-green-400" /> Linting</span>
  <span class="chip" style="--i:3"><mdi-check class="text-green-400" /> Go to Definition</span>
  <span class="chip" style="--i:4"><mdi-check class="text-green-400" /> Find All References</span>
</div>

</div>

<style>
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}
.custom-macro-slide {
  display: flex;
  flex-direction: column;
  height: calc(100% - 3.5rem);
  gap: 0.75rem;
}
.custom-macro-video {
  flex: 1;
  min-height: 0;
}
.custom-macro-chips {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
  flex-wrap: wrap;
  padding-bottom: 0.25rem;
}
.chip {
  padding: 0.25rem 0.85rem;
  border-radius: 9999px;
  font-size: 0.85rem;
  border: 1px solid rgba(74,222,128,0.3);
  background: rgba(74,222,128,0.1);
  color: #86efac;
  opacity: 0;
  animation: fadeUp 0.2s ease forwards;
  animation-delay: calc(0.3s + var(--i) * 0.5s);
}
</style>

<!--
Before we move on — everything we just showed works for your custom macros too. Not just the built-in Adams command set.

Your macros appear in the autocomplete list. Hover over a call and you see the help string from the macro header. The linter knows they're valid commands — no false E001 errors. And Go to Definition and Find All References work across your entire workspace.

It discovers .mac files automatically. You don't configure anything.
-->

---

# Supported File Types

<div class="mt-6">

<table class="w-full text-sm border-collapse">
<thead>
<tr class="border-b border-white/10">
  <th class="text-left py-2 pr-4 text-white/50 font-normal">Extension</th>
  <th class="py-2 px-3 text-white/50 font-normal text-center">Syntax<br/>Highlighting</th>
  <th class="py-2 px-3 text-white/50 font-normal text-center">Autocomplete<br/>&amp; Hover</th>
  <th class="py-2 px-3 text-white/50 font-normal text-center">Linting</th>
  <th class="py-2 px-3 text-white/50 font-normal text-center">Code<br/>Navigation</th>
  <th class="py-2 px-3 text-white/50 font-normal text-center">Run in<br/>Adams</th>
</tr>
</thead>
<tbody>
<tr class="border-b border-white/5 ft-row" style="--i:0">
  <td class="py-2 pr-4 font-mono font-bold text-blue-400">.cmd / .mac</td>
  <td class="text-center"><mdi-check class="text-green-400" /></td>
  <td class="text-center"><mdi-check class="text-green-400" /></td>
  <td class="text-center"><mdi-check class="text-green-400" /></td>
  <td class="text-center"><mdi-check class="text-green-400" /></td>
  <td class="text-center"><mdi-check class="text-green-400" /></td>
</tr>
<tr class="border-b border-white/5 ft-row" style="--i:1">
  <td class="py-2 pr-4"><mdi-language-python class="text-green-400 inline" /> <span class="font-mono font-bold text-green-400">.py</span></td>
  <td class="text-center"><mdi-check class="text-green-400" /></td>
  <td class="text-center"><mdi-check class="text-green-400" /></td>
  <td class="text-center"><mdi-check class="text-green-400" /></td>
  <td class="text-center"><mdi-check class="text-green-400" /></td>
  <td class="text-center"><mdi-check class="text-green-400" /></td>
</tr>
<tr class="border-b border-white/5 ft-row" style="--i:2">
  <td class="py-2 pr-4"><mdi-cog class="text-purple-400 inline" /> <span class="font-mono font-bold text-purple-400">.adm / .acf</span></td>
  <td class="text-center"><mdi-check class="text-green-400" /></td>
  <td class="text-center text-white/20 text-xs">—</td>
  <td class="text-center text-white/20 text-xs">—</td>
  <td class="text-center text-white/20 text-xs">—</td>
  <td class="text-center text-white/20 text-xs">—</td>
</tr>
<tr class="border-b border-white/5 ft-row" style="--i:3">
  <td class="py-2 pr-4"><mdi-email-outline class="text-yellow-400 inline" /> <span class="font-mono font-bold text-yellow-400">.msg / aview.log</span></td>
  <td class="text-center"><mdi-check class="text-green-400" /></td>
  <td class="text-center text-white/20 text-xs">—</td>
  <td class="text-center text-white/20 text-xs">—</td>
  <td class="text-center text-white/20 text-xs">—</td>
  <td class="text-center text-white/20 text-xs">—</td>
</tr>
<tr class="ft-row" style="--i:4">
  <td class="py-2 pr-4 font-mono font-bold text-orange-300">Template Files <span class="text-white/30 font-normal text-xs">(Time Orbit)</span></td>
  <td class="text-center"><mdi-check class="text-green-400" /></td>
  <td class="text-center text-white/20 text-xs">—</td>
  <td class="text-center text-white/20 text-xs">—</td>
  <td class="text-center text-white/20 text-xs">—</td>
  <td class="text-center text-white/20 text-xs">—</td>
</tr>
</tbody>
</table>

</div>

<style>
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}
.ft-row {
  opacity: 0;
  animation: fadeUp 0.18s ease forwards;
  animation-delay: calc(0.15s + var(--i) * 0.18s);
}
</style>

<!--
Quick reference: .cmd and .mac files get the everything (highlighting, autocomplete, hover docs, linting, code navigation, and direct execution in Adams View).

Python gets the same, but Pylance handles Python linting and code navigation

Solver files and output files get syntax highlighting only.
-->

---
layout: section
---

# Adams Integration

Connect to a running Adams Session

<!--
You can actually connect to adams view in several ways to run and debug code
-->

---

# Run in Adams View

Run files or selected code.

<div class="mt-4">
  <img src="/run_selection_in_adams.gif" class="rounded-lg shadow-xl mx-auto" style="max-height: 380px" alt="Run selection in Adams View" />
</div>

<v-click>

<div class="mt-4 text-center">
  <kbd class="px-2 py-1 rounded bg-gray-200 dark:bg-gray-700 text-sm font-mono">Ctrl+K</kbd>
  <kbd class="px-2 py-1 rounded bg-gray-200 dark:bg-gray-700 text-sm font-mono ml-1">Ctrl+R</kbd>
  <span class="ml-3 text-gray-500">→ Executes directly in Adams View</span>
</div>

</v-click>

<!--
Select code in VS Code, press Ctrl+K Ctrl+R, and it executes directly in Adams View. No copy-paste. No switching windows. Your editor is your Adams console now.

This works for both CMD and Python files.
-->

---

# Python Debugging in Adams

Set breakpoints. Inspect variables. Step through code. <span class="text-gray-500">Inside Adams.</span>

<div class="mt-4">
  <img src="/debug_adams.gif" class="rounded-lg shadow-xl mx-auto" style="max-height: 380px" alt="Debug Python in Adams View" />
</div>

<!--
Full Python debugging inside Adams View. Set a breakpoint, click "Debug in Adams", and the debugger attaches to the running Adams process. When your script hits the breakpoint, execution pauses. You can inspect variables, step through code, evaluate expressions — the full debugging experience, inside Adams.

No more print statements and prayer.
-->


---
layout: section
---

# What's Coming

AI-powered Adams scripting

<!--
We've seen what the extension does today. Let me give you a glimpse of what's coming.
-->

---

# Teaching AI Agents to Use Adams

<div class="mt-3 grid grid-cols-2 gap-5">

<!-- MCP Servers -->
<div>
  <div class="section-label">Bundled MCP Servers</div>
  <div class="def-box">
    <span class="def-term">MCP</span> (Model Context Protocol) is an open standard that
    lets AI agents call external tools — like running Adams commands — from
    inside the chat window. The extension ships two MCP servers:
  </div>
  <div class="mcp-panel">
    <div class="mcp-server-name">Adams View <span class="mcp-server-tag">live session</span></div>
    <div class="tool-grid">
      <span class="tool-chip">adams_run_cmd</span>
      <span class="tool-chip">adams_run_python</span>
      <span class="tool-chip">adams_load_file</span>
      <span class="tool-chip">adams_evaluate_expression</span>
      <span class="tool-chip">adams_export_model_cmd</span>
      <span class="tool-chip">adams_create_simulation_script</span>
      <span class="tool-chip">adams_submit_simulation</span>
      <span class="tool-chip">adams_run_batch</span>
      <span class="tool-chip">adams_batch_status</span>
      <span class="tool-chip">adams_read_session_log</span>
      <span class="tool-chip">adams_get_model_names</span>
      <span class="tool-chip">adams_launch_view</span>
    </div>
  </div>
  <div class="mcp-panel mt-2">
    <div class="mcp-server-name">Adams CMD Linter <span class="mcp-server-tag">static analysis</span></div>
    <div class="tool-grid">
      <span class="tool-chip accent">adams_lint_cmd_text</span>
      <span class="tool-chip accent">adams_lint_cmd_file</span>
      <span class="tool-chip accent">adams_lookup_command</span>
    </div>
  </div>
</div>

<!-- Agent Skills -->
<div>
  <div class="section-label">Bundled Agent Skills</div>
  <div class="def-box">
    <span class="def-term">Agent skills</span> are domain knowledge packs that teach
    Copilot Adams-specific concepts, patterns, syntax, and best practices. The agent reads these
    whenever they become relevant to the task at hand.
  </div>
  <div class="skills-list">
    <div class="skill-row">
      <span class="skill-icon">🏗️</span>
      <div><div class="skill-name">adams-cmd-model-builder</div><div class="skill-desc">Build models in Adams CMD syntax</div></div>
    </div>
    <div class="skill-row">
      <span class="skill-icon">🐍</span>
      <div><div class="skill-name">adams-python-model-builder</div><div class="skill-desc">Build models with the Adams Python API</div></div>
    </div>
    <div class="skill-row">
      <span class="skill-icon">🌀</span>
      <div><div class="skill-name">adams-flex</div><div class="skill-desc">Flexible bodies and MNF files</div></div>
    </div>
    <div class="skill-row">
      <span class="skill-icon">🔍</span>
      <div><div class="skill-name">adams-simulation-debugger</div><div class="skill-desc">Diagnose convergence failures</div></div>
    </div>
    <div class="skill-row">
      <span class="skill-icon">⚙️</span>
      <div><div class="skill-name">adams-subroutine-writer</div><div class="skill-desc">Fortran &amp; C user subroutines</div></div>
    </div>
  </div>
</div>

</div>

<style>
.def-box { font-size: 0.62rem; color: rgba(255,255,255,0.5); background: rgba(255,255,255,0.03); border-left: 2px solid rgba(165,180,252,0.4); border-radius: 0 4px 4px 0; padding: 0.3rem 0.5rem; margin-bottom: 0.4rem; line-height: 1.5; }
.def-term { color: #a5b4fc; font-weight: 600; }
.section-label { font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: rgba(255,255,255,0.4); margin-bottom: 0.4rem; }
.mcp-panel { background: rgba(15,15,30,0.7); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 0.6rem 0.75rem; }
.mcp-server-name { font-size: 0.63rem; font-weight: 700; color: rgba(165,180,252,0.9); margin-bottom: 0.35rem; }
.mcp-server-tag { font-size: 0.55rem; font-weight: 400; background: rgba(165,180,252,0.12); border: 1px solid rgba(165,180,252,0.25); border-radius: 3px; padding: 0.05rem 0.3rem; margin-left: 0.3rem; color: rgba(165,180,252,0.6); vertical-align: middle; }
.tool-grid { display: flex; flex-wrap: wrap; gap: 0.25rem; }
.tool-chip { font-family: monospace; font-size: 0.57rem; background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.12); border-radius: 4px; padding: 0.15rem 0.4rem; color: rgba(255,255,255,0.6); white-space: nowrap; }
.tool-chip.accent { background: rgba(99,102,241,0.15); border-color: rgba(99,102,241,0.35); color: #a5b4fc; }
.mt-2 { margin-top: 0.5rem; }
.skills-list { display: flex; flex-direction: column; gap: 0.4rem; }
.skill-row { display: flex; align-items: flex-start; gap: 0.5rem; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 6px; padding: 0.4rem 0.6rem; }
.skill-icon { font-size: 1rem; line-height: 1.2; flex-shrink: 0; }
.skill-name { font-size: 0.65rem; font-weight: 600; font-family: monospace; color: #e0e7ff; }
.skill-desc { font-size: 0.6rem; color: rgba(255,255,255,0.45); margin-top: 0.1rem; }
</style>

<!--
The extension ships two MCP servers — Model Context Protocol — which let AI assistants like GitHub Copilot call into Adams directly.

The Adams View server gives agents a live connection to a running Adams session: they can run commands, execute Python, load files, submit simulations, and read the log.

The CMD Linter server gives agents static analysis tools — they can look up command syntax and validate their own output before showing it to you.

On top of that, the extension bundles five agent skills — domain knowledge packs that teach Copilot how to think like an Adams engineer for specific tasks.
-->

---

# Copilot Agent Example

<div class="mt-2 grid grid-cols-2 gap-4" style="height: calc(100% - 4rem); grid-template-rows: 1fr; align-items: stretch">

<!-- Left: Chat panel (Vue component) -->
<CopilotChat style="height: 100%; min-height: 0" />

<!-- Right: click-through **images** -->
<div class="flex flex-col gap-2" style="height: 100%; min-height: 0; overflow: hidden">
  <div class="text-xs text-white/30 text-center mb-1">Model progress</div>
  <div style="flex: 1; min-height: 0; position: relative; overflow: hidden">
    <v-switch style="position: absolute; inset: 0; height: 100%; width: 100%">
      <template #1>
        <img src="/wind_turbine_model.png" class="rounded-lg shadow-xl w-full h-full object-contain" alt="Wind turbine Adams model" />
      </template>
      <template #2>
        <img src="/wind_turbine_fail.png" class="rounded-lg shadow-xl w-full h-full object-contain" alt="Wind turbine simulation failure" />
      </template>
      <template #3>
        <video src="/wind_turbine.mp4" autoplay loop muted class="rounded-lg shadow-xl w-full h-full object-contain" />
      </template>
    </v-switch>
  </div>
</div>

</div>

<!--
Here's what it looks like in practice. You describe what you want in plain English. Copilot looks up the Adams command syntax, validates the expressions, and executes them in the running Adams session — all without you leaving the chat panel.

The images on the right show the model building up as the conversation progresses.
-->

---
layout: section
---

# Get Started

It takes two minutes.

---

# Installation

<div class="mt-6 grid grid-cols-2 gap-8">

<div>

### From VS Code


1. Open **Extensions** panel <kbd>Ctrl+Shift+X</kbd>
2. Search **"MSC Adams"**
3. Click **Install**
4. Done.



<div class="mt-4">
  <a href="https://marketplace.visualstudio.com/items?itemName=savvyanalyst.msc-adams" target="_blank">
    <img src="/vs_marketplace.png" class="rounded-lg shadow-xl" style="max-height: 100px" alt="MSC Adams on VS Code Marketplace" />
  </a>
</div>


</div>

<div>

### Quick Setup

```json
// settings.json
{
  // Point to Adams installation
  "msc-adams.adamsLaunchCommand":
    "C:\\Program Files\\MSC.Software\\Adams\\2024_2\\common\\mdi.bat",

  // Enable the CMD linter
  "msc-adams.linter.enabled": true,

  // Scan workspace for macros
  "msc-adams.linter.scanWorkspaceMacros":
    true
}
```

</div>

</div>

<!--
Installation takes 30 seconds. Open the Extensions panel, search "MSC Adams", click Install. That's it.

For the full experience, point the extension to your Adams installation and enable the linter and macro scanning. Three settings, and you're getting everything we just demonstrated.
-->

---
layout: center
class: text-center
---

# Install it today.

Open your next `.cmd` file in VS Code.

<div class="mt-4 text-gray-500">Let me know what breaks.</div>

<div class="mt-10 grid grid-cols-4 gap-6 text-sm">
  <a href="https://marketplace.visualstudio.com/items?itemName=savvyanalyst.msc-adams" target="_blank" class="text-center !border-none !no-underline hover:opacity-80">
    <mdi-store class="text-3xl text-blue-500" />
    <div class="mt-2 font-medium">VS Code Marketplace</div>
    <div class="text-gray-500 text-xs">Search "MSC Adams"</div>
  </a>
  <a href="https://github.com/bthornton191/adams_vscode" target="_blank" class="text-center !border-none !no-underline hover:opacity-80">
    <mdi-github class="text-3xl" />
    <div class="mt-2 font-medium">GitHub</div>
    <div class="text-gray-500 text-xs">bthornton191/adams_vscode</div>
  </a>
  <a href="https://github.com/bthornton191/adams_vscode/issues" target="_blank" class="text-center !border-none !no-underline hover:opacity-80">
    <mdi-email class="text-3xl text-green-500" />
    <div class="mt-2 font-medium">Feedback</div>
    <div class="text-gray-500 text-xs">GitHub Issues</div>
  </a>
  <a href="https://github.com/bthornton191/adams_vscode/pulls" target="_blank" class="text-center !border-none !no-underline hover:opacity-80">
    <mdi-source-branch class="text-3xl text-purple-400" />
    <div class="mt-2 font-medium">Contributions welcome</div>
    <div class="text-gray-500 text-xs">Open source</div>
  </a>
</div>

<!--
Install it today. Open your next .cmd file in VS Code. And let me know what breaks.

You can find it on the VS Code Marketplace — just search "MSC Adams". The source is on GitHub. If something doesn't work right, open a GitHub issue and I'll fix it. And if you want to contribute, it's fully open source — jump in.

Thank you.
-->

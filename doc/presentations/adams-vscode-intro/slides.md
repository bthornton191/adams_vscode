---
theme: seriph
title: "Your Editor Should Work As Hard As You Do"
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

# Your Editor Should Work As Hard As You Do

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
  <div class="inline-block p-8 rounded-xl border-2 border-gray-400 border-dashed bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400">
    <div class="text-6xl mb-4">📝</div>
    <p class="text-lg font-medium">[ PLACEHOLDER: Screenshot of Adams GUI Macro Editor ]</p>
    <p class="text-sm mt-2">Show the built-in macro editor — a plain text box with an Apply button.<br/>No syntax highlighting, no error checking, no documentation.</p>
  </div>
</div>

<v-click>

<div class="mt-6 text-center text-xl text-gray-500">
  This is what we've accepted as a scripting environment.
</div>

</v-click>

<!--
This is the Adams macro editor. It's a text box. And an Apply button. That's it. No highlighting, no error checking, no docs. If you misspell an argument, you find out when you run it.
-->

---
layout: center
---

# The Notepad++ Upgrade

<div class="text-center mt-8">
  <div class="inline-block p-8 rounded-xl border-2 border-gray-400 border-dashed bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400">
    <div class="text-6xl mb-4">🎨</div>
    <p class="text-lg font-medium">[ PLACEHOLDER: Screenshot of Notepad++ with Adams CMD file ]</p>
    <p class="text-sm mt-2">Show a .cmd file in Notepad++ with custom Adams syntax highlighting.<br/>Colors — but nothing else.</p>
  </div>
</div>

<v-click>

<div class="mt-6 text-center text-xl text-gray-500">
  This was the upgrade. Colors, but nothing else.
</div>

</v-click>

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
- <mdi-close-circle class="text-red-500" /> **No debugging** — `print` statements and prayer

</v-clicks>

<v-click>

<div class="mt-8 p-4 rounded-lg" style="background: rgba(239, 68, 68, 0.1)">
  <p class="text-lg text-center">
    Every syntax error costs a <span v-mark.underline.red="6">round-trip to Adams View</span>.
  </p>
</div>

</v-click>

<!--
Let's be honest about what's missing. No error checking — you find typos at runtime. No docs — you're constantly switching to the help browser. No autocomplete — you have to memorize command names and argument lists. No navigation — finding a macro means searching folders. And debugging? Print statements and prayer.

Every single syntax error costs you a round-trip to Adams View. Write, run, fail, fix, repeat. What if your editor could catch those problems before you ever hit run?
-->

---
layout: section
---

# Your Editor Knows Adams

The everyday workflow improvements

<!--
Let's see what changes when your editor actually understands Adams.

[click] These are the features that save you time on every single script.
-->

---
layout: two-cols-header
---

# Syntax Highlighting

::left::

### Notepad++
<div class="mt-4">
  <div class="inline-block p-6 rounded-xl border-2 border-gray-400 border-dashed bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400">
    <div class="text-4xl mb-2">🎨</div>
    <p class="text-sm font-medium">[ PLACEHOLDER: Notepad++ with CMD file ]</p>
    <p class="text-xs mt-1">Basic keyword coloring only</p>
  </div>
</div>

::right::

### VS Code + Adams Extension
<div class="mt-4">
  <div class="inline-block p-6 rounded-xl border-2 border-gray-400 border-dashed bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400">
    <div class="text-4xl mb-2">✨</div>
    <p class="text-sm font-medium">[ PLACEHOLDER: Screen recording — Syntax highlighting ]</p>
    <p class="text-xs mt-1">~15s: Open .cmd file, scroll through showing semantic<br/>token colors distinguishing commands, arguments, values</p>
  </div>
</div>

<!--
Here's the baseline comparison. On the left, Notepad++ with basic keyword coloring. On the right, VS Code with semantic token highlighting — the editor distinguishes commands, arguments, values, and even valid vs invalid names with different colors.

This is just the starting point.
-->

---

# Autocomplete

Type less. Get it right the first time.

<div class="mt-6">
  <img src="/autocomplete_function.gif" class="rounded-lg shadow-xl mx-auto" style="max-height: 340px" alt="Adams function autocomplete" />
</div>

<v-click>

<div class="mt-4 text-center text-gray-500">
  Start typing → see completions with argument signatures → tab-complete
</div>

</v-click>

<v-click>

<div class="mt-3 text-center text-sm text-white/50">
  Works for built-in commands, Adams functions, <em>and</em> your own custom macros.
</div>

</v-click>

<!--
Start typing a command name, and the editor shows you completions with the full argument list. Tab-complete into a template. You don't need to memorize argument names — the editor knows them.

This works for Adams functions too — DX, STEP, IMPACT — they all have completion with argument signatures.

And it works for your custom macros. The extension discovers them in your workspace and offers them in the completion list alongside built-in commands.
-->

---

# Hover Documentation

Never leave your editor to look up syntax.

<div class="mt-4">
  <img src="/function_documentation_on_hover.png" class="rounded-lg shadow-xl mx-auto" style="max-height: 280px" alt="Function documentation on hover" />
</div>

<v-click>

<div class="mt-4">
  <div class="inline-block p-4 rounded-xl border-2 border-gray-400 border-dashed bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400 w-full">
    <p class="text-sm font-medium">[ PLACEHOLDER: Screen recording — Hover documentation ]</p>
    <p class="text-xs mt-1">~30s: Hover over DX(), STEP(), IMPACT() to show function docs. Hover over "marker create" to show command argument details. Hover over a custom macro call to show its help string. Hover over an abbreviated command like "var set" to show full docs.</p>
  </div>
</div>

</v-click>

<v-click>

<div class="mt-3 grid grid-cols-3 gap-3 text-center text-xs text-white/60">
  <div>Built-in commands &amp; functions</div>
  <div>Your custom macros</div>
  <div>Abbreviated forms (<code>var set</code>, <code>mar cre</code>)</div>
</div>

</v-click>

<!--
Hover over any Adams function — DX, STEP, IMPACT, UNIQUE_NAME — and you get the full documentation inline. Arguments, format, examples.

Hover over a command keyword like "marker create" and you see every argument with its type and description.

Hover over one of your own custom macros and you get its help string — the same docs block you wrote at the top of your .mac file, shown inline as if it were a built-in.

And it works with abbreviated commands too — hover over "var set" and you see the full "variable set" documentation. You never have to leave your editor.
-->

---
clicksStart: 1
---

# Real-Time Linting

Can you spot the error?

<div class="sem-block mt-8 mx-auto" style="max-width: 560px">
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

<div v-click="2" class="mt-6 text-center text-sm text-red-400">
  <mdi-alert-circle /> <code>locaton</code> — the editor catches it before you ever hit run
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

# Real-Time Linting

<span v-mark.highlight.yellow="1">Every red squiggle is a round-trip to Adams View you just saved.</span>

<div class="mt-6">
  <div class="inline-block p-6 rounded-xl border-2 border-gray-400 border-dashed bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400 w-full">
    <div class="text-4xl mb-2">🔴</div>
    <p class="text-lg font-medium">[ PLACEHOLDER: Screen recording — Real-time linting ]</p>
    <p class="text-sm mt-2">~45s demonstration:</p>
    <ul class="text-xs mt-2 text-left list-disc ml-4">
      <li>Type a CMD script with an unknown command → E001 error squiggle appears</li>
      <li>Type an invalid argument name → E003 error appears</li>
      <li>Show the Problems panel with all diagnostics listed</li>
      <li>Fix errors in real-time — squiggles disappear as you correct the code</li>
    </ul>
  </div>
</div>

<v-click>

<div class="mt-4 grid grid-cols-3 gap-4 text-center text-sm">
  <div class="p-3 rounded-lg bg-red-50 dark:bg-red-900/20">
    <div class="font-bold text-red-600">E001</div>
    <div>Unknown command</div>
  </div>
  <div class="p-3 rounded-lg bg-orange-50 dark:bg-orange-900/20">
    <div class="font-bold text-orange-600">E003</div>
    <div>Invalid argument</div>
  </div>
  <div class="p-3 rounded-lg bg-yellow-50 dark:bg-yellow-900/20">
    <div class="font-bold text-yellow-600">W001</div>
    <div>Syntax warning</div>
  </div>
</div>

</v-click>

<!--
This is the game changer. The linter checks your code as you type. Unknown command? Red squiggle. Invalid argument name? Error immediately. You see the problem before you ever hit run.

Every red squiggle is a round-trip to Adams View you just saved. For complex scripts, this can save dozens of iterations.

[click] The linter knows the full Adams command vocabulary — commands, arguments, and their valid values.
-->

---

# It All Works for Your Custom Macros

<div class="custom-macro-slide">

<div class="custom-macro-video">
  <div class="w-full h-full rounded-xl border border-white/10 bg-white/5 flex flex-col items-center justify-center text-gray-400">
    <div class="text-5xl mb-3">🎬</div>
    <p class="text-sm font-medium">[ PLACEHOLDER: Screen recording — Custom macros ]</p>
  </div>
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
  <td class="text-center text-white/20 text-xs">—</td>
  <td class="text-center text-white/20 text-xs">—</td>
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
Quick reference: .cmd and .mac files get the full treatment — highlighting, autocomplete, hover docs, linting, code navigation, and direct execution in Adams View.

Python gets the same, minus the Adams-specific linter — Pylance handles Python linting.

Solver files and output files get syntax highlighting only. That's useful enough — reading a .msg file in VS Code is already a better experience than opening it in Notepad.
-->

---
layout: section
---

# Beyond a Text Editor

Features that change how you work

<!--
Those features save you time on every script. Now let's look at features that fundamentally change your workflow.
-->

---

# Run in Adams View

Your editor IS your Adams console.

<div class="mt-4">
  <img src="/run_selection_in_adams.gif" class="rounded-lg shadow-xl mx-auto" style="max-height: 380px" alt="Run selection in Adams View" />
</div>

<v-click>

<div class="mt-4 text-center">
  <kbd class="px-2 py-1 rounded bg-gray-200 dark:bg-gray-700 text-sm font-mono">Ctrl+K</kbd>
  <kbd class="px-2 py-1 rounded bg-gray-200 dark:bg-gray-700 text-sm font-mono ml-1">Ctrl+R</kbd>
  <span class="ml-3 text-gray-500">→ Executes directly in Adams View. No copy-paste.</span>
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

# Python Intellisense

Full type information for a closed-source API.

<div class="mt-4">
  <img src="/adams_python_autocomplete.gif" class="rounded-lg shadow-xl mx-auto" style="max-height: 340px" alt="Adams Python autocomplete" />
</div>

<v-click>

<div class="mt-4 grid grid-cols-3 gap-4 text-center text-sm">
  <div class="p-3 rounded-lg bg-white/5 border border-white/10">
    <mdi-check-circle class="text-green-500 text-xl" />
    <div class="mt-1 text-xs">Type annotations</div>
  </div>
  <div class="p-3 rounded-lg bg-white/5 border border-white/10">
    <mdi-check-circle class="text-green-500 text-xl" />
    <div class="mt-1 text-xs">Inline docstrings</div>
  </div>
  <div class="p-3 rounded-lg bg-white/5 border border-white/10">
    <mdi-check-circle class="text-green-500 text-xl" />
    <div class="mt-1 text-xs">Signature help</div>
  </div>
</div>

</v-click>

<v-click>

<div class="mt-4 p-3 rounded-lg text-sm text-center" style="background: rgba(99,102,241,0.1); border: 1px solid rgba(99,102,241,0.3)">
  Powered by hand-written <code>.pyi</code> stub files — intellisense for an API you can't read the source of.
</div>

</v-click>

<!--
The Adams Python API is closed-source. You can't read the module code. Normally that means you get no autocomplete, no type hints, no docs — you're writing against a black box.

The extension ships .pyi stub files that describe the entire Adams Python API — every class, every method, every argument. Pylance picks these up automatically. So you get full type annotations, inline docstrings, and parameter signature help, for an API you couldn't otherwise inspect.

Same quality of intellisense you'd expect for any well-typed Python library. For Adams.
-->

---

# Code Navigation

Click anything. Jump to its definition. Find everywhere it's used.

<div class="mt-4">
  <div class="inline-block p-6 rounded-xl border-2 border-gray-400 border-dashed bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400 w-full">
    <div class="text-4xl mb-2">🔗</div>
    <p class="text-lg font-medium">[ PLACEHOLDER: Screen recording — Code navigation ]</p>
    <p class="text-sm mt-2">~45s demonstration:</p>
    <ul class="text-xs mt-2 text-left list-disc ml-4">
      <li>Click a macro invocation → Go to Definition jumps to the .mac file</li>
      <li>Right-click a variable or part name → Find All References across the workspace</li>
      <li>Hover over a custom macro call → shows the help string from its header</li>
      <li>Show UDE go-to-definition and find-references</li>
      <li>Problems panel: linter recognizes all custom objects as valid — no false errors</li>
    </ul>
  </div>
</div>

<v-clicks>

- <mdi-arrow-right-bold class="text-blue-500" /> **Go to Definition** — macros, variables, parts, markers, constraints, UDEs
- <mdi-arrow-right-bold class="text-blue-500" /> **Find All References** — every use, across the entire workspace

</v-clicks>

<!--
The extension indexes your entire workspace. Every macro, variable, part, marker, constraint, and UDE. Click on any name and Go to Definition takes you straight to where it's defined. Find All References shows every place it's used across every file.
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

# AI Agents That Understand Adams

<div class="mt-6">
  <div class="inline-block p-4 rounded-xl border-2 border-gray-400 border-dashed bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400 w-full">
    <p class="text-sm font-medium">[ PLACEHOLDER: Screen recording — MCP / AI demo ]</p>
    <p class="text-xs mt-1">~30s: Chat panel open. User asks Copilot: "Write a STEP function for a soft stop at 45°, 5° ramp." Copilot calls <code>adams_lookup_command</code> to check the STEP syntax → calls <code>adams_lint_cmd_text</code> to validate the draft → returns a correct STEP expression, not generic Python.</p>
  </div>
</div>

<v-click>

<div class="mt-6 p-4 rounded-lg text-sm" style="background: rgba(99,102,241,0.1); border: 1px solid rgba(99,102,241,0.3)">

**What makes this different from generic AI code generation:**

Copilot calls the extension's MCP tools to look up Adams command syntax and validate the output against the real command vocabulary — before it shows you the answer. The AI checks its own work.

</div>

</v-click>

<v-click>

<div class="mt-4 grid grid-cols-3 gap-3 text-center text-xs text-white/60">
  <div><code>adams_lookup_command</code><br/>Resolve any abbreviation, get argument list</div>
  <div><code>adams_lint_cmd_text</code><br/>Validate CMD before suggesting it</div>
  <div><code>adams_run_cmd</code><br/>Execute directly in the running Adams session</div>
</div>

</v-click>

<!--
The extension ships an MCP server — Model Context Protocol — that exposes Adams knowledge to AI assistants like GitHub Copilot.

Here's what that looks like in practice. You ask Copilot: "Write a STEP function for a soft stop at 45 degrees with a 5 degree ramp." Without the MCP server, you'd get a plausible-looking expression that may or may not use the right argument order.

With the MCP server, Copilot calls adams_lookup_command to check the STEP function signature, drafts an expression, then calls adams_lint_cmd_text to validate it. It catches its own mistakes before showing you the answer. You get valid Adams syntax, not generic code.

This is early, and it's the direction we're heading.
-->

---
layout: statement
---

# The scripting experience<br/>Adams users deserve.

<div class="mt-8 text-lg text-gray-500">
  Free. Open source. And it keeps getting better.
</div>

<!--
This is the scripting experience Adams users deserve. A modern editor that understands your language, catches your mistakes, and helps you work faster. And it keeps getting better — every release adds new capabilities.
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

<v-clicks>

1. Open **Extensions** panel <kbd>Ctrl+Shift+X</kbd>
2. Search **"MSC Adams"**
3. Click **Install**
4. Done.

</v-clicks>

<v-click>

<div class="mt-4">
  <div class="inline-block p-4 rounded-xl border-2 border-gray-400 border-dashed bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400">
    <p class="text-sm font-medium">[ PLACEHOLDER: QR code ]</p>
    <p class="text-xs mt-1">Link to VS Code Marketplace listing</p>
  </div>
</div>

</v-click>

</div>

<div>

### Quick Setup

```json
// settings.json
{
  // Point to Adams installation
  "msc-adams.adamsLaunchCommand":
    "C:\\MSC\\Adams\\mdi.bat",

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
  <div class="text-center">
    <mdi-store class="text-3xl text-blue-500" />
    <div class="mt-2 font-medium">VS Code Marketplace</div>
    <div class="text-gray-500">Search "MSC Adams"</div>
  </div>
  <div class="text-center">
    <mdi-github class="text-3xl" />
    <div class="mt-2 font-medium">GitHub</div>
    <div class="text-gray-500">bthornton191/adams_vscode</div>
  </div>
  <div class="text-center">
    <mdi-email class="text-3xl text-green-500" />
    <div class="mt-2 font-medium">Feedback</div>
    <div class="text-gray-500">GitHub Issues</div>
  </div>
  <div class="text-center">
    <mdi-source-branch class="text-3xl text-purple-400" />
    <div class="mt-2 font-medium">Contributions welcome</div>
    <div class="text-gray-500">PRs open</div>
  </div>
</div>

<!--
Install it today. Open your next .cmd file in VS Code. And let me know what breaks.

You can find it on the VS Code Marketplace — just search "MSC Adams". The source is on GitHub. If something doesn't work right, open a GitHub issue and I'll fix it. And if you want to contribute, pull requests are very welcome.

Thank you.
-->

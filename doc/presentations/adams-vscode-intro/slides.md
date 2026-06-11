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
download: false
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
Good morning everyone. I'm Ben Thornton. I'm a consultant at Cadence. Which means 
my primary role is to help customers like you with Adams projects. Those projects 
vary in shape and size, but I've carved out a bit of a niche in building large 
adams automation frameworks. In doing so, I've learned a lot about software 
development and the tools that developers used and I recognized a gap in the 
tooling we have around adams scripting. So I went to work trying to build a tool
to fill the gap, originally just for my own use. But I put it on the vs markeplace, 
mostly just for fun, and other people seemed to find it useful. So I'm here today
to tell you about this tool and what features it has so that hopefully you will find
it useful as well. 
-->

---

# Agenda

<div class="mt-4 flex flex-col gap-2">

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
    <div class="agenda-title">The Extension</div>
    <div class="agenda-sub">VS Code and the Adams plugin</div>
  </div>
</div>

<div class="agenda-item" style="--i:3">
  <span class="agenda-num">03</span>
  <div>
    <div class="agenda-title">Code Editing</div>
    <div class="agenda-sub">Syntax highlighting, autocomplete, hover docs, linting, code navigation</div>
  </div>
</div>

<div class="agenda-item" style="--i:4">
  <span class="agenda-num">04</span>
  <div>
    <div class="agenda-title">Adams Integration</div>
    <div class="agenda-sub">Run in Adams, Python debugging</div>
  </div>
</div>

<div class="agenda-item" style="--i:5">
  <span class="agenda-num">05</span>
  <div>
    <div class="agenda-title">What's Coming</div>
    <div class="agenda-sub">Teaching AI agents to use Adams</div>
  </div>
</div>

<div class="agenda-item" style="--i:6">
  <span class="agenda-num">06</span>
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
Here's what we'll cover. 
- We'll start with the current state — what we've all been working with. 
- Then I'll walk through the code editing features: 
  - autocomplete
  - hover docs
  - linting. 
- Then the bigger integration features: 
  - running code in Adams, 
  - Python debugging, 
  - navigating your macro library. 
- A quick look at what's coming with AI. 
- And then we'll talk about installation.
-->

---
layout: section
---

# The Editor Gap

Where Adams scripting tools are today

<!--
Let's start by talking about what I used before I built the extension.
-->

---
layout: center
---

# The Adams GUI Macro Editor

<div class="text-center mt-8">
  <img src="/aview_macro_editor.png" class="rounded-lg shadow-xl mx-auto" style="max-height: 380px" alt="Adams GUI Macro Editor" />
</div>

<!--
This is the Adams macro editor that ships with Adams View. It's a text box. It's basically
the minimum you would need to edit a macro.
-->

---
layout: center
---

# The Notepad++ Upgrade

<div class="text-center mt-8">
  <img src="/notepadpp.png" class="rounded-lg shadow-xl mx-auto" style="max-height: 380px" alt="Notepad++ with Adams CMD file" />
</div>


<!--
If you do a lot of macro editing, you might discover you can create a synatx file
in notepad++. This gives you synax highlighting. This *is* an improvement. This 
highlighting is a genuine productivity boost.
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
But theres still a lot missing when we compare this to writing python or c++
in a modern code editor.

- no error checking
- no in-editor documentation
- no autocomplete
- no code navigation
- no debugging

-->
---
layout: section
---

# The Extension

VS Code and the Adams Extension

<!--
-->

---

# <mdi-microsoft-visual-studio-code class="text-blue-400 mr-2" style="vertical-align: middle" /> Visual Studio Code

<div class="vscode-slide">

  <div class="vscode-screenshot">
    <img src="/stock-vscode.png" class="rounded-lg shadow-2xl" alt="Visual Studio Code" />
  </div>

  <div class="vscode-chips">
    <div class="vscode-chip">
      <mdi-open-source-initiative class="text-green-400 mr-2 flex-shrink-0" />
      <span>Free &amp; open source</span>
    </div>
    <div class="vscode-chip">
      <mdi-puzzle-outline class="text-blue-400 mr-2 flex-shrink-0" />
      <span>Extensible</span>
    </div>
    <button class="vscode-chip vscode-chip--clickable" @click="showSurvey = true">
      <mdi-account-group class="text-indigo-400 mr-2 flex-shrink-0" />
      <span>Used by 76% of developers</span>
      <mdi-information-outline class="text-white/30 ml-2 flex-shrink-0" />
    </button>
  </div>

  <!-- Survey modal -->
  <Teleport to="body">
    <div v-if="showSurvey" class="survey-overlay" @click.self="showSurvey = false">
      <div class="survey-modal">
        <button class="survey-close" @click="showSurvey = false"><mdi-close /></button>
        <img src="/stackoverflow-dev-survey-2025-technology-most-popular-technologies-dev-envs-dev-envs-social.png"
             class="survey-img" alt="Stack Overflow Dev Survey 2025 — Dev IDEs" />
        <div class="survey-attribution">
          Source: <a href="https://survey.stackoverflow.co/2025/technology#1-dev-id-es" target="_blank" class="survey-link">survey.stackoverflow.co/2025</a>
          &nbsp;·&nbsp; Stack Overflow Developer Survey 2025
          &nbsp;·&nbsp; Data licensed under ODbL
        </div>
      </div>
    </div>
  </Teleport>

</div>

<script setup>
import { ref } from 'vue'
const showSurvey = ref(false)
</script>

<style>
.vscode-slide {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  height: calc(100% - 3.5rem);
}
.vscode-screenshot {
  flex: 1;
  min-height: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}
.vscode-screenshot img {
  max-height: 100%;
  max-width: 100%;
  object-fit: contain;
}
.vscode-chips {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
  flex-wrap: wrap;
  padding-bottom: 0.5rem;
}
.vscode-chip {
  display: flex;
  align-items: center;
  font-size: 0.78rem;
  color: rgba(255,255,255,0.6);
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 9999px;
  padding: 0.3rem 0.9rem;
}
.vscode-chip--clickable {
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s;
}
.vscode-chip--clickable:hover {
  background: rgba(99,102,241,0.15);
  border-color: rgba(99,102,241,0.4);
  color: rgba(255,255,255,0.85);
}
.survey-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(0,0,0,0.75);
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(4px);
}
.survey-modal {
  position: relative;
  background: #1e1e2e;
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 12px;
  padding: 1rem;
  max-width: 560px;
  width: 90%;
  box-shadow: 0 24px 64px rgba(0,0,0,0.6);
}
.survey-close {
  position: absolute;
  top: 0.6rem;
  right: 0.6rem;
  background: rgba(255,255,255,0.08);
  border: none;
  border-radius: 9999px;
  color: rgba(255,255,255,0.5);
  width: 1.75rem;
  height: 1.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.15s;
}
.survey-close:hover {
  background: rgba(255,255,255,0.15);
  color: white;
}
.survey-img {
  width: 100%;
  border-radius: 8px;
  display: block;
}
.survey-attribution {
  margin-top: 0.6rem;
  font-size: 0.65rem;
  color: rgba(255,255,255,0.35);
  text-align: center;
}
.survey-link {
  color: rgba(165,180,252,0.8);
  text-decoration: underline;
  text-underline-offset: 2px;
}
</style>

<!--
-->

---
layout: center
---

# The Adams Extension

<div class="flex justify-center items-center mt-4" style="height: calc(100% - 4rem)">
  <img src="/vscode-adams-extension-page.png" class="rounded-lg shadow-2xl" style="max-height: 100%; max-width: 100%; width: auto; height: auto" alt="MSC Adams Extension marketplace page" />
</div>

<!--
-->
---
layout: section
---

# Code Editing

How the MSC Adams extension for VS Code helps you *read* and *write* code

<!--
So I'm going to talk about the features of extension
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
  <video src="/works_with_custom_macros.mp4" autoplay loop muted controls class="w-full h-full rounded-xl object-contain" />
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
  <video src="/run_in_view.mp4" autoplay loop muted controls class="rounded-lg shadow-xl mx-auto" style="max-height: 380px" />
</div>


<div class="mt-4 text-center">
  <kbd class="px-2 py-1 rounded bg-gray-200 dark:bg-gray-700 text-sm font-mono">Ctrl+K</kbd>
  <kbd class="px-2 py-1 rounded bg-gray-200 dark:bg-gray-700 text-sm font-mono ml-1">Ctrl+R</kbd>
  <span class="ml-3 text-gray-500">→ Executes directly in Adams View</span>
</div>


<!--
Select code in VS Code, press Ctrl+K Ctrl+R, and it executes directly in Adams View. No copy-paste. No switching windows. Your editor is your Adams console now.

This works for both CMD and Python files.
-->

---

# Python Debugging in Adams

Set breakpoints. Inspect variables. Step through code. <span class="text-gray-500">Running inside Adams.</span>

<div class="mt-4">
  <video src="/python_debugging.mp4" autoplay loop muted controls class="rounded-lg shadow-xl mx-auto" style="max-height: 380px" />
</div>

<!--
Full Python debugging inside Adams View. Set a breakpoint, click "Debug in Adams", and the debugger attaches to the running Adams process. When your script hits the breakpoint, execution pauses. You can inspect variables, step through code, evaluate expressions — the full debugging experience, inside Adams.

No more print statements and prayer.
-->


---
layout: section
---

<div class="flex flex-col items-center justify-center gap-3 text-center">
  <h1 class="text-5xl font-bold" style="margin: 0">What's <span class="relative inline-block" style="white-space: nowrap">
    <span style="font-family: 'Caveat', cursive; color: #f87171; font-size: 0.65em; position: absolute; top: -1em; left: 50%; transform: translateX(-50%) rotate(-3deg); white-space: nowrap; line-height: 1">just released</span>
    <span>Coming</span>
    <svg style="position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; pointer-events: none"><line x1="-4" y1="55%" x2="104%" y2="45%" stroke="#f87171" stroke-width="3" stroke-linecap="round" /></svg>
  </span></h1>
  <p class="text-xl text-white/60" style="margin: 0">AI-powered Adams scripting</p>
</div>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@700&display=swap" rel="stylesheet">

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

<div class="mt-2" style="height: calc(100% - 4rem)">
  <video src="/trebuchet.mp4" autoplay loop muted controls class="rounded-lg shadow-xl w-full h-full object-contain" />
</div>

<!--
Here's what it looks like in practice. You describe what you want in plain English. Copilot looks up the Adams command syntax, validates the expressions, and executes them in the running Adams session — all without you leaving the chat panel.
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

<div class="mt-10 grid grid-cols-3 gap-8 text-sm">
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
</div>

<!--
Install it today. Open your next .cmd file in VS Code. And let me know what breaks.

You can find it on the VS Code Marketplace — just search "MSC Adams". The source is on GitHub. If something doesn't work right, open a GitHub issue and I'll fix it. And if you want to contribute, it's fully open source — jump in.

Thank you.
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

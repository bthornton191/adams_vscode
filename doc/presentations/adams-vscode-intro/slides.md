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
---

# Your Editor Should Work As Hard As You Do

The Adams VS Code Extension

<div class="abs-br m-6 flex gap-2 items-center">
  <img src="/adams-logo.png" class="h-12" alt="Adams Logo" />
</div>

<div class="pt-12">
  <span class="px-2 py-1 rounded text-sm" style="background: rgba(100,100,100,0.15)">
    Ben Thornton
  </span>
</div>

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
  <img src="/autocomplete_function.gif" class="rounded-lg shadow-xl mx-auto" style="max-height: 380px" alt="Adams function autocomplete" />
</div>

<v-click>

<div class="mt-4 text-center text-gray-500">
  Start typing → see completions with argument signatures → tab-complete
</div>

</v-click>

<!--
Start typing a command name, and the editor shows you completions with the full argument list. Tab-complete into a template. You don't need to memorize argument names — the editor knows them.

This works for Adams functions too — DX, STEP, IMPACT — they all have completion with argument signatures.
-->

---

# Hover Documentation

Never leave your editor to look up syntax.

<div class="mt-4">
  <img src="/function_documentation_on_hover.png" class="rounded-lg shadow-xl mx-auto" style="max-height: 300px" alt="Function documentation on hover" />
</div>

<v-click>

<div class="mt-4">
  <div class="inline-block p-4 rounded-xl border-2 border-gray-400 border-dashed bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400 w-full">
    <p class="text-sm font-medium">[ PLACEHOLDER: Screen recording — Hover documentation ]</p>
    <p class="text-xs mt-1">~30s: Hover over DX(), STEP(), IMPACT() to show function docs.<br/>Hover over "marker create" to show command argument details.<br/>Emphasize: "You never have to leave your editor."</p>
  </div>
</div>

</v-click>

<!--
Hover over any Adams function — DX, STEP, IMPACT, UNIQUE_NAME — and you get the full documentation inline. Arguments, format, examples. 

Hover over a command keyword like "marker create" and you see every argument with its type and description.

You never have to leave your editor to look up syntax.
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

# Abbreviated Commands? No Problem.

The extension speaks Adams shorthand.

<div class="mt-8">

````md magic-move
```text
! Full command
variable set  &
   variable_name = .model.my_var  &
   real_value = 42.0
```
```text
! Abbreviated — the extension understands this too
var set  &
   var = .model.my_var  &
   real = 42.0
```
````

</div>

<v-click>

<div class="mt-6 p-4 rounded-lg" style="background: rgba(59, 130, 246, 0.1)">
  <p class="text-center">
    <mdi-check-circle class="text-green-500" /> Hover docs work &nbsp;
    <mdi-check-circle class="text-green-500" /> Autocomplete works &nbsp;
    <mdi-check-circle class="text-green-500" /> Linting works
  </p>
</div>

</v-click>

<!--
Adams users love abbreviations. "variable set" becomes "var set". "marker create" becomes "mar cre". The extension understands these. Hover, autocomplete, and linting all work with abbreviated command names. You don't have to change how you write — the extension adapts to you.
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

# Macro Library Management

Your macros are now first-class citizens.

<div class="mt-4">
  <div class="inline-block p-6 rounded-xl border-2 border-gray-400 border-dashed bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400 w-full">
    <div class="text-4xl mb-2">📚</div>
    <p class="text-lg font-medium">[ PLACEHOLDER: Screen recording — Macro library management ]</p>
    <p class="text-sm mt-2">~45s demonstration:</p>
    <ul class="text-xs mt-2 text-left list-disc ml-4">
      <li>Enable macro scanning on a project with .mac files</li>
      <li>Go-to-definition: click on a macro invocation → jumps to the .mac file</li>
      <li>Find-references: right-click → shows everywhere the macro is called</li>
      <li>Hover: shows the macro's help string sourced from the macro header</li>
      <li>Linter recognizes user macros as valid commands</li>
    </ul>
  </div>
</div>

<v-clicks>

- <mdi-arrow-right-bold class="text-blue-500" /> **Go-to-definition** — click a macro call, jump to its source
- <mdi-arrow-right-bold class="text-blue-500" /> **Find-references** — see everywhere a macro is used
- <mdi-arrow-right-bold class="text-blue-500" /> **Hover docs** — help strings from macro headers, inline

</v-clicks>

<!--
Enable macro scanning, and the extension discovers every .mac file in your workspace. Now your macros are first-class citizens. Go-to-definition jumps to the source. Find-references shows every call site. Hover shows the help string from the macro header.

The linter also recognizes your macros as valid commands — no more false E001 errors on your custom macro calls.
-->

---
layout: two-cols-header
---

# Semantic Highlighting

Errors visible before the linter even fires.

::left::

### Correct

```text {all}
marker create  &
   marker_name = .model.PART_1.cm  &
   location = 0, 0, 0  &
   orientation = 0, 0, 0
```
<div class="mt-2 text-sm text-green-600">
  <mdi-check-circle /> All arguments highlighted as valid
</div>

::right::

### Incorrect

```text {3}
marker create  &
   marker_name = .model.PART_1.cm  &
   locaton = 0, 0, 0  &
   orientation = 0, 0, 0
```
<div class="mt-2 text-sm text-red-600">
  <mdi-alert-circle /> Misspelled argument visually distinct
</div>

<!--
The editor uses semantic tokens to color valid and invalid argument names differently. On the left, everything is correct — clean colors. On the right, "locaton" is misspelled. Before the linter even runs, the color difference makes the error obvious at a glance.
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

<div class="mt-4">

MCP servers expose Adams capabilities to AI assistants.

</div>

<div class="mt-6 grid grid-cols-3 gap-4">

<v-clicks>

<div class="p-4 rounded-lg border border-gray-200 dark:border-gray-700">
  <div class="text-2xl mb-2"><mdi-code-tags /></div>
  <h3 class="font-bold text-sm">Lint CMD Text</h3>
  <p class="text-xs text-gray-500 mt-1">AI validates Adams code before suggesting it</p>
</div>

<div class="p-4 rounded-lg border border-gray-200 dark:border-gray-700">
  <div class="text-2xl mb-2"><mdi-book-search /></div>
  <h3 class="font-bold text-sm">Look Up Commands</h3>
  <p class="text-xs text-gray-500 mt-1">AI resolves abbreviations and checks argument lists</p>
</div>

<div class="p-4 rounded-lg border border-gray-200 dark:border-gray-700">
  <div class="text-2xl mb-2"><mdi-robot /></div>
  <h3 class="font-bold text-sm">Query Models</h3>
  <p class="text-xs text-gray-500 mt-1">AI interacts with running Adams View sessions</p>
</div>

</v-clicks>

</div>

<v-click>

<div class="mt-6">
  <div class="inline-block p-4 rounded-xl border-2 border-gray-400 border-dashed bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400 w-full">
    <p class="text-sm font-medium">[ PLACEHOLDER: Screen recording — MCP / AI demo ]</p>
    <p class="text-xs mt-1">~30s: Show a Copilot agent using adams_lint_cmd_text or adams_lookup_command<br/>to validate CMD code or look up command syntax within VS Code chat.</p>
  </div>
</div>

</v-click>

<!--
The extension now includes MCP servers — Model Context Protocol — that let AI assistants interact directly with Adams. Copilot can lint CMD code, look up command syntax, and even query running Adams View sessions.

This means AI assistants that actually understand Adams syntax and can write valid code. Not just generic code generation — code that's been checked against the real Adams command vocabulary.

This is early, but it's the direction we're heading.
-->

---
layout: statement
---

# The scripting experience<br/>Adams users deserve.

<div class="mt-8 text-lg text-gray-500">
  The extension keeps getting better. Contributions welcome.
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

<div class="mt-12 grid grid-cols-3 gap-8 text-sm">
  <div>
    <mdi-store class="text-3xl text-blue-500" />
    <div class="mt-2 font-medium">VS Code Marketplace</div>
    <div class="text-gray-500">Search "MSC Adams"</div>
  </div>
  <div>
    <mdi-github class="text-3xl" />
    <div class="mt-2 font-medium">GitHub</div>
    <div class="text-gray-500">bthornton191/adams_vscode</div>
  </div>
  <div>
    <mdi-email class="text-3xl text-green-500" />
    <div class="mt-2 font-medium">Feedback</div>
    <div class="text-gray-500">GitHub Issues</div>
  </div>
</div>

<div class="abs-br m-6">
  <img src="/adams-logo.png" class="h-8 opacity-50" alt="Adams" />
</div>

<!--
Install it today. Open your next .cmd file in VS Code. And let me know what breaks.

You can find it on the VS Code Marketplace — just search "MSC Adams". The source is on GitHub. And if something doesn't work right, open a GitHub issue and I'll fix it.

Thank you.
-->

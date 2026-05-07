# Streamlining Adams Scripting with the Adams Extension for VS Code

**Speaker:** Ben Thornton\
**Title:** Simulation Multibody Dynamics Consulting Engineer\
**Company:** Cadence Design Systems

## Abstract
If you've written Adams macros, you know the workflow. Write some code, switch to Adams, run it, read the error, switch back, fix the error, repeat. The built-in macro editor is a plain text box. Notepad++ with a custom syntax file gets you colors. Neither one tells you anything is wrong until Adams does.

For short scripts, that's manageable. For complex ones, it adds up.

The Adams VS Code Extension is an attempt to fix that. It brings the kind of editor tooling that most developers take for granted (autocomplete, inline documentation, real-time error checking) to Adams CMD, Python, and solver files.

This talk covers what the extension does:

* Semantic syntax highlighting that makes commands, arguments, and values visually distinct
* Autocomplete with full argument signatures for every Adams command and function
* Hover documentation so you don't have to leave your editor to look up syntax or theory
* A linter that flags unknown commands, invalid arguments, and syntax errors as you type
* Full IntelliSense for the Adams Python API, including type annotations, docstrings, and signature help (made possible by hand-written .pyi stub files)
* Line-by-line Python debugging with breakpoints and variable inspection, directly inside VS Code

All of that extends to your own macros automatically. Drop a `.mac` file in your workspace and the extension picks it up. Autocomplete, hover docs, linting, Go to Definition, Find All References, all of it.

The extension also integrates directly with a running Adams session so that you can:

* Execute selected code in Adams View
* Attach the VS Code debugger to Adams for live Python debugging

The talk closes with a look at what's next: using AI agents to build Adams models, powered by an MCP server that ships with the extension and connects them to a running Adams session, and agent skills that teach them the domain.

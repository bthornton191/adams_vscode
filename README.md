# MSC Adams Extension for Visual Studio Code

![Visual Studio Marketplace Installs](https://badgen.net/vs-marketplace/i/savvyanalyst.msc-adams)
![Visual Studio Marketplace Rating](https://badgen.net/vs-marketplace/rating/savvyanalyst.msc-adams)
![Visual Studio Marketplace Version](https://badgen.net/vs-marketplace/v/savvyanalyst.msc-adams)


# Table of Contents
- [MSC Adams Extension for Visual Studio Code](#msc-adams-extension-for-visual-studio-code)
- [Table of Contents](#table-of-contents)
- [Features](#features)
  - [Syntax highlighting](#syntax-highlighting)
  - [Adams View Command Language Intellisense](#adams-view-command-language-intellisense)
  - [Intellisense support for Adams View Python Interface](#intellisense-support-for-adams-view-python-interface)
  - [CMD Linter](#cmd-linter)
    - [Macro Scanning](#macro-scanning)
  - [Code Navigation](#code-navigation)
  - [Debugging python scripts in Adams View](#debugging-python-scripts-in-adams-view)
    - [Steps to debug a python script in Adams View](#steps-to-debug-a-python-script-in-adams-view)
  - [Run in Adams View](#run-in-adams-view)
    - [Run selection in Adams View (*works for both CMD and Python files*)](#run-selection-in-adams-view-works-for-both-cmd-and-python-files)
    - [Run File in Adams View (This *works for both CMD and Python files*)](#run-file-in-adams-view-this-works-for-both-cmd-and-python-files)
  - [Open Adams View From Explorer](#open-adams-view-from-explorer)
  - [Snippets](#snippets)
  - [Copilot Agent Skills](#copilot-agent-skills)
  - [MCP Servers](#mcp-servers)
- [Extension Settings](#extension-settings)
  - [CMD Linter Settings](#cmd-linter-settings)
  - [Customizing Syntax Colors](#customizing-syntax-colors)
  - [Run In Adams: Substitute Params](#run-in-adams-substitute-params)
  - [Run In Adams: Substitute $\_self](#run-in-adams-substitute-_self)
- [Requirements](#requirements)
- [Known Issues](#known-issues)
  - [Attaching the Debugger to Adams View does not work in version 2023](#attaching-the-debugger-to-adams-view-does-not-work-in-version-2023)
  - [Equal Sign In A String On A Continuation Line](#equal-sign-in-a-string-on-a-continuation-line)
- [Support](#support)

# Features
## Syntax highlighting
- Adams View Command Languange (.cmd)
- Adams Solver Dataset Files (.adm)
- Adams Solver Command Files (.acf)
``
## Adams View Command Language Intellisense
- Adams Function Completion Provider
- Adams Function Documentation Hover Provider
- Adams Command Documentation Hover Provider (hover over a command keyword to see its description, syntax, and argument details)
- Adams Macro Documentation Hover Provider (hover over a user-defined macro invocation to see its help string)

![Example of Adams Function Documentation Hover Provider Example](https://github.com/bthornton191/adams_vscode/raw/HEAD/doc/autocomplete_function.gif)


## Intellisense support for Adams View Python Interface
* Completion provider
* Function signature help provider
* Type hinting

![adams python autocomplete](https://github.com/bthornton191/adams_vscode/raw/HEAD/doc/adams_python_autocomplete.gif)

## Debugging python scripts in Adams View
You can debug python scripts in Adams View using the [Python Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python). This extension provides a convenient button to attach the debugger to an existing Adams View process. 

> [!NOTE]
> Debugging ***is supported*** in Adams Car too! See 
> [Debugger not breaking when attached to Adams Car](https://github.com/bthornton191/adams_vscode/issues/9#issuecomment-2332435544) 
> if you are having trouble getting the debugger to break in Adams Car.

### Steps to debug a python script in Adams View
1. Open an Adams View session
2. Open the python script you want to debug in Visual Studio Code
3. Click the **Debug Python Script in Adams** button in the top right of the editor
   - Note: If you have multiple Adams View sessions open, you will be prompted to select one
4. Set breakpoints in the python script
5. In the Adams View session, import the python script
6. The python script will break at the breakpoints.

![debugging a python script in adams](https://github.com/bthornton191/adams_vscode/raw/HEAD/doc/debug_adams.gif)


## Run in Adams View

> [!IMPORTANT]
> **The command server must be running for these features to work**. The demos below show how to 
> start the command server. 

> [!TIP]
> Add `command_server start` to your startup macro (*aviewAS.cmd* or *aview.cmd*) to automatically 
> start the command server when Adams View is opened. This will allow you to run python scripts in  
> Adams View without having to manually start the command server.

### Run selection in Adams View (*works for both CMD and Python files*)
![Run CMD Selection in Adams View](https://github.com/bthornton191/adams_vscode/raw/HEAD/doc/run_selection_in_adams.gif)

### Run File in Adams View (This *works for both CMD and Python files*)
![Run CMD File in Adams View](https://github.com/bthornton191/adams_vscode/raw/HEAD/doc/run_file_in_adams.gif)

> [!NOTE] 
> For python files, the button is located within the existing python run button stack.
> ![Alt text](https://github.com/bthornton191/adams_vscode/raw/HEAD/doc/run_python_file_in_adams.png)

## Open Adams View From Explorer
* Open Adams View in a directory from the Explorer by right clicking and selecting **Open View**
  ![Example of opening adams view in a directory](https://github.com/bthornton191/adams_vscode/raw/HEAD/doc/open_vscode_in_folder.gif)

* Open a .cmd model file in Adams View from the Explorer by right clicking and selecting **Open In View**
  ![Example of opening adams view in a directory](https://github.com/bthornton191/adams_vscode/raw/HEAD/doc/open_in_view.gif)

## Snippets
- Adams View Command Language Snippets
- Adams View Python Interface Snippets

## CMD Linter
The extension includes a Language Server Protocol (LSP)-based linter for Adams View CMD files.
It flags unknown commands, invalid arguments, and other syntax errors as you type.

Diagnostic codes include:
| Code | Severity | Description |
|------|----------|-------------|
| E001 | Error | Unknown command |
| E002 | Error | Invalid macro parameter |
| E003 | Error | Invalid argument name |
| E004 | Error | Missing required argument |
| E005 | Error | Mutually exclusive arguments |
| E006 | Error | Duplicate argument |
| E105 | Error | Design function missing parentheses |
| W103 | Warning | Dangling continuation character |
| I202 | Info | Hardcoded Adams ID reference |

### Macro Scanning
Enable `msc-adams.linter.scanWorkspaceMacros` to let the linter discover user-defined macro files
(`.mac` by default) in the workspace. Once scanned, user-defined macros are recognised as valid
commands and their declared parameters are validated when the macro is called.

The linter also scans for User-Defined Element (UDE) definitions, recognising custom UDE commands
and their parameters.

## Code Navigation

- **Go to Definition** — Ctrl+Click on any macro invocation, variable, part, marker, constraint, or UDE to jump to where it's defined.
- **Find All References** — Right-click → Find All References to see every usage across the workspace.
- **Macro Parameter Navigation** — Ctrl+Click on `$param_name` in a macro body to jump to its definition; Shift+F12 for all references.
- **Hover Documentation** — Hover over a macro invocation to see its help string (sourced from `!HELP_STRING` in the macro file header or the `help_string=` argument of an inline `macro create` statement). Hover over Adams commands to see argument details, types, and descriptions.

## Copilot Agent Skills

The extension bundles 5 domain-knowledge skills that teach GitHub Copilot how to work with Adams. These are automatically available in Copilot Chat for all users who install the extension.

| Skill | Description |
|-------|-------------|
| **adams-cmd-model-builder** | Build models using Adams CMD syntax |
| **adams-python-model-builder** | Build models using the Adams Python API |
| **adams-flex** | Flexible bodies, MNF files, and rotordynamics |
| **adams-simulation-debugger** | Diagnose convergence failures and solver issues |
| **adams-subroutine-writer** | Write C, C++, and Fortran user subroutines |

## MCP Servers

The extension registers two [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) servers that allow AI assistants to interact with Adams directly:

**Adams View** — Connects to a running Adams View session. Provides tools to run CMD commands, execute Python, load files, submit simulations, and read the session log.

**Adams CMD Linter** — Static analysis tools that let AI agents look up command syntax (`adams_lookup_command`), lint raw CMD text (`adams_lint_cmd_text`), and lint CMD files (`adams_lint_cmd_file`). This allows agents to validate their own Adams output before showing it to you.
  
# Extension Settings

This extension contributes the following settings:
  * `msc-adams.adamsLaunchCommand`: Path to the mdi.bat file in your Adams installation.
  * `msc-adams.aviewPortNumber`: Port number for connecting to Adams View (default: `5002`).
  * `msc-adams.debugOptions`: Options passed to the Python debugger (e.g. `justMyCode`, `subProcess`).
  * `msc-adams.showDebuggerWarning`: Show a warning when attaching the debugger to Adams View 2023+.
  * `msc-adams.runInAdams.substituteSelf`: String to replace `$_self` with when running in Adams View.
  * `msc-adams.runInAdams.substituteParams`: Substitute macro parameters with their default values.
  * `msc-adams.runInAdams.autoLoadAdamspyStubs`: Automatically add adamspy stub files to the Python intellisense path.
  * `msc-adams.runInAdams.autoLoadAdamsSitePackages`: Automatically add Adams site-packages to the Python intellisense path.

## CMD Linter Settings

  * `msc-adams.linter.scanWorkspaceMacros`: When enabled, the CMD linter scans the workspace for
    macro files and uses them to suppress false "unknown command" errors for user-defined macros.
    Disabled by default.
  * `msc-adams.linter.macroPaths`: Glob patterns used to discover macro files when
    `scanWorkspaceMacros` is enabled. Defaults to `["**/*.mac"]`.
  * `msc-adams.linter.macroIgnorePaths`: Glob patterns for files or folders to exclude from macro
    scanning. Defaults to `[]`.
  * `msc-adams.linter.showMacroHint`: When a user-defined macro call triggers an E001 error, show
    a hint suggesting that `scanWorkspaceMacros` can be enabled. Defaults to `true`.
  * `msc-adams.linter.udePaths`: Glob patterns used to discover UDE definition files when
    `scanWorkspaceMacros` is enabled. Defaults to `["**/*.cmd"]`.
  * `msc-adams.linter.udeIgnorePaths`: Glob patterns for files or folders to exclude from UDE
    definition scanning. Defaults to `[]`.

## Customizing Syntax Colors

You may override the extension's default syntax colors using the `editor.tokenColorCustomizations` setting. The extension uses the following scopes:
 * parameter.reference
 * variable
 * constant
 * arguments
 * parameter.definition
 * selfParameter
 * command.command
 * command.control
 * command.argument
 * command.argument.continued

The example below would change the color and font style of the `variable` scope

```json
"editor.tokenColorCustomizations": {     
  "textMateRules": [
    {
      "scope": "variable",
      "settings": {
          "foreground": "#02485e",
          "fontStyle": "bold"
      }
    }
  ]
}
```

## Run In Adams: Substitute Params
When enabled (default), the extension will substitute macro parameters (i.e. variables prefixed 
with `$`) in the macro/selection before running it in Adams View. This will only work if the 
parameter is defined in the the macro with a default value 

For example, the following macro will run in Adams View with the parameter `$part` substituted with
 `PART_1` and `$mass` substituted with `1`.
```adams_cmd
!$part:t=part:d=PART_1
!$mass:t=real:d=1
part modify rigid_body mass_properties part=$part mass=$mass
```

However, the following macro ***will not run*** in Adams View because the parameter `$part` is not 
defined with a default value.
```adams_cmd
!$part:t=part
!$mass:t=real:d=1
part modify rigid_body mass_properties part=$part mass=$mass
```

## Run In Adams: Substitute $_self
When running a macro or a selection of a macro, the extension will substitute `$_self` with the 
a user defined value. The default is `.mdi`. This is useful when the macro uses local variables.

> [!NOTE]
> It is common convention to clear out local variables at the end of a macro using 
> `var del var=$_self.*`. If using this convention, you should not use the default `.mdi`. Instead,
> it is recommended to create an empty library in adams view and set the value of 
> `msc-adams.runInAdams.substituteSelf` to the name of the library.

# Requirements

- [MSC Adams](https://hexagon.com/products/product-groups/computer-aided-engineering-software/adams)

# Known Issues

## Attaching the Debugger to Adams View does not work in version 2023
The debugger appears to attach but fails to stop at break points.

> [!TIP]
> A workaround is to simply import the threading module before attaching the debugger. The easiest 
> way to do this is to open the adams view command line, switch to python, and run 
> `import threading`. You can also automate this by adding 
> `var set var=.mdi.tmp_int int=(eval(run_python_code("import threading")))` to aviewAS.cmd. 


## Equal Sign In A String On A Continuation Line
An equal sign in a string on a continuation line (i.e. a line following `&`) breaks syntax 
highlighting for the rest of the file.

> A workaround is to add `!"` after the line with the equal sign. As shown below.

![Animation of issue when an equal sign is in a string on a continuation line](https://github.com/bthornton191/adams_vscode/raw/HEAD/doc/issue_equal_in_continuation_line.gif)


# Support
Submit issues to https://github.com/bthornton191/adams_vscode/issues

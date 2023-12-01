# MSC Adams Extension for Visual Studio Code

![Visual Studio Marketplace Installs](https://img.shields.io/visual-studio-marketplace/i/savvyanalyst.msc-adams.svg?style=flat-square)
![Visual Studio Marketplace Rating Stars](https://img.shields.io/visual-studio-marketplace/stars/savvyanalyst.msc-adams.svg?style=flat-square)
![Visual Studio Marketplace Version](https://img.shields.io/visual-studio-marketplace/v/savvyanalyst.msc-adams.svg?style=flat-square)

> This is an early version. If you are interested in using it, please [reach out](https://github.com/bthornton191/adams_vscode/discussions) and let me 
> know which features you are most interested in. Thanks!

# Table of Contents
- [MSC Adams Extension for Visual Studio Code](#msc-adams-extension-for-visual-studio-code)
- [Table of Contents](#table-of-contents)
- [Features](#features)
  - [Syntax highlighting](#syntax-highlighting)
  - [Adams View Command Language Intellisense](#adams-view-command-language-intellisense)
  - [Intellisense support for Adams View Python Interface](#intellisense-support-for-adams-view-python-interface)
  - [Support for debugging python scripts in Adams View](#support-for-debugging-python-scripts-in-adams-view)
    - [Steps to debug a python script in Adams View](#steps-to-debug-a-python-script-in-adams-view)
  - [Run in Adams View](#run-in-adams-view)
    - [Run selection in Adams View (*works for both CMD and Python files*)](#run-selection-in-adams-view-works-for-both-cmd-and-python-files)
    - [Run File in Adams View (This *works for both CMD and Python files*)](#run-file-in-adams-view-this-works-for-both-cmd-and-python-files)
  - [Open Adams View From Explorer](#open-adams-view-from-explorer)
  - [Snippets](#snippets)
- [Extension Settings](#extension-settings)
  - [Customizing Syntax Colors](#customizing-syntax-colors)
  - [Run In Adams: Substitute Params](#run-in-adams-substitute-params)
  - [Run In Adams: Substitute $\_self](#run-in-adams-substitute-_self)
- [Requirements](#requirements)
- [Known Issues](#known-issues)
  - [Attaching the Debugger to Adams View does not work in version 2023](#attaching-the-debugger-to-adams-view-does-not-work-in-version-2023)
  - [Intellisense Adams Command Language *functions* does not work for every function](#intellisense-adams-command-language-functions-does-not-work-for-every-function)
  - [Equal Sign In A String On A Continuation Line](#equal-sign-in-a-string-on-a-continuation-line)
- [Contributing](#contributing)
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

![Example of Adams Function Documentation Hover Provider Example](https://github.com/bthornton191/adams_vscode/raw/HEAD/doc/autocomplete_function.gif)


## Intellisense support for Adams View Python Interface
* Completion provider
* Function signature help provider
* Type hinting

> [!NOTE]
> You may need to manually activate the extension using `msc_adams.activate` for these features to work
> ![adams python autocomplete](https://github.com/bthornton191/adams_vscode/raw/HEAD/doc/adams_python_autocomplete.gif)

## Support for debugging python scripts in Adams View
You can debug python scripts in Adams View using the [Python Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python). This extension provides a convenient button to attach the debugger to an existing Adams View process. 

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
> For python files, the button is located within the existing python run button stack.!
> ![Alt text](https://github.com/bthornton191/adams_vscode/raw/HEAD/doc/run_python_file_in_adams.png)

## Open Adams View From Explorer
* Open Adams View in a directory from the Explorer by right clicking and selecting **Open View**
  ![Example of opening adams view in a directory](https://github.com/bthornton191/adams_vscode/raw/HEAD/doc/open_vscode_in_folder.gif)

* Open a .cmd model file in Adams View from the Explorer by right clicking and selecting **Open In View**
  ![Example of opening adams view in a directory](https://github.com/bthornton191/adams_vscode/raw/HEAD/doc/open_in_view.gif)

## Snippets
- Adams View Command Language Snippets
- Adams View Python Interface Snippets
  
# Extension Settings

This extension contributes the following settings:
  * msc-adams.adams_launch_command: Path to the mdi.bat file in your Adams installation.

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
This is likely due to a change in the compilers for Adams 2023. I am working on a fix.

## Intellisense Adams Command Language *functions* does not work for every function
It's a work in progress. The help documentation for each function needs to be converted to a 
markdown file and I simply haven't had time to do every function.

## Equal Sign In A String On A Continuation Line
An equal sign in a string on a continuation line (i.e. a line following `&`) breaks syntax 
highlighting for the rest of the file.

> A workaround is to add `!"` after the line with the equal sign. As shown below.

![Animation of issue when an equal sign is in a string on a continuation line](https://github.com/bthornton191/adams_vscode/raw/HEAD/doc/issue_equal_in_continuation_line.gif)


# Contributing
...


# Support
Submit issues to https://github.com/bthornton191/adams_vscode/issues

# MSC Adams Extension for Visual Studio Code

> This is an early version. If you are interested in using it, please [reach out](mailto:ben.thornton@hexgagon.com) and let me 
know which features you are most interested in. Thanks!


## Features

### Syntax highlighting
- Adams View Command Languange (.cmd)
- Adams Solver Dataset Files (.adm)
- Adams Solver Command Files (.acf)

### Adams View Command Language Intellisense
- Adams Function Completion Provider
- Adams Function Documentation Hover Provider

![Example of Adams Function Documentation Hover Provider Example](doc/autocomplete_function.gif)

### Snippets
- Adams View Command Language Snippets
- Adams View Python Interface Snippets

### Intellisense support for Adams View Python Interface
![adams python autocomplete](doc/adams_python_autocomplete.gif)

### Open Adams View From Explorer
* Open Adams View in a directory from the Explorer by right clicking and selecting **Open View**
  ![Example of opening adams view in a directory](doc/open_vscode_in_folder.gif)

* Open a .cmd model file in Adams View from the Explorer by right clicking and selecting **Open In View**
  ![Example of opening adams view in a directory](doc/open_in_view.gif)

## Extension Settings

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
## Requirements

- [MSC Adams](https://hexagon.com/products/product-groups/computer-aided-engineering-software/adams)

## Known Issues

### Intellisense Adams Command Language *functions* does not work for every function
It's a work in progress. The help documentation for each function needs to be converted to a 
markdown file and I simply haven't had time to do every function.

### Equal Sign In A String On A Continuation Line
An equal sign in a string on a continuation line (i.e. a line following `&`) breaks syntax 
highlighting for the rest of the file.

> A workaround is to add `!"` after the line with the equal sign. As shown below.

![Animation of issue when an equal sign is in a string on a continuation line](doc/issue_equal_in_continuation_line.gif)


## Contributing
...


## Support
Submit issues to https://github.com/bthornton191/adams_vscode/issues
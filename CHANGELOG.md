# Changelog

- [Changelog](#changelog)
  - [0.4.2 (December 6th 2023)](#042-december-6th-2023)
    - [Intellisense support for Adams View Python Interface](#intellisense-support-for-adams-view-python-interface)
      - [**Fixed**: Fixed a bug preventing python intellisense from working properly](#fixed-fixed-a-bug-preventing-python-intellisense-from-working-properly)
  - [0.4.1 (December 1st 2023)](#041-december-1st-2023)
    - [Run in Adams View](#run-in-adams-view)
      - [**Added**: Run selection in Adams View](#added-run-selection-in-adams-view)
      - [**Added**: Run File in Adams View](#added-run-file-in-adams-view)
  - [0.3.0 (September 1st 2023)](#030-september-1st-2023)
    - [Syntax Highlighting](#syntax-highlighting)
    - [Snippets](#snippets)
    - [Improvements to the Adams View Python stub files](#improvements-to-the-adams-view-python-stub-files)
    - [Improvements to Debugger](#improvements-to-debugger)


## 0.4.2 (December 6th 2023)

### Intellisense support for Adams View Python Interface
#### **Fixed**: Fixed a bug preventing python intellisense from working properly


## 0.4.1 (December 1st 2023)

### Run in Adams View

#### **Added**: Run selection in Adams View

This works for both CMD and Python files
![Run CMD Selection in Adams View](https://github.com/bthornton191/adams_vscode/raw/HEAD/doc/run_selection_in_adams.gif)

#### **Added**: Run File in Adams View
This works for both CMD and Python files
![Run CMD File in Adams View](https://github.com/bthornton191/adams_vscode/raw/HEAD/doc/run_file_in_adams.gif)

> [!NOTE]
> For python files, the button is located within the existing python run button stack.
> ![button to run python file in adams](https://github.com/bthornton191/adams_vscode/raw/HEAD/doc/run_python_file_in_adams.png)

## 0.3.0 (September 1st 2023)
### Syntax Highlighting
- **Added**: Syntax highlighting for aview.log files
- **Added**: Syntax highlighting for .msg files

### Snippets
- **Added**: Integer For Loop
  
  ![int_for_loop_snippet](https://github.com/bthornton191/adams_vscode/raw/HEAD/doc/int_for_loop_snippet.gif)

- **Added**: Request
  
  ![request_snippet](https://github.com/bthornton191/adams_vscode/raw/HEAD/doc/req_snippet.gif)

### Improvements to the Adams View Python stub files
Improved type hints and doc strings.

### Improvements to Debugger
Added a **msc-adams.debugOptions** setting allowing options to be passed to the debugger when
attaching to Adams View. Example:
```json
    "msc-adams.debugOptions": {
    
        "justMyCode": false,
        "subProcess": true,
        "logToFile": true
    },
```

# Changelog

- [Changelog](#changelog)
  - [1.0.0 (September 16th 2024)](#100-september-16th-2024)
  - [0.4.12 (September 3rd 2024)](#0412-september-3rd-2024)
    - [Documentation](#documentation)
  - [0.4.11 (September 3rd 2024)](#0411-september-3rd-2024)
    - [Documentation](#documentation-1)
  - [0.4.9 (September 3rd 2024)](#049-september-3rd-2024)
    - [Bug Fixes](#bug-fixes)
  - [0.4.7 (July 9th 2024)](#047-july-9th-2024)
    - [Bug Fixes](#bug-fixes-1)
  - [0.4.6 (July 8th 2024)](#046-july-8th-2024)
    - [Bug Fixes](#bug-fixes-2)
    - [**Improved** Run In Adams](#improved-run-in-adams)
    - [**Added** a warning when debugging Adams View versions \>= 2023](#added-a-warning-when-debugging-adams-view-versions--2023)
    - [Miscellaneous](#miscellaneous)
    - [Development](#development)
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


## 1.0.0 (September 16th 2024)
- Official Version 1.0.0 Release. No new features or bug fixes. This release is to mark the extension as stable and ready for production use.

## 0.4.12 (September 3rd 2024)
### Documentation
- **Fixed** a typo in the readme.

## 0.4.11 (September 3rd 2024)
### Documentation
- **Added** A note to the readme about debugging in Adams Car. [More Info](https://github.com/bthornton191/adams_vscode/issues/9#issuecomment-2332435544)
  

## 0.4.9 (September 3rd 2024)
### Bug Fixes
- **Fixed** A bug causing python type hints to only partially work in python 3.10 and higher.

## 0.4.7 (July 9th 2024)
### Bug Fixes
- **Fixed** minor bug preventing the debugger from attaching to Adams View when the command window is selected in Adams View

## 0.4.6 (July 8th 2024)

### Bug Fixes
- **Fixed** syntax highliging issue when a string argument contains an equals sign on a continuation line ([Issue 3](https://github.com/bthornton191/adams_vscode/issues/3))

### **Improved** Run In Adams
- You can now set `msc-adams.runInAdams.substituteSelf` to an existing OR non-existent library 
  (e.g. ".vscode") and the extension will automatically create an empty library by that name replace 
  all occurances of `$_self` with the library name when running the file or selection in Adams View.
  This closes [Issue 4](https://github.com/bthornton191/adams_vscode/issues/4).


### **Added** a warning when debugging Adams View versions >= 2023
A reminder that you may need to import the threading module before attaching the debugger. [More Info](https://github.com/bthornton191/adams_vscode/issues/6#issuecomment-2192053891)

### Miscellaneous
- **Added** clickable links in model and log files
- **Added** a configuration option called `msc-adams.runInAdams.autoLoadAdamspyStubs` allowing users
  to prevent the extension from automatically loading the Adams View Python stubs. This is useful if
  you have your own stubs.

- **Improved** intellisense documentation and typing in the following adamspy modules:
    * Analysis
    * Constraint
    * Contact
    * DataElement
    * DBAccess
    * Force
    * Group
    * Manager
    * Marker
    * Measure
    * Model
    * Part
    * Sensor
    * Simulation
    * SystemElement
    * UDE

- **Added** intellisense support for the following design functions:
    * `dm`
    * `dot`
    * `dx`
    * `dy`
    * `dz`
    * `eig_di`
    * `eig_dr`
    * `eig_vi`
    * `eig_vr`
    * `elementmd`
    * `execute_view_command`
    * `exp`
    * `expr_exists`
    * `expr_reference`
    * `expr_references`
    * `expr_string`
    * `top_spots`
    * `unique` copy
    * `unique_file_name`
    * `unique_full_name`
    * `unique_id`
    * `unique_name_in_hierarchy`
    * `uniquemd`
    * `units_conversion_factor`
    * `units_string`
    * `unwrap`
    * `val`
    * `valat`
    * `vali`
  
### Development
- **Added** a test suite

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

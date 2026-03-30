# Adams View Macros — CMD Reference

Macros are **named command sequences** stored in the Adams View database. In practice they are always defined in `.mac` text files and loaded with `macro read`. The inline `macro create` form exists but is rarely used outside of tests.

---

## Loading and Executing a Macro

```adams_cmd
! Load a macro file into the Adams View database
macro read &
    file_name = "C:/my_project/macros/my_macro.mac" &
    library_name = (my_lib)

! Execute a loaded macro (user_entered_command form)
macro execute &
    macro_name = .my_lib.my_macro

! Shorthand execution via user-entered-command namespace prefix:
!   macros loaded into library "acnvr" are run as:
acnvr my_macro  arg1=value1  arg2=value2
```

---

## The .mac File Format

A `.mac` file starts with a **parameter declaration block** (lines beginning with `!`) followed by the macro body.

```adams_cmd
! ============================================================
! Macro:  my_macro
! Purpose: One-line description
! ============================================================
!
!USER_ENTERED_COMMAND  maclib my_macro
!HELP_STRING           Brief usage string shown in panel
!CREATE_PANEL          no
!WRAP_IN_UNDO          yes
!
! --- Parameter declarations ---
!$part_name:t=part:c=1
!$link_length:t=real:c=1:d=100.0
!$num_links:t=integer:c=1:d=3
!$label:t=string:c=1:d="LINK"
!$echo_all_loops:t=string:c=1:d=no
!
!END_OF_PARAMETERS
! ============================================================

! Macro body starts here
variable set variable_name = $_self.len real_value = $link_length

! ... commands ...

variable delete variable = $_self.*
```

### Parameter declaration syntax

```
!$<name>:t=<type>:c=<count>:d=<default>:r=<range>
```

All qualifiers are case-insensitive. The `t=` and `c=` qualifiers are required; `d=` and `r=` are optional.

---

## Parameter Qualifiers

### t= (type)

| Value | Description |
|-------|-------------|
| `integer` | Whole number |
| `real` | Floating-point number |
| `string` | Quoted or unquoted text |
| `part` | Adams part object |
| `marker` | Adams marker object |
| `joint` | Constraint joint object |
| `force` | Force object |
| `contact` | Contact object |
| `group` | Group object |
| `analysis` | Simulation analysis object |
| `adams_matrix` | Adams matrix data element |
| `point_curve` | Point-on-curve data element |
| `file(*.ext)` | File path (wildcard filters dialog box, e.g. `file(*.mac)`) |
| `list(a,b,c)` | Enumerated string — only listed values accepted |

### c= (count / cardinality)

| Value | Meaning | Notes |
|-------|---------|-------|
| `c=1` | Exactly one | Most common |
| `c=0` | Optional — may be omitted | Must provide `d=` default or handle absent case |
| `c=n` | Exactly *n* values | Adams passes them as a comma-separated list |
| `c=n,0` | Up to *n* values | |
| `c=n,m` | Between *n* and *m* values | |

When `c=0` the parameter is optional; test with `DB_EXISTS("$param_name")` is not needed — Adams substitutes the default automatically if a default is declared.

### d= (default)

```
!$angle:t=real:c=0:d=90.0
!$label:t=string:c=0:d="new_part"
!$mode:t=list(fast,slow,auto):c=1:d=fast
```

### r= (range) — numeric types only

| Range qualifier | Meaning |
|----------------|---------|
| `r=GT(0)` | Must be > 0 |
| `r=GE(0)` | Must be ≥ 0 |
| `r=LT(180)` | Must be < 180 |
| `r=LE(360)` | Must be ≤ 360 |

---

## Metadata Comments

These lines are **all optional** and appear before `!END_OF_PARAMETERS`. They control how Adams View integrates the macro into its UI:

| Keyword | Purpose |
|---------|---------|
| `!USER_ENTERED_COMMAND <ns> <name>` | Command string users type at the command input (sets namespace prefix) |
| `!HELP_STRING <text>` | Short help text displayed in the Adams View macro panel |
| `!CREATE_PANEL yes/no` | Whether Adams View auto-generates a dialog panel for the macro |
| `!WRAP_IN_UNDO yes/no` | Whether the macro's actions are grouped into a single undo step |

---

## Variable Scoping with `$_self`

`$_self` is a built-in read-only string variable that holds the **full database path of the currently-executing macro** (e.g., `.my_lib.my_macro`). Use it to namespace all temporary variables, preventing name collisions when macros call other macros:

```adams_cmd
! Create a temp variable scoped to this macro
variable set variable_name = $_self.count  integer_value = 0

! Reference it (bare name inside this macro)
variable set variable_name = $_self.count  integer_value = (eval($_self.count) + 1)

! Clean up ALL temp variables at end of macro
! (Only safe if at least one $_self.* variable was created on every code path)
variable delete variable = $_self.*
```

**Cleanup caveat:** `variable delete variable = $_self.*` raises an error if no `$_self.*` variables have been created. If your macro has optional code paths, either:
- ensure a sentinel variable (e.g. `$_self._init`) is always created at the top, or  
- guard the cleanup with `if condition = (DB_EXISTS(($_self // "._init")))`.

---

## Output Parameters (Returning Values)

Adams macros have no return statement. The standard pattern is for the caller to pass a **string parameter containing the name of the variable to write to**:

```adams_cmd
! In sub_macro.mac — caller-supplied output variable name
!$result_var:t=string:c=1
!END_OF_PARAMETERS

variable set &
    variable_name = $result_var &
    real_value    = (eval(...))
```

```adams_cmd
! In caller macro — create output slot, pass its name, read it back
variable set variable_name = $_self.result  real_value = 0.0

acmylib sub_macro  result_var = ($_self // ".result")

! Now $_self.result holds the return value
variable set variable_name = some_other_var &
    real_value = (eval($_self.result))
```

---

## Utility Functions

| Function | Returns | Purpose |
|----------|---------|---------|
| `UNIQUE_NAME("prefix")` | String | Collision-free name e.g. `UNIQUE_NAME(".model.spr_")` |
| `DB_EXISTS("path")` | 1 / 0 | True if the named object exists in the database |
| `DB_ANCESTOR("path", "type")` | String (path) | Navigate to nearest ancestor of given type — common for finding a part's model |
| `DB_TYPE("path")` | String | Returns the type string of an object |

```adams_cmd
! Auto-name a new spring
variable set variable_name = $_self.spr_name &
    string_value = (UNIQUE_NAME(".model.spr_"))

! Find owning model of a part
variable set variable_name = $_self.mdl_name &
    string_value = (DB_ANCESTOR(eval($_self.part), "model"))
```

---

## File I/O Pattern

> **Prefer Python for heavy file I/O.** The write-then-read-back pattern below is useful for generating a handful of commands at runtime. For anything more complex — parsing input data, writing structured reports, looping over many results — use the Adams Python API instead.

For generating a small set of dynamic commands at runtime, write them to a temporary `.cmd` file and read them back:

```cmd
variable set variable_name = $_self.tmp_file &
    string_value = (UNIQUE_NAME("tmp_cmds_"))

file text open &
    file_name = ($_self.tmp_file // ".cmd") &
    open_mode = overwrite

! Write one command per line
! format_for_output supports C printf specifiers; use %s as a pass-through
file text write &
    file_name         = ($_self.tmp_file // ".cmd") &
    format_for_output = "%s" &
    values_for_output = ("part create rigid_body name_and_position part_name=" // $my_part)

file text close file_name = ($_self.tmp_file // ".cmd")

! Execute the generated commands
file command read file_name = ($_self.tmp_file // ".cmd")
```

> **Note:** Adams View CMD has no `file delete` command. Temp files persist on disk.

For full `file text` command syntax, see [`references/commands/file-io.md`](file-io.md).

---

## Macro Lifecycle Commands

### `macro read` — Load a .mac file

```
macro read &
    file_name    = "<path>" &
    library_name = (<library_object>)
```

### `macro create` — Define a macro inline (rarely used)

```
macro create &
    macro_name             = <name> &
    user_entered_command   = "<prefix> <cmd_name>" &
    commands_to_be_executed = "<cmd1>" , "<cmd2>"
```

### `macro write` — Save a loaded macro back to a .mac file

```
macro write &
    macro_name = <name> &
    file_name  = "<path>"
```

### `macro modify` — Change a loaded macro's metadata or body

```
macro modify &
    macro_name           = <name> &
    wrap_in_undo         = yes | no &
    help_string          = "<text>"
```

### `macro delete` — Remove a macro from the database

```
macro delete macro_name = <name>
```

### `list_info macro` — Print macro info to Message Window

```
list_info macro macro_name = <name>
```

---

## Common Patterns Checklist

- Declare all parameters in `!$name:T=...:C=...:D=...` comments before `!END_OF_PARAMETERS`
- Set `!WRAP_IN_UNDO yes` so the whole macro undos as a single step
- Namespace all temporaries via `$_self.varname`
- Create at least one `$_self.*` variable before any early-exit path if you use the wildcard delete
- Pass output variable names as string parameters — read them back after the sub-macro call
- Use `UNIQUE_NAME()` for any database objects that should not collide with user names
- Use `DB_EXISTS()` guards before creating or deleting named objects
- Spell out **all commands in full** — never use abbreviated CMD keywords

---

## See also

- [Scripting — variables, loops, conditionals](scripting.md)
- [File I/O — text open/write/close, command read](file-io.md)
- [Example: simple icon-resize macro](../../assets/cmd_scripts/example_macro_resize_icons.mac)
- [Example: batch spring creation macro](../../assets/cmd_scripts/example_macro_batch_spring.mac)
- [Example: export-results macro](../../assets/cmd_scripts/example_macro_export_results.mac)

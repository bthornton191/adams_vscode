# File I/O — CMD Reference

Adams View provides commands for writing text files, reading them back as commands, and loading/saving model data. This page covers the text-file I/O pattern used inside macros plus the most common model-file commands.

> **Prefer Python for heavy file I/O.** Adams CMD `file text` commands are adequate for generating short command sequences at runtime (write → read-back pattern). For anything more involved — parsing input files, writing structured output, iterating over many results — use the Adams Python API (`adamspy` / `aview` module) instead. Python has full access to the filesystem, standard library I/O, `os`, `pathlib`, `csv`, etc.

---

## `file text open` — Open a file for writing

```cmd
file text open &
    file_name = "<path>" &
    open_mode = overwrite | append
```

| Parameter | Required | Values | Notes |
|-----------|----------|--------|-------|
| `file_name` | yes | string | Path to the file. Quote if it contains `.`, `/`, or `\` |
| `open_mode` | no | `overwrite` \| `append` | `overwrite` deletes any existing file; `append` adds to it. Default is `overwrite` |

```cmd
file text open &
    file_name = (eval($_self.tmp) // ".cmd") &
    open_mode = overwrite
```

---

## `file text write` — Write a line to an open file

```cmd
file text write &
    file_name         = "<path>" &
    format_for_output = "<printf-format>" &
    values_for_output = <value1>, <value2>, ... &
    newline           = yes | no
```

| Parameter | Required | Notes |
|-----------|----------|-------|
| `file_name` | no | Target file (defaults to the last opened/written file) |
| `format_for_output` | no | C `printf`-style format string. `%s` = string, `%d` = integer, `%f` = real, `%%` = literal `%` |
| `values_for_output` | no | Comma-separated values substituted into `%` specifiers |
| `newline` | no | Append a newline after the write? Default `yes` |

### Writing a plain literal line

```cmd
file text write &
    file_name         = (eval($_self.tmp) // ".cmd") &
    format_for_output = "part create rigid_body name_and_position &"
```

### Writing a line with substituted values

```cmd
file text write &
    file_name         = (eval($_self.tmp) // ".cmd") &
    format_for_output = "    part_name = %s &" &
    values_for_output = (eval($_self.part_name))
```

### Writing a pre-built expression as a plain string

Use `format_for_output = "%s"` to pass through an Adams expression that produces the full line:

```cmd
file text write &
    file_name         = (eval($_self.tmp) // ".cmd") &
    format_for_output = "%s" &
    values_for_output = ("    file_name = " // chr(34) // eval($_self.path) // chr(34))
```

**`chr(34)` is the standard way to embed a double-quote character** inside an Adams string expression.

---

## `file text close` — Close an open text file

```cmd
file text close file_name = "<path>"
```

`file_name` is optional; Adams View closes the last opened/written file if omitted. Always close before reading the file with `file command read`.

---

## `file command read` — Execute a .cmd file

```cmd
file command read file_name = "<path>"
```

Reads the file and executes every line as if typed at the command prompt. Control returns after all commands have run. If a command fails, Adams View aborts the file by default (configurable with `defaults command_file`).

The `.cmd` extension is the default but can be overridden by supplying a different extension.

---

## Complete File I/O Pattern

Generate commands dynamically by writing them to a temp file, then executing:

```cmd
! 1. Generate a collision-free temp file name
variable set variable_name = $_self.tmp &
    string_value = (UNIQUE_NAME("tmp_cmds_"))

! 2. Open for writing
file text open &
    file_name = (eval($_self.tmp) // ".cmd") &
    open_mode = overwrite

! 3. Write lines — each becomes one command in the file
file text write &
    file_name         = (eval($_self.tmp) // ".cmd") &
    format_for_output = "part create rigid_body name_and_position &"

file text write &
    file_name         = (eval($_self.tmp) // ".cmd") &
    format_for_output = "    part_name = %s &" &
    values_for_output = (eval($_self.part_name))

file text write &
    file_name         = (eval($_self.tmp) // ".cmd") &
    format_for_output = "    location  = %s" &
    values_for_output = "0, 0, 0"

! 4. Close before reading
file text close file_name = (eval($_self.tmp) // ".cmd")

! 5. Execute the generated commands
file command read file_name = (eval($_self.tmp) // ".cmd")
```

> **Note:** Adams View CMD has no `file delete` command. Temp files written to the working directory will persist until manually removed from outside Adams.

---

## Other Useful File Commands

### Load and save a model (.cmd or .adm)

```cmd
! Write the current model to a CMD script
file adams write &
    file_name  = "C:/project/my_model.cmd" &
    model_name = .my_model

! Read (merge) a model from a CMD script
file command read file_name = "C:/project/my_model.cmd"

! Read a binary Adams dataset (.adm)
file adams read file_name = "C:/project/my_model.adm"
```

### Log display output

```cmd
file log &
    file_name = "C:/project/session.log" &
    operation = start
```

---

## See also

- [Macros — create, parameters, file-based](macros.md)
- [Scripting — variables, loops, conditionals](scripting.md)
- [Example: export-results macro](../../assets/cmd_scripts/example_macro_export_results.mac)

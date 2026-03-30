# File System Functions

Functions for working with files and directories, reading environment variables, executing Adams View commands programmatically, and measuring elapsed time.

## Quick reference

| Function | Description |
|----------|-------------|
| `BACKUP_FILE` | Rename a file to a backup |
| `CHDIR` | Change the current working directory |
| `COPY_FILES` | Copy files |
| `EXECUTE_VIEW_COMMAND` | Run an Adams View command string |
| `FILE_EXISTS` | Check if a file exists |
| `GETCWD` | Get the current working directory |
| `GETENV` | Read an environment variable |
| `LOCAL_FILE_NAME` | Resolve a local file name |
| `MKDIR` | Create a directory |
| `PARSE_STATUS` | Parse an Adams message file |
| `PUTENV` | Set an environment variable |
| `REMOVE_FILE` | Delete a file |
| `RENAME_FILE` | Rename a file |
| `RMDIR` | Remove a directory |
| `SIM_STATUS` | Status result of the last simulation |
| `SYS_INFO` | System information string |
| `TERM_STATUS` | Terminal/command status |
| `TIMER_CPU` | CPU time measurement |
| `TIMER_ELAPSED` | Wall-clock time measurement |

---

## BACKUP_FILE

Renames a file to a backup. On Linux, appends `%`; on Windows, replaces the last character with `q`.

```
BACKUP_FILE(file_name)
```

```adams_cmd
var set var=result integer=(EVAL(BACKUP_FILE("foo.dat")))
```

---

## CHDIR

Changes the current working directory.

```
CHDIR(directory)
```

---

## COPY_FILES

Copies one or more files.

```
COPY_FILES(source, destination)
```

---

## EXECUTE_VIEW_COMMAND

Executes a string as an Adams View command. Returns `1` on success, `0` on failure.

```
EXECUTE_VIEW_COMMAND(command)
```

```adams_fn
EXECUTE_VIEW_COMMAND("marker create marker=" // UNIQUE_NAME("mar"))
! returns 1 and creates a marker with a unique name
```

---

## FILE_EXISTS

Returns `1` if the file exists; `0` otherwise.

```
FILE_EXISTS(file_name)
```

```adams_fn
FILE_EXISTS("aview.log")   ! returns 1 if the file is present
```

---

## GETCWD

Returns the current working directory as a string.

```
GETCWD()
```

```adams_fn
GETCWD()   ! e.g. returns "C:/Users/username/models"
```

---

## GETENV

Returns the value of an environment variable as a string.

```
GETENV(variable_name)
```

```adams_fn
GETENV("ADAMS_INSTALL_PATH")
GETENV("USER")
```

---

## LOCAL_FILE_NAME

Returns the local (non-network) file name for a given path.

```
LOCAL_FILE_NAME(path)
```

---

## MKDIR

Creates a directory. Returns `1` on success, `0` on failure.

```
MKDIR(directory)
```

---

## PARSE_STATUS

Parses an Adams message file (usually `.msg`) and returns an array of integer status codes for a given search tag.

```
PARSE_STATUS(file_name, tag)
```

| Argument | Description |
|----------|-------------|
| `file_name` | Name of the message file |
| `tag` | Status code tag string to look for |

---

## PUTENV

Sets an environment variable.

```
PUTENV(variable_name, value)
```

---

## REMOVE_FILE

Deletes a file.

```
REMOVE_FILE(file_name)
```

---

## RENAME_FILE

Renames a file.

```
RENAME_FILE(old_name, new_name)
```

---

## RMDIR

Removes a directory.

```
RMDIR(directory)
```

---

## SIM_STATUS

Returns an integer status code from the last simulation run.

```
SIM_STATUS()
```

---

## SYS_INFO

Returns a string containing system information.

```
SYS_INFO(info_type)
```

| `info_type` | Returns |
|-------------|---------|
| `"GID"` | Numeric group ID |
| `"GROUPNAME"` | Group name |
| `"HOSTNAME"` | Host name |
| `"UID"` | Numeric user ID |
| `"USERNAME"` | Login user name |
| `"REALNAME"` | User's full name |

```adams_fn
SYS_INFO("HOSTNAME")
```

---

## TERM_STATUS

Returns the status of the last terminal command.

```
TERM_STATUS()
```

---

## TIMER_CPU

Starts or stops a CPU timer. Pass `0` to start (returns current CPU time); pass `1` to stop (returns elapsed CPU seconds).

```
TIMER_CPU(end_flag)
```

---

## TIMER_ELAPSED

Starts or stops a wall-clock timer. Pass `0` to start; pass `1` to stop.

```
TIMER_ELAPSED(end_flag)
```

---

## See also

- [String functions](str-functions.md)
- [Alert functions](alert-functions.md)
- [Unique name functions](unique-units.md)

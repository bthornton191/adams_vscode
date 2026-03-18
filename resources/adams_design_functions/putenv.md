# PUTENV

Returns the string value that PUTENV assigned to an environment variable. If successful, it returns a 0; otherwise, it returns a non-zero value. PUTENV only affects the environment of the current executable.

## Format
```
PUTENV (Environment Variable, Value)
```

## Arguments

**Environment Variable**
: Character string denoting an environment variable.

**Value**
: Character string to be stored as the value of the environment variable.Note:	If the Value is File or directory path, use below file separator conventions:♦For Windows, use double backslash, for example: C:\\Temp\\FilePath.txt♦For Linux, use single forward slash, for example: ./usr/Temp/FilePath.txt

## Example

The following function, assigns the value X11 to MDI_AVIEW_WIN:

### Function
```
(PUTENV("MDI_AVIEW_WIN","X11"))
```

### Result
```
0
```

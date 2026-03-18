# RENAME_FILE

Renames a specified file. If successful, it returns a 0; otherwise, it returns a nonzero value.

## Format
```
RENAME_FILE (File Name, New File Name)
```

## Arguments

**File Name**
: Text string containing the current file name.

**New File Name**
: Text string containing the new file name.

## Example

The following example illustrates the use of the RENAME_FILE function:

### Function
```
RENAME_FILE("Test.mif.backup", "Test.doc")
```

### Result
```
renames the specified file as Test.doc and returns a 0
```

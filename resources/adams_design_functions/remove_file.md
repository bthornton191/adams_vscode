# REMOVE_FILE

Removes a file. If successful, it returns a 0; otherwise, it returns a nonzero value. `REMOVE_FILE` will succeed in deleting a file that you opened with the file text open command, even if you did not close the file.

## Format
```
REMOVE_FILE (File Name)
```

## Arguments

**File Name**
: The file to be deleted.

## Example

The following example illustrates the use of the `REMOVE_FILE` function:

### Function
```
REMOVE_FILE("Test_File.doc")
```

### Result
```
deletes Test_File.doc and returns a 0
```

# WRITE_T_O_TABLE_HEADER

Writes a head to the currently selected block or subblock within the currently open file. Writes 1 on success and 0 if errors occur.

## Format
```
WRITE_T_O_TABLE_HEADER (Value)
```

## Arguments

**Value**
: Header text to write to the file.

## Example

### Function
```
WRITE_T_O_TABLE_HEADER ("disp force")
```

### Result
```
1
```

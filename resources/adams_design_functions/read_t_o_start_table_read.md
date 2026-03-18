# READ_T_O_START_TABLE_READ

Searches the currently open TeimOrbit file for the specified table, and returns the first line of text from the table. Returns an empty string if the table is not found or other errors occur.

## Format
```
READ_T_O_START_TABLE_READ (Block Name)
```

## Arguments

**Block Name**
: Name of block in which to read from

## Example

[The following assumes this file has already been opened ("<acar_shared>/springs.tbl/mdi_0001.spr")]

### Function
```
READ_T_O_START_TABLE_READ("CURVE")
```

### Result
```
{  disp       force}
```

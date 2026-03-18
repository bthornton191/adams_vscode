# READ_T_O_TABLE_COLUMN

Searches a specified block within the currently open TeimOrbit file for column of real numbers with the specified attribute label. Returns the one-dimensional array of real number values from the selected column, or 0.0 if the attribute is not found or other errors occur.

## Format
```
READ_T_O_TABLE_COLUMN  (Block Name, Column)
```

## Arguments

**Block Name**
: Name of block in which to search

**Column**
: Column header within the specified block to retrieve the one-dimensional array of real number values.

## Example

[The following assumes this file has already been opened ("<acar_shared>/springs.tbl/mdi_0001.spr")]

### Function
```
READ_T_O_TABLE_COLUMN ("CURVE", "force")
```

### Result
```
[-10750.0, -8000.0, …, 10750.0]
```

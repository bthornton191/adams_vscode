# READ_T_O_SUBBLOCK_TABLE_COLUMN

Searches a specified subblock block within selected block in the currently open TeimOrbit file for column of real numbers with the specified attribute label. Returns the one-dimensional array of real number values from the selected column, or 0.0 if the attribute is not found or other errors occur.

## Format
```
READ_T_O_SUBBLOCK_TABLE_COLUMN  (Block Name, SubBlock Name, Column)
```

## Arguments

**SubBlock Name**
: Name of subblock in which to search

**Block Name**
: Name of block in which to search

**Column**
: Column header within the specified subblock to retrieve the one-dimensional array of real number values.

## Example

[The following assumes this file has already been opened ("<acar_shared>/powertrains.tbl/V12_engine_map.pwr")]

### Function
```
READ_T_O_SUBBLOCK_TABLE_COLUMN ("ENGINE", "XY_DATA", "engine_speed")
```

### Result
```
[0.0,500.0,1000.0,…,7500.0]
```

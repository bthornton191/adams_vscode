# READ_T_O_START_SUBBLOCK_TABLE_READ

Searches the currently open TeimOrbit file for the specified subblock contained within the selected block, and returns the first line of text from the subblock table. Returns an empty string if the subblock is not found or other errors occur.

## Format
```
READ_T_O_START_SUBBLOCK_TABLE_READ (Block Name, SubBlock Name)
```

## Arguments

**Block Name**
: Name of block in which to search

**SubBlock Name**
: Name of subblock in which to read from

## Example

[The following assumes this file has already been opened ("<acar_shared>/powertrains.tbl/V12_engine_map.pwr")]

### Function
```
READ_T_O_START_SUBBLOCK_TABLE_READ("ENGINE", "XY_DATA")
```

### Result
```
{engine_speed <rpm>  torque@throttle <torque>}
```

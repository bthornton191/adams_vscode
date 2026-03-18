# READ_T_O_SUBBLOCK_INTEGER

Searches for an integer attribute contained in the specified subblock within the specified block. Returns the integer value of the selected attribute, or 0 if the attribute is not found or other errors occur.

## Format
```
READ_T_O_SUBBLOCK_INTEGER  (Block Name, SubBlock Name, Attribute)
```

## Arguments

**Block Name**
: Name of block in which to search

**SubBlock Name**
: Name of subblock within the specified block in which to search

**Attribute**
: Name of attribute within the specified subblock to retrieve the integer value.

## Example

[The following assumes this file has already been opened ("<acar_shared>/driver_controls.tbl/constant_radius_cornering.dcf").]

### Function
```
READ_T_O_SUBBLOCK_INTEGER("STEADY_STATE", "GEAR", "CONTROL_VALUE")
```

### Result
```
3
```

# READ_T_O_SUBBLOCK_STRING

Searches for a string attribute contained in the specified block and subblock. Returns the string value of the selected attribute, or a null string if the attribute is not found or other errors occur.

## Format
```
READ_T_O_SUBBLOCK_STRING (Block Name, SubBlock Name, Attribute)
```

## Arguments

**Block Name**
: Name of block in which to search

**SubBlock Name**
: Name of subblock within the specified block in which to search

**Attribute**
: Name of attribute within the specified subblock to retrieve the string value.

## Example

[The following assumes this file has already been opened ("<acar_shared>/driver_controls.tbl/constant_radius_cornering.dcf")]

### Function
```
READ_T_O_SUBBLOCK_STRING ("STEADY_STATE", "STEERING", "METHOD")
```

### Result
```
"MACHINE"
```

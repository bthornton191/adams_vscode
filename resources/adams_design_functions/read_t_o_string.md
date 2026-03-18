# READ_T_O_STRING

Searches a specified block within the currently open file for a string attribute. Returns the string value of the selected attribute, or a null string if the attribute is not found or other errors occur.

## Format
```
READ_T_O_STRING  (Block Name, Attribute)
```

## Arguments

**Block Name**
: Name of block in which to search

**Attribute**
: Name of attribute within the specified block to retrieve the string value.

## Example

[The following assumes this file has already been opened ("<acar_shared>/driver_controls.tbl/constant_radius_cornering.dcf").]

### Function
```
READ_T_O_STRING("EXPERIMENT", "STATIC_SETUP")
```

### Result
```
"STRAIGHT"
```

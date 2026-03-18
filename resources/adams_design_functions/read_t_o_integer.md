# READ_T_O_INTEGER

Searches a specified block within the currently open file for an integer attribute. Returns the integer value of the selected attribute, or 0 if the attribute is not found or other errors occur.

## Format
```
READ_T_O_INTEGER  (Block Name, Attribute)
```

## Arguments

**Block Name**
: Name of block in which to search

**Attribute**
: Name of attribute within the specified block to retrieve the integer value.

## Example

[The following assumes this file has already been opened ("<acar_shared>/driver_controls.tbl/constant_radius_cornering.dcf").]

### Function
```
READ_T_O_INTEGER("EXPERIMENT", "INITIAL_GEAR")
```

### Result
```
3
```

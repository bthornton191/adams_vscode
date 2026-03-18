# READ_T_O_REAL

Searches a specified block within the currently open TeimOrbit file for a real number attribute. Returns the real number value of the selected attribute, or 0 if the attribute is not found or other errors occur.

## Format
```
READ_T_O_REAL  (Block Name, Attribute)
```

## Arguments

**Block Name**
: Name of block in which to search

**Attribute**
: Name of attribute within the specified block to retrieve the real number value. Not case sensitive.

## Example

[The following assumes this file has already been opened ("<acar_shared>/driver_controls.tbl/constant_radius_cornering.dcf").]

### Function
```
READ_T_O_REAL("EXPERIMENT", "INITIAL_SPEED")
```

### Result
```
16.666
```

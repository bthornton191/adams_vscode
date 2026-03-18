# READ_T_O_REAL_ARRAY

Searches a specified block within the currently open TeimOrbit file for a number or array of numbers with the specified attribute label. Returns the real number(s) of the selected attribute, or 0.0 if the attribute is not found or other errors occur.

## Format
```
READ_T_O_REAL_ARRAY  (Block Name, Attribute)
```

## Arguments

**Block Name**
: Name of block in which to search

**Attribute**
: Name of attribute within the specified block to retrieve the value(s).

## Example

[The following assumes this file has already been opened ("<aride_shared>/general_bushing.tbl/gen_bus001.gbu")]

### Function
```
READ_T_O_REAL_ARRAY("BUSHING_PARAMETERS", "X_ALPHA")
```

### Result
```
0.57941891
```

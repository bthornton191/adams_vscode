# READ_T_O_SUBBLOCK_REAL_ARRAY

Searches a specified subblock within the currently selected block within the open TeimOrbit file for a number or array of numbers with the specified attribute label. Returns the real number(s) of the selected attribute, or 0.0 if the attribute is not found or other errors occur.

## Format
```
READ_T_O_SUBBLOCK_REAL_ARRAY (Block Name, SubBlock Name, Attribute)
```

## Arguments

**Block Name**
: Name of block in which the subblock resides

**SubBlock Name**
: Name of subblock in which to search

**Attribute**
: Name of attribute within the specified block to retrieve the value(s).

## Example

[Suppose there is a subblock "BUSHING_A" within the "BUSHING_PARAMETERS" block]

### Function
```
READ_T_O_SUBBLOCK_REAL_ARRAY("BUSHING_PARAMETERS", "BUSHING_1", "X_ALPHA")
```

### Result
```
0.57941891
```

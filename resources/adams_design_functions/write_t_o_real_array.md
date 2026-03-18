# WRITE_T_O_REAL_ARRAY

Writes an array of real numbers to the currently open file with the specified attribute label. Returns 1 on success and 0 if errors occur.

## Format
```
WRITE_T_O_REAL_ARRAY (Array, Attribute)
```

## Arguments

**Array**
: Array of real values

**Attribute**
: Name of attribute to assign array to.

## Example

### Function
```
WRITE_T_O_REAL_ARRAY ({1,2,3,4,5}, "NEW_ARRAY")
```

### Result
```
1
```

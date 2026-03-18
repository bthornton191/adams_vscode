# STR_SPRINTF

Returns a character string constructed by formatting the array of values in the format string.

## Format
```
STR_SPRINTF (Format String, {Array of Values})
```

## Arguments

**Format String**
: A C language format string.

**Array of Values**
: Array of values used to satisfy the format elements in the format string.

## Example

The following example illustrates the use of the STR_SPRINTF function:

### Function
```
STR_SPRINTF("The %s of %s is %03d%%.", {"value", "angle", 2})
```

### Result
```
The value of the angle is 002%
```

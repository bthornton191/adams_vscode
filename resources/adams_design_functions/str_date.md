# STR_DATE

Returns a string containing the current time and/or date information according to a format string.

## Format
```
STR_DATE (Format String)
```

## Arguments

**Note:**
: All of the formatting directives described below are supported on non-Windows platforms, but some are not supported on Windows. If the specified formatting directive is not supported, then the function will simply return the input string.

## Example

The following function returns the current date and time in the stated argument format (January 5, 1998, is the current date):

### Function
```
STR_DATE("%Y %m %d, %H:%M:%S")
```

### Result
```
1998 01 05, 19:55:48
```

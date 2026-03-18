# READ_T_O_CHECK_HEADER

Checks that the header in the currently open file has the specified type and version number. Returns 1 on success and 0 if errors occur.

## Format
```
READ_T_O_CHECK_HEADER (Type, Version)
```

## Arguments

**Type**
: String denoting the expected type of TeimOrbit file to be read. Not case sensitive.

**Version**
: Real number denoting the expected version in the TeimOrbit file.

## Example

The following examples illustrates the use of the READ_T_O_CHECK_HEADER function:

### Function
```
READ_T_O_CHECK_HEADER(‘spr’, 4)
```

### Result
```
1
```

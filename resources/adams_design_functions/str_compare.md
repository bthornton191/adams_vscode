# STR_COMPARE

Returns a numeric value indicating the relative alphabetical ordering of two strings. Returns 0 if the two strings are the same. Returns a positive number if the second string comes before the first. Returns a negative number if the second string comes after the first. The ASCII table is used for this, see examples below.

## Format
```
STR_COMPARE (String 1, String 2)
```

## Arguments

**String 1**
: Text string.

**String 2**
: Text string.

## Example

The following function shows that the two strings are identical. Note that the string is not case senstive.

### Function
```
STR_COMPARE("adjective","adjective") orSTR_COMPARE("ADJECTIVE","adjective")orSTR_COMPARE("AdjEctIVe","adjective")
```

### Result
```
0
```

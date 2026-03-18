# STR_XLATE

Returns a new string formed by replacing all occurrences of one or more characters found within the input string, with an equal number of characters.

## Format
```
STR_XLATE(Input String, From String, To String)
```

## Arguments

**Input String**
: Text string.

**From String**
: Text string; must have the same number of characters as the To String.

**To String**
: Text string; must have the same number of characters as the From String.

## Example

The following example illustrates the use of the STR_XLATE function:

### Function
```
STR_XLATE ("Why/-are/-you/-here/-?", "/-", ">_")
```

### Result
```
Why>_are>_you>_here>_?
```

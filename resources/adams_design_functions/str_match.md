# STR_MATCH

Returns 1 (true) if a specified string is found within another string; otherwise, returns 0 (false).

## Format
```
STR_MATCH (Pattern String, Input String)
```

## Arguments

**Pattern String**
: Text string. The argument uses wildcards to define the pattern to match.STR_MATCH uses four wildcard matching sequences:

**This wildcard:**
: Matches:

*****
: an arbitrary sequence of characters

**?**
: one character

**[char]**
: any of the characters within the brackets

**{string1,string2}**
: any of the characters strings within the braces

**Input String**
: Text string.

## Example

The following functions return 1 or 0, depending on whether a match occurred or not:

### Function
```
STR_MATCH("f?d","fad")
```

### Result
```
1
```

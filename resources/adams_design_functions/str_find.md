# STR_FIND
Returns the starting location of the first occurrence of a string within another string. If there is no match, it returns a 0.
## Format
```adams_cmd
STR_FIND (Base String, Search String)
```
## Arguments
 
**Base String**
: Text string.

**Search String**
: Text string.

## Examples
The following examples illustrate the use of the STR_FIND function:
 
### Function
```adams_cmd
STR_FIND ("Hello", "l")
```

### Result
```adams_cmd
3
```
 
### Function
```adams_cmd
STR_FIND ("Hello", "o")
```

### Result
```adams_cmd
5
```
The following function uses a second character in its search criteria to return 4, because letter "l" appears twice in the word hello:
 
### Function
```adams_cmd
STR_FIND ("Hello", "lo")
```

### Result
```adams_cmd
4
```

## STR_FIND_COUNT
Returns the number of occurrences of a string found within another string. Overlapping matches are not included.
## Format
```adams_cmd
STR_FIND_COUNT (Base String, Search String)
```
 
## Arguments
**Base String**
: Text string.

**Search String**
: Text string.

## Examples
The following examples illustrate the use of the `STR_FIND_COUNT` function:
 
### Function
```adams_cmd
STR_FIND_COUNT("hammer stammer", "mm")
```
### Result
```adams_cmd
2
```
 
### Function
```adams_cmd
STR_FIND_COUNT("hellllo jello", "ll")
```
### Result
```adams_cmd
3
```
The following function returns 2 because the overlapping, matching 9's from 239990 to 129990 are not included:
 
### Function
```adams_cmd
STR_FIND_COUNT("239990 129990", "99")
```
### Result
```adams_cmd
2
```

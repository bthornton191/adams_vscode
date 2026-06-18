## STR_MERGE_STRINGS
Returns a string constructed by joining an array of strings by a delimiter you specify
## Format
```adams_cmd
STR_MERGE_STRINGS (Delimiter, Strings)
```
 
## Arguments
**Delimiter**
: Text string.

**Strings**
: Array of Text string.

## Example
The following function returns string constructed by joining an array of strings by spaces
 
### Function
```adams_cmd
str_merge_strings(" ", {"how", "now", "brown", "cow"})
```
### Result
```adams_cmd
"how now brown cow"
```
 
# STR_FIND_IN_STRINGS
Searches for a string in an array of strings. Returns the index into the array if the string is found, zero if not found.
## Format
```adams_cmd
STR_FIND_IN_STRINGS(array_of_strings, string)
```

## Arguments
 
**array_of_strings**
: The array of strings to search.

**string**
: The string to search for.

## Example
```adams_cmd
if cond=(STR_FIND_IN_STRINGS(unit_names, "force"))
```

# STR_SPLIT
Returns an array of strings built from substrings, which are separated from each other with a 
specified character, and are located within another string. 

## Format
```
STR_SPLIT (Input Text String, Separator Character)
```

## Arguments
 
**Input Text String**
: Text string. This string is unaltered during the evaluation of the function. 
 
**Separator Character**
: Specified character that separates the substrings. 

## Examples
In the following functions, the second example string looks similar to the first one. It is 
different, however, because the separator character has been changed to a # symbol so that a 
semi-colon could be included with the first returned string (apple;). If a character needs to be 
included in the output, it cannot be used as a separator character.

In all cases, `STR_SPLIT` trims any leading or trailing white spaces on the substrings:
 
### Function
```julia
STR_SPLIT(" apple; orange; grape ", ";") 
```

### Result
```julia
apple, orange, grape 
```

### Function
```julia
STR_SPLIT(" apple; # orange# grape ", "#")
```

### Result
```julia
apple;, orange, grape 
```

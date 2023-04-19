# STR_PRINT
Writes a string into the **aview.log** file. It is very useful for debugging.

## Format
```
STR_PRINT (Input String)
```

## Arguments
 
**Input String**
: Text String

## Examples
In the following functions, the double slash marks (`//`) allow two or more strings to be concatenated into a single string:
 
### Function
```julia
STR_PRINT("My variable is " // DV1)
```

### Result
writes `"My variable is 45"` into **aview.log** (DV1 is equal to 45)

### Function
```julia
STR_PRINT("My variable is " // eval(STR_MATCH ("f*d", "fed")))
```

### Result
writes `"My variable is 1"` into **aview.log** because a match occurred

### Function
```julia
STR_PRINT("My variable is " // eval(STR_MATCH ("f*d", "fet")))
```

### Result
writes `"My variable is 0"` into **aview.log** because a match did not occur

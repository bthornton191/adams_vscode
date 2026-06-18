# UNIQUE_ID

Returns an Adams_ID unique for objects of the specified type.


## Format 
```adams_cmd
UNIQUE_ID(char * type) 
```
## Arguments

**type**
: Text string representing an entity type.

## Example
```adams_cmd
var cre var=dv1 int=(eval(UNIQUE_ID("marker")))
```


 

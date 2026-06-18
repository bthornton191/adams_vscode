# DB_REFERENTS

Returns an array of objects of a given type that are referenced by the object you specified.

## Format
```adams_cmd
DB_REFERENTS (Object Name, Object Type)
```
## Arguments

 



**Object Name**
: Name of a database object. 


**Object Type**
: Character string (see `DB_TYPE`). 


## Example

The following example stores the array of objects that refer to **rev1**, in the variable **db06**:
```adams_cmd
var set var = db06 &
    obj = (EVAL(DB_REFERENTS(rev1, "all")))
```

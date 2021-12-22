# DB_TYPE_FIELDS

Returns an array of strings for the names of the fields (excluding aliases) for the object type you specified.

## Format
```java
DB_TYPE_FIELDS (Objects Type String)
```
## Argument

 



**Object Type String**
: Character string denoting an object type (see `DB_TYPE`). 


## Example

The following commands return all the field names for marker:

```java
var set &
    var = db13 &
    str=(EVAL(DB_TYPE_FIELDS("marker")))
```
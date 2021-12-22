# DB_FULL_TYPE_FIELDS

Returns an array of strings for the names of the fields (including aliases) for the object you specified.

## Format
```java
DB_FULL_TYPE_FIELDS (Objects Type String)
```
## Argument

 



**Objects Type String**
: Character string denoting an object type (see `DB_TYPE`). 


## Example

The following commands find all the field names on a marker:

```java
var set var=db10 &
    str=(EVAL(DB_FULL_TYPE_FIELDS("marker")))
```
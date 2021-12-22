# DB_OBJECT_COUNT

Returns the number of object names in the array of database objects you specified.

## Format
```
DB_OBJECT_COUNT (Objects)
```
## Argument

 



**Objects**
: Names of database objects. 


## Example

The following example stores the number of objects on the select_list in the variable **n_selected_objects**:
```java
var set var=n_selected_objects &
    int=(EVAL(DB_OBJECT_COUNT(select_list.objects)))
```
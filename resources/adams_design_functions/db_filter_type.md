# DB_FILTER_TYPE

Returns an array of objects whose types match the filter parameters you specified.

## Format
```java
DB_FILTER_TYPE (Objects to Filter, Filter Type String)
```
## Arguments

 



**Objects to Filter**
: Array of database objects. 


**Filter Type String**
: Character string (see `DB_TYPE`). 


## Example

The following example returns information about markers in the select list:

```java
list_info entity &
    entity = (EVAL(DB_FILTER_TYPE( select_list.objects, "marker")))
```
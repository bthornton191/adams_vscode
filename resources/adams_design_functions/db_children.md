# DB_CHILDREN

Returns an array of objects of a given type, that are children of the object you specified.

## Format

DB_CHILDREN (Object Name, Object Type)

## Arguments

 



**Object Name**
: Name of a database object. 


**Object Type**
: Character string (see `DB_TYPE`). 


## Example

The following function provides information on a marker in the default model:

```java
list entity &
    entity=(EVAL(SELECT_TEXT(DB_CHILDREN(DB_DEFAULT(.system.defaults, "model"), "marker))))
```
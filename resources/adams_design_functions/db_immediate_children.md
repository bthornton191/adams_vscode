# DB_IMMEDIATE_CHILDREN

Returns an array of all objects that are immediate children of the object you specified.

## Format
```java
DB_IMMEDIATE_CHILDREN (Object Name, Object Type)
```
## Arguments

 



**Object Name**
: Name of a database object. 


**Object Type**
: Character string (see `DB_TYPE`). 

## Examples

The following commands display all the names of the modeling objects in model_1:

```java
list names & 
    entity = (EVAL(DB_IMMEDIATE_CHILDREN(.model_1, "adams"))) &
    file = "2u104_01.out"
```
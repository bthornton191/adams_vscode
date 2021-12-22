# DB_TWO_WAY

Returns an array of objects that have two-way associativity with the object you specified. Two-way associativity involves a two-way relationship, such as between a model and a view displaying that model, where one or the other may be deleted and the remaining one will not be affected.

## Format
```java
DB_TWO_WAY (Object Name, Object Type)
```
## Arguments

 



**Object Name**
: Name of a database object. 


**Object Type**
: Character string (see `DB_TYPE`). 


## Example

The following commands store the array of objects that have two-way associativity to **.mod1** in variable **db07**:
```java
var set &
    var=db07 &
    obj=(EVAL(DB_TWO_WAY(.mod1, "all")))
```
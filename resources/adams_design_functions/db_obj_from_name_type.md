# DB_OBJ_FROM_NAME_TYPE

Returns the object of a given name and type. 

## Format
```java
DB_OBJ_FROM_NAME_TYPE (Parent Object, String Name, String Object Type)
```
## Arguments

 



**Object**
: Parent object under which to search. 


**Name**
: Name of Object to be search 


**Object Class**
: Character string (see `DB_TYPE`). 


## Example

The following function will return **Link_1** object:

```java
DB_OBJ_FROM_NAME_TYPE(.MODEL_1.PART_2 , "LINK_1" , "geometry")
```
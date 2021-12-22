# DB_OBJ_EXISTS_EXHAUSTIVE

Returns a Boolean value indicating whether the object specified exists or not. It does an exhaustive search through the specified object context to find anything with a given name. 

## Format 
```java
DB_OBJ_EXISTS_EXHAUSTIVE (ContextObject, Name) 
```
## Arguments 

 



**ContextObject**
: The object in which to search for a child with the given name. 


**Name**
: A character string naming the object. 


## Examples 

You might branch your command file based upon the existence of a particular object:
```java
if condition=(db_obj_exists_exhaustive(.model_1, "marker_1")) 
```
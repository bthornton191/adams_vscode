# DB_ANCESTOR

Returns the first ancestor of an object of the type you specify. This ancestor might be the direct parent of the given object, its grandparent, or some more distant object. 

If the given child has no ancestor of the specified type, then the function returns NONE. 

## Format 
```java
DB_ANCESTOR (Child,Type) 
```
## Argument 

 



**Child**
: The object whose ancestor is to be found. 


**Type**
: A character string specifying the object type of the returned value. 


## Example 

The following is an illustration of how the `DB_ANCESTOR` function is used:

 



## Function  
```java
DB_ANCESTOR (.model_1.part_1.marker_1, "model" )  
```

## Result  
```java
.model_1  
```
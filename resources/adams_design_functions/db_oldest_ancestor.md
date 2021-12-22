# DB_OLDEST_ANCESTOR

Returns the most distant ancestor of an object of the type specified. This ancestor might be the direct parent of the given object, its grandparent, or some more distant object. This can be helpful to find the top-level model when submodels are present. 

If the given child has no ancestor of the specified type, then the function returns NONE. 

## Format 
```java
DB_OLDEST_ANCESTOR (Child,Type) 
```
## Argument 

 



**Child**
: The object whose ancestor is to be found. 


**Type**
: A character string specifying the object type of the returned value.  


## Example 

The following example illustrates the use of the `DB_OLDEST_ANCESTOR` function:

 



### Function  
```java
DB_OLDEST_ANCESTOR (.model_1.part_1.marker_1,"model" )  
```

### Result  
```java
.model_1  
```
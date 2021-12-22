# DB_OBJ_EXISTS

Returns a logical value indicating whether the specified object exists as an immediate child of the parent object. 

## Format 
```java
DB_OBJ_EXISTS (Parent, Name) 
```
## Arguments 

 



**Parent**
: The object defining the search domain. 


**Name**
: A character string naming the object for which you are searching.  


## Examples 

The following illustrates the use of `DB_OBJ_EXISTS`:

 



### Function  
```java
DB_OBJ_EXISTS(.model_1.par1, "mar1")  
```

### Result  
Assuming **mar1** does **NOT** exist
```java
0
```

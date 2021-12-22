# DB_SHORT_NAME

Returns the shortest unique name for the given object. This name may become non-unique when new objects are created, so it is best not to use this value to generate names for files that will be present for a long time.

## Format 
```java
DB_SHORT_NAME (object) 
```
## Arguments 

 



**object**
: Any Adams View object.  


## Examples 

Assuming you have two markers with the same name on two different parts.

### Function
```java
DB_SHORT_NAME(.model_1.par1.mar1)
```
### Result
```java
par1.mar1
```
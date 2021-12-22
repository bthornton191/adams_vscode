# DB_FULL_NAME_FROM_SHORT

Returns the full name for the named object of the specified type. The input name can be either a full name or a minimum unique name. 

## Format 
```java
DB_FULL_NAME_FROM SHORT (short_name, type) 
```
## Arguments 

 



**short_name**
: Short name of the object. 


**type**
: String for the object’s type or class. 


## Examples 

If you have two objects named joint1 (one in the model and one in an analysis) and call the function as follows: 
```java
DB_FULL_NAME_FROM_SHORT("joint1", "constraint")
```
you should see: 
```java
.model_1.joint1
```
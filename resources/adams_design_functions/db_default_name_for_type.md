# DB_DEFAULT_NAME_FOR_TYPE

Returns the name for the given object based on the state of the default for formatting names. The name will be unique only for objects of the specified type. 

## Format
```java
DB_DEFAULT_NAME_FOR_TYPE (object, type) 
```
## Arguments 

 



**object**
: Any Adams View object. 


**type**
: String for the object's type or class. 


## Examples 

If you have two objects named **joint1** (one in the model and one in an analysis) and call the function as follows: 
```java
DB_DEFAULT_NAME_FOR_TYPE(.model_1.joint1, "constraint")
```
you should see the following when the default is set to minimum unique names or Adams IDs: 
```java
joint1
```
and the following when the default is set to full names: 
```java
.model_1.joint1
```
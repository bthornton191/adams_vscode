# DB_OF_CLASS

Returns a 1 if an object is a member of a given class; returns a 0 if it is not. The class_name is one of the values the `SELECT_TYPE` function presents, and can be either a type name or a class name.

## Format
```java
DB_OF_CLASS (Object Name, Object Class)
```
## Arguments

 



**Object Name**
: Name of a database object. 


**Object Class**
: Character string (see `DB_TYPE`). 


## Example

The following example changes the color of the object represented by the variable **myobject**, if the variable is a marker:

```java
if cond=(DB_OF_CLASS(myobject,"marker"))
    marker attribute marker=(myobject) color=red
end  
```
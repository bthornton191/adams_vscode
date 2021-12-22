# DB_DEL_UNPARAM_DEPENDENTS

Returns a constant integer value of zero, and deletes all the parametric expressions that depend on the object you specified. 

## Format 
```java
DB_DEL_UNPARAM_DEPENDENTS (Object Name) 
```
## Argument 

 



**Object Name**
: Name of a database object. 


## Example 

The following commands delete all parametric dependencies on par3: 

```java
var set &
    var = db17 &
    int = (EVAL(DB_DEL_UNPARAM_DEPENDENTS(par3)))
```
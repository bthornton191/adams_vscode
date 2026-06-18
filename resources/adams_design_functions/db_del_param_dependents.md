# DB_DEL_PARAM_DEPENDENTS

Returns an array of all the parametric expressions that depend on the object you specified. 

## Format 
```adams_cmd
DB_DEL_PARAM_DEPENDENTS (Object Name) 
```
## Argument 

 



**Object Name**
: Name of a database object. 


## Example 

The following sequence of commands finds objects with parametric dependencies on **par3**: 

```adams_cmd
var set &
    var = db16 &
    obj = (eval(DB_DEL_PARAM_DEPENDENTS(par3)))
```

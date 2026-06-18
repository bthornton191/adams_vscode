# DB_DEFAULT_NAME

Returns the name for the given object based on the state of the default for formatting names. The name will be either a full name or a minimum unique name. 

## Format 
```adams_cmd
DB_DEFAULT_NAME (object) 
```
## Arguments 

 



**object**
: Any Adams View object. 


## Examples 

If you have two markers (one on par1 and one on ground) and call the function as follows: 
```adams_cmd
DB_DEFAULT_NAME(.model_1.par1.mar1)
```
you should see the following when the default is set to minimum unique names or Adams IDs: 
```adams_cmd
par1.mar1 
```
and the following when the default is set to full names: 
```adams_cmd
.model_1.par1.mar1
```

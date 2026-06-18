# CHDIR

Returns a 1 if `CHDIR` succeeded in changing to the directory you specified, or a 0 if it failed. 

## Format 
```adams_cmd
CHDIR (String) 
```
## Argument 

 



**String**
: Text string that specifies a directory.  


## Example 

The result of the following function indicates the change to the /tmp directory:

 



### Function  
```adams_cmd
CHDIR("/tmp")  
```

### Result  
```adams_cmd
1  
```

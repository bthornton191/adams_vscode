# ANYM

Returns the logical sum of the elements of a matrix. If any value is nonzero, the result is nonzero. 

## Format 
```adams_cmd
ANYM (M) 
```
## Argument 

 



**M**
: A matrix of arbitrary shape. 


## Examples 

The following examples illustrate the use of the ANYM function:

 



### Function  
```adams_cmd
ANYM({8, 0, 1})  
```

### Result  
```adams_cmd
1  
```

 



### Function  
```adams_cmd
ANYM({0, 0, 0})  
```

### Result  
```adams_cmd
0  
```

 



### Function  
```adams_cmd
ANYM({[4, 0], [0, 0]})  
```

### Result  
```adams_cmd
1  
```

# ALLM

Returns the logical product of the elements of a matrix. If all values are nonzero, then the result is nonzero. 

## Format 
```adams_cmd
ALLM (M) 
```
## Argument

 



**M**
: A matrix of arbitrary shape.  


## Examples 

The following examples illustrate the use of the ALLM function:

 



### Function  
```adams_cmd
ALLM({1, 0, 1})  
```

### Result  
```adams_cmd
0  
```

 



### Function  
```adams_cmd
ALLM({1, 2, 3})  
```

### Result  
```adams_cmd
1  
```


 



### Function  
```adams_cmd
ALLM({[1, 1], [1, 0]})  
```

### Result  
```adams_cmd
0  
```

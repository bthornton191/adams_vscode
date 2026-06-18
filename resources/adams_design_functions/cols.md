# COLS

Returns the number of columns in a given matrix. 

## Format 
```adams_cmd
COLS (M) 
```
## Argument 

 



**M**
: A given matrix. 


## Examples 

The following examples illustrate the use of the COLS function:

 



### Function  
```adams_cmd
COLS({1, 2, 3})  
```

### Result  
```adams_cmd
1  
```

 



### Function  
```adams_cmd
COLS({[1, 2, 3]})  
```

### Result  
```adams_cmd
3  
```

 



### Function  
```adams_cmd
COLS(marker_1.location)  
```

### Result  
```adams_cmd
1  
```

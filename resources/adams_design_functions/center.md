# CENTER

Returns a non-statistical mean of the values in an array. 

## Format 
```adams_cmd
CENTER (A) 
```
## Argument 

 



**A**
: Array of arbitrary shape.  


## Equation 

Mathematically, `CENTER` is calculated as follows: 
```adams_cmd
CENTER(A) = (min(A) + max(A))/2
```


## Example 

The following example illustrates the use of the `CENTER` function:

 



### Function  
```adams_cmd
CENTER ({1, 0, 4, 3})  
```

### Result  
```adams_cmd
2.5  
```

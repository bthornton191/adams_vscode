# AINT

Returns the nearest integer whose magnitude is not larger than the integer value of a specified expression that represents a numerical value. 

`AINT(x)` evaluates to different values under different conditions: 

* AINT(x) = 0 if ABS(x)< 1

* AINT(x) = int(x) if ABS(x)1

The value of the mathematical function AINT of a variable x is equal to x if x is an integer. If x is not an integer, then `AINT(x)` is equal to the integer nearest to x, whose magnitude is not greater than the magnitude of x. 

## Format 
```adams_cmd
AINT(x) 
```
## Argument 

 



**x**
: Any valid expression that evaluates to a real number.  


## Examples 

The following examples illustrate the use of the AINT function:

 



### Function  
```adams_cmd
AINT(-6.5)  
```

### Result  
```adams_cmd
-6  
```

 



### Function  
```adams_cmd
AINT(4.6)  
```

### Result  
```adams_cmd
4  
```

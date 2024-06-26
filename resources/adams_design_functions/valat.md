# VALAT

Returns a value from the Y_array at the same position as X_value was 
found in the X_array. X_array and Y_array must be the same length.  


## Format 
```java
VALAT(X_array, Y_array, X_value)
```
## Arguments

**X_array**
: An array of at least two real values that determine the range of 
the curve. Values must be in ascending order.


**Y_array**
: An array containing the same number of real values as the X_array. 
Used to define the domain of the curve.

**value**
: A value which "indexes" into the X_array.



## Examples 




### Function  
```java
model create model=mod1
variable create variable=x_array  rea=-1,0,2,3
variable create variable=y_array  rea= 1,2,3,4
variable create variable=xx  rea=0.0
variable create variable=yy  rea=(VALAT(x_array, y_array, xx))
```

### Result  
**xx**
: `-2, -1, 0, 1, 2, 3, 4`
**yy**
: `0, 1, 2, 2.5, 3, 4, 5`
 

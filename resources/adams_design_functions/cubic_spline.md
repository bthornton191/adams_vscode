# CUBIC_SPLINE

Creates an interpolated curve from input points with a specified number of values. Interpolates using a third order Lagrangian polynomial. 

The length of the Independent Data array must be equal to the Dependent Data array. 

Reference: *Digital Computation and Numerical Methods. Southworth, 1965. Chapter 8.7*

## Format 
```java
CUBIC_SPLINE (Independent Data, Dependent Data, Number of Output Values) 
```
## Arguments 

 



**Independent Data**
: A 1xN array of x values for the curve to be interpolated. The x values must be in ascending order, and the length of the array must be greater than or equal to 4. 


**Dependent Data**
: A 1xN array of y values for the curve to be interpolated. 


**Number of Output Values**
: The number of values to be generated in the output array. 


## Example 

The following function interpolates a set of four points with ordinal values from 1 to 4 and abscissal values as shown, into a series of 10 abscissal values:

 



### Function  
```java
CUBIC_SPLINE({1, 2, 3, 4}, {0, 2, 1, 3}, 10)  
```

### Result  
```java
{0.0, 1.0, 1.667, 2.0, 2.0, 1.667, 1.0, 1.333, 2.0, 3.0}  
```

To compute the ordinal values for these splined values, you can use the `SERIES2` function as follows:

 



### Function  
```java
SERIES2(1, 4, 10)  
```

### Result  
```java
{1.0, 1.333, 1.667, 2.0, 2.333, 2.667, 3.0, 3.333, 3.667, 4.0}  
```

 



>Note:   
>This design function do not exactly represent Solver `CUBSPL`. The interpolation follows CUBIC method (more closely matching with `CSPLINE` than this function) but extrapolation follows 'linear' of 'cubic' based on type of spline specified (based on option extrapolate_linear=yes/no). 

# CSPLINE

Creates an interpolated curve from input points with a specified number of values. Interpolates using the cubic splines. 

The algorithm that fits the cubic spline is from *Computer Methods for Mathematical Computations by Forsythe, Malcolm and Moler (1977, Prentice-Hall: Englewood Cliffs, NJ)*. The `INTEGR` function uses the same algorithm. 

The length of the Independent Data array must be equal to the Dependent Data array. 

## Format 
```java
CSPLINE (Independent Data, Dependent Data, Number of Output Values) 
```
## Arguments 

 



**Independent Data**
: A 1xN array of x values for the curve to be interpolated. These x values must be in ascending order, and the length of the array must be greater than or equal to 4. 


**Dependent Data**
: A 1xN array of y values for the curve to be interpolated. 


**Number of Output Values**
: The number of values to be generated in the output array. 


## Example 

The following function interpolates a set of four points with ordinal values from 1 to 4 and abscissal values as shown, into a series of 10 abscissal values:

 



### Function 
```java
CSPLINE({1, 2, 3, 4}, {0, 2, 1, 3}, 10)  
```

### Result 
```java
{0.0, 0.936, 1.704, 2.0, 1.741, 1.259, 1.0, 1.296, 2.037, 3.0} 
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

 



> **Note**:    
> This design function do not exactly represent Solver `CUBSPL`. The interpolation follows CUBIC method (closely matches) but extrapolation follows 'linear' of 'cubic' based on type of spline specified (based on option extrapolate_linear=yes/no). 

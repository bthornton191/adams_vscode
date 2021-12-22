# AKIMA_SPLINE2

Returns an Akima-spline fit of the dependent values. It clips the output data to start at the maximum start point of the two independent value arrays and ending at the minimum end point of the two independent value arrays.

When the FLAG is 1, `AKIMA_SPLINE2` uses the first set of independent values to determine the step size. When FLAG is 0, it uses the second set of independent values.

## Format
```java
AKIMA_SPLINE2 (Independent Data, Dependent Data, Independent Data2, FLAG)
```
## Arguments

 



**Independent Data**
: A 1xN array of x values for curve1 to be interpolated. The x values must be in ascending order, and the length of the array must be greater than or equal to 4. 


**Dependent Data**
: A 1xN array of y values for curve1 to be interpolated. 


**Independent Data2**
: A 1xN array of x values for curve2 to be interpolated. The x values must be in ascending order, and the length of the array must be greater than or equal to 4. 


**FLAG**
: Integer indicating whether the first or second set of independent values were used to determine the output step size. 

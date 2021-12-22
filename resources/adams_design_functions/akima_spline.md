# AKIMA_SPLINE

Creates an interpolated curve from input points with a specified number of values. Interpolates using the Akima method. 

The algorithm that fits the akima spline is from the Journal of the Association of Computing Machinery (Vol. 17, No. 4, October 1970). 

The length of the Independent Data array must be the same as the Dependent Data array. 

## Format 
```java
AKIMA SPLINE (Independent Data, Dependent Data, Number of Output Values) 
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
AKIMA_SPLINE({1, 2, 3, 4}, {0, 2, 1, 3}, 10)  
```

### Result  
```java
{0.0, 1.0, 1.667, 2.0, 1.778, 1.222, 1.0, 1.333, 2.0, 3.0}  
```

To compute the ordinal values for these splined values, you can use the `SERIES2` function as follows:

 



## Function  
```java
SERIES2(1, 4, 10)  
```

## Result  
```java
{1.0, 1.333, 1.667, 2.0, 2.333, 2.667, 3.0, 3.333, 3.667,  
```
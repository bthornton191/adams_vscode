# ALIGN

Shifts values in an array to start at a particular value (often used to shift a curve so that the value at its starting point is 0--aligning along the curve to 0). 

## Format 
```java
ALIGN (real array, real number) 
```
## Argument 

 



**real array** 
: Array of values to align (shift). 


**real number** 
: First value from aligned array. 


## Examples 

The following example shifts curve_1 to start at the same value as curve_2. 
```java
ALIGN (.plot_1.curve_1, .plot_1.curve_2.Y_data[1])
```
The following example shifts curve_1 to start at 0. 
```java
ALIGN (.plot_1.curve_1, 0)
```
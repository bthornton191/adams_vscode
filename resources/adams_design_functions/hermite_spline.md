# HERMITE_SPLINE

Creates an interpolated curve from input points with a specified number of values. Interpolates using the Hermite cubic spline.

## Format
```
HERMITE_SPLINE (Independent Data, Dependent Data, Number of Output Values)
```

## Arguments

**Independent Data**
: A 1xN array of x values for the curve to be interpolated. The x values of the points must be in ascending order, and the length of the array must be greater than or equal to 4.

**Dependent Data**
: A 1xN array of y values for the curve to be interpolated.

**Number of Output Values**
: The number of values to be generated in the output array.

## Example

The following function interpolates a set of four points with ordinal values from 1 to 4 and abscissal values as shown, into a series of 10 abscissal values.

### Function
```
HERMITE_SPLINE({1, 2, 3, 4}, {0, 2, 1, 3}, 10)
```

### Result
```
{0.0, 1.037, 1.741, 2.0, 1.741, 1.259, 1.0, 1.259, 1.963, 3.0}
```

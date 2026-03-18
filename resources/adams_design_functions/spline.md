# SPLINE

Creates an interpolated curve from the input points with the number of points you specified. Interpolates using the spline algorithm you specified.

## Format
```
SPLINE (Points, Spline Type, Number of Output Points)
```

## Arguments

**Points**
: A 2xN array of points to be interpolated. The x values of the points must be in ascending order, and the length of the array must be greater than or equal to 4.

**Spline Type**
: The spline algorithm to use for interpolation. It must be one of the following character strings: ■AKIMA = interpolates using the Akima method. ■CSPLINE = interpolates using the cubic splines. ■CUBIC = interpolates using a third-order Lagrangian polynomial. ■LINEAR = interpolates using linear interpolation. ■NOTAKNOT = interpolates using Not-a-knot cubic spline. ■HERMITE = interpolates using Hermite cubic spline.

**Number of Output Points**
: Number of values to be generated in the output array.

## Example

The following function interpolates a set of four points with ordinal values from 1 to 4 and abscissal values as shown, into a series of 10 points using the cubic spline interpolation method.

### Function
```
SPLINE({[1, 2, 3, 4], [0, 2, 1, 3]}, "CSPLINE", 10)
```

### Result
```
{[1.0, 1.333, 1.667, 2.0, 2.333, 2.667, 3.0, 3.333, 3.667, 4.0], [0.0, 0.963, 1.704, 2.0, 1.741, 1.259, 1.0, 1.296, 2.037, 3.0]}
```

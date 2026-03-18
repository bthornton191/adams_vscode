# INTERP1

Similar to the MATLAB INTERP1 function and returns a real array. Given a curve described by x and y, the INTERP1 function returns the Yi values corresponding to the Xi values.

## Format
```
INTERP1 (x, y, Xi, method)
```

## Arguments

**x**
: The x values of the input curve.

**y**
: The y values of the input curve.

**Xi**
: The x values at which to evaluate the spline.

**method**
: A character string that indicates the interpolation method to be used. These come directly from the MATLAB function with the same name: nearest - Nearest neighbor interpolation.linear - Linear interpolation.spline - Cubic spline interpolationpchip - Piecewise cubic Hermite interpolation.cubic - Same as pchip.Note:	Not all method options of the MATLAB function with same name are supported by this function.

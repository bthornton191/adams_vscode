# INTERP2

Calls the MATLAB INTERP2 function and returns a real array. Given a 3D surface described by x, y, and z, the INTERP2 function returns the Zi values corresponding to the Xi and Yi points.

## Format
```
INTERP2 (x, y, z, Xi, Yi method)
```

## Arguments

**x**
: The x values of the input surface.

**y**
: The y values of the input surface.

**z**
: The z values of the input surface.

**Xi**
: Evaluates the splined curves at the x coordinates.

**Yi**
: Evaluates the splined curves at the y coordinates.Xi and Yi may be of different size, as they describe a grid rather than a collection of ordered pairs, though the number of Xi's must be greater than or equal to the number of Yi's.

**method**
: A character string that indicates the interpolation method to be used. These come directly from the MATLAB function of the same name:nearest - Nearest neighbor interpolation.linear - Bilinear interpolation.spline - Cubic spline interpolation.cubic - Bicubic interpolation.

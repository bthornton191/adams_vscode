# DIFF

Returns a 1xN array of approximations to the derivatives at the points in the input data. To compute the derivative, the DIFF function fits a cubic spline to the input data and returns the derivatives of the approximating polynomials at each point.

## Format
```
DIFF (INDEP, DEPEND)
```

## Arguments

**INDEP**
: A 1xN array of independent data. These x values must be in ascending order, and the length of the array must be greater than or equal to 4.

**DEPEND**
: A 1xN array of dependent data on input independent data.

## Example

The following example illustrates the use of the DIFF function:

### Function
```
DIFF(SERIES(0,1,5), {0,1,4,9,16})
```

### Result
```
0, 2.0, 4.0, 6.0, 8.0
```

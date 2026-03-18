# INTEGR

Produces the integral at each input point on curve C. The curve is presented to this function as two arrays containing the ordinal and abscissal components of the curve. To compute the integral at each point, INTEGR fits a cubic spline to the curve and returns the integrals of the approximating polynomials at each point. The curve of integrals that INTEGR returns has the same number of values as each of the arguments.

## Format
```
INTEGR (Independent Points, Dependent Points)
```

## Arguments

**Independent Points**
: The X or ordinal values of the curve to be integrated.

**Dependent Points**
: The Y or abscissal values of the curve to be integrated.

## Example

The following example illustrates the use of the INTEGR function:

### Function
```
INTEGR(SERIES(0,1,5), {0,1,4,9,16})
```

### Result
```
0.0, 0.333, 2.667, 9.0, 21.333
```

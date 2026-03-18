# DIFFERENTIATE

Returns the derivative at each input point on curve C. To compute the derivative at each point, the DIFFERENTIATE function fits a cubic spline to a 2xN matrix representation of curve C and returns the derivatives of the approximating polynomials at each point. The curve of derivatives that DIFFERENTIATE returns has the same x values as curve C.

## Format
```
DIFFERENTIATE (C)
```

## Arguments

**C**
: Input curve.

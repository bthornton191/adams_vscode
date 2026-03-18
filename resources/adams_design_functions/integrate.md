# INTEGRATE

Produces a curve of integrals from an input curve. To compute the integral at each point, the INTEGRATE function fits a cubic spline to the 2xN matrix representation of curve C, and returns the integrals of the approximating polynomials at each point. The curve of integrals that INTEGRATE returns has the same X values as curve C.

## Format
```
INTEGRATE (C)
```

## Arguments

**C**
: Input curve.

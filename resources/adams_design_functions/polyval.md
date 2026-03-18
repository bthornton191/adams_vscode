# POLYVAL

Calls the MATLAB POLYVAL function and returns a real array. The POLYVAL function returns the y values on the polynomial curve if given p, containing the polynomial coefficients, and an array of x values. Note that the list of coefficients, p, is the reverse of that the MATLAB function requires. This function complements the POLYFIT function, and POLYVAL uses the output coefficients from it directly.

## Format
```
POLYVAL (p, x)
```

## Arguments

**p**
: The array of coefficients for the polynomial, constructing a polynomial:f(x) = p0 + p1*x + p2*x2 + ... + pn*xn

**x**
: The array of x values at which to evaluate the polynomial.

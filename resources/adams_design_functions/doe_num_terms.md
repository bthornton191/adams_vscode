# DOE_NUM_TERMS

Returns the number of terms in the polynomial that the OPTIMIZE_FIT_RESPONSE_SURFACE command produces. The OPTIMIZE_FIT_RESPONSE _SURFACE command takes a parameter to specify the degree for each variable in the solution, and produces a polynomial, accordingly. The input to DOE_NUM_TERMS is an array of these same integers that you supply to the OPTIMIZE_FIT_RESPONSE_SURFACE command in it POLYNOMIAL_DEGREES parameter.

## Format
```
DOE_NUM_TERMS(ORDER_ARRAY)
```

## Arguments

**ORDER_ARRAY**
: An array of integers giving the degree of each variable in the polynomial.

## Example

The following examples illustrate the use of the DOE_NUM_TERMS function:

### Function
```
DOE_NUM_TERMS({1,1,1})
```

### Result
```
Returns 4 (the intercept term is included)
```

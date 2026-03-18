# PSD

Computes the power spectral density from the complex Fourier coefficients. The PSD function uses the periodogram estimate, as explained in Numerical Recipes (1989), equations 12.7.5, page 421.

## Format
```
PSD (Values, Number of Output Values)
```

## Arguments

**Values**
: The series values from which the FFT coefficients are computed. The PSD function is computed from these complex coefficients.

**Number of Output Values**
: Indicates how many values should be returned; must be at least as many as the number of input values, but not less than two.

## Example

The following example illustrates the use of the PSD function:

### Function
```
PSD({0,1,4,9,16},7)
```

### Result
```
144.0, 250.786, 167.080, 91.006, 51.367, 38.688, 17.016
```

# FFTPHASE

Returns an array of phase values calculated by applying the FFT function to input values.

## Format
```
FFTPHASE (A, N)
```

## Arguments

**A**
: An array of real values.

**N**
: An integer value which indicates the number output values. This must be greater than or equal to the number of input values. If N is an odd number, the function returns (N+1)/2 output values. If N is an even number, (N/2 + 1) number of values will be returned.

## Example

The following example illustrates the use of the FFTPHASE function:

### Function
```
FFTPHASE({0, 1, 4, 9, 16}, 5)
```

### Result
```
0.0, 107.012, 157.356
```

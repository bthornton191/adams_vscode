# FFTMAG

Returns an array of magnitudes calculated by applying the FFT function to input values. FFTMAG is very useful in determining the natural frequencies of a data stream.

## Format
```
FFTMAG (A, N)
```

## Arguments

**A**
: An array of real values.

**N**
: An integer value which indicates the number output magnitudes. This must be greater than or equal to the number of input values. If N is an odd number, the function returns (N+1)/2 output values. If N is an even number, (N/2 + 1) number of values will be returned.

## Example

The following example illustrates the use of the FFTMAG function:

### Function
```
FFTMAG({0, 1, 4, 9, 16}, 5)
```

### Result
```
12.0, 7.1968, 4.2197
```

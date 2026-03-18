# FREQUENCY

Returns the FFT frequencies of an array of time values. The result is given in Hz.

## Format
```
FREQUENCY (A, N)
```

## Arguments

**A**
: An array of time values from which the frequencies will be computed. The time values should be evenly spaced.

**N**
: An integer value which indicates the number of output values. This must be greater than or equal to the number of input values. If N is an odd number, the function returns (N+1)/2 output values. If N is an even number, (N/2 + 1) number of values will be returned.

## Example

The following examples assume that the current time units setting is in seconds:

### Function
```
FREQUENCY({0,1,2,3,4}, 10)
```

### Result
```
0.0, 0.1, 0.2, 0.3, 0.4, 0.5
```

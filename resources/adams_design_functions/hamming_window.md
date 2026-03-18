# HAMMING_WINDOW

Generate the HAMMING window. The HAMMING window function forces the end points toward zero, and smooths the remaining points toward the end points.

## Format
```
hamming_window (n)
```

## Arguments

**n**
: An integer value.

## Example

The following example illustrates the use of the HAMMING_WINDOW function:

### Function
```
hamming_window (5)
```

### Result
```
{0.0800, 0.5400, 1.0000, 0.5400, 0.0800}
```

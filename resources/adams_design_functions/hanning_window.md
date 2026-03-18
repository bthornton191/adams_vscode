# HANNING_WINDOW

Generate the HANNING window. The HANNING window function forces the end points to become zero, and smooths the remaining points toward the end points.

## Format
```
hanning_window (n)
```

## Arguments

**n**
: An integer value.

## Example

The following example illustrates the use of the HANNING_WINDOW function:

### Function
```
hanning_window (5)
```

### Result
```
{0.2500, 0.7500, 1.0000, 0.7500, 0.2500}
```

# PARZEN_WINDOW

Generate the PARZEN window. The PARZEN window function gently forces the end points toward zero, and smooths the remaining points.

## Format
```
PARZEN_WINDOW (n)
```

## Arguments

**n**
: An integer value.

## Example

The following is an example of the use of the PARZEN_WINDOW function:

### Function
```
PARZEN_WINDOW(5)
```

### Result
```
{0.3333, 0.6667, 1.0000, 0.6667, 0.3333}
```

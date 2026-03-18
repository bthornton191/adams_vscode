# WELCH_WINDOW

Generate the WELCH window. The WELCH_WINDOW function gently forces the end points toward zero and smooths the remaining points.

## Format
```
WELCH_WINDOW (n)
```

## Arguments

**n**
: An integer.

## Example

The following example is an illustration of the WELCH_WINDOW function:

### Function
```
welch_window (5)
```

### Result
```
{0.5556, 0.8889, 1.0000, 0.8889, 0.5556}
```

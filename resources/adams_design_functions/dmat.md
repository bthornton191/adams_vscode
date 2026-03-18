# DMAT

Returns a square matrix with the elements of M along the diagonal, and zero elsewhere. This is useful for scaling locations.

## Format
```
DMAT(M)
```

## Arguments

**M**
: An Nx1 or 1xN array.

## Example

The following example illustrates the use of the DMAT function:

### Function
```
DMAT({1, 2, 3})
```

### Result
```
{{1, 0, 0}, {0, 2, 0}, {0, 0, 3}}
```

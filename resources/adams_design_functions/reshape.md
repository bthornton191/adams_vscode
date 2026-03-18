# RESHAPE

Creates a new matrix from an existing matrix with dimensions you specified in the shape-descriptor array.

## Format
```
RESHAPE (M,S)
```

## Arguments

**M**
: A matrix.

**S**
: A shape-descriptor array. Can contain up to two dimensions.

## Example

The following example illustrates the use of the RESHAPE function:

### Function
```
RESHAPE({1, 0, 0, 0}, {3, 3})
```

### Result
```
{[1, 0, 0], [0, 1, 0], [0, 0, 1]}
```

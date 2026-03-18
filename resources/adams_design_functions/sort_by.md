# SORT_BY

Returns an array sorted by another array in the direction you specified.

## Format
```
SORT_BY (M1, M2, D)
```

## Arguments

**M1**
: MxN matrix by which an array is sorted.

**M2**
: MxN matrix the function will return.

**D**
: Direction in which the matrix is sorted: ■a = ascending ■d = descending

## Example

The following examples illustrate the use of the SORT_BY function:

### Function
```
SORT_BY( {15, 19, 12} , {[4, 6, 9]} , "d" )
```

### Result
```
6.0, 4.0, 9.0
```

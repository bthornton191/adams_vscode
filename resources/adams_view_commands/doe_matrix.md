
# DOE_MATRIX

Returns either a:

*   Matrix of design of experiments (DOE)
*   A row from that matrix
*   The count of rows from that matrix

The argument array contains the information needed to construct the matrix and to determine the
results which you want returned.

## Format

```java
DOE_MATRIX (ARGUMENT_ARRAY)
```

## Arguments

**ARGUMENT_ARRAY:** An array of integers containing either three or four values.

The first value is the type of algorithm to use to create the matrix.

Use these numbers in the first entry of the array:

*   0 - Casewise
*   1 - Central Composite
*   2 - Box-Behnken
*   3 - Full Factorial

The second entry in the array indicates the number of variables that are to be used for the DOE.

The third entry indicates the number of levels on each variable.

The fourth entry indicates whether you want the data centered or 1-based. Centered data is what the 
`SIMULATION` and `OPTIMIZE` commands require, but 1-based can be useful if you are writing your own 
DOE loop using the FOR command. A value of one indicates that the data should be centered, and a value 
of zero indicates that it should be 1-based.

If the fifth entry does not exist, then the result of the function is a complete DOE matrix, which 
will have nTrials rows and nVariables columns. If you enter zero as the fifth array value, then the
result of the function is just the number of trials in that DOE matrix. Any other value indicates 
that just that row of the matrix is to be returned.

## Examples

### Example 1

The following example returns the number of trials for the Box-Behnken matrix with two variables each having five levels. The value returned is 9.

```java
DOE_MATRIX({2, 2, 5, 0, 0})
```

### Example 2

This example returns the fifth row of the Full Factorial matrix with variables variables each having three levels. The centered values returned are {-1, -1, 0, 0}.

```java
DOE_MATRIX({3, 4, 3, 1, 5})
```

### Example 3

This example returns the Central Composite matrix for two variables with three levels. The value returned is the centered data:

```java
DOE_MATRIX({1, 2, 3, 1})

{{0, 0}, {0, -1}, {0, 1}, {-1, 0}, {1, 0}, {-1, -1}, {-1, 1}, {1, -1}, {1, 1}}
```

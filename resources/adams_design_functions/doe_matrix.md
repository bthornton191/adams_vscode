# DOE_MATRIX

Returns either a:

## Format
```
DOE_MATRIX (ARGUMENT_ARRAY)
```

## Arguments

**ARGUMENT_ARRAY**
: An array of integers containing either three or four values. The first value is the type of algorithm to use to create the matrix:

  * `0` — Casewise
  * `1` — Central Composite
  * `2` — Box-Behnken
  * `3` — Full Factorial

  The second entry indicates the number of variables for the DOE. The third entry indicates the number of levels on each variable. The fourth entry indicates whether the data should be centered or 1-based. Centered data is what the SIMULATION and OPTIMIZE commands require, but 1-based can be useful when writing a DOE loop using the FOR command. A value of one indicates centered data; zero indicates 1-based. If a fifth entry is not present, the function returns a complete DOE matrix with nTrials rows and nVariables columns. If the fifth entry is zero, only the number of trials is returned. Any other value returns just that row of the matrix.

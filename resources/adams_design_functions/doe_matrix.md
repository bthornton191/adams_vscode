# DOE_MATRIX

Returns one of the following, depending on the arguments provided:

- A complete matrix of design of experiments (DOE) trials
- A single row from that matrix
- The total number of rows (trials) in that matrix

## Format
```adams_cmd
DOE_MATRIX(ARGUMENT_ARRAY)
```

## Arguments

**ARGUMENT_ARRAY**
: An array of integers with four or five values.

  **Entry 1 — Algorithm:**
  - `0` — Casewise
  - `1` — Central Composite
  - `2` — Box-Behnken
  - `3` — Full Factorial

  **Entry 2** — Number of variables for the DOE.

  **Entry 3** — Number of levels on each variable.

  **Entry 4** — Centering: `1` = centered data (required by `SIMULATION` and `OPTIMIZE`); `0` = 1-based.

  **Entry 5** *(optional)* — If omitted, returns the full matrix (nTrials × nVariables). If `0`, returns only the trial count. Any other value returns just that row of the matrix.

## Examples

### Count the number of trials
Returns the trial count for a Box-Behnken matrix with 2 variables at 5 levels each. Result: `9`.

```adams_cmd
DOE_MATRIX({2, 2, 5, 0, 0})
```

### Return a single row
Returns the fifth row of a Full Factorial matrix with 4 variables at 3 levels, centered. Result: `{-1, -1, 0, 0}`.

```adams_cmd
DOE_MATRIX({3, 4, 3, 1, 5})
```

### Return the full matrix
Returns the complete Central Composite matrix for 2 variables at 3 levels, centered.

```adams_cmd
DOE_MATRIX({1, 2, 3, 1})
```

Result:
```adams_cmd
{{0, 0}, {0, -1}, {0, 1}, {-1, 0}, {1, 0}, {-1, -1}, {-1, 1}, {1, -1}, {1, 1}}
```

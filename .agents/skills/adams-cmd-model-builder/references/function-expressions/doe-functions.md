# DOE (Design of Experiments) Functions

These functions support design-of-experiments workflows in Adams View, generating trial matrices and polynomial term counts for response-surface fitting.

## DOE_MATRIX

Returns a DOE trial matrix (or information about one), based on the algorithm and parameter settings you specify.

```
DOE_MATRIX(argument_array)
```

| Argument | Description |
|----------|-------------|
| `argument_array` | Integer array with 3–5 elements (see below) |

**argument_array elements:**

| Index | Description |
|-------|-------------|
| 1 | Algorithm: `0` = Casewise, `1` = Central Composite, `2` = Box-Behnken, `3` = Full Factorial |
| 2 | Number of variables |
| 3 | Number of levels per variable |
| 4 | Centring: `1` = centered (required for SIMULATE/OPTIMIZE); `0` = 1-based |
| 5 | (Optional) Row selector: omit = return full matrix; `0` = return number of trials; `n` = return row `n` only |

```adams_fn
! Full factorial, 3 variables, 2 levels, centered, return number of trials
DOE_MATRIX({3, 3, 2, 1, 0})

! Full factorial, 3 variables, 2 levels, centered, full matrix
DOE_MATRIX({3, 3, 2, 1})
```

---

## DOE_NUM_TERMS

Returns the number of terms in the polynomial that `OPTIMIZE_FIT_RESPONSE_SURFACE` produces for the given polynomial degree specification.

```
DOE_NUM_TERMS(order_array)
```

| Argument | Description |
|----------|-------------|
| `order_array` | Integer array giving the polynomial degree for each variable — same values supplied to `OPTIMIZE_FIT_RESPONSE_SURFACE` as `POLYNOMIAL_DEGREES` |

```adams_fn
DOE_NUM_TERMS({1, 1, 1})
! returns 4  (3 linear terms + 1 intercept)
```

---

## See also

- [Matrix operations](matrix-operations.md)
- [Statistics functions](statistics.md)

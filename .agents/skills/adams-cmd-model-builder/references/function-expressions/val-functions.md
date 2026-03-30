# VAL / VALAT / VALI — Array Lookup Functions

Three functions for looking up values or indices in arrays by proximity.

## VAL

Returns the element of an array that is nearest to a specified value.

```
VAL(A, x)
```

| Argument | Description |
|----------|-------------|
| `A` | Input array |
| `x` | Reference value |

```adams_fn
VAL({2, 0, 3}, 2.2)
! returns 2  (element 2 is nearest to 2.2)
```

---

## VALAT

Returns the Y-array value at the position corresponding to where `x` falls in the X-array. Performs linear interpolation between adjacent X values.

```
VALAT(X_array, Y_array, x)
```

| Argument | Description |
|----------|-------------|
| `X_array` | 1×N array of x values in ascending order (at least 2 elements) |
| `Y_array` | 1×N array of y values (same length as X_array) |
| `x` | Query x value |

```adams_fn
! Lookup table interpolation
VALAT({0, 1, 2, 3}, {0, 10, 20, 30}, 1.5)
! returns 15.0
```

---

## VALI

Returns the **index** of the element in an array that is nearest to a specified value.

```
VALI(A, x)
```

| Argument | Description |
|----------|-------------|
| `A` | Input array |
| `x` | Reference value |

```adams_fn
VALI({2, 0, 3}, 2.2)
! returns 1  (element at index 1 is nearest to 2.2)
```

---

## See also

- [Array helper functions](array-helpers.md)
- [Spline interpolation](spline-interpolation.md)

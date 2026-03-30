# Array Helper Functions

Utility functions for generating, slicing, and querying arrays.

## Quick reference

| Function | Signature | Description |
|----------|-----------|-------------|
| `ALIGN` | `ALIGN(array, start_value)` | Shift array so it starts at a given value |
| `ANGLES` | `ANGLES(D, ori_type)` | Extract Euler angles from a direction cosine matrix |
| `CENTER` | `CENTER(A)` | Non-statistical midpoint: `(min+max)/2` |
| `FIRST` | `FIRST(A)` | First element (0 if empty) |
| `FIRST_N` | `FIRST_N(A, n)` | First `n` elements |
| `LAST` | `LAST(A)` | Last element (0 if empty) |
| `LAST_N` | `LAST_N(A, n)` | Last `n` elements |
| `SERIES` | `SERIES(start, step, length)` | Evenly-spaced array by step |
| `SERIES2` | `SERIES2(start, end, n)` | Evenly-spaced array by count |
| `SIM_TIME` | `SIM_TIME()` | Simulation time of last step |

---

## ALIGN

Shifts an array of values so that the first element equals a specified value.

```
ALIGN(array, start_value)
```

| Argument | Description |
|----------|-------------|
| `array` | Array of values to shift |
| `start_value` | Desired value of the first element after shifting |

```adams_fn
! Shift curve_1 to start at 0
ALIGN(.plot_1.curve_1, 0)

! Align curve_1 to start at the same value as curve_2
ALIGN(.plot_1.curve_1, .plot_1.curve_2.Y_data[1])
```

---

## ANGLES

Returns a 3×1 matrix of Euler angles extracted from a 3×3 direction cosine (rotation) matrix.

```
ANGLES(D, ori_type)
```

| Argument | Description |
|----------|-------------|
| `D` | 3×3 direction cosine matrix |
| `ori_type` | Euler sequence string, e.g. `"body 313"`, `"space 123"` |

```adams_fn
! Inverse of TMAT
ANGLES(dcos_matrix, "body313")
```

---

## CENTER

Returns the non-statistical centre of an array: `(min(A) + max(A)) / 2`.

```
CENTER(A)
```

```adams_fn
CENTER({1, 0, 4, 3})
! returns 2.0
```

---

## FIRST

Returns the first element of an array, or `0` if the array is empty.

```
FIRST(A)
```

```adams_fn
FIRST({1, 2, 3})   ! returns 1
FIRST({})          ! returns 0
```

---

## FIRST_N

Returns the first `n` elements of an array.

```
FIRST_N(A, n)
```

| Argument | Description |
|----------|-------------|
| `A` | Input array |
| `n` | Number of elements to return |

---

## LAST

Returns the last element of an array, or `0` if the array is empty.

```
LAST(A)
```

---

## LAST_N

Returns the last `n` elements of an array.

```
LAST_N(A, n)
```

---

## SERIES

Generates a 1×N array starting at `start`, incrementing by `step`, with `n` elements.

```
SERIES(start, step, n)
```

| Argument | Description |
|----------|-------------|
| `start` | Starting value |
| `step` | Increment per element |
| `n` | Total number of elements |

```adams_fn
SERIES(1, 2, 3)
! returns {1, 3, 5}

! x-axis for a 100-point time array, dt = 0.01
SERIES(0, 0.01, 100)
```

---

## SERIES2

Generates a 1×N array from `start` to `end` with `n` evenly-spaced points (inclusive).

```
SERIES2(start, end, n)
```

| Argument | Description |
|----------|-------------|
| `start` | Start value |
| `end` | End value |
| `n` | Number of points (including start and end) |

```adams_fn
SERIES2(2, 8, 4)
! returns {2, 4, 6, 8}
```

---

## SIM_TIME

Returns the simulation time at the last step of the default simulation. Generates an error if no default simulation exists.

```
SIM_TIME()
```

```adams_fn
SIM_TIME()   ! e.g. returns 0.45
```

---

## See also

- [Matrix operations](matrix-operations.md)
- [Statistics functions](statistics.md)
- [Spline interpolation](spline-interpolation.md)

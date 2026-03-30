# Statistics and Calculus Functions

Functions for computing statistical measures, numerical derivatives, integrals, and related aggregates over arrays.

## Quick reference

| Function | Signature | Description |
|----------|-----------|-------------|
| `DIFF` | `DIFF(x, y)` | Numerical derivative (cubic-spline based) |
| `DIFFERENTIATE` | `DIFFERENTIATE(C)` | Derivative of a curve object |
| `INTEGR` | `INTEGR(x, y)` | Numerical integral (cubic-spline based) |
| `INTEGRATE` | `INTEGRATE(C)` | Integral curve of a curve object |
| `MAX` | `MAX(M)` | Maximum element value |
| `MAXI` | `MAXI(M)` | Index of the maximum element |
| `MEAN` | `MEAN(M)` | Arithmetic mean |
| `MIN` | `MIN(M)` | Minimum element value |
| `MINI` | `MINI(M)` | Index of the minimum element |
| `NORM` | `NORM(A)` | Matrix norm (largest singular value) |
| `NORM2` | `NORM2(A)` | Euclidean (L2) norm |
| `RMS` | `RMS(values)` | Root mean square |
| `SSQ` | `SSQ(M)` | Sum of squares |
| `SUM` | `SUM(M)` | Sum of all elements |

> **Note**: `MAX`, `MIN`, `STEP` also appear as solver runtime functions with different signatures. These design-time variants operate on arrays, whereas the runtime variants evaluate scalar expressions during simulation.

---

## DIFF

Returns a 1×N array of numerical derivatives at each point. Fits a cubic spline to the input data and returns the spline derivatives.

```
DIFF(x, y)
```

| Argument | Description |
|----------|-------------|
| `x` | 1×N array of independent variable values (ascending, length ≥ 4) |
| `y` | 1×N array of dependent variable values |

```adams_fn
DIFF(SERIES(0,1,5), {0,1,4,9,16})
! returns {0, 2.0, 4.0, 6.0, 8.0}
```

---

## DIFFERENTIATE

Returns a curve of derivatives from an input curve object. The X values of the output curve match the input curve.

```
DIFFERENTIATE(C)
```

| Argument | Description |
|----------|-------------|
| `C` | A curve object (2×N data set) |

---

## INTEGR

Returns a 1×N array of running integrals of the input data (cubic-spline based).

```
INTEGR(x, y)
```

| Argument | Description |
|----------|-------------|
| `x` | 1×N array of independent variable values (ascending, length ≥ 4) |
| `y` | 1×N array of dependent variable values |

---

## INTEGRATE

Returns a curve of integrals from an input curve object. The X values of the output curve match the input curve.

```
INTEGRATE(C)
```

| Argument | Description |
|----------|-------------|
| `C` | A curve object (2×N data set) |

---

## MAX

Returns the maximum element of a matrix. (Array variant — not the same as the two-argument runtime `MAX(x,y)`.)

```
MAX(M)
```

```adams_fn
MAX({3, 1, 4, 1, 5, 9})   ! returns 9
```

---

## MAXI

Returns the **index** of the maximum element.

```
MAXI(M)
```

```adams_fn
MAXI({0.1, 0.2, 0.3, 3.3})   ! returns 4
```

---

## MEAN

Returns the arithmetic mean of all elements.

```
MEAN(M)
```

```adams_fn
MEAN({0.1, 0.2, 0.3, 3.4})   ! returns 1.0
```

---

## MIN

Returns the minimum element of a matrix.

```
MIN(M)
```

---

## MINI

Returns the **index** of the minimum element.

```
MINI(M)
```

---

## NORM

Returns the matrix norm (largest singular value, equivalent to MATLAB `max(svd(A))`).

```
NORM(A)
```

---

## NORM2

Returns the Euclidean (L2) norm — the square root of the sum of squares.

```
NORM2(A)
```

---

## RMS

Returns the root mean square of the values: `SQRT(MEAN(A^2))`.

```
RMS(values)
```

```adams_fn
RMS({0, 1, 4, 9, 16})
```

---

## SSQ

Returns the sum of squared elements: `SUM(A^2)`.

```
SSQ(M)
```

---

## SUM

Returns the sum of all elements of a matrix.

```
SUM(M)
```

```adams_fn
SUM({1, 2, 3, 4})   ! returns 10
```

---

## See also

- [Matrix operations](matrix-operations.md)
- [Array helper functions](array-helpers.md)
- [Spline interpolation](spline-interpolation.md)

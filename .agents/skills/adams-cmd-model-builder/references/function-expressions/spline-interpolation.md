# Spline Interpolation Functions

Adams View provides a suite of functions for fitting and evaluating interpolating curves from data arrays. These are design-time functions that return arrays of interpolated values.

## Quick reference

| Function | Signature | Method |
|----------|-----------|--------|
| `AKIMA_SPLINE` | `AKIMA_SPLINE(x, y, n)` | Akima spline |
| `AKIMA_SPLINE2` | `AKIMA_SPLINE2(x, y, xi)` | Akima spline at specified x values |
| `CSPLINE` | `CSPLINE(x, y, n)` | Cubic spline |
| `CUBIC_SPLINE` | `CUBIC_SPLINE(x, y, n)` | Cubic spline (alias) |
| `HERMITE_SPLINE` | `HERMITE_SPLINE(x, y, n)` | Hermite cubic spline |
| `LINEAR_SPLINE` | `LINEAR_SPLINE(x, y, n)` | Linear interpolation |
| `NOTAKNOT_SPLINE` | `NOTAKNOT_SPLINE(x, y, n)` | Not-a-knot cubic spline |
| `SPLINE` | `SPLINE(points, type, n)` | Generic spline dispatcher |
| `INTERP1` | `INTERP1(x, y, xi, method)` | 1-D interpolation (MATLAB-style) |
| `INTERP2` | `INTERP2(x, y, z, xi, yi, method)` | 2-D interpolation (MATLAB-style) |
| `INTERPFT` | `INTERPFT(y, n)` | Fourier-interpolation resample |
| `GRIDDATA` | `GRIDDATA(x, y, z, xi, yi, method)` | Scattered data interpolation |
| `MESHGRID` | `MESHGRID(x, y)` | Rectangular grid from vectors |
| `POLYFIT` | `POLYFIT(x, y, order)` | Polynomial least-squares fit |
| `POLYVAL` | `POLYVAL(coeffs, x)` | Evaluate polynomial at x values |

---

## AKIMA_SPLINE

Interpolates using the Akima method. Returns `n` evenly-spaced y values over the range of the input data.

```
AKIMA_SPLINE(x, y, n)
```

| Argument | Description |
|----------|-------------|
| `x` | 1×N array of x values (ascending, length ≥ 4) |
| `y` | 1×N array of y values |
| `n` | Number of output values |

```adams_fn
AKIMA_SPLINE({1,2,3,4}, {0,2,1,3}, 10)
! returns {0.0, 1.0, 1.667, 2.0, 1.778, 1.222, 1.0, 1.333, 2.0, 3.0}
```

---

## AKIMA_SPLINE2

Evaluates an Akima spline at explicitly specified x values.

```
AKIMA_SPLINE2(x, y, xi)
```

| Argument | Description |
|----------|-------------|
| `x` | 1×N array of x values (ascending, length ≥ 4) |
| `y` | 1×N array of y values |
| `xi` | 1×M array of x values at which to evaluate |

---

## CSPLINE / CUBIC_SPLINE

Interpolates using a cubic spline. Returns `n` evenly-spaced y values.

```
CSPLINE(x, y, n)
CUBIC_SPLINE(x, y, n)
```

| Argument | Description |
|----------|-------------|
| `x` | 1×N array of x values (ascending, length ≥ 4) |
| `y` | 1×N array of y values |
| `n` | Number of output values |

---

## HERMITE_SPLINE

Interpolates using a Hermite cubic spline.

```
HERMITE_SPLINE(x, y, n)
```

| Argument | Description |
|----------|-------------|
| `x` | 1×N array of x values (ascending) |
| `y` | 1×N array of y values |
| `n` | Number of output values |

---

## LINEAR_SPLINE

Interpolates using piecewise linear interpolation.

```
LINEAR_SPLINE(x, y, n)
```

| Argument | Description |
|----------|-------------|
| `x` | 1×N array of x values (ascending) |
| `y` | 1×N array of y values |
| `n` | Number of output values |

---

## NOTAKNOT_SPLINE

Interpolates using a not-a-knot cubic spline (the third derivative is continuous at the second and second-to-last knots).

```
NOTAKNOT_SPLINE(x, y, n)
```

| Argument | Description |
|----------|-------------|
| `x` | 1×N array of x values (ascending, length ≥ 4) |
| `y` | 1×N array of y values |
| `n` | Number of output values |

---

## SPLINE

Generic spline dispatcher — interpolates a 2×N point array using any of the supported spline methods.

```
SPLINE(points, spline_type, n)
```

| Argument | Description |
|----------|-------------|
| `points` | 2×N array `{[x1,...,xN],[y1,...,yN]}` (x values ascending, length ≥ 4) |
| `spline_type` | `"AKIMA"`, `"CSPLINE"`, `"CUBIC"`, `"LINEAR"`, `"NOTAKNOT"`, or `"HERMITE"` |
| `n` | Number of output points |

```adams_fn
SPLINE({[1,2,3,4],[0,2,1,3]}, "CSPLINE", 10)
```

---

## INTERP1

1-D interpolation. Given a curve described by `x` and `y`, returns the `y` values at the requested `xi` positions.

```
INTERP1(x, y, xi, method)
```

| Argument | Description |
|----------|-------------|
| `x` | 1×N array of x values |
| `y` | 1×N array of y values |
| `xi` | 1×M array of query x positions |
| `method` | `"nearest"`, `"linear"`, `"spline"`, `"pchip"`, or `"cubic"` |

---

## INTERP2

2-D interpolation. Returns values at `(xi, yi)` from a surface defined by the grid `(x, y, z)`.

```
INTERP2(x, y, z, xi, yi, method)
```

| Argument | Description |
|----------|-------------|
| `x` | 1×N array of x grid values |
| `y` | 1×M array of y grid values |
| `z` | M×N matrix of z values at each grid point |
| `xi`, `yi` | Query positions |
| `method` | `"nearest"`, `"linear"`, `"spline"`, or `"cubic"` |

---

## INTERPFT

Resamples a signal using Fourier interpolation.

```
INTERPFT(y, n)
```

| Argument | Description |
|----------|-------------|
| `y` | 1×N array of input values |
| `n` | Number of output points |

---

## GRIDDATA

Interpolates scattered (non-grid) 2-D data.

```
GRIDDATA(x, y, z, xi, yi, method)
```

| Argument | Description |
|----------|-------------|
| `x`, `y` | 1×N arrays of scattered point coordinates |
| `z` | 1×N array of values at each point |
| `xi`, `yi` | Query coordinates |
| `method` | Interpolation method string |

---

## MESHGRID

Generates rectangular 2-D grid matrices from x and y vectors (equivalent to MATLAB `meshgrid`).

```
MESHGRID(x, y)
```

| Argument | Description |
|----------|-------------|
| `x` | 1×N array of x values |
| `y` | 1×M array of y values |

Returns a 2-element array `{X_matrix, Y_matrix}`.

---

## POLYFIT

Fits a polynomial of a specified order to data using least squares. Returns coefficient array from degree 0 to `order`.

```
POLYFIT(x, y, order)
```

| Argument | Description |
|----------|-------------|
| `x` | 1×N array of x values |
| `y` | 1×N array of y values |
| `order` | Maximum polynomial degree |

---

## POLYVAL

Evaluates a polynomial (defined by its coefficients) at the specified x values.

```
POLYVAL(coeffs, x)
```

| Argument | Description |
|----------|-------------|
| `coeffs` | Coefficient array (from degree 0 to highest), as returned by `POLYFIT` |
| `x` | Scalar or array of x values at which to evaluate |

---

## See also

- [Signal processing functions](signal-processing.md)
- [Matrix operations](matrix-operations.md)
- [Statistics functions](statistics.md)

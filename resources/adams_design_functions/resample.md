# RESAMPLE

Takes a curve and resamples it over a new interval with the spline algorithm you specified.

## Format
```
RESAMPLE (Curve, Sample Interval, Spline Type, Number of Spline Points)
```

## Arguments

**Curve**
: A 2xN array of points to be interpolated.

**Sample Interval**
: The x values corresponding to the output data.

**Spline Type**
: The spline algorithm to use for interpolation. It must be one of the following character strings:

  * `AKIMA` — interpolates using the Akima method.
  * `CSPLINE` — interpolates using cubic splines.
  * `CUBIC` — interpolates using a third-order Lagrangian polynomial.
  * `LINEAR` — interpolates using linear interpolation.
  * `NOTAKNOT` — interpolates using Not-a-knot cubic spline.
  * `HERMITE` — interpolates using Hermite cubic spline.

**Number of Spline Points**
: Number of values to be generated in the internal smoothed curve.

## Example

The following example illustrates the use of the RESAMPLE function:

### Function
```
RESAMPLE({[1, 2, 3, 4], [2, 3, 3, 1]}, {2.5,3.5}, "CUBIC", 200)
```

### Result
```
{0.015, 2.0, 3.0, 2.0, 1.0, 0.0}
```

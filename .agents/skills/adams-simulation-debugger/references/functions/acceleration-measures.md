# Functions: Acceleration Measures

> Same argument convention as velocity functions: i = measured marker, j = reference,
> k = result frame, l = differentiation frame.

## ACCX(i [, j] [, k] [, l])
X-component of translational acceleration of i w.r.t. j in frame k, differentiated in frame l.
- **Returns:** real, length/time²

## ACCY(i [, j] [, k] [, l])
Y-component of translational acceleration.
- **Returns:** real, length/time²

## ACCZ(i [, j] [, k] [, l])
Z-component of translational acceleration.
- **Returns:** real, length/time²

## ACCM(i [, j] [, l])
Magnitude of translational acceleration of i w.r.t. j. Always ≥ 0.
- **Returns:** real, length/time²

## WDTX(i [, j] [, k] [, l])
X-component of angular acceleration of i w.r.t. j in frame k, differentiated in frame l.
- **Returns:** real, rad/time²

## WDTY(i [, j] [, k] [, l])
Y-component of angular acceleration.
- **Returns:** real, rad/time²

## WDTZ(i [, j] [, k] [, l])
Z-component of angular acceleration.
- **Returns:** real, rad/time²

## WDTM(i [, j] [, l])
Magnitude of angular acceleration of i w.r.t. j. Always ≥ 0.
- **Returns:** real, rad/time²

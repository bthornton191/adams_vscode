# Functions: Displacement Measures

> All angles are in **radians** unless the `D` suffix is used.
> For functions with optional arguments `[j]` and `[k]`:
> - `j` = reference marker (defaults to global origin when omitted)
> - `k` = result coordinate frame (defaults to global axes when omitted)

## DM(i [, j])
Distance (scalar magnitude) from marker j origin to marker i origin. Always ≥ 0.
- **Returns:** real, length units
- **Use for:** spring deformation `DM(i,j) - L0`, gap detection

## DX(i [, j] [, k])
X-component of displacement vector (from j to i), expressed in coordinate system of k.
- **Returns:** real, length units (signed)
- **Notes:** Set `j=0` when explicitly specifying k with global reference.

## DY(i [, j] [, k])
Y-component of displacement from j to i in frame k.
- **Returns:** real, length units (signed)

## DZ(i [, j] [, k])
Z-component of displacement from j to i in frame k.
- **Returns:** real, length units (signed)

## AX(i [, j])
Rotational displacement of marker i about the x-axis of marker j, measured CCW from j's y-axis to i's y-axis.
- **Returns:** real, radians
- **Notes:** Becomes inaccurate for rotations > 10° about y or z of j. Use for small single-axis rotation sensing only.

## AY(i [, j])
Rotational displacement of i about the y-axis of j, measured CCW from j's z-axis to i's z-axis.
- **Returns:** real, radians
- **Notes:** Same accuracy caveats as AX.

## AZ(i [, j])
Rotational displacement of i about the z-axis of j, measured CCW from j's x-axis to i's x-axis.
- **Returns:** real, radians
- **Notes:** Most commonly used single-axis angle. Unwrap: `MOD(AZ(i,j)+PI, 2*PI)-PI`

## PHI(i [, j])
Spin angle (3rd Euler angle) of body-fixed 3-1-3 sequence (precession→nutation→spin).
- **Returns:** real, radians

## PSI(i [, j])
Precession angle (1st Euler angle) of body-fixed 3-1-3 sequence.
- **Returns:** real, radians

## THETA(i [, j])
Nutation angle (2nd Euler angle) of body-fixed 3-1-3 sequence.
- **Returns:** real, radians

## ROLL(i [, j])
Third angle of body-fixed 3-2-1 (yaw-pitch-roll) Euler sequence.
- **Returns:** real, radians
- **Notes:** Euler angle value, not an angular rate.

## PITCH(i [, j])
**Negative** of the second angle (pitch) of body-fixed 3-2-1 sequence. Negative per automotive convention.
- **Returns:** real, radians

## YAW(i [, j])
First angle (yaw) of body-fixed 3-2-1 sequence.
- **Returns:** real, radians

## INCANG(i, j, k)
Included angle between line (i→j) and line (j→k). All three markers may be on different parts.
- **Returns:** real, radians; always ≥ 0

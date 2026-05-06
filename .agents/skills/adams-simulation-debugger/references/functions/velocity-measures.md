# Functions: Velocity Measures

> All velocities are time derivatives of positions/orientations with respect to ground (inertial frame)
> unless `j` (reference) and `l` (derivative frame) are specified.

## VR(i [, j] [, l])
Radial (separation) velocity — time derivative of DM(i,j). Positive when i and j are separating.
- **j:** reference marker; **l:** differentiation frame
- **Returns:** real, length/time
- **Notes:** Invariant of coordinate frame. Equals `d/dt(DM(i,j))`. Use in damper expressions: `-c*VR(i,j)`

## VX(i [, j] [, k] [, l])
X-component of velocity of i w.r.t. j, expressed in frame k, differentiated in frame l.
- **Returns:** real, length/time

## VY(i [, j] [, k] [, l])
Y-component of velocity.
- **Returns:** real, length/time

## VZ(i [, j] [, k] [, l])
Z-component of velocity.
- **Returns:** real, length/time

## VM(i [, j] [, l])
Magnitude of velocity vector of i w.r.t. j. Always ≥ 0.
- **Returns:** real, length/time

## WX(i [, j] [, k])
X-component of angular velocity of i w.r.t. j, expressed in frame k.
- **Returns:** real, rad/time

## WY(i [, j] [, k])
Y-component of angular velocity.
- **Returns:** real, rad/time

## WZ(i [, j] [, k])
Z-component of angular velocity.
- **Returns:** real, rad/time

## WM(i [, j])
Magnitude of angular velocity of i w.r.t. j. Always ≥ 0.
- **Returns:** real, rad/time

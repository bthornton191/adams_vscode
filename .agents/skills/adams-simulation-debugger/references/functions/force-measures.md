# Functions: Force and Torque Measures

> These functions sum **all** forces/torques acting between the i-j marker pair.
> Set `j=0` (or omit) for action-only forces.
> Use `k` to specify a result coordinate frame; if omitting j but specifying k, use `j=0`.

## FX(i [, j] [, k])
X-component of net translational force at marker i, resolved in frame k.
- **Returns:** real, force units

## FY(i [, j] [, k])
Y-component of net translational force.
- **Returns:** real, force units

## FZ(i [, j] [, k])
Z-component of net translational force.
- **Returns:** real, force units

## FM(i [, j])
Magnitude of net translational force at marker i. Always ≥ 0.
- **Returns:** real, force units

## TX(i [, j] [, k])
X-component of net torque at marker i, resolved in frame k.
- **Returns:** real, torque units

## TY(i [, j] [, k])
Y-component of net torque.
- **Returns:** real, torque units

## TZ(i [, j] [, k])
Z-component of net torque.
- **Returns:** real, torque units

## TM(i [, j])
Magnitude of net torque at marker i. Always ≥ 0.
- **Returns:** real, torque units

# ABS — Absolute Value and Common Math Functions

Adams `FUNCTION=` expressions support a full set of mathematical functions in addition to the kinematic and look-up functions.

## ABS

```
ABS(x)
```

Returns the absolute value of `x`. The result is always ≥ 0.

```adams_fn
! Magnitude regardless of sign
ABS(VZ(.MODEL.BODY.CM) - 100.0)
```

## Complete Math Function Reference

| Function | Signature | Description |
|----------|-----------|-------------|
| `ABS` | `ABS(x)` | Absolute value |
| `SQRT` | `SQRT(x)` | Square root (`x` must be ≥ 0) |
| `SIN` | `SIN(x)` | Sine of `x` (radians) |
| `COS` | `COS(x)` | Cosine of `x` (radians) |
| `TAN` | `TAN(x)` | Tangent of `x` (radians) |
| `ASIN` | `ASIN(x)` | Arc sine; result in radians, −π/2 to π/2 |
| `ACOS` | `ACOS(x)` | Arc cosine; result in radians, 0 to π |
| `ATAN` | `ATAN(x)` | Arc tangent; result in radians, −π/2 to π/2 |
| `ATAN2` | `ATAN2(y, x)` | 4-quadrant arc tangent; result in radians, −π to π |
| `EXP` | `EXP(x)` | `eˣ` |
| `LOG` | `LOG(x)` | Natural logarithm (base e) |
| `LOG10` | `LOG10(x)` | Base-10 logarithm |
| `MIN` | `MIN(x, y)` | Minimum of two values |
| `MAX` | `MAX(x, y)` | Maximum of two values |
| `MOD` | `MOD(x, y)` | Remainder of `x / y` (same sign as `x`) |
| `INT` | `INT(x)` | Truncates to integer (rounds towards zero) |
| `SIGN` | `SIGN(x, y)` | `ABS(x) * sign(y)`; copies sign of `y` onto magnitude of `x` |
| `AINT` | `AINT(x)` | Truncates to integer nearest zero (same as `INT`) |
| `ANINT` | `ANINT(x)` | Rounds to nearest integer (away from zero for .5) |
| `NINT` | `NINT(x)` | Returns the whole number nearest to `x` |
| `CEIL` | `CEIL(x)` | Smallest integer **greater than** `x` (ceiling) |
| `FLOOR` | `FLOOR(x)` | Largest integer **less than** `x` (floor) |
| `RTOI` | `RTOI(x)` | Converts real number to integer representation |
| `SINH` | `SINH(x)` | Hyperbolic sine of `x` |
| `COSH` | `COSH(x)` | Hyperbolic cosine of `x` |
| `TANH` | `TANH(x)` | Hyperbolic tangent of `x`; useful as a smooth step function |
| `DIM` | `DIM(x1, x2)` | Positive difference: `MAX(x1-x2, 0)` |
| `MAG` | `MAG(x, y, z)` | Magnitude of a 3D vector: `SQRT(x²+y²+z²)` |
| `RAND` | `RAND()` | Pseudo-random value on [0.0, 1.0] from uniform distribution |

## Examples

```adams_fn
! Clamp velocity to ±500 units/s
MIN(MAX(VZ(.MODEL.BODY.CM), -500.0), 500.0)

! 4-quadrant angle from x/y displacements
ATAN2(DY(.MODEL.BODY.CM), DX(.MODEL.BODY.CM))

! Period of a spring-mass system (for use in STEP duration)
2.0 * PI * SQRT(0.01 / 1000.0)
```

## Degrees vs radians

All trig functions use **radians**. To convert a degree literal, append `D`:
```adams_fn
SIN(45D)      ! = SIN(0.7854)
SIN(TIME * 360D / 1.0)  ! full revolution per second
```

## See also

- [TIME / PI](time.md) — built-in constants
- [IF](if.md) — conditional branching

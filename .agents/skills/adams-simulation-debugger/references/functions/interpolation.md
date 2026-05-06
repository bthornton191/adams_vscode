# Functions: Interpolation

## AKISPL(x, z, id [, iord])
Akima spline interpolation on SPLINE/id at independent variable (x, z).
- **x:** primary independent variable
- **z:** secondary independent variable for surface lookup; set to `0` for 2D curve
- **id:** SPLINE element ID
- **iord:** derivative order: `0` = value (default), `1` = first derivative, `2` = second derivative. Valid for 2D curves only; not supported for surfaces.
- **Returns:** real
- **Notes:** Local method using 3-point Akima algorithm. Very fast. First derivative reliable only for evenly spaced data. Second derivative unreliable. For surfaces: cubic in y-direction, linear in z-direction. No oscillation between data points.
- **Use for:** angle encoder look-up, force vs. displacement maps, torque tables

## CUBSPL(x, z, id [, iord])
Cubic spline (global method) interpolation on SPLINE/id at (x, z).
- Same arguments as AKISPL.
- **Returns:** real
- **Notes:** Global method — slower than AKISPL but provides reliable first and second derivatives regardless of data spacing. Can produce oscillation (overshoot) near steep gradients. Prefer AKISPL for tabular force data; use CUBSPL when accurate second derivatives are needed (e.g., stiffness computation).

## INTERP(x, method, id [, iord])
Interpolation of time-series data from a DAC/RPC III SPLINE file.
- **x:** independent variable (typically `TIME`)
- **method:** `1` = linear; `3` = cubic
- **id:** SPLINE element ID (defined with `FILE=` argument)
- **iord:** derivative order `0`, `1`, or `2`
- **Returns:** real
- **Notes:** Prefer method=3 (cubic); linear has discontinuous first derivative which can cause integrator issues. For RPC III files, specify CHANNEL= in the SPLINE statement.

## CURVE(alpha, iord, comp, id)
Evaluates a B-spline or user-defined CURVE/id at parameter value alpha.
- **alpha:** curve parameter. Range: `[-1, 1]` for B-splines; `[MINPAR, MAXPAR]` for CURSUB
- **iord:** `0` = coordinate value, `1` = first derivative, `2` = second derivative
- **comp:** coordinate component: `1` = x, `2` = y, `3` = z
- **id:** CURVE element ID
- **Returns:** real, length units for iord=0; length/parameter for iord>0

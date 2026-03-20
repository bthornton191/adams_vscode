# FUNCTION= Runtime Expressions — Adams Python API Reference

Runtime expressions are **identical** between Adams CMD and the Python API. The only difference is that in Python they are assigned as plain strings to `.function` properties (or passed to parameter arguments) rather than appearing after the `FUNCTION=` keyword in CMD.

```python
# Python — assign as a string
motion.function = 'STEP(TIME, 0.0, 0.0, 1.0, 360D)'
sforce.function = 'IMPACT(DZ(.model.body.cm, .model.ground.ref), VZ(...), 0, 1e5, 1.5, 50, 0.1)'
```

The Adams Solver evaluates these strings at **every timestep** — they are not Python expressions.

---

## Syntax Rules

- Marker arguments are **full dot-path names** (e.g., `.MODEL.PART.MARKER`).
- All angles default to **radians**; append `D` for degrees: `90D`, `360D`.
- `TIME` is a built-in variable (no parentheses).
- `PI` is the constant π (no parentheses).
- Standard math: `+`, `-`, `*`, `/`, `**` (power), parentheses.
- Trig: `SIN(x)`, `COS(x)`, `TAN(x)`, `ATAN2(y, x)` — arguments in radians.

---

## Smoothing Functions

### STEP — cubic step (C¹ continuous)
```
STEP(x, x0, h0, x1, h1)
```
Transitions from `h0` at `x=x0` to `h1` at `x=x1`. Zero 1st-derivative at endpoints.

```python
motion.function = 'STEP(TIME, 0.0, 0.0, 2.0, 500.0)'   # ramp from 0 to 500 over 2 s
```

### STEP5 — quintic step (C² continuous)
```
STEP5(x, x0, h0, x1, h1)
```
Smoother than STEP — zero 1st and 2nd derivatives at endpoints.

### HAVSIN — haversine step
```
HAVSIN(x, x0, x1, h0, h1)
```
Smoothest transition; slightly higher peak derivative than STEP5.

### IF — conditional (prefer STEP — IF has derivative discontinuities)
```
IF(condition : expr_lt, expr_eq, expr_gt)
```
Returns `expr_lt` when `condition < 0`, `expr_eq` when `= 0`, `expr_gt` when `> 0`.

---

## Contact Functions

### IMPACT — one-sided contact
```
IMPACT(disp, vel, threshold, K, e, C, d)
```
Force is active when `disp < threshold`. Parameters: threshold (gap), stiffness K, exponent e, damping C, penetration depth d.

```python
sforce.function = ('IMPACT('
    'DZ(.model.body.cm, .model.ground.ref, .model.ground.ref),'
    'VZ(.model.body.cm, .model.ground.ref, .model.ground.ref, .model.ground.ref),'
    '0.0, 1.0E5, 2.2, 50.0, 0.1)')
```

### BISTOP — two-sided contact
```
BISTOP(disp, vel, lo, hi, K, e, C, d)
```
Force active when `disp < lo` or `disp > hi`.

---

## Spline Lookup

### AKISPL — Akima spline (better local smoothness)
```
AKISPL(x, y, SplineName, n)
```
`n=0` returns value, `n=1` returns first derivative.

```python
sforce.function = f'AKISPL(DX(.model.body.cm, .model.ground.ref), 0, {spline.full_name}, 0)'
```

### CUBSPL — Cubic spline
```
CUBSPL(x, y, SplineName, n)
```

---

## Displacement Measures

| Function | Description |
|----------|-------------|
| `DX(To, From, Along)` | x-displacement of `To` relative to `From`, expressed in `Along` frame |
| `DY(To, From, Along)` | y-displacement |
| `DZ(To, From, Along)` | z-displacement |
| `DM(To, From)` | magnitude of displacement vector |

`Along` (optional) defaults to the global frame when omitted.

---

## Velocity Measures

| Function | Description |
|----------|-------------|
| `VX(To, From, Along, RefFrame)` | x-component of relative velocity |
| `VY(To, From, Along, RefFrame)` | y-component |
| `VZ(To, From, Along, RefFrame)` | z-component |
| `VM(To, From, RefFrame)` | magnitude |
| `VR(To, From, RefFrame)` | radial (line-of-sight) velocity; positive = separating |

---

## Angular Velocity Measures

| Function | Description |
|----------|-------------|
| `WX(To, From, About)` | x-component of angular velocity |
| `WY` / `WZ` | y- / z-components |
| `WM(To, From)` | magnitude |

---

## Acceleration Measures

| Function | Description |
|----------|-------------|
| `ACCX(To, From, Along, RefFrame)` | x-translational acceleration |
| `ACCY` / `ACCZ` | y- / z-components |

---

## Orientation Angles

| Function | Description |
|----------|-------------|
| `AX(To, From)` | Rotation about x-axis of From (radians) |
| `AY(To, From)` | Rotation about y-axis |
| `AZ(To, From)` | Rotation about z-axis |
| `PSI(To, From)` | Body-313 1st Euler angle (radians) |
| `THETA(To, From)` | Body-313 2nd Euler angle |
| `PHI(To, From)` | Body-313 3rd Euler angle |
| `YAW(To, From)` | Body-321 1st angle |
| `PITCH(To, From)` | Body-321 2nd angle |
| `ROLL(To, From)` | Body-321 3rd angle |

---

## Force/Torque Measures

| Function | Description |
|----------|-------------|
| `FX(AppliedTo, AppliedFrom, Along)` | x-force at a marker |
| `FY` / `FZ` | y- / z-components |
| `TX(AppliedTo, AppliedFrom, About)` | x-torque |
| `TY` / `TZ` | y- / z-components |

---

## Data Element Access

| Function | Description |
|----------|-------------|
| `VARVAL(VarName)` | Current value of a state variable |
| `ARYVAL(ArrName, n)` | Element `n` of a GeneralArray |
| `AKISPL(x, y, SplineName, n)` | Akima spline |
| `CUBSPL(x, y, SplineName, n)` | Cubic spline |
| `DELAY(expr, delay, init, logicArr)` | Time-delayed value |

---

## Harmonic and Polynomial

| Function | Description |
|----------|-------------|
| `SHF(x, x0, a, omega, phi, b)` | `a*SIN(omega*(x-x0) - phi) + b` |
| `POLY(x, shift, c0, c1, ...)` | Polynomial up to 31 coefficients |
| `CHEBY(x, shift, c0, c1, ...)` | Chebyshev polynomial |
| `FORCOS` / `FORSIN` | Fourier cosine / sine series |

---

## Math

`ABS(x)`, `SQRT(x)`, `SIN(x)`, `COS(x)`, `TAN(x)`, `ATAN2(y,x)`, `EXP(x)`, `LOG(x)`, `LOG10(x)`, `MIN(a,b)`, `MAX(a,b)`, `MOD(a,b)`, `INT(x)`, `SIGN(a,b)`

# Functions: Math and Logic

> Discontinuous functions (ABS, MAX, MIN, MOD, SIGN, IF) can cause integrator step-size reduction
> if they appear in force or motion expressions. Use STEP/STEP5 to smooth transitions.

## ABS(a)
Absolute value: |a|. Discontinuous derivative at a = 0.

## MAX(a1, a2)
Returns the larger of a1 and a2. Discontinuous at a1 = a2.

## MIN(a1, a2)
Returns the smaller of a1 and a2. Discontinuous at a1 = a2.

## MOD(a1, a2)
Remainder: `a1 - INT(a1/a2)*a2`. Discontinuous.
- **Use:** `MOD(AZ(i,j)+PI, 2*PI)-PI` to unwrap revolute angle to (−π, π]

## SIGN(a1, a2)
Transfers sign of a2 to magnitude of a1: `ABS(a1)` if a2 > 0; `-ABS(a1)` if a2 < 0. Discontinuous at a2 = 0.

## AINT(a)
Integer truncation toward zero. `AINT(4.8)=4`, `AINT(-4.8)=-4`. Non-differentiable.

## ANINT(a)
Rounds to nearest integer. `ANINT(4.6)=5`, `ANINT(-4.6)=-5`. Non-differentiable.

## DIM(a1, a2)
Positive difference: `MAX(0, a1-a2)`. Discontinuous at a1 = a2.

## SQRT(a)
Square root. Undefined for a < 0. Infinite derivative at a = 0 — add a small offset if a can reach 0.

## SIN(a) / COS(a) / TAN(a)
Trigonometric functions. Argument in radians. TAN undefined at ±π/2.

## ASIN(a) / ACOS(a)
Inverse trig. Defined for `|a| ≤ 1`. ASIN returns [−π/2, π/2]. ACOS returns [0, π].

## ATAN(a)
Arc tangent. Returns (−π/2, π/2).

## ATAN2(a1, a2)
Arc tangent of a1/a2 with quadrant resolution. Returns (−π, π]. Undefined if a1=0 and a2=0.

## EXP(a)
Natural exponential: eᵃ.

## LOG(a)
Natural logarithm. Defined only for a > 0.

## SINH(a) / COSH(a) / TANH(a)
Hyperbolic functions. **TANH** useful as a smooth sigmoid approximation:
`0.5*(1+TANH(k*(x-x0)))` ≈ Heaviside step with width ~1/k.

## IF(test : lt, eq, gt)
Arithmetic conditional. Returns:
- `lt` if test < 0
- `eq` if test = 0
- `gt` if test > 0
- **Critical:** The resulting function must be continuous, otherwise the integrator may fail. For MOTION expressions, continuous second derivative is also required. **Prefer STEP/STEP5** over IF for most force/motion applications.
- **Example:** `IF(MODE-4 : 0, 0, force_expr)` — apply force only during dynamic analysis.

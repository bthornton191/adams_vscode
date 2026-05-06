# Debugging Guide: EPRINT and Step/Iteration Diagnostics

## What EPRINT Shows

Enable with `DEBUG/EPRINT` in the dataset (statement) or `debug/eprint` (command during `.acf` run).

Each step produces a message-file line. Sample:
```
>>> C  8  1  1.59E-04  1.20E-05  0  PART 3 DY      DIFF 12
```

| Column | Meaning |
|--------|---------|
| `>>> C` or `>>> P` | Corrector or Predictor phase |
| `8` | Step number |
| `1` | Iteration count (corrector) or integration order (predictor) |
| `1.59E-04` | Largest weighted error in the step (corrector: `‖residual‖`; predictor: integration error) |
| `1.20E-05` | Largest state correction magnitude |
| `0` | Jacobian evaluation flag: `0` = reused, `1` = newly evaluated |
| `PART 3 DY` | Body with largest correction (part ID 3, Y displacement) |
| `DIFF 12` | Element with largest residual error (DIFF element ID 12) |

---

## Predictor Phase (`>>> P`)
- Adams uses a polynomial predictor to estimate the next state from the last few accepted steps
- Predictor failures are rare; if the step size drops to HMIN it means the model is too stiff
- Third column in predictor lines is the **integration order** (1–6 for GSTIFF)

## Corrector Phase (`>>> C`)
- Newton-Raphson iteration to converge the algebraic-differential residuals
- Convergence criterion: `‖correction‖ < ERROR·‖scale‖` (element-wise, then global norm)
- **Too many corrector iterations** (MAXIT exceeded) → step is rejected, step size halved
- If step size reaches HMIN → simulation aborted with "HMIN exceeded" error

---

## Reading EPRINT Output: Diagnosis Steps

### Step 1 — Find the problematic element
Look for the **element ID** in the last column (e.g., `CONTACT 7`, `DIFF 12`, `VARIABLE 44`).

### Step 2 — Identify the DOF
The body/variable column (e.g., `PART 3 DY`) tells you:
- Which body (`PART 3`)
- Which generalised coordinate (`DX/DY/DZ` = translational; `Ψ/Θ/Φ` = Euler angles)
- `Q` prefix on system elements = their state variable

### Step 3 — Track convergence trend
- Error increasing iteration-to-iteration → diverging Newton iteration
  - Cause: near-singular Jacobian, over-constrained model, or expression discontinuity
- Error decreasing slowly → stiff element or poorly scaled forces
  - Cause: very high stiffness ratio, CONTACT with large EXPONENT, or FRICTION stiction

### Step 4 — Check Jacobian flag
- Many consecutive `0` (reused) Jacobian flags → saved computation, usually fine
- Persistent `0` flags with slow convergence → PATTERN= settings reusing stale Jacobian
  - Fix: add `INTEGRATOR/CORRECTOR=MODIFIED` or change `PATTERN=TTT...`

---

## JMDUMP and RHSDUMP

Enable with `DEBUG/JMDUMP` or `DEBUG/RHSDUMP`.

**JMDUMP** — Jacobian matrix written to `<job>.jac`:
- Format: row, column, value triplets (or MATLAB sparse format with `/MATLAB`)
- Near-zero diagonal entries → singular/near-singular Jacobian → identify redundant constraint or zero-inertia part
- Large off-diagonal values connecting a constraint equation to an inertia DOF → stiff force element

**RHSDUMP** — Right-hand-side residual vector written to `<job>.rhs`:
- Each entry is the residual for one equation
- Large residuals at t=0 → initial condition assembly problem (check IC tolerances)
- Residuals that grow without bound → numerical instability or expression error

**MATLAB import**:
```matlab
[i, j, val] = textread('model.jac', '%d %d %f');
J = sparse(i, j, val);
spy(J)          % visualise sparsity pattern
cond(full(J))   % condition number (singular if > 1e12)
```

---

## Element Code Reference

Adams EPRINT uses these types in the last column:

| Code | Element Type |
|------|-------------|
| `PART` | Rigid body |
| `POINT_MASS` | Particle |
| `FLEX_BODY` | Flexible body |
| `DIFF` | User differential equation |
| `GSE` | General state equation |
| `LSE` | Linear state equation |
| `TFSISO` | Transfer function |
| `VARIABLE` | Algebraic variable |
| `JOINT` | Kinematic joint |
| `JPRIM` | Joint primitive |
| `GCON` | General constraint |
| `MOTION` | Prescribed motion |
| `SFORCE` | Single-component force |
| `VFORCE` | Vector force |
| `GFORCE` | Generalized force |
| `BEAM` | Beam element |
| `BUSHING` | Bushing |
| `CONTACT` | Contact |
| `SPRINGDAMPER` | Spring-damper |
| `NFORCE` | N-body force |
| `FRICTION` | Friction |

---

## Common EPRINT Patterns and Fixes

| EPRINT Pattern | Root Cause | Fix |
|----------------|-----------|-----|
| Same element ID in every iteration, error not decreasing | Expression discontinuity (IF function, STEP at boundary) | Smooth the expression; widen STEP transition; add HMAX limit |
| `CONTACT` ID dominating, many iterations | Penetration too deep, STIFFNESS too high, EXPONENT > 2 | Reduce STIFFNESS×10; set EXPONENT=1.5; add DMAX; use CORRECTOR=MODIFIED |
| `FRICTION` element, stiction loop | Transition velocity too small | Increase STICTION_TRANSITION_VEL to ≥ 0.1 mm/s |
| Euler angle component (`Ψ/Θ`) for ground-connected part | Over-constraint or redundant joint | Count DOFs; remove duplicate constraint or add JPRIM |
| Progressive step-size reduction to HMIN | Highly stiff forces or near-singular Jacobian | Check force magnitudes; add damping; switch to WSTIFF/SI2 |
| Error spike exactly at specified time | SENSOR trigger or motion discontinuity | Enable BISECTION on SENSOR; smooth motion profile |

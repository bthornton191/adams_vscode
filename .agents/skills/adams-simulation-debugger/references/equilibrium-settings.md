# Equilibrium Settings Reference

## Parameter Reference

### ERROR
- Force/torque residual tolerance for equilibrium convergence; default = `1e-4`
- Units: model force units
- Reduce to `1e-6` for precise load extraction; increase to `1e-3` if high geometric compliance
- Both ERROR and IMBALANCE must be satisfied for convergence

### IMBALANCE
- Displacement correction tolerance; default = `1e-4`
- Units: model length units (translational), radians (rotational)
- Controls Newton step size acceptance, not just final residual
- Typically matches ERROR; loosen if model has soft compliant joints

### MAXIT
- Maximum Newton iterations; default = `25`
- Typical converged solution needs 3–8 iterations; hitting MAXIT → static failure
- Increase to 50 or 100 only after checking ALIMIT/TLIMIT are not the bottleneck

### ALIMIT
- Maximum angular correction per Newton iteration; default = π/6 rad (~30°)
- Reduce if large rotation steps cause the solver to "jump" to a wrong configuration
- Increase if initial conditions are far from equilibrium (e.g., `ALIMIT=3.14` for π rad max swing)
- Adams documentation guideline: keep at default for most models; reduce for constrained rotation

### TLIMIT
- Maximum translational correction per Newton iteration; default = 100 (model length units)
- Reduce below the characteristic dimension of the model to prevent large steps
- Example: 500 mm link → set TLIMIT=50 mm to keep steps within 10% of model scale

### STABILITY
- Multiplier `α` for stiffness augmentation: adds `α·(M+C)` to the stiffness matrix
- Default = `1e-5`; range: `0` (no augmentation) to `~1.0`
- Use when model has neutrally-stable DOFs (zero-frequency modes at equilibrium)
- Increase in steps: `1e-4`, `1e-3`, `1e-2`, `0.1`
- Too high → artificial stiffness distorts equilibrium position; check residual after solving

### PATTERN
- Same format as INTEGRATOR/PATTERN — controls Jacobian reuse during Newton iterations
- Default: `TFFFFFFFFF` (evaluate Jacobian once per iteration sequence)
- For very nonlinear static problems: use `TTTTFFFFFF`

### METHOD
| Value | Algorithms Tried |
|-------|-----------------|
| `ORIGINAL` | Standard Newton-Raphson only |
| `ADVANCED` | Newton; if fails → Trust-Region; if fails → Tensor-Krylov |
| `AGGRESSIVE` | Extends ADVANCED with more aggressive Armijo line search |
| `ALL` | All above + Broyden-Armijo + Hooke-Jeeves pattern search |

- `ORIGINAL` is the default and fastest
- **Try `ADVANCED` first** when ORIGINAL fails — it usually succeeds without parameter changes
- `ALL` is the last resort; slower but will find equilibrium in pathological geometric configurations

---

## Static Funnel Technique

Used when the model geometry is far from equilibrium and Newton-Raphson diverges.

**Concept**: run a series of short quasi-static analyses with progressively increasing load/motion, using the end state as IC for the next segment.

**ACF Example**:
```adams_acf
! Step 1: gravity off, apply 10% of load
equilibrium/error=1e-2, maxit=50, method=advanced
simulate/static, end_time=0.1, steps=10

! Step 2: gravity on, relax tolerances less
equilibrium/error=1e-3
simulate/static, end_time=0.2, steps=20

! Step 3: full load, tight tolerances
equilibrium/error=1e-4
simulate/static, end_time=1.0, steps=100
```

**When to use**:
- Model starts far from equilibrium (e.g., unloaded structure subject to gravity)
- Large initial geometric mismatch (assembled in wrong configuration)
- Contact-loaded models where contact patches need to form gradually

---

## STABILITY Parameter: Practical Steps

```
Static simulation failing with "Equilibrium not found"?
  1. Add EQUILIBRIUM/STABILITY=1e-4 to dataset
  2. If still failing → 1e-3
  3. If still failing → 1e-2 (unusual, indicates genuine mechanism DOF)
  4. Check for neutrally-stable DOF (mechanism mode, free part, unconstrained rotation)
  5. If >1e-2 needed → model has a real free DOF; must constrain it
```

---

## Common Static Failure Patterns

| Error Message | Cause | Fix |
|---------------|-------|-----|
| `Equilibrium not found after N iterations` | Newton diverging or oscillating | Try METHOD=ADVANCED; increase STABILITY; use static funnel |
| `Largest residual: PART X DY` | Gravity load unbalanced on part X | Check for missing ground connection or wrong ACCGRAV direction |
| `Model has zero stiffness in direction...` | Rigid body mode at equilibrium | Add soft joint or increase STABILITY; check constraint count |
| `IC assembly failed` | Initial conditions inconsistent | Correct geometry; adjust ALIMIT/TLIMIT; use IC/MAXIT=100 |
| Static OK but dynamic diverges immediately | Equilibrium found at metastable configuration | Perturb IC slightly; verify STABILITY value is not masking real DOF |

---

## Quasi-Static vs. True Static

| Analysis | Command | When to Use |
|----------|---------|-------------|
| True static | `SIMULATE/STATIC` | Single configuration, velocity=0 |
| Quasi-static | `SIMULATE/QUASISTATIC` | Slowly varying loads; implicit quasi-static path |
| Transient static ramp | `SIMULATE/TRANSIENT` with slow time input | When quasi-static fails; explicit integration handles dynamics |

- Quasi-static uses static solver at each output step — subject to same EQUILIBRIUM settings
- Transient ramp avoids static solver entirely; trade-off: more time steps required

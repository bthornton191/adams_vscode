# Integrator Settings Reference

## Integrator Selection Guide

| Integrator | Formulation | Best For |
|-----------|-------------|---------|
| GSTIFF/I3 | BDF (variable-order), index-3 | Default; general multibody dynamics |
| GSTIFF/SI2 | BDF, index-2 | Better velocity accuracy; recommended for most models |
| WSTIFF/SI2 | Wielenga BDF, index-2 | WSTIFF adds INTERPOLATE=ON; ensures constraint satisfaction at output steps |
| HASTIFF/SI1 | Modified BDF, index-1 | Highly nonlinear or impulsive models |
| HHT | Hilber-Hughes-Taylor | Structural/flexible body dynamics; unconditionally stable |
| NEWMARK | Newmark-β | Rigid + flexible body dynamics; user-controlled numerical damping |

---

## Key Parameters

### ERROR
- Global error tolerance (weighted `L2` norm); default = `1e-3`
- HHT/Newmark default = `1e-5` (implicit structural formulation needs tighter tolerance)
- Reducing ERROR from 1e-3 to 1e-4 roughly doubles execution time
- Use `1e-4` as the first fix for erratic high-frequency results
- Do *not* set below `1e-10`; round-off errors dominate below this level

### HMAX / HMIN
- HMAX: maximum allowed step size (default = output step size / 2)
- HMIN: minimum allowed step size; default = `1e-12` s
  - Note: HMIN is in seconds regardless of UNITS setting
- Reducing HMAX forces smaller steps through rapid-change regions (contact impacts, step functions)
- If simulation aborts at HMIN → something is preventing corrector convergence

### HINIT
- Initial step size; default: solver selects automatically
- For impulsive start conditions, set HINIT to a small value (e.g., `1e-5`) to give the integrator a stable start

### MAXIT
- Maximum corrector iterations per step; default = `10`
- If MAXIT is hit regularly → step is rejected and halved
- Increasing MAXIT beyond 10 rarely helps; address the root cause instead
- Symptom: message file shows many `>>>C` lines with same step number

### KMAX
- Maximum integration order; default = `6` (GSTIFF)
- Lower KMAX (e.g., 2 or 3) for highly nonlinear or impulsive models to improve stability
- Low-order stiff integrator may be more robust than high-order with large steps

### CORRECTOR
| Value | Behaviour |
|-------|-----------|
| `ORIGINAL` | Evaluates Jacobian based on PATTERN (default) |
| `MODIFIED` | Re-evaluates Jacobian at every corrector iteration; slower but more robust |
| `ORIG_CONSTANT` | Evaluates Jacobian once at start; use only for near-linear models |

- **CORRECTOR=MODIFIED** is the most important single setting to add for contact-heavy models

### PATTERN
- 10-character string of `T` (evaluate) and `F` (reuse) for corrector iterations 1–10
- Default: `TFFFFFFFFF` (evaluate only on first iteration)
- Changing to `TTFFFFFFFF` or `TTTTFFFFFF` helps when Jacobian goes stale mid-iteration
- Full `TTTTTTTTTT` equivalent to CORRECTOR=MODIFIED

### INTERPOLATE (WSTIFF only)
- `ON`: solver re-runs IC assembly at every output step to enforce exact constraint satisfaction
- Recommended for models with joints and non-trivial constraint equations
- Adds computation proportional to output step count

### ALPHA (HHT only)
- Numerical damping coefficient; range `[-1/3, 0]`; recommended: `-0.05`
- More negative = more damping of high-frequency modes; may under-damp slow dynamics
- Set `ALPHA=0` for undamped HHT (equivalent to Newmark trapezoidal)

### FIXIT
- Forces `FIXIT` fixed corrector steps per output interval; disables adaptive step control
- Used for real-time simulation hardware-in-the-loop applications
- Dramatically reduces solution quality — only for cosimulation I/O synchronisation

---

## Switching Strategy for Convergence Problems

```
GSTIFF/I3 failing?
  ├─ Try GSTIFF/SI2 (better velocity accuracy, often more stable)
  ├─ Try WSTIFF/SI2 (for constraint-heavy or flexible models)
  ├─ If impulsive: try HASTIFF/SI1 or GSTIFF/I3 with KMAX=3
  └─ If flexible bodies: try HHT with ALPHA=-0.05, ERROR=1e-5
```

---

## Interaction with Other Settings

| Problem | Integrator Setting | Companion Setting |
|---------|--------------------|-------------------|
| High-frequency noise | HMAX = output_step/10 | ERROR = 1e-4 |
| Contact spikes | CORRECTOR=MODIFIED | HMAX = contact_event_duration/100 |
| Stiction oscillation | None (integrator won't fix friction) | FRICTION/STICTION_TRANSITION_VEL |
| Flexible body chatter | HHT, ALPHA=-0.05 | FLEX_BODY/DAMPING=MODAL |
| Linearization fails | WSTIFF/SI2, INTERPOLATE=ON | IC/ERROR=1e-10 |

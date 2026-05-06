# Common Error Messages Reference

## Convergence Failure Errors

### `HMIN exceeded at T = <time>`
**Meaning**: The integrator reduced the step size below HMIN without achieving convergence.
**Root causes**:
- Highly stiff force (large stiffness, low damping) — CONTACT or SPRINGDAMPER
- Expression discontinuity (jump in FUNCTION= expression without smoothing)
- Near-singular Jacobian (zero-inertia part, over-constrained model, or degenerate contact)
**Fix sequence**:
1. Enable `DEBUG/EPRINT` — note which element/DOF dominates
2. Add `INTEGRATOR/CORRECTOR=MODIFIED`
3. Reduce `INTEGRATOR/HMAX` to 1/10th of the event duration
4. Smooth discontinuous expressions (`STEP` instead of `IF`)
5. For contact: reduce `STIFFNESS`, check `DMAX`, verify geometry normals

---

### `Equilibrium not found after N iterations`
**Meaning**: Static or quasi-static Newton-Raphson did not converge within MAXIT iterations.
**Root causes**:
- Model far from equilibrium at start configuration
- Neutral mode / mechanism DOF with zero stiffness
- Over-constrained model preventing rigid-body equilibration
**Fix sequence**:
1. Try `EQUILIBRIUM/METHOD=ADVANCED` first
2. Add `EQUILIBRIUM/STABILITY=1e-4` (increase to 1e-3, 1e-2 if needed)
3. Reduce `EQUILIBRIUM/ALIMIT` to 0.1 rad, `TLIMIT` to 10 mm to prevent overshoot
4. Use static funnel (series of short static analyses with ramped loading)
5. Check DOF count with `simulate/static` messages

---

### `Initial conditions inconsistent`
**Meaning**: IC assembly (Newton solve for consistent q, q̇, q̈ at t=0) failed.
**Root causes**:
- Conflicting joint + motion constraints (position overdetermined)
- Marker orientations prevent joint from assembling at t=0
- Part initial positions violating joint geometry
**Fix sequence**:
1. Increase `IC/MAXIT=100`
2. Separate declaration of position from orientation: check `QG` and `REULER` on markers
3. Check joint I and J marker Z-axis alignment (REVOLUTE, TRANSLATIONAL require co-linear Z)
4. Verify initial position satisfies all constraint equations geometrically

---

### `Singular Jacobian at T = <time>`
**Meaning**: Jacobian matrix becomes numerically singular — cannot be factored.
**Root causes**:
- Redundant constraint (two constraints imposing same restriction)
- Zero effective mass in a DOF driven by a stiff constraint
- All forces perpendicular to a free DOF (no restoring stiffness)
**Fix sequence**:
1. Use `DEBUG/JMDUMP,MATLAB` — check condition number of sparse Jacobian
2. Count constraints vs. DOFs: joints remove DOFs; verify model is not over-constrained
3. Add small mass to massless parts: `PART/1, MASS=1e-6, ...`
4. Add a soft spring/damper to strongly under-constrained directions

---

### `User function/routine failed` or `GFOSUB returned error`
**Meaning**: A user subroutine (GFOSUB, SFOSUB, REQSUB, etc.) returned a non-zero error flag.
**Root causes**:
- Array index out of bounds in subroutine
- Division by zero or NaN/Inf in force expression
- User expression evaluated at non-physical state (negative under a square root)
**Fix sequence**:
1. Add `DEBUG/EPRINT` — note which element ID triggers the error
2. Add guard conditions to the subroutine: `IF (x > 0.0) THEN ... ELSE ...`
3. For derivative evaluation calls, check the `IFLAG` argument (do not apply forces when `IFLAG >= 1`)
4. Print intermediate variables to message file to trace calculation failure

---

### `Step size < HMIN` after contact event
**Meaning**: Contact impact causes extreme stiffness spike.
**Root causes**:
- Geometry overlap at t=0 (initial penetration)
- Very high CONTACT/STIFFNESS with small DMAX
- EXPONENT > 2
**Fix sequence**:
1. Verify no overlap at initial configuration (check geometry in Adams View)
2. Reduce STIFFNESS by 10×; increase DMAX to 0.1 mm minimum
3. Set `INTEGRATOR/CORRECTOR=MODIFIED, HMAX=1e-4`
4. Switch to `INTEGRATOR/WSTIFF/SI2` for hard impact problems

---

### `GSE/LSE state did not converge during IC assembly`
**Meaning**: System element states could not be initialised consistently.
**Root causes**:
- Missing `STATIC_HOLD` flag when system element has dynamic-only states
- IC array values inconsistent with model equilibrium
**Fix sequence**:
1. Add `STATIC_HOLD` to GSE/LSE/TFSISO/DIFF elements with dynamic-only behaviour
2. Set IC_ARRAY values to zero for all states (let static analysis find equilibrium)
3. Check that U_ARRAY inputs are defined and non-singular at t=0

---

## Warning Messages

### `Integration order reduced to 1`
- Solver is struggling with rapidly changing state — common during contact events
- Not fatal; if persistent over many steps, reduce HMAX or smooth forcing functions

### `Jacobian not evaluated for N consecutive steps`
- PATTERN setting is reusing old Jacobian across too many steps
- OK if converging well; problematic if error is slowly growing
- Fix: change `PATTERN=TTFFFFFFFF` or use `CORRECTOR=MODIFIED`

### `Equilibrium converged with STABILITY augmentation`
- The stiffness matrix was augmented to achieve convergence
- Check whether a real DOF is being masked; verify equilibrium is physically meaningful

### `Flex body modal coordinates exceeding limit`
- Modal amplitudes large enough to violate small-deformation assumption
- Reduce load or add FLEX_BODY/DAMPING; consider reducing active MODES count

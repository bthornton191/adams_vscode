# Troubleshooting Decision Flowchart

## Start: Identify the Failure Mode

```
Simulation fails or gives bad results
│
├─ 1. STATIC / EQUILIBRIUM failure ────────────────────────────┐
│                                                               ↓
├─ 2. DYNAMIC divergence / HMIN exceeded ──────────────────┐   │
│                                                           ↓   │
├─ 3. Solution converges but results look wrong ────────┐   │   │
│                                                        │   │   │
└─ 4. Simulation is too slow ───────────────────────┐   │   │   │
                                                    ↓   ↓   ↓   ↓
                                            See sections below
```

---

## 1. Static / Equilibrium Failure

**Symptom**: "Equilibrium not found after N iterations"; static analysis returns non-zero status

```
Step 1: Try METHOD=ADVANCED
   └─ If passes → done (add EQUILIBRIUM/METHOD=ADVANCED to dataset)
   └─ If fails → Step 2

Step 2: Add STABILITY augmentation
   ├─ Try STABILITY=1e-4 → still fails?
   ├─ Try STABILITY=1e-3 → still fails?
   ├─ Try STABILITY=1e-2 → still fails?
   └─ If >1e-2 needed → model has a real free DOF; constrain it

Step 3: Tighten Newton step limits
   └─ EQUILIBRIUM/ALIMIT=0.1, TLIMIT=10

Step 4: Check initial configuration
   ├─ Is geometry assembled correctly? (no overlapping parts)
   ├─ Is ACCGRAV direction correct for the model coordinate system?
   └─ Are all moving parts connected to ground (directly or via chain)?

Step 5: Use Static Funnel
   └─ Run series of short static analyses with ramped loading
      (see equilibrium-settings.md for ACF example)

Step 6: Enable EPRINT on short static run
   └─ DEBUG/EPRINT — identify which part/element has largest residual
```

**Key settings**: `EQUILIBRIUM/METHOD=ADVANCED, STABILITY=1e-4, ALIMIT=0.3, TLIMIT=50`

---

## 2. Dynamic Divergence / HMIN Exceeded

**Symptom**: Simulation stops with "HMIN exceeded" or step size decreases to tiny values

```
Step 1: Enable EPRINT
   └─ DEBUG/EPRINT — identify culprit element type and ID

Step 2: Classify element type

   ├─ CONTACT ──────────────────────────────────────────────────────────┐
   │   Symptoms: step drops during contact event                        │
   │   Fixes:                                                           │
   │   ├─ INTEGRATOR/CORRECTOR=MODIFIED                                 │
   │   ├─ INTEGRATOR/HMAX = (event_duration / 100)                      │
   │   ├─ CONTACT/STIFFNESS decrease by 10×                             │
   │   ├─ CONTACT/DMAX minimum 0.1 mm                                   │
   │   ├─ CONTACT/EXPONENT = 1.5 (Hertz) or 1.0 (compliant)            │
   │   └─ Verify no initial geometry penetration                        │
   │                                                                    │
   ├─ FRICTION ─────────────────────────────────────────────────────────┤
   │   Symptoms: oscillation in stiction zone                           │
   │   Fixes:                                                           │
   │   ├─ Increase STICTION_TRANSITION_VEL to ≥ 0.1 mm/s               │
   │   ├─ Reduce MU_STATIC / MU_DYNAMIC ratio                          │
   │   └─ Add SFORCE damping in joint to remove stiction hunting        │
   │                                                                    │
   ├─ DIFF / VARIABLE with IF or discontinuous expression ──────────────┤
   │   Symptoms: step drops at specific time; same instant each run     │
   │   Fixes:                                                           │
   │   ├─ Replace IF(cond:val1:val2) with STEP(expr, lo, val1, hi, val2)│
   │   ├─ Widen STEP transition zone                                    │
   │   └─ For physical discontinuity: SENSOR/BISECTION to find crossing │
   │                                                                    │
   ├─ SPRINGDAMPER or BEAM very high stiffness ─────────────────────────┤
   │   Symptoms: step drop from start; constant chatter                 │
   │   Fixes:                                                           │
   │   ├─ Reduce stiffness or add damping (CRATIO=0.01 for BEAM)        │
   │   ├─ Switch to INTEGRATOR/WSTIFF/SI2 or HASTIFF/SI1                │
   │   └─ Verify LENGTH/free length so preload is not artificially high │
   │                                                                    │
   └─ FLEX_BODY high-frequency chatter ─────────────────────────────────┘
       Symptoms: step drop with flexible body; high-freq noise in output
       Fixes:
       ├─ Switch from GSTIFF to HHT with ALPHA=-0.05, ERROR=1e-5
       ├─ Add FLEX_BODY/DAMPING=MODAL with DAMPING_RATIOS=0.01,...
       └─ Reduce active MODES count (remove high-frequency modes)

Step 3: General integrator tuning
   ├─ INTEGRATOR/ERROR=1e-4 (tighten to reduce error estimate mismatch)
   ├─ INTEGRATOR/KMAX=3 (lower order = more robust for impulsive models)
   └─ Try WSTIFF/SI2 if GSTIFF/I3 or GSTIFF/SI2 fails

Step 4: Check model topology
   ├─ Is there a massless part? → Add MASS=1e-6 (very small)
   ├─ Is DOF count correct? (Adams shows DOF in simulation output)
   └─ Are there redundant constraints? → Remove duplicate joints
```

**Key settings**: `INTEGRATOR/CORRECTOR=MODIFIED, HMAX=1e-4, GSTIFF/SI2`

---

## 3. Solution Converges But Results Look Wrong

**Symptom**: Simulation completes but forces/motion don't match expectations

```
Step 1: Check UNITS
   └─ Are ACCGRAV values correct for unit system?
      MKS → JGRAV=-9.80665; IPS → JGRAV=-386.09

Step 2: Verify marker frame orientations
   └─ SFORCE/VFORCE resolved along/in I marker Z-axis / RM marker frame
   └─ Check RM vs JFLOAT: VFORCE resolved in RM, not in moving I frame

Step 3: Check reference frame for measurements
   └─ REQUEST/RM: results in global unless RM= specified
   └─ DM(I,J): total distance, not relative to any axis

Step 4: Validate initial conditions
   └─ Part velocities in global frame (PART/VX,VY,VZ = global components)
   └─ Initial Euler angles in radians unless D suffix used

Step 5: Check ACTIONONLY flags
   └─ ACTIONONLY forces do not apply reaction to J marker
   └─ Missing ACTIONONLY → unexpected torques on ground

Step 6: Inspect EPRINT for unexpected element activity
   └─ A constraint showing residual in a supposedly rigid connection
      may mean incorrect joint type
```

---

## 4. Simulation Too Slow

**Symptom**: Acceptable results but simulation takes too long

```
Step 1: Profile with EPRINT
   └─ Which elements dominate Newton iterations?

Step 2: Reduce output resolution
   └─ Increase output step → fewer WSTIFF IC assemblies & less I/O

Step 3: Relaxing integrator settings safely
   └─ INTEGRATOR/ERROR=1e-3 (default; loosen to 5e-3 only if physics allows)
   └─ INTEGRATOR/HMAX=larger value if dynamics are slow relative to stiffness

Step 4: Use adaptive Jacobian
   └─ INTEGRATOR/CORRECTOR=ORIGINAL (default — reuses Jacobian)
   └─ INTEGRATOR/PATTERN=TFFFFFFFFF (evaluate Jacobian less frequently)

Step 5: Parallelism
   └─ PREFERENCES/NTHREADS=N (set to physical core count)

Step 6: Contact optimisation
   └─ Use convex-hull or simplified geometry for contact bodies
   └─ Reduce number of active contact pairs
   └─ Set PREFERENCES/CONTACT_GEOMETRY_LIBRARY=Default_library (faster than Parasolid)

Step 7: Flex body mode reduction
   └─ FLEX_BODY/MODES=id1,id2,...  (select only modes below highest frequency of interest)
   └─ FLEX_BODY/FORMULATION=OPTIMIZED via PREFERENCES
```

---

## Quick Reference: Most Impactful Single Changes

| Scenario | Highest-Impact Setting |
|----------|----------------------|
| Static fails, mystery | `EQUILIBRIUM/METHOD=ADVANCED` |
| Static fails, neutral mode | `EQUILIBRIUM/STABILITY=1e-4` |
| Dynamic HMIN, contact | `INTEGRATOR/CORRECTOR=MODIFIED` |
| Dynamic HMIN, general | `INTEGRATOR/GSTIFF, SI2, ERROR=1e-4` |
| Flex body chatter | `INTEGRATOR/HHT, ALPHA=-0.05` |
| Friction stiction loop | `FRICTION/STICTION_TRANSITION_VEL=0.1` |
| Step drive discontinuity | Replace `IF` with `STEP` function |
| Too slow, contact model | `PREFERENCES/NTHREADS=N` |
| Too slow, general | `INTEGRATOR/ERROR=1e-3, HMAX=larger` |

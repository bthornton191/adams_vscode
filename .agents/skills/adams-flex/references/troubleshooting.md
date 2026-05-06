# Flex Body Troubleshooting Reference

## Table of Contents
1. [Pre-Simulation Checklist](#pre-sim)
2. [Verification via Adams Linear](#verification)
3. [Troubleshooting Decision Tree](#decision-tree)
4. [Common Problems Table](#common-problems)
5. [Mode Diagnostics](#mode-diagnostics)
6. [Performance Tuning](#performance)
7. [Solver Debug Commands](#debug-commands)

---

## Pre-Simulation Checklist {#pre-sim}

Run these checks before every flex body simulation:

- [ ] **Info tool** on flex body: units correct, mass matches FEA value
- [ ] **DOF count** in first run's `.msg` file matches expectation (rigid-body DOF + 6 per attachment node + 1 per active mode)
- [ ] **Mode count**: is `selected_modes` set, or are all modes active?
- [ ] **Damping specified**: default (frequency-dependent 1%/10%/100%) or custom?
- [ ] **Marker-node assignment** reviewed (if recently replaced rigid body)
- [ ] **Solver version known**: FORTRAN or C++? (affects connection limitations — see connections.md)
- [ ] **Adams Linear run** (optional but recommended on first import): frequencies match FEA?

---

## Verification via Adams Linear {#verification}

Adams Linear (optional module) computes eigenvalues of the linearized system, allowing direct comparison with FEA natural frequencies.

### Procedure
1. Create a test model with only the flex body, constrained to ground with the same boundary conditions as the FEA model
2. Run a static equilibrium to an unloaded state
3. Run Adams Linear: `Simulate → Linear Analysis → Calculate` (or `LINEAR/EIGENSOL` in `.acf`)
4. Compare reported frequencies with FEA predictions

### Pass Criteria
- Frequencies should agree within 5–10%
- All expected modes present, no extra spurious modes with non-zero frequency

### What Mismatches Indicate
| Mismatch | Likely Cause |
|---|---|
| All frequencies shifted by a factor | Unit inconsistency (e.g., mm vs m) |
| Frequencies too high | Too many constraint modes relative to FEA setup |
| Extra near-zero frequency modes | Spurious rigid body modes in MNF |
| Missing modes | MNF generated with too few modes for frequency range |
| Large errors (>20%) at specific mode | Modal truncation — increase mode count |

---

## Troubleshooting Decision Tree {#decision-tree}

```
Flex Body Simulation Problem
│
├─ FAILS TO START / CREATE
│  ├─ "Flex body not created" / import error
│  │  ├─ Check: MNF file path correct and accessible?
│  │  ├─ Check: MNF file format compatible with Adams version?
│  │  │  └─ MNF with shortened stress/strain modes (Nastran 2005+) is
│  │  │     incompatible with Adams < 2005 — use mnf2mtx optimizer to convert
│  │  └─ Check: MD DB index correct (1-based)?
│  │
│  ├─ Initial condition error at t=0
│  │  ├─ Set modal_exact_coordinates = True
│  │  └─ Check: are initial modal displacements physically possible?
│  │
│  └─ Equilibrium failure at t=0
│     ├─ EQUILIBRIUM/METHOD=ADVANCED, STABILITY=1e-4
│     ├─ Check: are all markers connected to correct nodes?
│     └─ Check: are there conflicting ICs on connected rigid bodies?
│
├─ HMIN EXCEEDED (dynamic simulation diverges)
│  │
│  ├─ Step 1: Enable EPRINT to identify the failing element
│  │  └─ DEBUG/EPRINT in .acf → read .msg file for largest residuals
│  │
│  ├─ High-frequency mode chatter (most common cause)
│  │  ├─ Identify: step size drops to ~1e-7 s or smaller
│  │  ├─ Fix A: Switch to HHT integrator (numerical damping)
│  │  │  └─ INTEGRATOR/HHT, ALPHA=-0.05, ERROR=1e-5
│  │  ├─ Fix B: Damp high-freq modes to 100% critical
│  │  │  └─ damping_ratio = 'IF(FXFREQ(id) - 500: 0.01, 0.01, 1.0)'
│  │  └─ Fix C: Disable modes above frequency cutoff entirely
│  │     └─ selected_modes = list(range(1, N))  # drop high-freq modes
│  │
│  ├─ Contact at flex body (flex-to-rigid or flex-to-flex)
│  │  ├─ INTEGRATOR/CORRECTOR=MODIFIED, HMAX=1e-4
│  │  └─ Reduce CONTACT/STIFFNESS by 10× and re-test
│  │
│  ├─ Stiff connector (beam/bushing/spring on massless link)
│  │  ├─ INTEGRATOR/WSTIFF/SI2 or GSTIFF/KMAX=1
│  │  └─ Check: preload not artificially high due to misalignment
│  │
│  └─ Massless part has zero mass/inertia causing solver singularity
│     └─ Add small mass: dummy.mass = 1e-6
│
├─ RESULTS CONVERGE BUT LOOK WRONG
│  │
│  ├─ Deformation in wrong direction / wrong magnitude
│  │  ├─ Check: coordinate frame — is MNF in same units as Adams model?
│  │  └─ Check: marker orientation correct for force direction
│  │
│  ├─ Rigid-body motion coupling error
│  │  ├─ Try FLEX_BODY_FORMULATION = ORIGINAL (most accurate)
│  │  └─ Is deformation > 10% of feature size? Consider nonlinear approach
│  │
│  ├─ Modal truncation artifact (e.g., body too stiff or too flexible)
│  │  ├─ Enable more modes, re-run Adams Linear verification
│  │  └─ Check: mode shapes correct using Flex Toolkit Browser
│  │
│  └─ Damping mismatch
│     └─ Verify damping_ratio setting; re-check default vs custom
│
└─ SIMULATION TOO SLOW
   ├─ Disable non-essential modes (see flex-body-setup.md — Strain Energy)
   ├─ Reduce active mode count (start at 10, add until results converge)
   ├─ Switch to Optimized or Max Optimization formulation (if compatible)
   ├─ Increase integrator error tolerance: INTEGRATOR/ERROR=1e-3
   └─ Use PREFERENCES/NTHREADS=N for multi-core parallelism
```

---

## Common Problems Table {#common-problems}

| Problem | Symptom | Root Cause | Solution |
|---|---|---|---|
| Spurious rigid body modes | Near-zero frequency extra modes; body drifts | FEA boundary conditions not correct; numerical solver artifact | Animate modes in Flex Toolkit to identify; disable in Adams |
| Unit mismatch | All frequencies wrong by √1000 (or similar factor) | MNF in mm, Adams in m (or vice versa) | Verify units with Info tool; regenerate MNF with correct units |
| Mode truncation | Body behaves too stiffly in one direction | Insufficient modes in MNF for frequency range | Increase mode count in FEA MNF generation; re-import |
| Over-constrained massless link | Auto-link warnings in `.msg` | Multiple unsupported elements on same flex body node | Use single massless link per flex body region; share via fixed joint |
| Large MNF file / slow simulation | Import takes minutes; simulation 10× slower than expected | Stress/strain modes retained, too many nodes | Optimize MNF in Flex Toolkit: coarsen mesh, shorten stress modes |
| Contact divergence | HMIN exceeded when flex contacts rigid | High contact stiffness + fine mesh | Reduce contact stiffness; use C++ solver; increase HMAX for contact |
| Generalized damping + Optimized formulation | Adams error at setup | Generalized damping unsupported with non-Original formulation | Switch to Original formulation or disable generalized damping |
| Marker snaps at t=0 | Large initial residual, body jumps | Approximate modal ICs + IC violation | Set `modal_exact_coordinates = True` |
| Missing attachment nodes | Joints disconnect after rigid-to-flex swap | MNF has no interface nodes at required locations | Re-generate MNF with correct attachment points; or use massless link |

---

## Mode Diagnostics {#mode-diagnostics}

### Animate Mode Shapes (Flex Toolkit)
1. Open Adams Flex Toolkit: Tools → Adams Flex Toolkit
2. Open MNF/MD DB browser
3. Select a mode number
4. Click Animate — watch for unexpected deformations:
   - **Expected**: smooth structural bending/torsion shape
   - **Suspicious**: whole-body translation or rotation (rigid body mode)
   - **Problematic**: chaotic node movement (numerical artifact — disable this mode)

### Check Mode Participation in Results
After simulation, examine modal coordinate time histories:
- Modal coordinate magnitude < 1e-7 → mode not contributing; safe to disable
- High-frequency oscillation in modal coordinates → mode causing step-size issues; damp or disable

### Strain Energy Analysis (Adams View)
1. Run pilot simulation
2. Flexible Body Modify → Auto Disable Modes by Strain Energy
3. Set tolerance = 0.001 (0.1%)
4. Review list of disabled modes — verify none are expected contributors

---

## Performance Tuning {#performance}

| Action | Typical Speedup | Risk |
|---|---|---|
| Reduce active modes from 40 → 15 | 3–5× | May miss high-freq response |
| Switch Formulation: Original → Optimized | 1.5–2× | Reduced accuracy for large deformations |
| Disable modes > 10× system frequency | 2–4× | Low risk if cutoff chosen correctly |
| Increase integrator error to 1e-3 | 1.5–2× | Reduced accuracy; check results |
| Use NTHREADS = N | Up to N× (diminishing returns) | None |
| Optimize MNF (mesh coarsen) | 2–10× animation | No physics impact — mesh only |

---

## Solver Debug Commands {#debug-commands}

Add to `.acf` command file:

```
! Print Newton iteration details — identifies which element has the largest residual
DEBUG/EPRINT

! Dump Jacobian matrix for rank analysis (verbose — use only for deep debugging)
DEBUG/JMDUMP

! Dump right-hand-side vector (helps find singular directions)
DEBUG/RHSDUMP
```

Read the `.msg` file after the run — search for:
- `ELEMENT` followed by a large force residual → that element is causing the failure
- `FLEX_BODY` in the residual list → mode or damping issue
- Massless link warnings → auto-created massless link — check if expected

For general solver diagnostics beyond flex bodies, see the `adams-simulation-debugger` skill.

# Solver Statements Reference — Adams Flex

This file covers the `.adm` dataset and `.acf` command file syntax for flex body elements. The `.adm` file defines the model topology; the `.acf` file controls simulation execution.

## Table of Contents
1. [FLEX_BODY Statement](#flex-body)
2. [MARKER on Flex Body](#marker)
3. [MATRIX Statements](#matrix)
4. [MFORCE Statement](#mforce)
5. [Damping Expressions](#damping-expressions)
6. [Solver Control for Flex Bodies](#solver-control)
7. [Runtime Representation Toggle](#representation)

---

## FLEX_BODY Statement {#flex-body}

Defines a flexible body in the Adams dataset.

```
FLEX_BODY/id,
    MNF_FILE = filename,
  [ QG = x, y, z ],                  ! Global position of floating marker
  [ REULER = psi, theta, phi ],       ! Euler orientation (radians)
  [ VX = r, VY = r, VZ = r ],        ! Initial translational velocities
  [ WX = r, WY = r, WZ = r ],        ! Initial angular velocities
  [ DAMPING = {OFF | MODAL | STIFFNESS | COMBINED} ],
  [ ALPHA = r ],                      ! Stiffness-proportional Rayleigh coefficient
  [ BETA = r ],                       ! Mass-proportional Rayleigh coefficient
  [ CRATIO = expression ],            ! Critical damping ratio expression
  [ MODES = id1, id2, ..., idN ],    ! Active mode indices (omit = all modes)
  [ LABEL = c ]                       ! Optional name
```

### DAMPING Options
| Value | Description |
|---|---|
| `OFF` | No structural damping |
| `MODAL` | Per-mode critical damping via `CRATIO=` expression (most common) |
| `STIFFNESS` | Proportional damping: $C = \alpha M + \beta K$ via `ALPHA=`, `BETA=` |
| `COMBINED` | Both modal and proportional |

### CRATIO Expression
The `CRATIO` expression is evaluated once per mode when setting up damping. Use `FXFREQ()` and `FXMODE()` for frequency/mode-dependent damping:

```
! 1% below 100 Hz, 10% from 100-1000 Hz, 100% above 1000 Hz (default behavior)
CRATIO = IF(FXFREQ(FLEX_LINK) - 100: 0.01, 0.01,
           IF(FXFREQ(FLEX_LINK) - 1000: 0.10, 0.10, 1.0))

! Uniform 2% across all modes
CRATIO = 0.02
```

### Example
```
FLEX_BODY/10,
    MNF_FILE = flex_link.mnf,
    QG = 0.0, 0.0, 250.0,
    REULER = 0.0, 1.5708, 0.0,
    DAMPING = MODAL,
    CRATIO = 0.02,
    MODES = 1, 2, 3, 4, 5, 6, 7, 8,
    LABEL = FLEX_LINK
```

---

## MARKER on Flex Body {#marker}

Markers on a flex body reference a node in the MNF by `NODE_ID`.

```
MARKER/id,
    FLEX_BODY = flex_body_id,
    NODE_ID = node_number
  [ QP = dx, dy, dz ]               ! Optional offset from node (C++ solver only)
```

### Example
```
! Coincident marker at node 1247
MARKER/101, FLEX_BODY=10, NODE_ID=1247

! Offset marker — 5 mm in X from node (C++ solver only; auto massless link in FORTRAN)
MARKER/102, FLEX_BODY=10, NODE_ID=1247, QP=5.0, 0.0, 0.0
```

**Note**: When Adams View creates a flex body, it automatically generates a floating reference marker (the rigid-body 6 DOF marker) and assigns it `ID = flex_body_id * 10` by convention. Do not overwrite this marker.

---

## MATRIX Statements {#matrix}

The flex body solver uses matrix files (`.mtx`) generated automatically from the MNF at simulation startup, or pre-generated with `mnf2mtx`. The following matrix names are recognized:

| Matrix Name | Description |
|---|---|
| `GENSTIFF` | Generalized stiffness matrix |
| `INVAR1` … `INVAR9` | Nine inertia invariants |
| `T_MODE` | Translational mode shapes at all nodes |
| `R_MODE` | Rotational mode shapes at all nodes |
| `SELNOD` | Selected node IDs and coordinates with attachment flags |
| `SELMOD` | Selected mode indices and natural frequencies |
| `PRELOAD` | Preload case (if exported via mnfload) |
| `MODLOAD` | Applied modal load cases (if exported via mnfload) |
| `GENDAMP` | Generalized damping matrix (if `generalized_damping ≠ off`) |

These are normally managed automatically. You only reference them manually if using a pre-generated `.mtx` file:

```
MATRIX/201, FILE=flex_link.mtx, NAME=GENSTIFF
MATRIX/202, FILE=flex_link.mtx, NAME=INVAR1
```

---

## MFORCE Statement {#mforce}

Defines a modal force applied to a flex body in generalized (modal) coordinates.

```
MFORCE/id,
    FLEX_BODY = flex_body_id,
  [ FUNCTION = expression ],        ! Time/state-dependent scale factor
  [ LOAD_CASE = load_case_name ],   ! Named load case from MNF (via mnfload)
  [ LABEL = c ]
```

### Example — Time-Varying Modal Force
```
MFORCE/20,
    FLEX_BODY = 10,
    FUNCTION = STEP(TIME, 0.1, 0.0, 0.2, 1000.0),
    LABEL = AERO_LOAD
```

### Example — Named Load Case from MNF
```
MFORCE/21,
    FLEX_BODY = 10,
    LOAD_CASE = braking_load,
    FUNCTION = STEP(TIME, 0.5, 0.0, 0.6, 1.0),
    LABEL = BRAKING_CASE
```

---

## Damping Expressions {#damping-expressions}

Two special functions are available for flex body damping expressions:

### FXFREQ(flex_body_id)
Returns the natural frequency (Hz) of the current mode being evaluated. Use in `CRATIO` to create frequency-dependent damping.

```
! Damp everything above 200 Hz heavily
CRATIO = IF(FXFREQ(10) - 200: 0.01, 0.01, 0.5)
```

### FXMODE(flex_body_id)
Returns the mode index (integer) of the current mode. Use to apply different damping per mode index.

```
! Apply 5% damping to mode 1, 2% to all others
CRATIO = IF(FXMODE(10) - 1.5: 0.05, 0.05, 0.02)
```

---

## Solver Control for Flex Bodies {#solver-control}

Add to `.acf` (Adams command file):

```acf
! Use C++ solver (removes FORTRAN connection limitations)
PREFERENCES/SOLVER=CPP

! HHT integrator — recommended for flex bodies (numerical damping helps stability)
INTEGRATOR/HHT, ALPHA=-0.05, ERROR=1e-5, HMAX=1e-3

! GSTIFF integrator (default)
INTEGRATOR/GSTIFF, ERROR=1e-3, HMAX=1e-2

! Enable debug output — identifies failing element in .msg file
DEBUG/EPRINT

! Static analysis for initial equilibrium
EQUILIBRIUM/METHOD=ADVANCED, STABILITY=1e-4

! Dynamic simulation
SIMULATE/DYNAMIC, END=1.0, DTOUT=0.01
```

### Integrator Recommendations for Flex Bodies

| Situation | Recommended Integrator |
|---|---|
| General flex body dynamics | `GSTIFF, ERROR=1e-4` |
| High-frequency modes present | `HHT, ALPHA=-0.05, ERROR=1e-5` |
| Contact + flex | `GSTIFF, CORRECTOR=MODIFIED, HMAX=1e-4` |
| Stiff beams/bushings on flex | `WSTIFF/SI2` or `GSTIFF/KMAX=1` |
| Smooth, low-frequency system | `ABAM` (explicit — fastest for smooth flex) |

---

## Runtime Representation Toggle {#representation}

Switch a flex body between flexible and rigid representations during a simulation:

```acf
! At t=0, simulate as flexible
SIMULATE/DYNAMIC, END=0.5, DTOUT=0.01

! Switch to rigid at t=0.5 (saves cost during non-critical phase)
FLEX_BODY/10, REPRESENTATION=RIGID
SIMULATE/DYNAMIC, END=2.0, DTOUT=0.01

! Switch back to flexible at t=2.0
FLEX_BODY/10, REPRESENTATION=MODAL
SIMULATE/DYNAMIC, END=3.0, DTOUT=0.01
```

Note: No stress/strain data is generated during the `RIGID` phase.

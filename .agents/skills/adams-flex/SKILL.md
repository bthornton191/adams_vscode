---
name: adams-flex
description: >
  Work with flexible bodies in MSC Adams using Adams Flex. Use whenever the user
  mentions flexible bodies, flex bodies, MNF files, modal neutral files, MD DB
  files, Craig-Bampton reduction, or wants to add structural compliance. Also
  covers rotordynamics: gyroscopic effects, spin softening, stress stiffening,
  Campbell diagrams, critical speeds, and the Rotor Dynamics Simulation Series.
  Topics: importing MNF/MD DB files, creating and configuring flex bodies (mode
  selection, damping, formulation), connecting flex bodies (markers on nodes,
  massless links, joints, contacts), replacing rigid bodies with flex bodies,
  troubleshooting (HMIN exceeded, frequency mismatch, spurious rigid body modes),
  Adams Flex Toolkit (mnf2mtx, mnfload, MNF browser), post-processing (modal
  forces, deformation, stress/strain), and FLEX_BODY .adm syntax. Supports
  Python API (createFlexBody()) and CMD/GUI. Use even if user says "make my part
  flexible", "spinning shaft", "Campbell diagram", "critical speed", or
  "gyroscopic effects".
compatibility: github-copilot, claude-code, cursor, windsurf
metadata:
  version: 1.5.1
---

# Adams Flex

## Local Lessons Learned

At the start of every session, check whether `lessons-learned.md` exists in the skill folder. If it does, read it before proceeding — it contains field-discovered gotchas and workarounds specific to this skill.

---

You are an expert MSC Adams Flex developer. You help users integrate flexible bodies into multibody dynamics simulations — from importing MNF files through configuring modes and damping, connecting to the model, running and troubleshooting simulations, and post-processing results.

**Scope**: This skill starts from an existing MNF or MD DB file. It does not cover FEA model preparation, Nastran ADAMSMNF card syntax, or how to generate MNF files in Abaqus/ANSYS/Marc.

---

## Core Rules (Never Violate)

1. **Prefer the Python API for scripted flex body creation** — use `m.Parts.createFlexBody()` rather than wrapping `part create flexible_body name_and_position` in `Adams.execute_cmd()`. The CMD command exists but the Python API is the correct idiomatic path: it exposes `selected_modes`, `modal_exact_coordinates`, and typed parameters directly. When helping with CMD workflows, focus on modification commands and `.adm` dataset syntax.

2. **C++ is the default solver — FORTRAN is deprecated** — Adams has used the C++ solver as the default since Adams 2018. FORTRAN is all but deprecated and requires explicit opt-in (`PREFERENCES/SOLVERBIAS=F77`). Do not assume the user is on FORTRAN unless they say so. The FORTRAN solver has strict flex body connection limits (massless links required for bushings, beams, offset markers, etc.); the C++ solver removes nearly all of these restrictions.

3. **Specify damping explicitly** — never leave the default frequency-dependent damping without documenting it. The default (1%/10%/100% critical at 100/1000 Hz cutoffs) is often appropriate, but users must know it's there. Undocumented damping is a common source of confusing results.

4. **Never enable all modes blindly** — an MNF may contain 50–200 modes. Enabling all of them causes integrator step-size problems and slow simulations. The safe workflow is: start with 10–15 modes, verify results converge, then use strain energy auto-disable to trim. Always state this when helping a user set up a new flex body.

5. **Verify frequencies after every import** — run Adams Linear on the isolated flex body and compare natural frequencies with the FEA values. A 5–10% agreement is the benchmark. Mismatches indicate unit errors, translation problems, or insufficient modes before anything else.

6. **Massless links for unsupported elements (FORTRAN — legacy)** — on the deprecated FORTRAN solver, beams, bushings, field elements, torsion springs, and VFORCE/VTORQUE with the flex body as reaction body all require massless links. Auto-created massless links appear in the `.msg` file but their reaction forces are NOT available in results. On the modern C++ solver (the default), none of these restrictions apply. Only raise massless link requirements if the user is explicitly running the FORTRAN solver.

7. **Check DOF count after the first run** — the `.msg` file reports the total DOF. Expected formula: 6 (rigid body) + 6 × (number of interface nodes) + N (active modes). A mismatch means a node assignment error or an unexpected auto-massless-link.

8. **MNF file paths are NOT relative to the Adams View working directory** — always use absolute paths or paths relative to the dataset (`.adm`) file location. Relative paths that work interactively often break when batch-running.

9. **Use `modal_exact_coordinates = True` for initial conditions** — approximate modal ICs can cause body "snapping" at t=0. Exact is almost always the right choice.

10. **Cross-reference with sibling skills** — for general Adams Python patterns (array reassignment, marker location asymmetry), see `adams-python-model-builder`. For general solver debugging (EPRINT, equilibrium, integrator tuning), see `adams-simulation-debugger`. Don't duplicate their guidance.

---

## Quick Start — What Do You Want to Do?

| Task | Start Here |
|---|---|
| Import an MNF and create a flex body | [flex-body-setup.md](references/flex-body-setup.md) |
| Choose how many modes to use | [flex-body-setup.md → Mode Selection](references/flex-body-setup.md#mode-selection) |
| Set up damping | [flex-body-setup.md → Damping](references/flex-body-setup.md#damping) |
| Connect flex body to joints, forces, springs | [connections.md](references/connections.md) |
| Replace a rigid body with a flex body | [connections.md → Replacement](references/connections.md#replacement) |
| Create a marker on a specific node | [connections.md → Marker Placement](references/connections.md#marker-placement) |
| Add a bushing/beam to a flex body (FORTRAN) | [connections.md → Massless Link](references/connections.md#massless-link) |
| Use flex body contacts | [connections.md → Contacts](references/connections.md#contacts) |
| Simulation fails or diverges | [troubleshooting.md](references/troubleshooting.md) |
| Verify frequencies match FEA | [troubleshooting.md → Adams Linear](references/troubleshooting.md#verification) |
| Simulation too slow | [troubleshooting.md → Performance Tuning](references/troubleshooting.md#performance) |
| Optimize a large MNF file | [toolkit.md → Optimization](references/toolkit.md#optimization) |
| Add load cases to MNF | [toolkit.md → mnfload](references/toolkit.md#mnfload) |
| Convert MNF to MD DB | [toolkit.md → mnf2mtx](references/toolkit.md#mnf2mtx) |
| View deformation / stress in post-processing | [results.md](references/results.md) |
| Write or read the FLEX_BODY .adm statement | [solver-statements.md](references/solver-statements.md) |
| Rotordynamics: gyroscopic effects, spin softening, Campbell diagram, critical speeds | [rotordynamics.md](references/rotordynamics.md) |
| Set up spinning shaft or high-speed rotor | [rotordynamics.md → Setup](references/rotordynamics.md#setup) |
| Generate Campbell diagram (frequency vs. RPM) | [rotordynamics.md → Campbell Diagram](references/rotordynamics.md#campbell) |
| MNF requirements for rotordynamic analysis | [rotordynamics.md → MNF Requirements](references/rotordynamics.md#mnf-requirements) |

---

## Typical Workflow

```
1. Import MNF/MD DB
   ├─ GUI: Build → Flexible Bodies → Adams Flex
   └─ Python: m.Parts.createFlexBody(name=..., modal_neutral_file_name=...)

2. Configure the flex body
   ├─ Mode selection (start conservative: 10–15 modes)
   ├─ Damping (explicit CRATIO or default)
   └─ Formulation (Original for accuracy, Optimized for speed)

3. Connect to the model
   ├─ Place markers at nodes: flex.Markers.create(node_id=...)
   ├─ Create joints/forces using those markers
   └─ Add massless links for unsupported elements (FORTRAN)

4. Verify (strongly recommended)
   ├─ Info tool: check mass and units
   ├─ DOF count: check .msg file
   └─ Adams Linear: compare frequencies with FEA

5. Simulate and iterate
   ├─ First run: short pilot (0.1–0.2 s) to check stability
   ├─ Mode count optimization via strain energy analysis
   └─ Formulation downgrade if performance is needed

6. Post-process
   ├─ Deformation animation (with scale factor if small deformations)
   ├─ Modal force contours / vectors
   └─ Stress/strain recovery (if MNF includes stress modes)
```

---

## Common Patterns

### Minimum Python Setup (MNF import with safe defaults)
```python
import Adams

m = Adams.Models['MY_MODEL']

flex = m.Parts.createFlexBody(
    name='FLEX_LINK',
    modal_neutral_file_name='C:/analysis/flex_link.mnf',
    damping_ratio='0.02',          # explicit 2% — don't rely on default
    selected_modes=list(range(1, 13)),  # start with 12 modes
    modal_exact_coordinates=True,   # exact ICs (no snapping at t=0)
)

# Marker at specific node
m_attach = flex.Markers.create(name='M_JOINT_A', node_id=1247)
```

### Minimum .adm FLEX_BODY Statement
```
FLEX_BODY/10,
    MNF_FILE = flex_link.mnf,
    QG = 0.0, 0.0, 250.0,
    DAMPING = MODAL,
    CRATIO = 0.02,
    MODES = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
    LABEL = FLEX_LINK

MARKER/101, FLEX_BODY=10, NODE_ID=1247, LABEL=M_JOINT_A
MARKER/102, FLEX_BODY=10, NODE_ID=2089, LABEL=M_JOINT_B
```

### Massless Link for Bushing (FORTRAN)
```python
# Flex body cannot be reaction body for bushing in FORTRAN solver
dummy = m.Parts.createRigidBody(name='DUMMY_LINK_FLEX')
dummy.mass = 0.0
dummy.ixx = 0.0; dummy.iyy = 0.0; dummy.izz = 0.0

m_flex  = flex.Markers.create(name='M_FIXED_TO_FLEX', node_id=1247)
m_dummy = dummy.Markers.create(name='M_FIXED_TO_DUMMY', location=[x, y, z])

m.Constraints.createJoint(
    name='FIXED_FLEX_DUMMY',
    joint_type='fixed',
    i_marker_name='.model.FLEX_LINK.M_FIXED_TO_FLEX',
    j_marker_name='.model.DUMMY_LINK_FLEX.M_FIXED_TO_DUMMY',
)
# Now attach bushing to DUMMY_LINK_FLEX
```

### Frequency-Dependent Damping (Suppress High-Freq Modes)
```python
# 2% for f < 200 Hz, ramp to 100% for f > 500 Hz
flex.damping_ratio = 'IF(FXFREQ(FLEX_LINK) - 200: 0.02, 0.02, IF(FXFREQ(FLEX_LINK) - 500: 0.50, 0.50, 1.0))'
```

### HHT Integrator (.acf) — Flex Body Divergence First Response
```
DEBUG/EPRINT
INTEGRATOR/HHT, ALPHA=-0.05, ERROR=1e-5, HMAX=1e-3
SIMULATE/DYNAMIC, END=1.0, DTOUT=0.01
```

---

## Antipatterns to Avoid

| Antipattern | Why It's Wrong | Correct Approach |
|---|---|---|
| Enabling all modes from a large MNF | Causes HMIN exceeded from high-freq modes; extremely slow simulation | Start with 10–15, use strain energy to trim |
| Relying on default damping silently | Default suppresses modes >1000 Hz to 100% — acceptable but should be intentional | Always set `damping_ratio` explicitly |
| Wrapping `part create flexible_body` in `Adams.execute_cmd()` for Python scripts | The CMD command exists, but the Python wrapper is not idiomatic and misses typed parameters | Use `m.Parts.createFlexBody()` directly — it exposes `selected_modes`, `modal_exact_coordinates`, etc. |
| Offset markers in FORTRAN solver | Auto-creates massless link — reaction forces unavailable | Either use coincident markers or switch to C++ solver |
| Absolute paths with backslashes in MNF_FILE | Fails cross-platform; fails if model is moved | Use forward slashes or relative path from .adm location |
| Forgetting `modal_exact_coordinates=True` | Body snaps at t=0 creating transient artifacts | Always set for initial modal displacements ≠ 0 |
| Skipping Adams Linear verification | Silent unit/translation errors go undetected | Run Adams Linear on isolated flex body after every import |

---

## Reference Files

| Topic | File |
|---|---|
| MNF/MD DB import, mode selection, damping, formulation | [references/flex-body-setup.md](references/flex-body-setup.md) |
| Marker placement, joints/forces capability matrix, massless links, contacts, rigid-to-flex replacement | [references/connections.md](references/connections.md) |
| Troubleshooting decision tree, common problems, performance tuning | [references/troubleshooting.md](references/troubleshooting.md) |
| Flex Toolkit GUI, mnf2mtx, mnfload, load case syntax | [references/toolkit.md](references/toolkit.md) |
| Post-processing: deformation, stress, modal forces, dual representation | [references/results.md](references/results.md) |
| .adm FLEX_BODY statement, MARKER, MATRIX, MFORCE, damping expressions | [references/solver-statements.md](references/solver-statements.md) |
| Rotordynamics: gyroscopic matrices, MNF requirements, Campbell diagram, critical speeds, spinning shaft setup | [references/rotordynamics.md](references/rotordynamics.md) |

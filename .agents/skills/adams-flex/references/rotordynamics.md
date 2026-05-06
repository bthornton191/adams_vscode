# Rotordynamics Reference

## Table of Contents
1. [Overview](#overview)
2. [MNF Requirements for Rotor Dynamics](#mnf-requirements)
3. [Theory — Equations of Motion](#theory)
4. [Setting Up the Flexible Rotor](#setup)
5. [Running the Rotor Dynamics Simulation Series](#running)
6. [Campbell Diagram](#campbell)
7. [Tutorial: Spinning Shaft with Flexible Beams](#tutorial)
8. [Common Pitfalls](#pitfalls)

---

## Overview {#overview}

Adams Flex supports rotordynamic analysis for flexible bodies (shafts, discs, impellers) that spin at high speed. When a flexible body rotates, its dynamic behaviour deviates from a static modal superposition because of:

- **Gyroscopic effects** — the spinning body resists changes to its rotation axis, splitting degenerate lateral mode pairs into forward/backward whirl modes whose frequencies diverge with speed.
- **Spin softening** — centrifugal loads reduce the effective stiffness of lateral bending modes; natural frequencies decrease with speed.
- **Stress stiffening** — axial tension from centrifugal loading stiffens certain bending modes; natural frequencies increase with speed.
- **Damping asymmetry** — damping in the rotating frame contributes a skew-symmetric *circulatory* stiffness term that can cause instability above the threshold speed.

Identifying **critical speeds** — RPM values where a natural frequency matches an integer multiple of the rotational frequency — is the core objective of most rotordynamic analyses. The **Campbell diagram** plots natural frequency vs. rotor RPM and highlights these crossings.

> **Important**: Standard MNF files generated for static/quasi-static flex bodies do **not** contain the extra matrices needed for rotordynamics. You must request a rotor-dynamics export from your FEA solver (MSC Nastran, etc.) to get an MNF with these terms embedded.

---

## MNF Requirements for Rotor Dynamics {#mnf-requirements}

A rotordynamics-capable MNF must contain three additional modal matrices beyond the standard [M], [K], and [B]:

| Matrix | Symbol | Description |
|--------|--------|-------------|
| Gyroscopic | [G] | Anti-symmetric; models gyroscopic coupling between lateral modes |
| Circulatory | [K_C]_R | Skew-symmetric stiffness from rotating-frame damping; can cause instability |
| Differential Stiffness | [K_G] | Stiffness change due to axial/radial centrifugal load (spin softening + stress stiffening) |

**To generate these matrices from MSC Nastran:**
- Use the `ROTORD` solution entry or equivalent in the Nastran Rotordynamics Guide.
- The ADAMSMNF bulk-data entry will embed [G], [K_C]_R, and [K_G] in the output MNF.
- Verify the exported MNF contains rotor data by checking the MNF Browser (Flex Toolkit) — rotor matrices appear as additional data blocks.

**If your MNF does not contain rotor matrices:**
- The simulation still runs, but gyroscopic effects, spin softening, and stress stiffening are all silently ignored.
- Natural frequencies will not shift with speed and no critical speeds will be detectable.
- The Rotor Dynamics Simulation Series can still be launched but the Campbell diagram will show flat frequency lines.

---

## Theory — Equations of Motion {#theory}

For a flexible rotor spinning at angular velocity Ω, the equation of motion in the **fixed (inertial) reference frame** is (Adams Flex Theory, §Rotor Dynamics; source: MSC.Nastran Rotordynamics Guide):

$$[M]\{\ddot{g}\} + ([B_S] + [B_R] + \Omega[G])\{\dot{g}\} + ([K] + [K_C]_R \cdot B_R + [K_G])\{g\} = \{F_S\}$$

where the matrices are modal-space quantities:

| Symbol | Meaning |
|--------|---------|
| [M] | Modal mass matrix |
| {g} | Modal DOF in the fixed reference frame |
| [B_S] | Modal damping in the fixed frame |
| [B_R] | Modal damping in the rotating frame |
| [G] | Gyroscopic matrix (anti-symmetric; scales with Ω) |
| [K] | Modal stiffness matrix |
| [K_C]_R | Circulatory matrix (skew-symmetric; scales with [B_R]) |
| [K_G] | Differential stiffness from centrifugal loads (scales with Ω²) |
| {F_S} | External force vector in the fixed frame |

Adams applies the speed-dependent terms collectively as a distributed force vector {Q_S}(Ω) acting on the flexible rotor. This force vector is re-evaluated at each time step as Ω changes, so it correctly captures transient spin-up and spin-down behaviour.

---

## Setting Up the Flexible Rotor {#setup}

### 1. Import the rotordynamics-capable MNF

```python
import Adams

m = Adams.Models['ROTOR_MODEL']

shaft = m.Parts.createFlexBody(
    name='FLEX_SHAFT',
    modal_neutral_file_name='C:/analysis/rotor_shaft.mnf',  # MNF with rotor matrices
    damping_ratio='0.01',          # explicit 1% — low damping typical for rotors
    selected_modes=list(range(1, 21)),  # lateral + axial bending modes
    modal_exact_coordinates=True,
)
```

### 2. Apply the spin constraint

The rotor must be constrained to rotate about its axis. A **revolute joint** or **cylindrical joint** at the bearing locations is standard:

```python
# Bearing marker on the flex body node
m_bearing = shaft.Markers.create(name='M_BEARING_1', node_id=101)

# Ground marker at the same location
m_ground = m.Ground.Markers.create(name='M_GROUND_BRG1',
                                    location=[0.0, 0.0, 0.0])

# Revolute joint (constrains lateral + axial; allows rotation)
m.Constraints.createJoint(
    name='REVOLUTE_BEARING_1',
    joint_type='revolute',
    i_marker_name='.ROTOR_MODEL.FLEX_SHAFT.M_BEARING_1',
    j_marker_name='.ROTOR_MODEL.ground.M_GROUND_BRG1',
)
```

### 3. Define the spin speed

Apply a **motion** on the revolute joint DOF (or a VFORCE/torque) to drive the rotor:

```python
# Example: ramp from 0 to 3000 RPM over 10 seconds (50 Hz = 314 rad/s)
# In a joint motion expression (Adams View CMD):
#   MOTION/1, JOINT=REVOLUTE_BEARING_1, ROTATIONAL, ACCE=acce(time)
#   acce expression: 314.16 / 10.0 * (1 - COS(PI * TIME / 10))  [rad/s²]
```

For the Rotor Dynamics Simulation Series (see below), the simulation sweeps through multiple steady-state RPM values rather than a single transient; the series manager handles speed stepping automatically.

### 4. Mode count for rotordynamics

- Include **all lateral bending mode pairs** up to ~3× the maximum operating frequency. Because gyroscopic effects split degenerate pairs, you need both the forward and backward whirl modes — they appear as two distinct modes per bending family.
- Include **axial modes** if thrust forces are significant.
- **Torsional modes** are usually decoupled from lateral dynamics for symmetric rotors; include them only if there is a torsional excitation source.
- Rule of thumb: aim for at least the first 4–6 bending mode pairs (8–12 modes) plus any rigid-body modes of the shaft section.

---

## Running the Rotor Dynamics Simulation Series {#running}

Adams View provides a dedicated **Run Rotor Dynamics** workflow that automates the series of dynamic + linear eigenvalue simulations needed to populate a Campbell diagram.

**Location in the GUI:**
> Ribbon → **Simulation Tab** → Simulate container → Run an Interactive Simulation → **Run a Rotor Dynamics Simulation Series**

| Dialog field | Description |
|---|---|
| **End Time** | Duration of each individual dynamic simulation (seconds). Keep short — just enough to reach quasi-steady state at each RPM. |
| **Step Size** | Time step for each dynamic simulation. Should be ≤ 1/(20 × f_max) where f_max is the highest mode frequency you care about. |
| **RPM Interval** | Number of speed intervals. At each interval boundary the solver runs a linear eigenvalue analysis to extract the current natural frequencies. More intervals → smoother Campbell curve but longer run time. |

**What the series does internally:**
1. Runs a dynamic simulation at RPM₁ (first interval) to let the rotor reach steady state.
2. Extracts linear eigenvalues (natural frequencies) at RPM₁.
3. Advances the speed to RPM₂, repeats.
4. Collects all (RPM, frequency) pairs as analysis result sets.

---

## Campbell Diagram {#campbell}

After running the Rotor Dynamics Simulation Series, generate the Campbell diagram:

**Adams PostProcessor location:**
> Plot menu → **Rotor Dynamics Campbell Plots**

| Dialog field | Description |
|---|---|
| **Analysis** | Select the analysis generated by the Rotor Dynamics Simulation Series. |
| **Rotational Velocity** | Select a result set component for the reference rotor speed. **Units must be RPM** (Adams PostProcessor assumes this). |

**Reading the Campbell diagram:**
- Each curve = natural frequency of one mode vs. rotor RPM.
- Diagonal **engine order lines** (N×RPM/60 Hz) represent excitation frequencies; intersections with natural frequency curves are critical speeds.
- **Forward whirl** modes (frequency increases with RPM) and **backward whirl** modes (frequency decreases with RPM) appear as separate diverging curves for each bending mode family.
- The operating speed range should avoid critical speed crossings wherever possible, or be traversed rapidly (< 1 second) if unavoidable.

---

## Tutorial: Spinning Shaft with Flexible Beams {#tutorial}

This is the worked example from Adams Flex 2025_2_1 documentation (`Adding_a_Spinning_Shaft.html`). It demonstrates coupling a spinning rigid cylinder to flexible beam structures.

**Model geometry:**
- Two flexible beams aligned along the model axis.
- Rigid cylinder: ~500 mm long, ~50 mm diameter, aligned with the global y-axis, positioned flush with the left end of the beams.

**Build steps (Adams View GUI):**
1. Create the cylinder geometry (Bodies tab → Solids container → Cylinder tool).
2. Fasten both beams to the cylinder using **Fixed joints** (2 Bod – 1 Loc construction method).
3. View from the top (press **T**).
4. Create a **Revolute joint** between the cylinder CM and ground (turn off the grid so the joint aligns normal to the y-axis view).
5. Modify the revolute joint: **Impose Motion(s)** → Rot Z → `acce(time)`.
6. Set the acceleration expression:
   ```
   6/15*(1-COS(2*PI*TIME/15))
   ```
   This ramps the angular acceleration smoothly, reaching ~6 rad/s² at 15 seconds.
7. Verify displacement and velocity ICs are zero (default).

**What this model demonstrates:**
- As the shaft spins up, the flexible beams deform due to centrifugal and Coriolis loads.
- The flex body formulation (FFRF) automatically captures these effects; no special settings are needed beyond a correctly configured MNF.
- To observe rotordynamic effects (gyroscopic splitting, speed-dependent frequencies), the beams' MNF would need to include the [G], [K_C]_R, and [K_G] matrices.

---

## Common Pitfalls {#pitfalls}

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| MNF without rotor matrices | Campbell diagram shows flat frequency lines; no critical speeds identified | Re-export MNF from Nastran with rotordynamic entries (ROTORD); verify in MNF Browser |
| Rotational velocity result in rad/s instead of RPM | Campbell x-axis scaled incorrectly | Convert to RPM in the result expression: `AZ(.shaft.M_CM, .ground.M_ORIGIN) * 60 / (2*PI)` |
| Too few modes — missing bending pairs | Campbell diagram missing forward or backward whirl branch | Add both modes in each bending pair; use at least 8–12 lateral bending modes |
| Speed ramp too slow — transient resonance | Large deformation amplitude at critical speed crossing | Increase ramp rate through critical speed, or add more structural damping temporarily |
| Bearing modeled as fixed joint | Ignores bearing stiffness and damping, shifts critical speed significantly | Use a BUSHING or FIELD element at bearing locations with appropriate stiffness/damping coefficients |
| Forgetting to check RPM vs rad/s units | Incorrect Campbell diagram scaling | Always confirm the rotational velocity result set component is in RPM |

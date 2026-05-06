# Flex Body Results & Post-Processing Reference

## Table of Contents
1. [Viewing Modal Forces](#modal-forces)
2. [Deformation Visualization](#deformation-viz)
3. [Stress and Strain Recovery](#stress-strain)
4. [Dual Representation Switching](#dual-representation)
5. [Numeric Results Access](#numeric-results)

---

## Viewing Modal Forces {#modal-forces}

### As Time-History Curves
In Adams PostProcessor, request modal force components as curves:
- Component options: FX, FY, FZ, TX, TY, TZ, FQi (generalized force for mode i)
- Path: Results → Measures → Flex Body → select flex body → select component

### As Contour Plots
Color-coded nodal force distribution over the flex body mesh.
- **Requires**: MNF must contain nodal masses (generated with `OUTGM=YES` in Nastran ADAMSMNF card, or equivalent in other FEA packages)
- Path: Adams PostProcessor → Flex Body → Contour → select load component

### As Vector Plots
Animated force/torque vectors showing magnitude and direction at each node.
- Useful for visualizing load paths through the structure
- Path: Adams PostProcessor → Flex Body → Vectors → select component

### Interpreting MFORCE Results
If an MFORCE was defined with a time-varying function, the force time history shows the modal force magnitude. To check physical effect: compare mode participation (modal coordinate amplitudes) with and without the MFORCE applied.

---

## Deformation Visualization {#deformation-viz}

### Deformation Scale Factor
In Adams View/PostProcessor animation settings:
- **Scale = 0**: No deformation shown (pure rigid body motion)
- **Scale = 1**: Actual deformation magnitude
- **Scale > 1**: Exaggerated (useful when deformations are physically small)

For small deformations (e.g., stiff structural member), a scale of 50–200× makes the flex body behavior visible.

### Datum Node
Specify a reference node from which deformations are measured visually. This subtracts the rigid translation of the datum node from all displayed deformations, making the bending/twisting deformation pattern much clearer.

Path: Flexible Body Modify → Display → Datum Node

### Outline Graphics Substitution
Replace the full finite element mesh with a simplified outline representation for cleaner animation:
- Path: Flexible Body Modify → Display → Graphics → Outline
- Use when the FE mesh is dense and clutters the animation view
- Outline is derived automatically from the mesh boundary

### Mode Filtering
Control which modes contribute to the animated deformation:
- **None**: All active modes shown (can be noisy at high frequencies)
- **Frequency**: Show only modes below a cutoff frequency
- **Min Displacement**: Show only modes contributing above a threshold amplitude
- **Percentage**: Show modes contributing at least N% of total deformation

Path: Flexible Body Modify → Display → Mode Filter

---

## Stress and Strain Recovery {#stress-strain}

Stress and strain results are only available if the MNF was generated with stress/strain modes included (e.g., Nastran `OUTGSTRS=YES OUTGSTRN=YES` in the ADAMSMNF card).

### Contour Stress Plots
1. Run simulation — stress data is recovered at each output step
2. In Adams PostProcessor: Results → Flex Body → Stress → select component (Von Mises, Sx, Sy, etc.)
3. Animate to see stress distribution evolving over time
4. Use the color scale slider to set min/max bounds

### Stress Recovery Performance
- Including stress modes significantly increases MNF file size and recovery computation
- For preliminary analysis, run without stress modes; add them for final stress assessment
- Shortened stress mode format (Nastran 2005+) provides a compact representation — use the Flex Toolkit optimizer if file size is prohibitive

### Element vs Grid Point Stress
- **Element stress** (`STRESS(PLOT)` in Nastran): Averaged per element, larger files
- **Grid point stress** (`GPSTRESS` in Nastran): Averaged to nodes, better performance in Adams
- Grid point stress is recommended for Adams Flex workflows

### XDB Format (Nastran)
For very large models or integration with MSC Fatigue:
- Request `EXPORT=DB` or `EXPORT=BOTH` in Nastran ADAMSMNF card
- XDB format stores stress/strain in the Nastran database rather than the MNF
- Supports unlimited model size (MNF has practical limits for stress data)

---

## Dual Representation Switching {#dual-representation}

A flex body can switch between flexible and rigid representations during a simulation. This is useful when:
- A body is only flexible during a critical phase (e.g., impact event)
- Computational cost savings needed for portions of the analysis

### Setting Representation
```python
# Python: set initial representation
flex.representation = 'modal'   # flexible (default)
flex.representation = 'rigid'   # treat as rigid body

# During simulation via .acf command:
# FLEX_BODY/id, REPRESENTATION=MODAL    (at specific simulation time)
# FLEX_BODY/id, REPRESENTATION=RIGID
```

### Notes on Dual Representation
- When running as `'rigid'`, stress/strain recovery is suspended (no flex data generated for that time period)
- The transition appears smooth in animation
- Results files show the switch-over time — plan your output requests accordingly
- Cannot switch mid-step; transition happens at the next output step

---

## Numeric Results Access {#numeric-results}

### Modal Coordinates
The flex body's deformation state is described by N modal coordinates (one per active mode). Access in Adams PostProcessor:
- Path: Results → State Variables → Flex Body → Q (modal displacement) or QD (modal velocity)
- Modal coordinate magnitude < 1e-7 at all times → mode not contributing; safe to disable
- High-frequency oscillation in a modal coordinate → that mode is causing step-size reduction

### Request Elements for Flex Body Outputs
Add measurement requests in the `.adm` for programmatic output:
```
REQUEST/1, FLEX_BODY=5, COMPONENT=Q1,Q2,Q3,Q4,Q5  ! modal coords 1–5
REQUEST/2, FLEX_BODY=5, COMPONENT=FX,FY,FZ          ! interface node forces
```

### Python Access to Results
```python
# After simulation, read results via Adams built-in result access
# (requires Adams PostProcessor Python API — see adams-python-model-builder skill)
import Adams
res = Adams.postprocessor.Result('simulation_name')
modal_q1 = res.getComponent('FLEX_BODY.Q1')
```

### Natural Frequencies from Adams Linear
After running Adams Linear, frequencies appear in the `.out` file and in the Adams PostProcessor linear analysis results. Export to CSV for comparison with FEA values.

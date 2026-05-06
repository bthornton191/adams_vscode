---
name: adams-python-model-builder
description: >
  Build, modify, simulate, and post-process MSC Adams multibody models using the
  Adams Python API (import Adams). Use for writing Python scripts that define model
  topology (parts, markers, geometry), constraints (joints, motions, couplers),
  forces (springs, bushings, beams, custom function expressions), data elements
  (splines, design variables, state variables), and simulations. Covers the
  manager-based creation pattern, dot-path naming conventions, Adams.expression()
  parameterization, array property assignment rules, units/defaults setup, and
  accessing Analysis results. Use this skill whenever the user mentions Adams
  Python, adamspy, import Adams, Adams View Python API, or asks to write a Python
  script for Adams — even if they don't say "Python API" explicitly.
compatibility: github-copilot, claude-code, cursor, windsurf
metadata:
  version: 1.5.1
---

# Adams Python Model Builder

## Local Lessons Learned

At the start of every session, check whether `lessons-learned.md` exists in the skill folder. If it does, read it before proceeding — it contains field-discovered gotchas and workarounds specific to this skill that should inform your work.

---

You are an expert MSC Adams Python API developer. You write correct, complete Python scripts that build and parameterize multibody dynamics models in Adams View using `import Adams`.

## Core Rules (Never Violate)

1. **Always start with `import Adams`** — the API is only available inside the Adams View embedded Python environment.
2. **Manager-based creation**: All objects are created through manager methods on the parent, never by calling class constructors directly.
   ```python
   part  = model.Parts.createRigidBody(name='LINK_1')
   marker = part.Markers.create(name='PIN', location=[0, 0, 0])
   joint  = model.Constraints.createRevolute(name='J1', i_marker=marker, j_marker=ground_mkr)
   ```
3. **Both object references and name strings are accepted** for related objects. Prefer object refs when already in scope; use name strings when building from existing models.
   ```python
   # Equivalent:
   joint = model.Constraints.createRevolute(i_marker=mkr_obj, j_marker=ground_mkr)
   joint = model.Constraints.createRevolute(i_marker_name='.MODEL.PART.PIN', j_marker_name='.MODEL.ground.REF')
   ```
4. **Array property reassignment**: Array-valued properties (location, orientation, stiffness, xyz_component_gravity, etc.) must be reassigned in full — in-place element mutation is silently ignored by Adams.
   ```python
   g = grav.xyz_component_gravity   # get a copy
   g[1] = -9806.65                  # modify the copy
   grav.xyz_component_gravity = g   # reassign — required
   # grav.xyz_component_gravity[1] = -9806.65  ← does NOT work
   ```
5. **`Marker.location` coordinate-frame asymmetry**: The getter returns **local** coordinates (in the parent part's CS) but the setter expects **global** coordinates (model CS). Do **not** read `.location`, modify it, and write it back — the frames differ so the result will be wrong. Instead, use `marker.location_global` for the round-trip, or set an absolute global position directly.
   ```python
   # ✗ WRONG — mixes local read with global write
   loc = marker.location        # local coords
   loc[0] += 50.0
   marker.location = loc        # interpreted as global — silently wrong!

   # ✓ CORRECT — read global, modify, write global
   loc = marker.location_global # global coords (read-only property, returns a copy)
   loc[0] += 50.0
   marker.location = loc        # global coords — correct

   # ✓ CORRECT — set an absolute global position
   marker.location = [100, 0, 250]
   ```
   The same local-get / global-set asymmetry applies to `marker.orientation`.
6. **`Adams.expression()` vs `Adams.eval()` vs direct assignment**:
   - `Adams.expression(str)` — stores the expression string; re-evaluates when the design variable changes (parametric).
   - `Adams.eval(str)` — evaluates once immediately and stores the resulting value (not parametric).
   - Direct assignment — stores a constant (e.g., `marker.location = [0, 0, 100]`).
   ```python
   from Adams import expression
   dv = model.DesignVariables.createReal(name='LENGTH', value=250.0)
   marker.location = expression(f'{{0, 0, {dv.full_name}}}')  # parametric
   ```
7. **Set units via `Adams.defaults`** before creating geometry — values are always interpreted in the current unit system.
   ```python
   d = Adams.defaults
   d.units.length = 'mm'
   d.units.mass   = 'kg'
   d.units.time   = 'second'
   d.units.force  = 'newton'
   ```
8. **Orientation angles are in degrees** when passed as `orientation=[psi, theta, phi]` to `create()` methods.
9. **Do not specify `adams_id`** unless you have a specific reason — Adams auto-assigns all IDs.
10. **Access the active model** with `Adams.defaults.model` or `Adams.getCurrentModel()`.
11. **CMD bridge** — use `Adams.execute_cmd(str)` for features not yet exposed in the Python API (e.g., `Adams.execute_cmd('simulation single_run transient ...')`).

---

## Common Patterns

### Returning a value to CMD from `run_python_code`

When Python code is executed from CMD via `run_python_code(str)`, the CMD-side return value is always `1` (success) or `0` (failure) — the Python expression's own return value is **discarded**. To pass a result back to CMD, store it in an Adams design variable using `set_dv` from the [`aviewpy`](https://pypi.org/project/aviewpy/) library. The CMD macro then reads it directly.

```adams_cmd
! Inside a CMD macro — run Python and capture the result via set_dv
var set var=$_self.py_str str=                             "from aviewpy.variables import set_dv"
var set var=$_self.py_str str=(eval($_self.py_str)),       "result = my_function()"
var set var=$_self.py_str str=(eval($_self.py_str)),       "set_dv('$_self', 'my_result', result)"
var set var=$_self.tmp_int int=(eval(run_python_code(str_merge_strings("\\n", $_self.py_str))))

! Now the result is stored in the macro's own design variable 'my_result'
if condition=(eval($_self.my_result) > 10)
    ! do something
end
```

The CMD macro reads the result back with `(eval($_self.my_result))`.

**Key points:**

- `set_dv(parent, name, value)` creates the design variable if it doesn't exist, or updates it. It auto-detects the type (`real`, `integer`, `string`).
- Inside a CMD macro, pass `'$_self'` as the parent string — Adams substitutes the macro's full dot-path name before Python sees it, so the DV becomes a child of the macro.
- **Installation:** `aviewpy` must be installed into the Adams Python environment: `path/to/mdi.bat python -m pip install aviewpy`.

---

## Common Antipatterns

### Using the return value of `run_python_code` as a result

```adams_cmd
! WRONG — CMD will see 1 (success), not the Python function's return value
var set var=$_self.my_result int=(eval(run_python_code("my_function()")))
```

`run_python_code` returns an exit-code (`1` = success, `0` = failure), **not** the value of the Python expression. See the `set_dv` pattern above for the correct approach.

---

## Model-Building Workflow

```python
import Adams

# 1. Create model
m = Adams.Models.create(name='my_model')

# 2. Set units
d = Adams.defaults
d.units.length = 'mm'
d.units.mass   = 'kg'
d.units.time   = 'second'
d.units.force  = 'newton'

# 3. Gravity
grav = m.Forces.createGravity(name='GRAVITY')
grav.xyz_component_gravity = [0, -9806.65, 0]

# 4. Access ground part and create reference marker
ground = m.ground_part                                   # ground is always .my_model.ground
gnd_mkr = ground.Markers.create(name='MOUNT_A', location=[0, 0, 0])

# 5. Create a rigid part (part origin placed at its CM for simplicity)
link = m.Parts.createRigidBody(name='link', location=[0, 0, 100])
link.mass = 1.5
link.ixx  = 1200.0
link.iyy  = 1200.0
link.izz  = 50.0

# 6. Create markers on the part
pin_mkr = link.Markers.create(name='pin_mkr', location=[0, 0, 0])   # local coords

# 7. Create a revolute joint
rev = m.Constraints.createRevolute(name='rev_1',
                                   i_marker=pin_mkr,
                                   j_marker=gnd_mkr)

# 8. Add geometry for visualization
link.Geometries.createCylinder(name='rod', center_marker=pin_mkr,
                               length=200, radius=5,
                               angle_extent=360, side_count_for_body=16,
                               segment_count_for_ends=8)

# 9. Run simulation
sim = m.Simulations.create(name='run1', end_time=2.0, number_of_steps=2000)
sim.simulate()
```

**Build order**: model → units → gravity → ground markers → parts → part markers → constraints → forces → geometry → data elements → simulation.

---

## Force Selection Guide

| Scenario | Method | Key Parameters |
|----------|--------|----------------|
| 1-DOF translational spring + damper | `Forces.createTranslationalSpringDamper()` | `stiffness`, `damping`, `displacement_at_preload`, `force_preload` |
| 1-DOF rotational spring + damper | `Forces.createRotationalSpringDamper()` | `r_stiff`, `r_damp`, `displacement_at_preload` |
| 6-DOF compliant mount (bushing) | `Forces.createBushing()` | `stiffness` (list[6]), `damping` (list[6]) |
| Structural beam element | `Forces.createBeam()` | `youngs_modulus`, `ixx`, `iyy`, `izz`, `area_of_cross_section`, `length` |
| Custom scalar force (FUNCTION=) | `Forces.createSingleComponentForce()` | `function`, `type_of_freedom`, `action_only` |
| 3-component force vector | `Forces.createForceVector()` | `x_force_function`, `y_force_function`, `z_force_function` |
| 3-component torque vector | `Forces.createTorqueVector()` | `x_torque_function`, `y_torque_function`, `z_torque_function` |
| 6-component force + torque | `Forces.createGeneralForce()` | same x/y/z for both force and torque |
| Gravity | `Forces.createGravity()` | `xyz_component_gravity` (list[3]) |
| 6-DOF force-field matrix | `Forces.createField()` | `stiffness_matrix`, `damping_ratio` |
| Force on flexible body modes | `Forces.createModalForce()` | `flexible_body`, `force_function` |

**Decision guide**: matches the CMD skill — the physics is identical, only the syntax differs.

---

## Constraints & Motions

| Joint | Method | DOF removed | Notes |
|-------|--------|-------------|-------|
| Revolute | `createRevolute()` | 5 | Rotates about z-axis of i-marker |
| Translational | `createTranslational()` | 5 | Slides along z-axis |
| Cylindrical | `createCylindrical()` | 4 | Rotate + translate along z |
| Spherical | `createSpherical()` | 3 | Ball joint, no rotation DOF |
| Universal (Hooke) | `createUniversal()` / `createHooke()` | 4 | Two perpendicular rotations |
| Planar | `createPlanar()` | 3 | Motion in the XY plane |
| Fixed | `createFixed()` | 6 | Rigid attachment |
| Convel | `createConvel()` | 4 | Constant-velocity joint |
| Screw | `createScrew()` | 5 | `pitch` param required |
| Rack & Pinion | `createRackpin()` | 5 | `diameter_of_pitch` param required |

**Primitive constraints**: `createAtPoint()`, `createInline()`, `createInPlane()`, `createOrientation()`, `createParallel()`, `createPerpendicular()`, `createPointPoint()`

**Motions**:
```python
# Apply motion to an existing joint
mo = m.Constraints.createJointMotion(name='drv', joint=rev,
                                     type_of_freedom='rotational',
                                     function='360D * time')

# Free-standing motion (not tied to a joint)
mo2 = m.Constraints.createMotion(name='drv2', i_marker=mkr_i, j_marker=mkr_j,
                                  type_of_freedom='translational',
                                  time_derivative='velocity',
                                  function='100.0')
```

---

## Geometry

| Shape | Method | Required params |
|-------|--------|-----------------|
| Box/Block | `createBlock()` | `corner_marker`, `x`, `y`, `z` |
| Cylinder | `createCylinder()` | `center_marker`, `radius`, `length`, `angle_extent` |
| Ellipsoid | `createEllipsoid()` | `center_marker`, `x_scale_factor`, `y_scale_factor`, `z_scale_factor` |
| Frustum (cone) | `createFrustum()` | `center_marker`, `top_radius`, `bottom_radius`, `length`, `angle_extent` |
| Torus | `createTorus()` | `center_marker`, `major_radius`, `minor_radius`, `angle_extent` |
| Link | `createLink()` | `i_marker`, `j_marker`, `depth`, `width` |
| Arc | `createArc()` | `center_marker`, `radius`, `angle_extent` |
| Spring-damper visual | `m.Geometries.createSpringDamper()` | `i_marker_name`, `j_marker_name` |
| Outline (wireframe) | `createOutline()` | `marker` (list[Marker]) |

Note: Geometries are created on a **part** (`part.Geometries.createX()`) except spring-damper visual and force display, which live on the model (`model.Geometries.createX()`).

---

## Data Elements

```python
# Spline (1D or 2D lookup table)
spl = m.DataElements.createSpline(name='road_profile',
                                  x=[0, 10, 20, 30],
                                  y=[0, 5, 3, 8],
                                  linear_extrapolate=True)

# Design variable (parametric)
dv = m.DesignVariables.createReal(name='SPRING_K', value=5000.0)
spring.stiffness = Adams.expression(dv.full_name)

# State variable (for FUNCTION= feedback)
sv = m.DataElements.createStateVariable(name='load_sensor',
                                        function='FZ(.model.axle.cm, .model.ground.ref, .model.ground.ref)')

# Material
mat = m.Materials.create(name='steel',
                          youngs_modulus=2.07e5, poissons_ratio=0.29, density=7.8e-6)
link.material_type = mat
```

---

## Simulation

```python
# Simple transient run
sim = m.Simulations.create(name='run1',
                           end_time=5.0,
                           number_of_steps=500,
                           initial_static=False)
sim.simulate()

# With initial static equilibrium
sim2 = m.Simulations.create(name='run2', end_time=2.0, number_of_steps=200,
                            initial_static=True)
sim2.simulate()

# Scripted — inline ACF solver commands
sim3 = m.Simulations.create(name='run3',
                            script_type='solver_commands',
                            script=['simulate/transient,duration=10,dtout=0.01',
                                    'linear/statemat,file=model.mat'])
sim3.simulate()

# Scripted — by CMD language commands
sim4 = m.Simulations.create(name='run4',
                            script_type='commands',
                            script='simulation single_run transient type=auto_select '
                                   'end_time=5.0 number_of_steps=500 model_name=.my_model')
sim4.simulate()
```

`script_type` options: `'simple'` (default), `'commands'` (CMD language), `'solver_commands'` (ACF).

---

## Post-processing

```python
# Access analysis results after simulate()
analysis = m.Analyses[sim.name]          # or m.Analyses['run1']

# Browse result components (OrderedDict)
print(analysis.results.keys())           # top-level groups
component = analysis.results['PART_1']['CM Position']['X']
values = component.values                # List[float], one per time step

# Create a measure (tracked during simulation)
meas = m.Measures.createObject(name='link_angle',
                               object=rev,
                               characteristic='ax_ay_az_projection_angles',
                               component='z_component')

# Function measure (arbitrary FUNCTION= expression)
fm = m.Measures.createFunction(name='spring_force',
                               function='DM(.model.link.pin_mkr, .model.ground.mount_a)')
```

---

## FUNCTION= Expressions Quick Reference

Runtime expressions are identical between CMD and Python — they're always passed as plain strings to `.function` properties. The Adams Solver evaluates them at each timestep.

```python
spring.function = 'STEP(TIME, 0.0, 0.0, 1.0, 500.0)'
motion.function = '360D * TIME'
sforce.function = 'IMPACT(DZ(.model.body.cm, .model.ground.ref), VZ(.model.body.cm, .model.ground.ref, .model.ground.ref), 0.0, 1e5, 1.5, 50.0, 0.1)'
sforce.function = 'AKISPL(DX(.model.body.cm, .model.ground.ref), 0, .model.road_profile, 0)'
```

Full expression reference: [`references/function-expressions.md`](references/function-expressions.md)

---

## Key Reference Files

| Topic | File | Stubs |
|-------|------|-------|
| Model, parts, markers | [`references/api-classes/model-parts-markers.md`](references/api-classes/model-parts-markers.md) | `Part.pyi`, `Marker.pyi`, `Model.pyi` |
| Constraints and motions | [`references/api-classes/constraints.md`](references/api-classes/constraints.md) | `Constraint.pyi` |
| Forces | [`references/api-classes/forces.md`](references/api-classes/forces.md) | `Force.pyi` |
| Geometry shapes | [`references/api-classes/geometry.md`](references/api-classes/geometry.md) | `Geometry.pyi` |
| Data elements (splines, arrays, matrices) | [`references/api-classes/data-elements.md`](references/api-classes/data-elements.md) | `DataElement.pyi`, `DesignVariable.pyi` |
| Simulation and analysis results | [`references/api-classes/simulation-analysis.md`](references/api-classes/simulation-analysis.md) | `Simulation.pyi`, `Analysis.pyi` |
| Measures | [`references/api-classes/measures.md`](references/api-classes/measures.md) | `Measure.pyi` |
| Contacts | [`references/api-classes/contacts.md`](references/api-classes/contacts.md) | `Contact.pyi` |
| System elements (ODEs, transfer functions) | [`references/api-classes/system-elements.md`](references/api-classes/system-elements.md) | `SystemElement.pyi` |
| Session utilities (stoo, eval, file I/O) | [`references/api-classes/utilities.md`](references/api-classes/utilities.md) | `Adams.pyi`, `Expression.pyi` |
| Naming conventions and dot-paths | [`references/naming-conventions.md`](references/naming-conventions.md) | — |
| FUNCTION= runtime expressions | [`references/function-expressions.md`](references/function-expressions.md) | — |
| Full type stubs (authoritative) | [`references/adamspy-stubs/`](references/adamspy-stubs/) | all `.pyi` files |
| Simple pendulum example | [`assets/python_scripts/simple_pendulum.py`](assets/python_scripts/simple_pendulum.py) | — |
| Parametric chain example | [`assets/python_scripts/parametric_chain.py`](assets/python_scripts/parametric_chain.py) | — |
| Oscillating slider example | [`assets/python_scripts/oscillating_slider.py`](assets/python_scripts/oscillating_slider.py) | — |

---

## Submit a Lesson Learned

If during your work you discover something useful that other Adams users would benefit from — a non-obvious behaviour, a reliable workaround, a better approach — do the following:

1. Draft the lesson:
   ```json
   {
     "skill": "adams-python-model-builder",
     "summary": "One-sentence description",
     "detail": "Full explanation with enough context to be actionable",
     "adams_version": "<version if relevant, else omit>",
     "os": "<windows/linux if relevant, else omit>"
   }
   ```
2. **Always** append it to `lessons-learned.md` in the skill folder (create the file if it doesn't exist). Use this format:
   ```markdown
   ## <summary>
   **Date:** <YYYY-MM-DD>  
   **Submitted:** <yes/no>

   <detail>
   ```
3. Show it to the user and ask: *"I've recorded this locally — want me to also submit it anonymously to the skill maintainer?"*
4. If yes, POST it:
   ```
   POST https://adams-skills-api.bthorn191.workers.dev/lessons
   Content-Type: application/json
   <lesson JSON>
   ```
   Then update the `Submitted:` field in `lessons-learned.md` to `yes`.
5. If the POST fails, tell the user and move on — do not retry. Leave `Submitted: no` in the local file.

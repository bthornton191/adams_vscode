---
name: adams-cmd-model-builder
description: >
  Build, modify, and debug MSC Adams multibody models using Adams View CMD scripting.
  Use for creating .cmd scripts that define model topology (parts, markers, geometry),
  constraints (joints, couplers, motions), forces (springs, bushings, beams, custom
  FUNCTION= expressions), scripting (macros, variables, loops, conditionals), and
  data elements (splines, variables, arrays). Covers Adams CMD syntax rules, object
  naming conventions, the full FUNCTION= run-time expression library (STEP, IMPACT,
  BISTOP, spline functions, displacement/velocity/acceleration sensors, orientation
  angles, force measurements, TIME, and more), and when to choose each force type.
compatibility: github-copilot, claude-code, cursor, windsurf
metadata:
  version: 0.0.16
---

# Adams CMD Model Builder

You are an expert MSC Adams View CMD scripter. You write correct, complete `.cmd` scripts that build and parameterize multibody dynamics models in Adams View.

## Core Rules (Never Violate)

1. **Spell out all keywords in full** — abbreviations work interactively but fail in macros and scripts.
2. **Object names use dot-path hierarchy**: `.model_name.part_name.marker_name`. The fixed ground part is `.model_name.ground`.
3. **Line continuation**: end a line with `&` to continue on the next line. Inline comments after continuation: `& ! comment text`.
4. **Comments**: `!` starts a comment to end-of-line.
5. **Runtime expressions** (in `FUNCTION=` values) are evaluated by the solver at each timestep — always wrap the entire expression in double quotes. Angles default to **radians**; append `D` for degrees (e.g., `90D`, `360D`).
6. **Build order**: model → parts → markers → geometry → data elements → constraints → forces/motions.
7. **Use `EVAL(expr)` inside loops** to force immediate evaluation of a variable expression rather than storing a literal string.
8. **Never specify `adams_id` manually** — Adams auto-assigns IDs. Adding them by hand is error-prone and unnecessary in CMD scripts.
9. **`part create` only once per part** — Use `part create rigid_body name_and_position` to create the part, then `part modify rigid_body mass_properties` (not `part create`) to set mass/inertia. Calling `part create` a second time on the same part will error.
10. **Always create `.cm` first, then pass `center_of_mass_marker`** — Adams does NOT auto-create the `.cm` marker. You must explicitly create it before calling `part modify rigid_body mass_properties`, and you must pass it via `center_of_mass_marker`. Omitting it causes Adams to error with "no CM marker" at simulation time. Place the `.cm` marker at the part's actual centre of mass location. Example:
    ```cmd
    part create rigid_body name_and_position &
        part_name = .model.link &
        location  = 0.0, 0.0, 0.0

    ! Create .cm marker BEFORE setting mass properties.
    ! Place it at the actual centre of mass in global coordinates.
    marker create &
        marker_name = .model.link.cm &
        location    = 0.0, -100.0, 0.0 &
        orientation = 0.0D, 0.0D, 0.0D

    part modify rigid_body mass_properties &
        part_name             = .model.link &
        mass                  = 1.0 &
        ixx                   = 100.0 &
        iyy                   = 100.0 &
        izz                   = 100.0 &
        center_of_mass_marker = .model.link.cm
    ```
11. **`part create point_mass` uses sub-commands, not inline parameters**: use `part create point_mass name_and_position & point_mass_name = ... & location = ...` to create, then `part modify point_mass mass_properties & point_mass_name = ... & mass = ...` (a `.cm` marker and `center_of_mass_marker` are NOT needed for point masses). Do NOT use `rigid_body` syntax for point masses.
12. **Do not use `constraint create joint fixed` with a point mass** — Adams only allows `spherical`, `atpoint`, `inline`, and `inplane` primitives on point masses. Use `constraint create joint spherical` to fully fix a point mass (spherical removes all 3 translational DOF; since point masses have no rotational DOF, this is fully constrained).
13. **Spring-damper keyword: `translational_spring_damper`, not `spring_damper`**: the correct command is `force create element_like translational_spring_damper`. Free length is set via `displacement_at_preload` (not `length`). The parameter `length` does not exist on this command — if you see `length = 200.0` in broken code, rename it to `displacement_at_preload = 200.0`.
14. **Simulation command: `simulation single_run transient`** — the keyword `simulate transient` does not exist. Use `simulation single_run transient & type = auto_select & end_time = ... & number_of_steps = ... & model_name = ... & initial_static = no`.
15. **Always add geometry to moving parts, using correct syntax** — Adams models without geometry are very difficult to inspect visually. Add at least one `geometry create shape` command to every moving rigid part or point mass. **Geometry syntax rules (Adams 2023.2):** `sphere` and `box` are not valid shape keywords — use `ellipsoid` (with equal x/y/z scale factors for a sphere-like shape) or `cylinder` instead. Do NOT include `part_name` or `adams_id` in geometry commands (the part is inferred from the object path). Do NOT use `side_count_for_perimeter` for cylinders. For `link` shape, use `i_marker`/`j_marker` (not `i_marker_name`/`j_marker_name`). See the geometry reference for complete examples.
16. **Expression values must stay on a single line** — the `&` continuation character works for splitting *commands* across lines, and plain comma-separated parameter values can be split across lines with `&` (e.g., `location = 0.0, &` on one line then `0.0, 0.0` on the next). However, inline-evaluated expressions — text inside parentheses like `(eval(...))` — cannot span multiple lines. Adams parses these as a single token and will error if it encounters a line break mid-expression, even with `&`.

    For arguments that *store* a function string (like `function = "..."`), you can pass multiple comma-separated quoted strings to break up long expressions — Adams concatenates them, and each appears on a new line in the GUI. This is the preferred way to keep long function expressions readable.

    ```cmd
    ! OK — plain comma-separated values can be split with &
    marker create marker_name = .mod.part.mkr &
        location = 0.0, &
                   50.0, &
                   100.0

    ! OK — function string split into multiple comma-separated quoted strings
    force create direct single_component_force &
        single_component_force_name = .model.my_force &
        function = "STEP(TIME, 0.0, 0.0, 1.0, 500.0)", &
                   " + STEP(TIME, 1.0, 0.0, 2.0, 200.0)"

    ! WRONG — eval expression broken across lines causes a parse error
    marker create marker_name = .mod.part.mkr &
        location = (eval(loc_global( &
            {0,0,0}, .mod.part.cm)))

    ! CORRECT — eval expression stays on one line
    marker create marker_name = .mod.part.mkr &
        location = (eval(loc_global({0,0,0}, .mod.part.cm)))
    ```

---

## Model-Building Workflow

```cmd
! 1. Create model
model create model_name = my_model

! 2. Set units
defaults units &
    length = mm &
    force = newton &
    mass = kg &
    time = sec

! 3. Add gravity
force create body gravitational &
    gravity_field_name = .my_model.gravity &
    x_component_gravity = 0.0 &
    y_component_gravity = -9806.65 &
    z_component_gravity = 0.0

! 4. Create markers on ground (fixed reference points)
marker create &
    marker_name = .my_model.ground.mount_a &
    location = 0.0, 0.0, 0.0 &
    orientation = 0.0D, 0.0D, 0.0D

! 5. Create a rigid part
part create rigid_body name_and_position &
    part_name = .my_model.link &
    location = 0.0, 0.0, 100.0 &
    orientation = 0.0D, 0.0D, 0.0D

! 6. Create .cm marker, then set mass/inertia properties (Rule 10).
!    You must create .cm BEFORE calling part modify mass_properties.
!    Place it at the actual centre of mass (here: part origin).
marker create &
    marker_name = .my_model.link.cm &
    location    = 0.0, 0.0, 100.0 &
    orientation = 0.0D, 0.0D, 0.0D

part modify rigid_body mass_properties &
    part_name             = .my_model.link &
    mass                  = 1.5 &
    ixx                   = 1200.0 &
    iyy                   = 1200.0 &
    izz                   = 50.0 &
    center_of_mass_marker = .my_model.link.cm

! 7. Create other markers on the part (e.g., pin location)
marker create &
    marker_name = .my_model.link.pin_mkr &
    location = 0.0, 0.0, 0.0 &
    orientation = 0.0D, 0.0D, 0.0D

! 8. Create a revolute joint
constraint create joint revolute &
    joint_name = .my_model.rev_1 &
    i_marker_name = .my_model.link.pin_mkr &
    j_marker_name = .my_model.ground.mount_a
```

---

## Force Selection Guide

| Scenario | Command | Key Parameters |
|----------|---------|----------------|
| 1-DOF spring + damper along axis | `force create element_like translational_spring_damper` | `stiffness`, `damping`, `displacement_at_preload` |
| 6-DOF compliant connection (rubber mount, bushing) | `force create element_like bushing` | `stiffness` (6 values), `damping` (6 values) |
| Structural flexible beam (Euler-Bernoulli) | `force create element_like beam` | `area`, `ixx`, `iyy`, `length`, material properties |
| Custom scalar force defined by expression | `force create direct single_component_force` | `function`, `action_only` |
| Custom 3-component translational force | `force create direct force_vector` | `function_x`, `function_y`, `function_z` |
| Custom 6-component force + torque | `force create direct general_force` | `x_force_function`, `y_force_function`, `z_force_function`, `x_torque_function`, `y_torque_function`, `z_torque_function` |
| Prescribed motion (kinematic driver) | `constraint create motion_generator` | `type`, `function` |
| Gravity | `force create body gravitational` | `x/y/z_component_gravity` |

**Decision guide:**
- Use `spring_damper` when the force acts along a single line of action with known stiffness K and damping C.
- Use `bushing` when compliance is needed in all 6 DOF simultaneously (translational + rotational stiffness/damping).
- Use `beam` for structural members where cross-section properties (area, second moment) determine stiffness.
- Use `single_component_force` (SFORCE) for any custom scalar force or torque driven by a `FUNCTION=` expression.
- Use `general_force` (GFORCE) when you need simultaneously applied forces and torques in multiple axes.
- Use `motion_generator` to drive kinematics (prescribe position, velocity, or acceleration) rather than apply free forces.

---

## FUNCTION= Expressions Quick Reference

Function expressions are evaluated at every solver timestep. They appear in `FUNCTION=` for forces, motions, variables, data elements, and any other element that accepts one.

```cmd
! Smooth ramp-up from 0 to 500 N over first 1 second
function = "STEP(TIME, 0.0, 0.0, 1.0, 500.0)"

! Quintic ramp (smoother, no 2nd-derivative discontinuity)
function = "STEP5(TIME, 0.0, 0.0, 1.0, 500.0)"

! One-sided impact contact (z-direction collision)
function = "IMPACT(DZ(.model.body.m1, .model.ground.m0, .model.ground.m0), &
                   VZ(.model.body.m1, .model.ground.m0, .model.ground.m0, .model.ground.m0), &
                   10.0, 1.0E5, 1.5, 50.0, 0.1)"

! Akima spline lookup
function = "AKISPL(DX(.model.body.cm, .model.ground.ref), 0, .model.my_spline, 0)"

! Simple harmonic
function = "SHF(TIME, 0, 10, 6.283, 0, 0)"

! Conditional (prefer STEP over IF — IF causes derivative discontinuities)
function = "IF(TIME - 2.5 : 0, 0, 100)"
```

Full function reference: [`references/function-expressions/README.md`](references/function-expressions/README.md)

---

## Scripting Quick Reference

```cmd
! Parameterized real variable
variable set variable_name = .model.par_length real_value = 250.0

! String variable
variable set variable_name = my_str string_value = "LINK_A"

! Integer Variable
variable set variable_name = .model.num_links integer_value = 5

! Object Variable (e.g., part, marker)
variable set variable_name = .model.link_part object_value = .model.link_1

! Check existence before acting
if condition = (DB_EXISTS(".my_model.link"))
    ! entity exists, modify it
end

! Concatenate strings: //
! Integers can be concatenated with strings
! reals cannot be concatenated with strings
! Convert real to integer before concatenation: RTOI(x)

! Loop (1 to 5)
for variable_name = i start_value = 1 end_value = 5
    part create rigid_body name_and_position &
        part_name = (eval(".my_model.link_" // RTOI(i))) &
        location = (eval(i * 100.0)), 0, 0
end
```

Full scripting reference: [`references/commands/scripting.md`](references/commands/scripting.md)

---

## Macros Quick Reference

Macros are `.mac` files loaded with `macro read` and executed by name.

```cmd
! Load a macro from disk
macro read &
    file_name    = "C:/macros/my_macro.mac" &
    library_name = (.my_lib)

! Execute it
.my_lib.my_macro  arg1 = value1
```

```cmd
! --- .mac file skeleton ---
!USER_ENTERED_COMMAND  mylib my_macro
!WRAP_IN_UNDO          yes
!
!$part_name:t=part:c=1
!$scale:t=real:c=0:d=1.0:r=gt(0)
!$label:t=string:c=0:d="Part"
!
!END_OF_PARAMETERS

! Always create a $_self var first so wildcard delete is safe
variable set variable_name = $_self._init  integer_value = 1

! ... macro body ...

variable delete variable = $_self.*
```

| Pattern | Key syntax |
|---------|------------|
| Temp variable namespace | `$_self.varname` — avoids collisions in macro-calls-macro |
| Optional cleanup (wildcard) | `variable delete variable = $_self.*` |
| Collision-free names | `UNIQUE_NAME(".model.spr_")` |
| Find owning model | `DB_ANCESTOR(eval($part), "model")` |
| Output parameter (return value) | Pass string containing target variable name; callee writes to it |

Full macro reference: [`references/commands/macros.md`](references/commands/macros.md)

---

## Key Reference Files

| Topic | File |
|-------|------|
| Object naming conventions | [`references/naming-conventions.md`](references/naming-conventions.md) |
| Parts, markers, point masses | [`references/commands/model-parts-markers.md`](references/commands/model-parts-markers.md) |
| Constraints and joints | [`references/commands/constraints.md`](references/commands/constraints.md) |
| Forces and force selection | [`references/commands/forces.md`](references/commands/forces.md) |
| Geometry shapes | [`references/commands/geometry.md`](references/commands/geometry.md) |
| Variables, loops, conditionals | [`references/commands/scripting.md`](references/commands/scripting.md) |
| Macros — parameters, patterns, lifecycle | [`references/commands/macros.md`](references/commands/macros.md) |
| File I/O — text open/write/close, command read | [`references/commands/file-io.md`](references/commands/file-io.md) |
| Function expressions index | [`references/function-expressions/README.md`](references/function-expressions/README.md) |
| Simple pendulum example | [`assets/cmd_scripts/simple_pendulum.cmd`](assets/cmd_scripts/simple_pendulum.cmd) |
| Parametric chain example | [`assets/cmd_scripts/parametric_chain.cmd`](assets/cmd_scripts/parametric_chain.cmd) |
| Example: icon-resize macro | [`assets/cmd_scripts/example_macro_resize_icons.mac`](assets/cmd_scripts/example_macro_resize_icons.mac) |
| Example: batch spring-creation macro | [`assets/cmd_scripts/example_macro_batch_spring.mac`](assets/cmd_scripts/example_macro_batch_spring.mac) |
| Example: export-results macro | [`assets/cmd_scripts/example_macro_export_results.mac`](assets/cmd_scripts/example_macro_export_results.mac) |

---

## Running a Simulation

To run a transient dynamics simulation from within a CMD script:

```cmd
simulation single_run transient &
    type            = auto_select &
    end_time        = 2.0 &
    number_of_steps = 2000 &
    model_name      = .my_model &
    initial_static  = no
```

- `number_of_steps` controls output frequency (end_time / number_of_steps = step_size).
- `initial_static = no` skips the static equilibrium step before the transient run.
- `type = auto_select` lets Adams choose the integrator automatically.
- **Do NOT use `simulate transient`** — that is not a valid Adams View keyword.

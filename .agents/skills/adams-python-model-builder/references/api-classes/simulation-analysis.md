# Simulation and Analysis Results — Python API Reference

> **Authoritative stubs**: `references/adamspy-stubs/Simulation.pyi`, `Analysis.pyi`

---

## Creating and Running Simulations

### Simple Transient (most common)

```python
sim = m.Simulations.create(
    name='run1',
    end_time=5.0,
    number_of_steps=500,     # output step count (not solver step size)
    initial_static=False,    # True = run static equilibrium before transient
)
sim.simulate()
```

### With Static Equilibrium First

```python
sim = m.Simulations.create(name='static_then_dyn',
                           end_time=3.0,
                           number_of_steps=300,
                           initial_static=True)
sim.simulate()
```

### Specifying Step Size Instead of Step Count

```python
sim = m.Simulations.create(name='run_ss',
                           end_time=2.0,
                           step_size=0.001)  # 1 ms output interval
sim.simulate()
```

### Scripted — Inline ACF Solver Commands

```python
sim = m.Simulations.create(
    name='scripted_acf',
    script_type='solver_commands',
    script=[
        'simulate/transient,duration=10,dtout=0.01',
        'linear/statemat,file=statemat.mat'
    ]
)
sim.simulate()
```

### Scripted — ACF File

```python
sim = m.Simulations.create(
    name='scripted_file',
    script_type='solver_commands',
    script='file/command=my_sim.acf'
)
sim.simulate()
```

### Scripted — Adams CMD Language

```python
sim = m.Simulations.create(
    name='scripted_cmd',
    script_type='commands',
    script='simulation single_run transient type=auto_select '
           'end_time=5.0 number_of_steps=500 model_name=.MY_MODEL '
           'initial_static=no'
)
sim.simulate()
```

### Simulation Properties

| Property | Type | Description |
|----------|------|-------------|
| `end_time` / `duration` | `float` | Simulation end time |
| `number_of_steps` | `int` | Number of output steps |
| `step_size` | `float` | Output step size (alternative to `number_of_steps`) |
| `initial_static` | `bool` | Run static equilibrium first |
| `sim_type` | `str` | `'auto_select'` (default), `'dynamic'`, `'kinematic'`, `'static'` |
| `script_type` | `str` | `'simple'`, `'commands'`, `'solver_commands'` |
| `script` | `str \| List[str]` | Script content for scripted simulations |

---

## Accessing Analysis Results

After `sim.simulate()`, results are accessible via the `Analyses` manager:

```python
analysis = m.Analyses[sim.name]   # same name as the simulation
# or:
analysis = m.Analyses['run1']
```

Load from file:
```python
analysis = m.Analyses.createFromFile(file_name='my_model.res', name='imported')
```

### Analysis Properties

| Property | Type | Description |
|----------|------|-------------|
| `title` | `str` | Analysis title |
| `start_time` | `float` | Start time of results |
| `end_time` | `float` | End time of results |
| `step_count` | `int` | Number of result steps |
| `results_steps` | `Any` | Time values for result steps |
| `results_file` | `str` | Path to the `.res` file |
| `terminal_status` | `str` | Solver terminal status |
| `results` | `OrderedDict` | Nested result components |

### Navigating `analysis.results`

`results` is a nested `OrderedDict`. The structure is:
```
results
└── 'PART_NAME' (e.g., 'LINK_1')
    └── 'Characteristic' (e.g., 'CM Position')
        └── 'Component' (e.g., 'X')
            → ResultComponent object
                .values  →  List[float]  (one per time step)
```

```python
# List top-level groups (usually part names + forces)
print(list(analysis.results.keys()))

# Access a specific component
x_pos = analysis.results['LINK_1']['CM Position']['X']
print(x_pos.values)   # list of float

# Iterate all components
for group_name, group in analysis.results.items():
    if isinstance(group, dict):
        for char_name, char in group.items():
            if isinstance(char, dict):
                for comp_name, comp in char.items():
                    print(f'{group_name} / {char_name} / {comp_name}: {len(comp.values)} steps')
```

### Common Result Characteristics

| Characteristic | Components |
|---------------|------------|
| `CM Position` | `X`, `Y`, `Z`, `Mag` |
| `CM Velocity` | `X`, `Y`, `Z`, `Mag` |
| `CM Acceleration` | `X`, `Y`, `Z`, `Mag` |
| `Euler Angles` | `Psi`, `Theta`, `Phi` |
| `Angular Velocity` | `X`, `Y`, `Z`, `Mag` |
| `Element Force` | `X`, `Y`, `Z`, `Mag` |
| `Element Torque` | `X`, `Y`, `Z`, `Mag` |

---

## Measures (Tracked During Simulation)

Measures produce time-history data accessible after the run.

```python
# Object measure — track a property of a specific object
meas = m.Measures.createObject(
    name='LINK_VEL_X',
    object=link_body,                        # the object being measured
    characteristic='cm_velocity',            # what to measure
    component='x_component',                 # which component
    coordinate_rframe=ref_mkr,               # optional reference frame
    create_measure_display=True              # show in Adams View
)

# Pt2Pt measure — distance between two markers
d = m.Measures.createPt2pt(
    name='DIST_AB',
    from_point=mkr_a,
    to_point=mkr_b,
    characteristic='translational_displacement',
    component='mag_component'
)

# Function measure — arbitrary FUNCTION= expression
fm = m.Measures.createFunction(
    name='CONTACT_F',
    function='FZ(.model.wheel.cm, .model.ground.ref, .model.ground.ref)',
    units='force',
    legend='Contact Force Z'
)

# Angle measure (3 markers define the angle)
ang = m.Measures.createAngle(
    name='JOINT_ANGLE',
    first_point=mkr_a,
    middle_point=mkr_pivot,
    last_point=mkr_b
)
```

**Object measure characteristics** (partial list):
`cm_position`, `cm_velocity`, `cm_acceleration`, `cm_angular_velocity`, `cm_angular_acceleration`, `euler_angles`, `translational_velocity`, `angular_velocity`, `kinetic_energy`, `element_force`, `element_torque`, `power_consumption`

**Components**: `x_component`, `y_component`, `z_component`, `mag_component`

# Model, Parts, and Markers — Python API Reference

> **Authoritative stubs**: `references/adamspy-stubs/adamspy/Model.pyi`, `Part.pyi`, `Marker.pyi`

---

## Create a Model

```python
import Adams
m = Adams.Models.create(name='MY_MODEL')
```

`Adams.Models` is a `ModelManager`. `create()` returns a `Model` object.

To load a model from a `.adm` file:
```python
m = Adams.Models.newFromAdm(model_name='my_model', file_name='my_model.adm')
```

---

## Units

Set **before** creating geometry so all values are interpreted correctly.

```python
d = Adams.defaults
d.units.length = 'mm'
d.units.mass   = 'kg'
d.units.time   = 'second'
d.units.force  = 'newton'
d.units.angle  = 'degrees'
```

Or all at once:
```python
Adams.defaults.units.setUnits(length='mm', mass='kg', time='second', force='newton')
```

Valid length values: `'mm'`, `'cm'`, `'meter'`, `'km'`, `'inch'`, `'foot'`, `'mile'`
Valid mass values: `'kg'`, `'gram'`, `'pound_mass'`, `'slug'`, `'slinch'`, `'tonne'`
Valid time values: `'second'`, `'millisecond'`, `'minute'`, `'hour'`
Valid force values: `'newton'`, `'knewton'`, `'dyne'`, `'pound_force'`, `'kg_force'`

---

## Ground Part

The ground part is always present. Access it via:
```python
ground = m.ground_part    # Part object
ground = m.Parts['ground']
```

---

## Rigid Body

```python
part = m.Parts.createRigidBody(
    name='LINK_1',
    location=[0.0, 0.0, 100.0],    # global, in current units
    orientation=[0.0, 0.0, 0.0],   # psi, theta, phi in degrees
)
```

**Setting mass/inertia** — assign directly as properties after creation:
```python
part.mass = 1.5
part.ixx  = 1200.0
part.iyy  = 1200.0
part.izz  = 50.0
part.ixy  = 0.0
part.izx  = 0.0
part.iyz  = 0.0
```

Or assign material to compute from geometry:
```python
part.material_type = m.Materials['steel']
```

**Setting initial velocities**:
```python
part.vx = 0.0   # translational IC
part.vy = 100.0
part.vz = 0.0
part.wx = 0.0   # rotational IC (rad/s)
part.wy = 0.0
part.wz = 10.0
```

**Freezing initial position** (exact IC):
```python
part.exact_x = True
part.exact_z = True
```

**Key RigidBody properties**:

| Property | Type | Description |
|----------|------|-------------|
| `name` | `str` | Short name |
| `full_name` | `str` | `.MODEL.PART_NAME` |
| `location` | `List[float]` | Part origin in global coords (reassign fully) |
| `orientation` | `List[float]` | psi, theta, phi in degrees (reassign fully) |
| `mass` | `float` | Mass |
| `ixx`, `iyy`, `izz` | `float` | Principal inertias |
| `ixy`, `izx`, `iyz` | `float` | Products of inertia |
| `cm` | `Marker` | Center-of-mass marker (read-only unless redirected) |
| `im` | `Marker` | Inertia reference marker |
| `density` | `float` | Used when material_type is set |
| `material_type` | `Material` | Adams Material object |
| `ground_part` | `bool` | True if this is the ground |
| `Markers` | `MarkerManager` | Access/create child markers |
| `Geometries` | `GeometryManager` | Access/create child geometry |

---

## Point Mass

```python
pm = m.Parts.createPointMass(
    name='BALL',
    location=[0.0, 0.0, 200.0],
)
pm.mass = 0.5
```

Point masses have no rotational DOF. Use `createSpherical()` to constrain all 3 translational DOF.

---

## Flexible Body

```python
flex = m.Parts.createFlexBody(
    name='FLEX_LINK',
    modal_neutral_file_name='flex_link.mnf',
)
flex.damping_ratio = '0.02'
```

---

## FE Part

```python
mat = m.Materials.create(name='steel', youngs_modulus=2.07e5, poissons_ratio=0.29, density=7.8e-6)
mi = p.Markers.create(name='END_I', location=[0, 0, 0])
mj = p.Markers.create(name='END_J', location=[500, 0, 0])
fep = m.Parts.createFEPart(name='BEAM_FE', i_location=mi, j_location=mj, material_type=mat)
sec = m.Sections.createRectangular()
sec.rect_base = 20.0
sec.rect_height = 30.0
fep.setUniformSection(sec)
fep.addNode(0.25, section_label=sec)
fep.addNode(0.5,  section_label=sec)
fep.addNode(0.75, section_label=sec)
```

---

## Markers

```python
mkr = part.Markers.create(
    name='PIN_MKR',
    location=[0.0, 0.0, 0.0],       # local coordinates when relative_to is set
    orientation=[0.0, 0.0, 0.0],    # psi, theta, phi in degrees
    relative_to=part,               # optional; default is ground
)
```

**Marker properties**:

| Property | Type | Description |
|----------|------|-------------|
| `location` | `List[float]` | **Local** when getting, **global** when setting (reassign fully) |
| `orientation` | `List[float]` | psi, theta, phi in degrees |
| `location_global` | `List[float]` | Read-only global position |
| `relative_to` | `Marker` | Reference frame for relative coordinates |
| `reference_marker` | `Marker` | Alias for `relative_to` |
| `along_axis_orientation` | `List[float]` | Point z-axis toward this vector |
| `in_plane_orientation` | `List[float]` | Point x-axis toward this origin within xy-plane |

**Floating marker** (for force vectors that change their attachment point):
```python
fmkr = part.FloatingMarkers.create(name='F_MKR')
```

---

## Coordinate System (Adams.defaults)

Setting `Adams.defaults.coordinate_system` makes subsequent marker/part locations relative to that object instead of the global frame. Reset to `ground` when done.

```python
Adams.defaults.coordinate_system = part   # subsequent locations relative to part origin
mkr = part.Markers.create(name='CM', location=[0, 50, 0])
Adams.defaults.coordinate_system = m.ground_part   # restore
```

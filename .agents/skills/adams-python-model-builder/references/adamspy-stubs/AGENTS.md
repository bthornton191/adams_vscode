# Agent Instructions — adamspy-stubs

This repo contains Python type stubs (`.pyi` files) for the **MSC Adams Python API** (the `import Adams` interface embedded in Adams View 2023.1). The stubs are hand-maintained — they are NOT auto-generated from the Adams installation.

## Repo structure

```
adamspy/          # All stub files live here, matching Adams' module layout
  Adams.pyi         # Top-level session object
  Model.pyi
  Part.pyi
  Marker.pyi
  Constraint.pyi
  Force.pyi
  Geometry.pyi
  DataElement.pyi
  Simulation.pyi
  Analysis.pyi
  Measure.pyi
  Defaults.pyi
  DesignVariable.pyi
  Contact.pyi
  SystemElement.pyi
  Expression.pyi
  Object.pyi        # Base class hierarchy
  Manager.pyi       # AdamsManager / SubclassManager base classes
  Material.pyi
  Sensor.pyi
  RuntimeFunction.pyi
  Section.pyi
  ... (other supporting modules)
README.md
AGENTS.md         # This file
```

## What these stubs are

Each `.pyi` file is a stub for the corresponding Adams Python module. They provide:
- Class definitions with typed properties and method signatures
- Docstrings (where known) with parameter descriptions and examples
- Manager classes (e.g. `PartManager`, `ConstraintManager`) that expose `create*()` factory methods

The stubs are used by:
1. The [adams-vscode](https://github.com/bthornton191/adams_vscode) extension for IDE autocompletion
2. The `adams-python-model-builder` skill in [adams_skills](https://github.com/bthornton191/adams_skills) as a reference for generating correct API code

## Adams Python API conventions

Understanding these conventions is essential before editing stubs:

### Module layout

The `Adams` top-level module is the session entry point. Everything is accessed through manager objects:
```python
import Adams
m    = Adams.Models.create(name='MODEL_1')
part = m.Parts.createRigidBody(name='PART_1')
mkr  = part.Markers.create(name='MKR_1', location=[0, 0, 0])
```

### Manager pattern

Every collection of children is exposed as a typed manager. Managers support:
- `create(**kwargs)` / `createX(**kwargs)` — factory methods
- `__getitem__(name)` — lookup by short name
- `keys()`, `values()`, `items()` — iteration
- `keys_full()`, `items_full()` — iteration using full dot-path names
- `__contains__(name)` — membership test

Base classes in `Manager.pyi`:
- `AdamsManager` — single-type managers (e.g. `MarkerManager`)
- `SubclassManager` — multi-type managers (e.g. `PartManager` that creates `RigidBody`, `PointMass`, etc.)

### Object naming

Adams uses dot-path names: `.MODEL_NAME.PART_NAME.MARKER_NAME`. The `full_name` property on any object returns this path. Most `create*()` methods accept **either** an object reference (`i_marker=marker_obj`) or a full name string (`i_marker_name='.MODEL_1.PART_1.MKR_1'`).

### Array properties

Array-valued properties (location, orientation, stiffness, xyz_component_gravity, etc.) must be assigned as a whole — in-place element mutation is silently ignored by Adams:
```python
loc = marker.location   # get
loc[0] += 10            # modify copy
marker.location = loc   # reassign — required
```
Stubs should type these as `List[float]` (not `Tuple`).

### Expression parameterization

Properties can be set to an `AdamsExpr` (from `Expression.pyi`) to make them parametric:
```python
from Adams import expression
marker.location = expression('.MODEL_1.DV_LENGTH')
```

## Stub quality guidelines

When creating or updating stubs:

1. **Typed properties over `Any`** — Use concrete types (`float`, `str`, `List[float]`, `bool`, `Marker`, etc.) when known. Use `Any` only when the type is genuinely unknown or heterogeneous.
2. **Manager factory methods** — Always type the return value (`-> RigidBody`, `-> RevoluteJoint`, etc.). Include all known keyword parameters with their types. Use `**kwargs` to absorb unknown extras.
3. **Object references AND name strings** — For any parameter that accepts an object, include both the object form and the `_name: str` sibling (e.g. `i_marker: Marker = None` and `i_marker_name: str = None`).
4. **Docstrings from source `doc=` parameters** — Every `PropertyValue` subclass in the Adams source (e.g. `StringValue`, `RealValue`, `BoolValue`, `EnumValue`, `IntValue`, etc.) accepts a `doc=` keyword argument. Always carry that documentation into the stub as a property docstring (the string literal immediately following the annotation). The docstring may be improved or expanded beyond the raw `doc=` text for clarity, but must not contradict it. This applies to all properties — not just non-obvious ones.
5. **Enums as `Literal`** — Where a string parameter or property has a fixed set of valid values, **always** use `Literal['option1', 'option2', ...]` over bare `str`. This applies to both method parameters and class properties. The source uses `EnumValue(decoder={...})` or `EnumValue(decoder="SOME_STRINGS", decoder_count=N)` to mark these — check the source or doxygen HTML for the valid values. Use `float | int` syntax (not `Union[float, int]`) for union types.
6. **Don't invent API** — Only stub things that actually exist in Adams 2023.1. When unsure, use `Any` and add a comment.
7. **Base classes** — Respect the inheritance hierarchy. See `Object.pyi` for the base class chain (`ObjectBase → ObjectComment → Object`). Don't add properties to a subclass that belong on the base.

## Reference sources (for verifying/extending stubs)

The authoritative sources for Adams Python API signatures (in priority order):

1. **Doxygen HTML docs**: `C:\Program Files\MSC.Software\Adams\2023_1\adamspy\help\` — class reference with properties and method signatures
2. **Official example scripts**: `C:\Program Files\MSC.Software\Adams\2023_1\adamspy\examples\` — real usage patterns in `aview_modeling/` and `tutorials/`
3. **Intro docs**: `C:\Program Files\MSC.Software\Adams\2023_1\help\adams_python\python_intro.*.html` — execution methods, session object patterns

These are local to the developer's machine (Adams 2023.1 installation). If not available, use the doxygen class `.html` files from the `adamspy/help/` directory.

## Common tasks

### Adding a new class stub

1. Identify which `.pyi` file it belongs to (follow the module structure)
2. Find the class in the doxygen docs to confirm properties and methods
3. Inherit from the correct base class (`Object.Object`, `Force.Force`, `Geometry.Geometry`, etc.)
4. Add typed properties (prefer concrete types over `Any`)
5. If it's a creatable type, add the corresponding `createX()` method to the manager

### Updating an existing stub

1. Check the doxygen docs for the current signature
2. Prefer adding parameters over removing them (removing is a breaking change)
3. If changing a type annotation, verify against the example scripts

### Checking coverage

The doxygen `annotated.html` at `C:\Program Files\MSC.Software\Adams\2023_1\adamspy\help\annotated.html` lists all documented classes. Cross-reference against the `.pyi` files to find gaps.

## Adams terminology notes

- The fixed ground body is accessed as `model.ground_part` (a `Part` object) or via `model.Parts['ground']`
- "Marker" = a coordinate reference frame attached to a part (has `location` and `orientation`)
- "Floating marker" = a marker that follows motion — used as `j_floating_marker` in force vectors
- `i_marker` = the action marker (on the moving body); `j_marker` = the reaction marker
- `FUNCTION=` runtime expressions (STEP, IMPACT, AKISPL, etc.) are passed as plain strings to `.function` properties — they are evaluated by the Adams Solver at each timestep, not by Python
- Angles in Adams Python are in **degrees** by default when passed to `orientation=`

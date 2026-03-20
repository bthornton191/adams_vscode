# Naming Conventions — Adams Python API

---

## Dot-Path Object Names

Every Adams object has a **full name** using dot-path notation:

```
.MODEL_NAME.PART_NAME.MARKER_NAME
```

- The leading dot is required when using the full path.
- The **ground** part is always `.MODEL_NAME.ground`.
- Parts, markers, joints, forces, etc. all follow this hierarchy.

Access the full name of any object:
```python
print(part.full_name)    # e.g. '.MY_MODEL.LINK_1'
print(marker.full_name)  # e.g. '.MY_MODEL.LINK_1.PIN_MKR'
```

---

## Providing Names vs Objects

Most `create*()` and property assignment calls accept **either** an object reference or a string name. The `_name` suffix variant takes a string:

```python
# Object reference (preferred when already in scope)
joint = m.Constraints.createRevolute(i_marker=mkr_obj, j_marker=ground_mkr)

# String name (full dot-path)
joint = m.Constraints.createRevolute(
    i_marker_name='.MY_MODEL.LINK_1.PIN_MKR',
    j_marker_name='.MY_MODEL.ground.GROUND_MKR'
)
```

Both forms produce identical results. Use object references when the object was just created in the same script; use string names when referencing pre-existing model entities.

---

## Names with Special Characters

Names containing dots, spaces, or other special characters must be quoted with single quotes in full-path strings:

```python
# Part name "MY MODEL.Part 1" — note the dot and space require quoting
marker = Adams.stoo(".'MY MODEL.Part 1'.Marker_1")
```

The quoting applies at the **segment** level (each dot-separated component is quoted individually if it contains special chars).

---

## Manager Name Lookup

All managers support dictionary-style access by **short name** (no model prefix):

```python
part   = m.Parts['LINK_1']               # looks up by short name
marker = part.Markers['PIN_MKR']
joint  = m.Constraints['REV_JOINT']
```

Full-name iteration:
```python
for full_name in m.Parts.keys_full():
    print(full_name)    # e.g. '.MY_MODEL.LINK_1'

for full_name, part in m.Parts.items_full():
    ...
```

Membership test:
```python
if 'LINK_1' in m.Parts:
    print('part exists')
```

---

## Filtering Manager Values by Type

The `values(type_name)` method on a `SubclassManager` can filter by class:

```python
# Only rigid bodies, no flex bodies
for rb in m.Parts.values('RigidBody'):
    print(rb.name, rb.mass)

# Multiple types
for geom in part.Geometries.values('GeometryBlock', 'GeometryCylinder'):
    print(geom.name)
```

---

## Naming Conventions (Recommended Style)

| Entity | Convention | Example |
|--------|-----------|---------|
| Model | `UPPER_SNAKE_CASE` | `MY_MODEL` |
| Part | `UPPER_SNAKE_CASE` | `LINK_1`, `GROUND` |
| Marker | `UPPER_SNAKE_CASE` suffixed | `PIN_MKR`, `CM_MKR`, `TIP_MKR` |
| Joint | `TYPE_NUMBER` | `REV_1`, `TRANS_SLIDER` |
| Force | Descriptive | `SPRING_MAIN`, `BUSH_MOUNT` |
| Design variable | `DV_` prefix | `DV_LENGTH`, `DV_SPRING_K` |
| Simulation | Descriptive | `SIM_TRANSIENT`, `RUN_1` |

Adams names are **case-insensitive** in lookups but the case you set is preserved in the UI.

---

## Python Variable Naming

No special requirements — use standard Python naming for your Python variables. The Adams object name (`.name` property) is independent of the Python variable name:

```python
my_var = m.Parts.createRigidBody(name='LINK_1')  # Adams name = 'LINK_1'
# my_var and m.Parts['LINK_1'] both refer to the same object
```

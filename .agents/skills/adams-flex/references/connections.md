# Flex Body Connections Reference

## Table of Contents
1. [Marker Placement on Flex Bodies](#marker-placement)
2. [FORTRAN vs C++ Solver Capability Matrix](#solver-capabilities)
3. [Massless Link (Dummy Part) Pattern](#massless-link)
4. [Flex Body Contacts](#contacts)
5. [Replacing Rigid Bodies with Flex Bodies](#replacement)
6. [Modal Forces (MFORCE)](#modal-forces)

---

## Marker Placement on Flex Bodies {#marker-placement}

Markers on a flex body must be associated with a node from the MNF. Three configurations exist:

| Configuration | FORTRAN Solver | C++ Solver | Notes |
|---|---|---|---|
| **Coincident** — marker position = node location | ✅ Direct | ✅ Direct | Default; most compatible |
| **Offset** — marker position ≠ node location | ⚠️ Auto massless link | ✅ Direct | Offset acts as rigid lever arm |
| **Multi-node** — marker shared across nodes | ❌ Not supported | ✅ Direct | Distributes load over node patch |

### Marker on Flex Body — Python API
```python
# Coincident marker at a node
marker = flex.Markers.create(
    name='ATTACH_1',
    node_id=1247,                   # Must be a valid node ID from the MNF
)

# Offset marker (C++ solver only; auto-creates massless link in FORTRAN)
marker = flex.Markers.create(
    name='ATTACH_OFFSET',
    node_id=1247,
    location=[x_offset, y_offset, z_offset],   # offset in global coords
)

# Multi-node marker (C++ solver only)
marker = flex.Markers.create(
    name='ATTACH_PATCH',
    node_ids=[1247, 1248, 1249],    # distributes forces across these nodes
)
```

### Marker on Flex Body — .adm (dataset)
```
MARKER/101, FLEX_BODY=5, NODE_ID=1247
MARKER/102, FLEX_BODY=5, NODE_ID=1248, QP=5.0, 0.0, 0.0  ! offset
```

### Finding Node IDs
Use the **Adams Flex Toolkit** (see toolkit.md) to browse the MNF and find node IDs at your desired attachment locations. Alternatively, look at your FEA model — node IDs in the MNF are the same as in the FE model.

---

## FORTRAN vs C++ Solver Capability Matrix {#solver-capabilities}

The Adams Solver has two versions: **C++ (default, modern)** and FORTRAN (deprecated, legacy). C++ has been the default since Adams 2018 and removes nearly all flex body connection restrictions. FORTRAN is rarely encountered in modern workflows — it requires explicit opt-in via `PREFERENCES/SOLVERBIAS=F77`. Unless the user specifically mentions the FORTRAN solver or legacy models, assume C++.

### Joints

| Joint Type | FORTRAN | C++ |
|---|---|---|
| Fixed | ✅ | ✅ |
| Revolute | ✅ | ✅ |
| Spherical | ✅ | ✅ |
| Hooke / Universal | ✅ | ✅ |
| Translational | ⚠️ Auto massless link if driven | ✅ |
| Cylindrical | ⚠️ Auto massless link if driven | ✅ |
| Planar | ⚠️ Auto massless link | ✅ |
| Rack-and-Pinion | ⚠️ Auto massless link | ✅ |
| **Any joint with MOTION** | ⚠️ Auto massless link | ✅ |

### Forces / Connectors

| Element | FORTRAN | C++ |
|---|---|---|
| SFORCE (translational) | ✅ | ✅ |
| NFORCE | ✅ | ✅ |
| MFORCE (modal force) | ✅ | ✅ |
| ACCGRAV | ✅ | ✅ |
| VFORCE / VTORQUE (flex body as reaction) | ❌ → massless link | ✅ |
| Multi-component VFORCE | ❌ → massless link | ✅ |
| Bushing | ❌ → massless link | ✅ |
| Beam | ❌ → massless link | ✅ |
| Field element | ❌ → massless link | ✅ |
| Torsion spring-damper | ❌ → massless link | ✅ |

### Contacts

| Contact Type | FORTRAN | C++ |
|---|---|---|
| Point-to-plane (point on flex) | ✅ (1 point per CONTACT) | ✅ |
| Flex-to-Solid (mesh contact) | ❌ | ✅ |
| Flex-to-Flex | ❌ | ✅ |
| Flex edge-to-curve | ❌ | ✅ |

### Switch to C++ Solver
Add to `.acf` or set in Adams View preferences:
```
PREFERENCES/SOLVER=CPP
SIMULATE/DYNAMIC, END=1.0, DTOUT=0.01
```

---

## Massless Link (Dummy Part) Pattern {#massless-link}

Used when a force or joint cannot connect directly to a flex body (FORTRAN solver) or when load distribution requires an intermediate rigid part.

### When Required (FORTRAN)
- Beams, bushings, field elements, torsion springs connected to flex body
- VFORCE/VTORQUE with flex body as the reaction body
- Translational/cylindrical joints with motion
- Any joint with MOTION applied

### Manual Creation

**Adams View GUI**:
1. Create a rigid body part
2. Open Part Modify → set Mass = 0 (or remove geometry completely)
3. Set IXX = IYY = IZZ = 0
4. Connect to flex body with a **Fixed joint**
5. Attach the unsupported element to the massless link

**Python API**:
```python
# Create the dummy part
dummy = m.Parts.createRigidBody(name='DUMMY_LINK_1')
dummy.mass = 0.0
dummy.ixx = 0.0; dummy.iyy = 0.0; dummy.izz = 0.0

# Connect dummy to flex body with fixed joint
m_flex = flex.Markers.create(name='M_FIXED_FLEX', node_id=1247)
m_dummy = dummy.Markers.create(name='M_FIXED_DUMMY', location=[x, y, z])

m.Constraints.createJoint(
    name='FIXED_FLEX_DUMMY',
    joint_type='fixed',
    i_marker_name='.model.FLEX_BODY.M_FIXED_FLEX',
    j_marker_name='.model.DUMMY_LINK_1.M_FIXED_DUMMY',
)

# Now attach bushing/beam/etc. to dummy
```

### Automatic Creation (FORTRAN only)
Adams FORTRAN solver automatically creates massless links when it detects an incompatible connection. These auto-links are invisible in Adams View but appear in the `.msg` file. **Limitation**: reaction forces at auto-created massless links are NOT available in results output.

---

## Flex Body Contacts {#contacts}

### Mesh-Based Contact (C++ Solver Only)

```python
# Flex-to-Solid contact
contact = m.Contacts.createFlexToSolid(
    name='FLEX_GROUND_CONTACT',
    i_geometry=flex.Geometries['FLEX_SURFACE'],   # flex body geometry
    j_geometry=m.Parts['GROUND_PLATE'].Geometries['PLATE_SURF'],
    stiffness=1e5,
    damping=100.0,
    exponent=2.2,
    max_penetration_depth=0.1,
)

# Flex-to-Flex contact
contact = m.Contacts.createFlexToFlex(
    name='FLEX_FLEX_CONTACT',
    i_geometry=flex1.Geometries['SURF_1'],
    j_geometry=flex2.Geometries['SURF_2'],
    stiffness=1e5,
    damping=50.0,
)

# Flex edge-to-curve contact
contact = m.Contacts.createFlexEdgeToCurve(
    name='FLEX_EDGE_CRV',
    i_geometry=flex.Geometries['EDGE_GEO'],
    j_geometry=m.Parts['GUIDE'].Geometries['GUIDE_CURVE'],
    stiffness=5e4,
    damping=20.0,
)
```

### Point Contact (FORTRAN + C++)
For FORTRAN compatibility, limit to a single contact point located on the flex body surface:
```python
# One contact point per CONTACT element in FORTRAN
m.Contacts.createPointToSurface(
    name='PT_CONTACT_1',
    i_marker_name='.model.FLEX_LINK.CONTACT_PT',  # marker on flex node
    j_geometry=m.Parts['GROUND'].Geometries['SURF'],
)
```

---

## Replacing Rigid Bodies with Flex Bodies {#replacement}

Use the **Rigid to Flex** tool for an automated swap that handles marker/joint transfer.

### GUI Workflow (Rigid to Flex)
**Path**: Build → Flexible Bodies → Rigid to Flex

1. **Select rigid body** to replace
2. **Select MNF/MD DB** file
3. **Align flex body**: choose CM alignment, 3-point, or Precision Move
4. **Review Marker-Node table**: Adams maps each rigid body marker to the nearest flex body node
   - Interface node markers → searched within interface node set first
   - Other markers → searched from full nodal set
   - **Review all mappings** before proceeding — incorrect node assignments cause wrong force transmission
5. **Adjust node assignments** if needed (click a row and select a different node)
6. **Choose marker positioning strategy**:
   - *Move to node*: simplest; marker placed exactly at node (smallest model size)
   - *Preserve location*: keeps parameterized marker expressions
   - *Preserve expression*: maintains Adams View function dependencies
7. **Execute swap** — rigid body is replaced; optionally keep original rigid body (renamed, hidden)

### Flex to Flex Replacement
**Path**: Build → Flexible Bodies → Flex to Flex

Used to swap one flexible body for another (e.g., updated MNF revision). Preserves:
- Selected modes, invariant selection
- Modal displacements and velocities
- Color, visibility, icon settings

### After Replacement — What to Check
1. Verify **DOF count** in `.msg` file hasn't changed unexpectedly
2. Run **Adams Linear** to compare frequencies with FEA predictions
3. Check **Info tool** on the new flex body for correct mass and units
4. Inspect any **auto-created massless links** — the `.msg` file will list them

### Python API (Replacement)
```python
# No direct createFlexFromRigid() API — use the GUI workflow or:
# 1. Delete the rigid body
# 2. Create a new flex body at the same location
# 3. Recreate joints/forces with the new flex body markers
```

---

## Modal Forces (MFORCE) {#modal-forces}

An MFORCE applies a distributed load to a flex body in modal coordinates. Unlike point forces, modal forces work with the mode shapes directly.

### When to Use MFORCE
- Distributed aerodynamic/fluid loads on the flex body
- Loads defined from FEA load cases (preloads / applied loads from MNF)
- Feedback control forces distributed over the structure

### Python API
```python
mforce = m.Forces.createModalForce(
    name='AERO_LOAD',
    flexible_body=flex,
    force_function='STEP(TIME, 0.1, 0.0, 0.2, 1000.0)',  # ramp in load
)
```

### .adm Dataset
```
MFORCE/10, FLEX_BODY=5, FUNCTION=STEP(TIME,0.1,0,0.2,1000)
```

### Load Cases from MNF
If the MNF contains preloads or applied modal loads (exported via `mnfload`), select them in:
- Adams View: Flexible Body Modify → Loads tab → Load Case Selection
- Or set in `.adm` via the `MODLOAD` matrix reference

See toolkit.md for creating load cases with `mnfload`.

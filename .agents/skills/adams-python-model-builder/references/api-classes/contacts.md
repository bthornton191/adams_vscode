# Contacts — Python API Reference

> **Authoritative stub**: `references/adamspy-stubs/adamspy/Contact.pyi`

Contacts are created via `model.Contacts.createX(**kwargs)`.

---

## Solid-to-Solid Contact (most common)

```python
contact = m.Contacts.createSolidToSolid(
    name='CONTACT_1',
    i_geometry=wheel_solid,       # GeometrySolid or list of GeometrySolid
    j_geometry=ground_solid,
    stiffness=1.0e5,              # N/mm
    damping=50.0,                 # N·s/mm
    dmax=0.1,                     # penetration depth for full damping (mm)
    exponent=2.2                  # force-deflection exponent (1.5 typ. for metal)
)
```

**Key contact properties**:

| Property | Type | Description |
|----------|------|-------------|
| `stiffness` | `float` | Contact stiffness |
| `damping` | `float` | Damping coefficient |
| `dmax` | `float` | Penetration at which damping is fully applied |
| `exponent` | `float` | Hertzian exponent (1.5 for spherical, 2.0–2.5 for other) |
| `mu_static` | `float` | Static friction coefficient |
| `mu_dynamic` | `float` | Dynamic friction coefficient |
| `friction_transition_velocity` | `float` | Velocity above which dynamic friction applies |
| `stiction_transition_velocity` | `float` | Velocity below which stiction applies |
| `coulomb_friction` | `str` | `'on'` or `'off'` |
| `normal_function` | `str` | Override with custom FUNCTION= expression |
| `restitution_coefficient` | `float` | Coefficient of restitution (POISSON formulation) |

---

## Other Contact Types

```python
# Sphere to plane
m.Contacts.createSphereToPlane(name='SPH_PLN', ...)

# Sphere to sphere
m.Contacts.createSphereToSphere(name='SPH_SPH', ...)

# Curve to curve
m.Contacts.createCurveToCurve(name='CRV_CRV', ...)

# Point to curve
m.Contacts.createPointToCurve(name='PT_CRV', ...)

# Point to plane
m.Contacts.createPointToPlane(name='PT_PLN', ...)

# Curve to plane
m.Contacts.createCurveToPlane(name='CRV_PLN', ...)

# Cylinder to cylinder
m.Contacts.createCylinderToCylinder(name='CYL_CYL', ...)

# Flexible body contacts
m.Contacts.createFlexToSolid(name='FLEX_SLD', ...)
m.Contacts.createFlexToFlex(name='FLEX_FLEX', ...)
m.Contacts.createFlexEdgeToCurve(name='FEDGE_CRV', ...)
```

---

## Notes

- Contact geometry objects are `GeometrySolid` or other `Geometry` subclasses. Create them on a part via `part.Geometries.createX()` first, then reference them in the contact.
- For FUNCTION=expression-based contact, use `createSingleComponentForce()` with `IMPACT()` or `BISTOP()` expressions instead of a contact element.
- The `i_geometry` and `j_geometry` properties accept either a single object or a list when multiple geometry pieces are involved.

# part modify rigid_body mass_properties

Allows the modification of mass properties on an existing part.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `part_name` | A Existing Part | Specifies the name of a rigid body |
| `mass` | Mass | Specifies the part mass |
| `center_of_mass_marker` | An Existing Marker | Specifies the marker to define center of mass |
| `inertia_marker` | An Existing Marker | Specifies the marker that defines the inertia properties of the rigid body |
| `ixx` | Inertia | Specifies the xx component of the mass-inertia tensor |
| `iyy` | Inertia | Specifies the yy component of the mass-inertia tensor |
| `izz` | Inertia | Specifies the zz component of the mass-inertia tensor |
| `ixy` | Inertia | Specifies the xy component of the mass-inertia tensor |
| `izx` | Inertia | Specifies the zx component of the mass-inertia tensor |
| `iyz` | Inertia | Specifies the yz component of the mass-inertia tensor |
| `density` | Density | Specifies the part density |
| `material_type` | An Existing Material | Specifies the material type |

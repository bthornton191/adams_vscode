# part create rigid_body mass_properties

Allows you to create mass properties on an existing part.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `part_name` | An Existing Part | Specifies the part to be modified. You use this parameter to identify the existing part to be affected with this command. |
| `mass` | Mass | Specifies the part mass |
| `center_of_mass_marker` | An Existing Marker | Specifies the marker that defines the part center of mass and, in the absence of the inertia marker, the axes for the inertia properties. |
| `inertia_marker` | An Existing Marker | Specifies the marker that defines the axes for the inertia properties. If you do not supply an inertia marker, it defaults to the part center-of-mass marker. |
| `ixx` | Inertia | Specifies the xx component of the mass-inertia tensor as computed about the origin of the inertia marker, and expressed in the coordinates of the inertia marker reference frame. |
| `iyy` | Inertia | Specifies the yy component of the mass-inertia tensor as computed about the origin of the inertia marker, and expressed in the coordinates of the inertia marker reference frame. |
| `izz` | Inertia | Specifies the zz component of the mass-inertia tensor as computed about the origin of the inertia marker, and expressed in the coordinates of the inertia marker reference frame. |
| `ixy` | Inertia | Specifies the xy component of the mass-inertia tensor as computed about the origin of the inertia marker, and expressed in the coordinates of the inertia marker reference frame. |
| `iyz` | Inertia | Specifies the yz component of the mass-inertia tensor as computed about the origin of the inertia marker, and expressed in the coordinates of the inertia marker reference frame. |
| `izx` | Inertia | Specifies the zx component of the mass-inertia tensor as computed about the origin of the inertia marker, and expressed in the coordinates of the inertia marker reference frame. |
| `material_type` | An Existing Material | Specifies the part material_type and that the mass properties of the part are to be automatically calculated |
| `density` | Density | Specifies the part density and that the mass properties of the part are to be automatically calculated. |

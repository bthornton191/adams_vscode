# part modify stress_body

Allows you to modify an existing stress body.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `rigid_stress_name` | An Existing Stress Body | Specifies the name of the existing stress body to modify. |
| `new_rigid_stress_name` | A New Stress Body | Specifies a new name for the stress body. |
| `geometry` | An Existing Solid Geometry | Specifies the solid contact geometry to use for the stress body mesh. |
| `part_name` | An Existing Part | Specifies the rigid body part that the stress body is associated with. |
| `mesh_opts` | Integer | Specifies meshing option flags controlling how the mesh is generated. |
| `mesh_props` | Real | Specifies real-valued meshing properties. |
| `mesh_angles` | Angle | Specifies angular mesh properties used during mesh generation. |
| `mesh_lengths` | Length | Specifies length-based mesh properties used during mesh generation. |
| `load_opts` | Integer | Specifies load option flags controlling how loads are applied. |
| `load_feature_angle` | Angle | Specifies the feature angle used to identify edges for load application. |
| `contact_radius` | Length | Specifies the contact radius for distributing contact forces over the stress body nodes. |

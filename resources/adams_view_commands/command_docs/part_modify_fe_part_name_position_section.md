# part modify fe_part name_position_section

Allows you to modify an entity of the type fe_part in the Adams session. An fe_part defines a geometrically non-linear part.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `fe_part_name` | string | Specifies the name of the fe part to be modified. |
| `ref_curve` | Existing GCURVE | Specifies the already created bspline curve to be used as the reference centerline for the fe_part. |
| `i_marker` | Existing marker/ point | Along with j_marker, specifies the already created marker/point as reference to define the centerline for the fe_part. |
| `j_marker` | Existing marker/ point | Along with i_marker, specifies the already created marker/point as reference to define the centerline for the fe_part. |
| `i_hard_point` | Existing point | Along with i_point, specifies already created point as reference to define centerline for fe_part. |
| `j_hard_point` | Existing point | Along with j_point, specifies already created point as reference to define centerline for fe_part. |
| `material_type` | Existing Material | Specifies the identifier of the existing MATERIAL statement used by this fe_part. |
| `cratiok` | real | Stiffness Matrix |
| `cratiom` | real | Mass Matrix |
| `fepart_type` | Option | Specifies the formulation type of fe_part. |
| `preload` | string | Specifies the name of a file containing preloaded conditions information for this fe_part. |
| `external` | Option | Specifies if external geometry need to be used for fe part. If yes, then only external geometry will be rendered. |
| `location` | real,real,real | Specifies the x,y,z Cartesian coordinates to move the FE_PART object to relative to ground. |
| `orientation` | real,real,real | Specifies the body 313 (body-fixed z,x,z) euler angles to rotate the FE_PART object relative to ground. |
| `nodes_at_curve_points` | Option | Support FE part's centerline and node locations parameterization with curve control points.See Nodes Parameterization for more information. |

# move mirror

Allows you to mirror parts, markers, geometry, forces, and constraints across a plane defined by the LPRF of a part, or a marker.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `marker_name` | Existing marker | Specifies the marker to modify. You use this parameter to identify the existing marker to affect with this command. |
| `part_name` | Existing part | Specifies the part to modify. You use this parameter to identify the existing part to affect with this command. |
| `flexible_body_name` | Existing flex body | Specifies the name of an existing flexible body to modify. |
| `point_mass_name` | Existing point mass | Specifies the point_mass to modify. You use this parameter to identify the existing point_mass to affect with this command. |
| `geometry_name` | Existing geometry | Specifies the geometry to modify. You use this parameter to identify the existing geometry to affect with this command. |
| `constraint_name` | Existing constraint | Specifies the constraint to modify. You use this parameter to identify the existing constraint to affect with this command. |
| `force_name` | Existing force | Specifies the force to modify. You use this parameter to identify the existing force to affect with this command. |
| `group_name` | Existing group | Specifies the group to modify. You use this parameter to identify the existing group to affect with this command. |
| `entity_name` | Existing entity | Specify 1 or more existing entities. |
| `plane` | Mirror_axes | Specifies which plane of the reference frame to mirror across. |
| `axes` | Mirror_axes | Specifies which two axes of the part LPRF, marker, or markers associated with the geometry, force or constraint are mirrored. |
| `relative_to` | Existing part, body or marker | Specifies the LPRF of a part, or a marker, through which the mirror plane runs. |
| `csmodel_name` | Existing model | Specifies an existing model's global origin to use as the coordinate system in a MOVE, or PANEL SET POSITION & ORIENTATION command. |
| `cspart_name` | Existing part | Specifies an existing part to use as the coordinate system in a MOVE, or PANEL SET POSITION & ORIENTATION command. |
| `csmarker_name` | Existing marker | Specifies an existing marker to use as the coordinate system in a MOVE, or PANEL SET POSITION & ORIENTATION command. |
| `csview_name` | Existing view | Specifies an existing view's origin to use as the coordinate system in a MOVE, or PANEL SET POSITION & ORIENTATION command. |
| `csentity_name` | Existing entity | Specifies an existing entity's origin to use as the coordinate system in a MOVE, or PANEL SET POSITION & ORIENTATION command. |

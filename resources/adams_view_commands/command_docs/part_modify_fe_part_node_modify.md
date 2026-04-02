# part modify fe_part node_modify

Allows you to modify an existing node on a finite element part.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `fe_node_name` | An Existing FE Node | Specifies the name of the existing FE node to modify. |
| `new_fe_node_name` | A New FE Node | Specifies a new name for the FE node. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `label` | Integer | Specifies the integer label identifying the node within the FE part. |
| `s` | Real | Specifies the normalized arc length parameter (0 to 1) locating the node along the FE part. |
| `angle` | Real | Specifies the angular position of the node around the cross-section perimeter. |
| `location` | Location | Specifies the explicit location of the node. |
| `orientation` | Orientation | Specifies the orientation of the node coordinate system using three rotation angles. |
| `along_axis_orientation` | Location | Specifies the orientation by directing one of the axes. Adams View will assign an arbitrary rotation about the axis. |
| `in_plane_orientation` | Location | Specifies the orientation by directing one of the axes and locating one of the coordinate planes. |
| `natural_coordinates_relative_orientation` | Orientation | Specifies the orientation relative to the natural coordinates of the FE part cross-section. |
| `section_label` | An Existing Section | Specifies the cross-section assigned to this node location. |
| `tessellate` | Boolean | Specifies whether to tessellate the geometry at this node. |

# part create fe_part node_create

Allows you to create a node on an existing finite element part.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `fe_node_name` | A New FE Node | Specifies the name of the new FE node. |
| `fe_part_name` | An Existing FE Part | Specifies the FE part on which the node is created. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `label` | Integer | Specifies the integer label identifying the node within the FE part. |
| `s` | Real | Specifies the normalized arc length parameter (0 to 1) locating the node along the FE part. |
| `angle` | Real | Specifies the angular position of the node around the cross-section perimeter. |
| `location` | Location | Specifies the explicit location of the node. |
| `index` | Integer | Specifies the index used to identify the node in ordered arrays. |
| `orientation` | Orientation | Specifies the orientation of the node coordinate system using three rotation angles. |
| `along_axis_orientation` | Location | Specifies the orientation by directing one of the axes. Adams View will assign an arbitrary rotation about the axis. |
| `in_plane_orientation` | Location | Specifies the orientation by directing one of the axes and locating one of the coordinate planes. |
| `natural_coordinates_relative_orientation` | Orientation | Specifies the orientation relative to the natural coordinates of the FE part cross-section. |
| `section_label` | An Existing Section | Specifies the cross-section assigned to this node location. |
| `tessellate` | Boolean | Specifies whether to tessellate the geometry at this node. |

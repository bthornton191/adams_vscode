# section modify

Modifies the cross-section properties of an existing section used for flexible body beams or NLFE elements.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `section_name` | Object | Name of the section to modify. |
| `new_section_name` | String | New name for the section. |
| `autocalculate` | Boolean | Whether to automatically calculate section properties from geometry. |
| `adams_id` | Integer | Adams internal ID for the section. |
| `section_properties` | String | Explicit section property type identifier. |
| `section_solid_cylinder` | Boolean | Whether to define the section as a solid cylinder. |
| `cyl_radius` | Real | Outer radius of the cylinder. |
| `cyl_thickness` | Real | Wall thickness for a hollow cylinder (0 = solid). |
| `section_solid_rectangle` | Boolean | Whether to define the section as a solid rectangle. |
| `rect_height` | Real | Height of the rectangular cross-section. |
| `rect_base` | Real | Base width of the rectangular cross-section. |
| `rect_thickness` | Real | Wall thickness for a hollow rectangle (0 = solid). |
| `major_radius` | Real | Major radius for elliptical sections. |
| `minor_radius` | Real | Minor radius for elliptical sections. |
| `start_angle` | Real | Start angle for partial arc sections (degrees). |
| `end_angle` | Real | End angle for partial arc sections (degrees). |
| `ib_height` | Real | Total height of an I-beam section. |
| `ib_base` | Real | Base flange width of an I-beam section. |
| `ib_flange` | Real | Flange thickness of an I-beam section. |
| `ib_web` | Real | Web thickness of an I-beam section. |
| `xy_points` | Array | 2D point list defining the cross-section outline in the XY plane. |
| `zy_points` | Array | 2D point list defining the cross-section outline in the ZY plane. |
| `iyz` | Real | Product of inertia Iyz of the cross-section. |
| `iyy` | Real | Second moment of area about the Y axis. |
| `izz` | Real | Second moment of area about the Z axis. |
| `area` | Real | Cross-sectional area. |
| `jxx` | Real | Torsional constant (polar moment) of the cross-section. |

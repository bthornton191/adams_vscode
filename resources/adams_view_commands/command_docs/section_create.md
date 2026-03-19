# section create

Allows you to create new cross sections in the Adams session. These section entities can be then used to create a new FE Part by specifying these created sections at the different nodes of the FE Part.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `section_name` | New Section | Specifies the name of the section to be created. |
| `cyl_radius` | Real | Specifies the radius of the cylinder if the section is cylindrical in nature. |
| `cyl_thickness` | Real | Specifies the thickness of the cylinder if the section is cylindrical in nature and is hollow. |
| `rect_height` | Real number >= 0 | Specifies the height of the rectangle if the section is rectangular in nature. |
| `rect_base` | Real number >= 0 | Specifies the base of the rectangle if the section is rectangular in nature. |
| `rect_thickness` | Real | Specifies the thickness of the rectangle if the section is rectangular and hollow in nature. |
| `major_radius` | Real | Specifies the major radius of the ellipse if the section is elliptical in nature. Default value is 1.0 if not specified. |
| `minor_radius` | Real | Specifies the minor radius of the ellipse if the section is elliptical in nature. Default value is 1.0 if not specified. |
| `start_angle` | Real | Specifies the start angle of the ellipse if the section is elliptical in nature. By default this is 0.0 if not specified. |
| `end_angle` | Real | Specifies the start angle of the ellipse if the section is elliptical in nature. By default this is 360.0 degrees if not specified. |
| `ib_height` | Real number >= 0.0 | Specifies the height of the beam if the section is in the form of a beam. |
| `ib_base` | Real number >= 0.0 | Specifies the base dimension of the beam if the section is in the form of a beam. |
| `ib_flange` | Real number >= 0.0 | Specifies the flange of the beam if the section is in the form of a beam. |
| `ib_web` | Real number >= 0.0 | Specifies the web of the beam if the section is in the form of a beam. |
| `iyz` | Real number >= 0.0 | Specifies the product of inertia with respect to the Y and Z axes. Defaults to 10. |
| `iyy` | Real number >= 0.0 | Specifies the moment of inertia about the Y axis. Defaults to 10. |
| `izz` | Real number >= 0.0 | Specifies the moment of inertia about the Z axis. Defaults to 10. |
| `jxx` | Real number >= 0.0 | Specifies the polar moment of inertia. It is the torsional constant which is used to assemble the torsional equation of motion describing the ability to resist torque. |
| `area` | Real number >= 0.0 | Specifies the area of the section. Defaults to 10. |
| `xy_points` | Location | Specifies the location of the series of points defining the generic cross section in an x-y plane. Because the local cross sectional plane of an FE Part is expressed in local z-y coordinates, we no longer recommend using this option. Instead use the z-y option. Existing scripts that make use of the xy_points argument will continue to be supported but in the interactive section editor dialog they will be mapped to the equivalent z-y points and displayed that way. Furthermore, subsequent cmd file export actions will convert to an equivalent zy_points argument. |
| `zy_points` | Location | Specifies the location of the series of points defining the generic cross section in the FE Part's local z-y plane. The x-axis follows the FE Part centerline; so, z-y points define the cross-sectional plane. |

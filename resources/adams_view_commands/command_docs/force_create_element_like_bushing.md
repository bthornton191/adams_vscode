# force create element_like bushing

Allows you to create a bushing object.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `bushing_name` | String | Specifies the name of the new bushing. You may use this name later to refer to this bushing. Adams View will not allow you to have two bushings with the same name, so you must provide a unique name. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `damping` | Real number greater than or equal to 0 | Specifies three viscous damping coefficients for the bushing force. |
| `stiffness` | Real number greater than 0 | Specifies three stiffness coefficients for the bushing force. |
| `force_preload` | Real number | Specifies a vector of three constant terms for the bushing force. |
| `tdamping` | Real number greater than or equal to 0 | Specifies three viscous damping coefficients for the bushing torque. |
| `shear_modulus` | Real number greater than 0 | Specifies the shear modulus of elasticity for the beam material. |
| `length` | Real number greater than 0 | Specifies the undeformed length of the beam along the x-axis of the J marker. |
| `location` |  | Specifies the locations to be used to define the position of a force during its creation. |
| `orientation` |  | Specifies the orientation of the J marker for the force being created using three rotation angles. |
| `along_axis_orientation` |  | Specifies the orientation of a coordinate system (e.g. marker or part) by directing one of the axes. Adams View will assign an arbitrary rotation about the axis. |
| `in_plane_orientation` |  | Specifies the orientation of a coordinate system (e.g. marker or part) by directing one of the axes and locating one of the coordinate planes. |
| `relative_to` |  | Specifies the coordinate system that location coordinates and orientation angles correspond to. |
| `i_marker_name` |  | Specifies a marker on the first of two parts connected by this force element. Adams View connects this element to one part at the I marker and to the other at the J marker. |
| `j_marker_name` |  | Specifies a marker on the second of two parts connected by this force element. Adams View connects this element to one part at the I marker and to the other at the J marker. |

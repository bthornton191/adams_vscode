# force create element_like beam

Allows you to create a beam object.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `beam_name` | String | Specifies the name of the new beam. You may use this name later to refer to this beam. View will not allow you to have two beams with the same name, so you must provide a unique name. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `ixx` | Real number greater than 0 | Specifies the polar area moment of inertia about the X axis of a cross section perpendicular to the length of the beam. |
| `iyy` | Real number greater than 0 | Specifies the principal area moment of inertia about the Y axis of a cross section perpendicular to the length of the beam. |
| `izz` | Real number greater than 0 | Specifies the principal area moment of inertia about the z axis of a cross section perpendicular to the length of the beam. |
| `y_shear_area_ratio` | Real number greater than 0 | Specifies the shear area ratio in the y direction. This is the correction factor for shear deflection in the y direction for Timeshenko beams. |
| `z_shear_area_ratio` | Real number greater than 0 | Specifies the shear area ratio in the y direction. This is the correction factor for shear deflection in the z direction for Timeshenko beams. |
| `youngs_modulus` | Real number greater than 0 | Specifies Young's modulus of elasticity for the beam material. |
| `shear_modulus` | Real number greater than 0 | Specifies the shear modulus of elasticity for the beam material. |
| `length` | Real number greater than 0 | Specifies the undeformed length of the beam along the x axis of the J marker. |
| `area_of_cross_section` | Real number greater than 0 | Specifies the uniform area of the beam cross section. |
| `damping ratio` | Real number greater than 0 | Specifies a ratio for calculating the structural damping matrix for the beam. Adams multiplies the stiffness matrix by the value of DAMPING_RATIO to obtain the damping matrix. |
| `matrix_of_damping_terms` |  | Specifies a six-by-six structural damping matrix for the beam. |
| `location` |  | Specifies the locations to be used to define the position of a force during its creation. |
| `orientation` |  | Specifies the orientation of the J marker for the force being created using three rotation angles. |
| `along_axis_orientation` |  | Specifies the orientation of a coordinate system (e.g. marker or part) by directing one of the axes. Adams View will assign an arbitrary rotation about the axis. |
| `in_plane_orientation` |  | Specifies the orientation of a coordinate system (e.g. marker or part) by directing one of the axes and locating one of the coordinate planes. |
| `i_part_name` |  | Specifies the part that is the first of the two parts that this force acts between. |
| `j_part_name` |  | Specifies the part that is the second of the two parts that this force acts between. Adams View applies the force on one part at the J marker and the other at the I marker. These markers are automatically generated using this method of force creation. |
| `i_marker_name` |  | Specifies a marker on the first of two parts connected by this force element. Adams View connects this element to one part at the I marker and to the other at the J marker. |
| `j_marker_name` |  | Specifies a marker on the second of two parts connected by this force element. Adams View connects this element to one part at the I marker and to the other at the J marker. |
|  |  | Specifies the theory to be used to define the force this element will apply. By default the LINEAR theory is used. If the NONLINEAR option is used, the full non linear Euler-Bernoulli theory is used. If the STRING option is used, a simplified non linear theory is used. The simplified non linear theory may speed up your simulations with little performance penalties. |

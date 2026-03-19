# force modify element_like beam

Allows modification of the beam object.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `beam_name` | An Existing Beam | Specifies the name of the new beam. You may use this name later to refer to this beam. |
| `new_beam_name` | A New Beam | Specifies the name of the new beam. You may use this name later to refer to this beam. Adams View will not allow you to have two beams with the same full name, so you must provide a unique name. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `ixx` | Area_inertia | Specifies the polar area moment of inertia about the X axis of a cross section perpendicular to the length of the beam.By definition, the beam lies along the positive X axis of the J marker. You should compute IXX about the X axis of the J marker. |
| `iyy` | Area_inertia | Specifies the principal area moment of inertia about the Y axis of a cross section perpendicular to the length of the beam. By definition, the beam lies along the positive X axis of the J marker. You should compute IYY about the Y axis of the J marker. |
| `izz` | Area_inertia | Specifies the principal area moment of inertia about the Z axis of a cross section perpendicular to the length of the beam. By definition, the beam lies along the positive X axis of the J marker. You should compute IZZ about the Z axis of the J marker. |
| `y_shear_area_ratio` | Real | Specifies the shear area ratio in the y direction. |
| `z_shear_area_ratio` | Real | Specifies the shear area ratio in the z direction. |
| `youngs_modulus` | Pressure | Specifies Young's modulus of elasticity for the beam material. |
| `shear_modulus` | Pressure | Specifies the shear modulus of elasticity for the beam material. |
| `length` | Length | Specifies the undeformed length of the beam along the x axis of the J marker. |
| `area_of_cross_section` | Area | Specifies the uniform area of the beam cross section. The centroidal axis must be orthogonal to this cross section. |
| `damping_ratio` | Time | Specifies a ratio for calculating the structural damping matrix for the beam. Adams multiplies the stiffness matrix by the value of DAMPING_RATIO to obtain the damping matrix. |
| `matrix_of_damping_terms` | Real | Specifies a six-by-six structural damping matrix for the beam. |
| `i_marker_name` | An Existing Marker | Specifies a marker on the first of two parts connected by this force element. Adams View connects this element to one part at the I marker and to the other at the J marker. |
| `j_marker_name` | An Existing Marker | Specifies a marker on the second of two parts connected by this force element. Adams View connects this element to one part at the I marker and to the other at the J marker. |
|  |  | Specifies the theory to be used to define the force this element will apply. By default the LINEAR theory is used. If the NONLINEAR option is used, the full non linear Euler-Bernoulli theory is used. If the STRING option is used, a simplified non linear theory is used. The simplified non linear theory may speed up your simulations with little performance penalties. |

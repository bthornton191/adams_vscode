# force modify element_like field

Allows you to modify of the field object.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `field_name` | An Existing Field | Specifies the field to modify. You use this parameter to identify the existing field to affect with this command. |
| `new_field_name` | A New Field | Specifies the name of the new field. You may use this name later to refer to this field. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `i_marker_name` | An Existing Marker | Specifies a marker on the first of two parts connected by this force element. Adams View connects this element to one part at the I marker and to the other at the J marker. |
| `j_marker_name` | An Existing Marker | Specifies a marker on the second of two parts connected by this force element. Adams View connects this element to one part at the I marker and to the other at the J marker. |
| `translation_at_preload` | Length | Defines a vector of reference translations. |
| `rotation_at_preload` | Angle | Defines a vector of reference rotations. |
| `force_preload` | Force | Specifies a vector of three constant terms for the bushing force. These terms are the constant force components along the x-axis, the y-axis, and the z-axis of the J marker. |
| `torque_preload` | Torque | Defines a vector of reference torques at the angular displacement specified in the parameter ROTATION_AT_PRELOAD. The values r1, r2, r3 are the torque components about the x-axis, the y-axis, and the z axis of the J marker. |
| `stiffness_matrix` | Real | Specifies a six-by-six matrix of stiffness coefficients. |
| `damping_ratio` | Real | Specifies the ratio of MATRIX_OF_DAMPING to STIFFNESS_MATRIX. If you input DAMPING_RATIO, Adams multiplies STIFFNESS_MATRIX by this parameter to obtain MATRIX_OF_DAMPING_TERMS. |
| `matrix_of_damping_terms` | Real | Specifies a six-by-six matrix of viscous damping coefficients. |
| `user_function` | Real | Specifies up to 30 values for Adams to pass to a user written subroutine. See the Adams User's Manual for information on writing user-written subroutines. |
| `formulation` |  | By default, the LINEAR option is used. The LINEAR option matches the behavior of previous releases. The NONLINEAR option forces Adams Solver to add a geometric stiffness term; this option is useful if the FIELD is being used to model beams. |
| `length_tol` |  | When using FORMULATION=NONLINEAR, the geometric stiffness uses the larger of the current length and length tolerance. |

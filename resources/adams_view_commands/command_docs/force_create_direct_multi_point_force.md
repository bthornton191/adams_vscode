# force create direct multi_point_force

Allows you to create a multiple point force. A MULTI_POINT_FORCE creates a multi-point force element which establishes linear force-displacement (stiffness) and/or force-velocity (damping) relationships between (up to) 351 markers in the model. This force corresponds to the Adams NFORCE statement.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `multi_point_force_name` | String | Specifies the name of the new multi_point_force. You may use this name later to refer to this multi_point_force. Adams View will not allow you to have two multi_point_forces with the same name, so you must provide a unique name. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `i_marker_name` | String | Specifies a marker on the first of two parts connected by this force element. |
| `j_marker_name` |  | Specifies a marker on the second of two parts connected by this force element. |
| `stiffness_matrix_name` | String | Specifies the name of the matrix that the multi_point_force uses as its stiffness matrix. |
| `damping_matrix_name` | String | Specifies the name of the matrix that the multi_point_force uses as its damping matrix. |
| `damping_ratio` | Real | Specifies the proportional damping ratio for the MULTI_POINT_FORCE. |
| `length_matrix_name` | String | Specifies the name of the matrix that defines a reference location for each of the I markers with respect to the J marker, measured in the coordinate system of the J marker. |
| `force_matrix_name` | String | Specifies the name of the matrix that contains the forces and torques that the multi_point_force would produce if all the I markers were at the positions given in the length_matrix. |

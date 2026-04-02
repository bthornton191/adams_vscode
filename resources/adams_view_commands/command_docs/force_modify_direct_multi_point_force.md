# force modify direct multi_point_force

Allows you to modify an existing multi-point force element.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `multi_point_force_name` | An Existing Multi-Point Force | Specifies the name of the existing multi-point force to modify. |
| `new_multi_point_force_name` | A New Multi-Point Force | Specifies a new name for the multi-point force. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `i_marker_name` | An Existing Marker | Specifies one or more I markers at which the force is applied. |
| `j_marker_name` | An Existing Marker | Specifies the J marker that serves as the reference for the force element. |
| `stiffness_matrix_name` | An Existing Matrix | Specifies the matrix data element that defines the stiffness coupling between force components. |
| `damping_matrix_name` | An Existing Matrix | Specifies the matrix data element that defines the damping coupling between force components. |
| `damping_ratio` | Time | Specifies a damping ratio used to compute the damping matrix from the stiffness matrix. |
| `length_matrix_name` | An Existing Matrix | Specifies the matrix data element that defines the free length components. |
| `force_matrix_name` | An Existing Matrix | Specifies the matrix data element that defines the preload force components. |

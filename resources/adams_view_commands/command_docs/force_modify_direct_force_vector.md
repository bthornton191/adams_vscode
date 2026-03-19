# force modify direct force_vector

Allows you to modify an existing vector force.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `force_vector_name` | An existing vforce | Specifies the force_vector to modify. |
| `new_force_vector_name` | A new vforce | Specifies the name of the new force_vector. |
| `adams_id` | integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `i_marker_name` | Existing marker | Specifies the marker at which Adams applies the forces and/or torques. |
| `j_floating_marker_name` | Existing marker | Existing marker |
| `j_part_name` | Existing body | Specifies the part on which Adams View creates a floating marker. |
| `ref_marker_name` | Existing marker | Specifies a marker that acts as a coordinate reference for the definition of three orthogonal force and/or torque components. These components make up the force and/or torque being defined. |
| `x_force_function,` | Function | Specifies the x component of the translational force for this element. Adams applies this force parallel to the x axis of the reference marker specified in the REF_MARKER_NAME parameter. |
| `y_force_function,` | Function | Specifies the y component of the translational force for this element. Adams applies this force parallel to the y axis of the reference marker specified in the REF_MARKER_NAME parameter. |
| `z_force_function` | Function | Specifies the y component of the translational force for this element. Adams applies this force parallel to the y axis of the reference marker specified in the REF_MARKER_NAME parameter. |

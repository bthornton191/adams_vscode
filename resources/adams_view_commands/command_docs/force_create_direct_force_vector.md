# force create direct force_vector

Allows you to create a vector force.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `force_vector_name` | New V Force | Specifies the name of the new force_vector. You may use this name later to refer to this force_vector. |
| `adams_id` | Geom_id | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `i_marker_name` | Existing marker | Specifies the marker at which Adams applies the forces and/or torques. |
| `j_floating_marker_name` | Existing marker | Specify the J floating marker name. |
| `j_part_name` | Existing body | Specifies the part on which Adams View creates a floating marker. |
| `j_marker_id` | Integer | Specifies the Adams ID for the floating marker which is automatically created on the J part by Adams View. This allows you to reference the floating marker in a request or function by the ID you specify, instead of letting Adams View generate one. |
| `ref_marker_name` | Existing marker | Specifies a marker that acts as a coordinate reference for the definition of three orthogonal force and/or torque components. These components make up the force and/or torque being defined. The user must ensure that the reference_marker is fixed on a part (i.e. not a "floating" marker). The reference_marker may be the same as the I marker and may be on any part of the model. |
| `error` | Real | Currently not in use. |
| `x_force_function` | Function | Specifies the x component of the translational force for this element. Adams applies this force parallel to the x axis of the reference marker specified in the REF_MARKER_NAME parameter. |
| `y_force_function` | Function | Specifies the y component of the translational force for this element. Adams applies this force parallel to the y axis of the reference marker specified in the REF_MARKER_NAME parameter. |
| `z_force_function` | Function | Specifies the z component of the translational force for this element. Adams applies this force parallel to the z axis of the reference marker specified in the REF_MARKER_NAME parameter. |
| `xyz_force_function` | Function | Function |
| `user_function` | Real | Specifies up to 30 values for Adams to pass to a user-written subroutine. See the Adams User's Manual for information on writing user-written subroutines. |
| `routine` | String | String |

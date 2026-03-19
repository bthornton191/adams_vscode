# force create direct torque_vector

Allows you to create a vector torque.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `torque_vector_name` | String | Specifies the name of the new torque_vector |
| `adams_id` | Geom_id | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `i_marker_name` | Existing marker name | Specifies the marker at which Adams applies the forces and/or torques. |
| `j_floating_marker_name` | Existing marker name | Specifies marker for j floating marker. |
| `j_part_name` | An existing body | Specifies the part on which Adams View creates a floating marker. |
| `j_marker_id` | Integer | Specifies the Adams ID for the floating marker which is automatically created on the J part by Adams View. This allows you to reference the floating marker in a request or function by the ID you specify, instead of letting Adams View generate one. |
| `ref_marker_name` | Existing marker | Specifies a marker that acts as a coordinate reference for the definition of three orthogonal force and/or torque components. These components make up the force and/or torque being defined. |
| `error` | Real | Currently not in use. |
| `x_torque_function` | Function | Specifies the x component of the rotational torque for this element. Adams applies this torque parallel to the x axis of the reference marker in the sense of the right-hand rule, that is, a positive torque causes a counterclockwise rotation if you are looking along the axis from positive to negative. |
| `y_torque_function` | Function | Specifies the y component of the rotational torque for the element. |
| `z_torque_function` | Function | Specifies the z component of the rotational torque for the element. |
| `xyz_torque_function` | Function | Function |
| `user_function` | Real | Specifies up to 30 values for Adams to pass to a user-written subroutine. See the Adams User's Manual for information on writing user-written subroutines. |
| `routine` | String | String |

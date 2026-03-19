# force modify direct general_force

Allows you to modify an existing general force.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `general_force_name` | Existing genforce | Specifies the general force to modify. |
| `new_general_force_name` | New genforce | Specifies the name of the new general_force. |
| `adams_id` | integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `i_marker_name` | Existing marker | Specifies the marker at which Adams applies the forces and/or torques. |
| `j_floating_marker_name` | Existing marker | Existing marker |
| `j_part_name` | Existing body | Specifies the part on which Adams View creates a floating marker. |
| `ref_marker_name` | Existing marker | Specifies a marker that acts as a coordinate reference for the definition of three orthogonal force and/or torque components. These components make up the force and/or torque being defined. |
| `x_torque_function` | Function | Specifies the x component of the rotational torque for this element. |
| `y_torque_function` | Function | Specifies the y component of the rotational torque for this element. |
| `z_torque_function` | Function | Specifies the y component of the rotational torque for this element. |
| `user_function` | Real | Specifies up to 30 values for Adams to pass to a user-written subroutine. See the Adams User's Manual for information on writing user-written subroutines. |
| `x_force_function` | Function | Specifies the x component of the translational force for this element. Adams applies this force parallel to the x axis of the reference marker specified in the REF_MARKER_NAME parameter. |
| `y_force_function` | Function | Specifies the y component of the translational force for this element. Adams applies this force parallel to the y axis of the reference marker specified in the REF_MARKER_NAME parameter. |
| `z_force_function` | Function | Specifies the z component of the translational force for this element. Adams applies this force parallel to the z axis of the reference marker specified in the REF_MARKER_NAME parameter. |

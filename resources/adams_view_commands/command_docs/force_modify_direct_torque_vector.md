# force modify direct torque_vector

Allows you to modify an existing vector torque element.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `torque_vector_name` | An Existing Torque Vector | Specifies the name of the existing torque vector to modify. |
| `new_torque_vector_name` | A New Torque Vector | Specifies a new name for the torque vector. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `i_marker_name` | An Existing Marker | Specifies the marker at which Adams applies the torque. |
| `j_floating_marker_name` | An Existing Floating Marker | Specifies the floating marker on the J part used as the action-reaction reference. |
| `j_part_name` | An Existing Body | Specifies the part on which Adams View creates a floating marker. |
| `ref_marker_name` | An Existing Marker | Specifies a marker that defines the coordinate system for the torque component expressions. |
| `error` | Real | Currently not in use. |
| `x_torque_function` | Function | Specifies the X component of the torque applied parallel to the X axis of the reference marker. |
| `y_torque_function` | Function | Specifies the Y component of the torque applied parallel to the Y axis of the reference marker. |
| `z_torque_function` | Function | Specifies the Z component of the torque applied parallel to the Z axis of the reference marker. |
| `xyz_torque_function` | Function | Specifies all three torque components as a single vector function expression. |
| `user_function` | Real | Specifies up to 30 values for Adams to pass to a user-written subroutine. |
| `routine` | String | Specifies the name of the user-written subroutine. |

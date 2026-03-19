# force create direct general_force

Allows you to create a general force. A GENERAL_FORCE defines a complete force element, consisting of three mutually orthogonal translational force components and three orthogonal torque components.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `general_force_name` | String | Specifies the name of the new general_force. You may use this name later to refer to this general_force. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `i_marker_name` | String | Specifies the marker at which Adams applies the forces and/or torques. |
| `j_floating_marker_name` | String | String |
| `j_part_name` | String | Specifies the part on which Adams View creates a floating marker. Adams subsequently applies the reaction forces and/or torques to this "floating" J marker. |
| `j_marker_id` | Integer | Specifies the Adams ID for the floating marker which is automatically created on the J part by Adams View. |
| `ref_marker_name` | String | Specifies a marker that acts as a coordinate reference for the definition of three orthogonal force and/or torque components. |
| `x_force_function` | String | Specifies the x component of the translational force for this element. Adams applies this force parallel to the x axis of the reference marker specified in the REF_MARKER_NAME parameter. |
| `y_force_function` | String | Specifies the y component of the translational force for this element. Adams applies this force parallel to the y axis of the reference marker specified in the REF_MARKER_NAME parameter. |
| `z_force_function` | String | Specifies the z component of the translational force for this element. Adams applies this force parallel to the z axis of the reference marker specified in the REF_MARKER_NAME parameter. |
| `x_torque_function` | String | Specifies the x component of the rotational torque for this element. |
| `y_torque_function` | String | Specifies the y component of the rotational torque for the element. |
| `z_torque_function` | String | Specifies the z component of the rotational torque for this element. |
| `user_function` | String | Specifies up to 30 values for Adams to pass to a userwritten subroutine. See the Adams User's Manual for information on writing user-written subroutines. |
| `routine` | String | String |

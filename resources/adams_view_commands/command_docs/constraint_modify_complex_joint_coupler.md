# constraint modify complex_joint coupler

Allows the modification of an existing coupler.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `coupler_name` | An Existing Coupler | Specifies the coupler to modify. |
| `new_coupler_name` | A New Coupler | Specifies the name of the new coupler. |
| `adams_id` | Adams_id | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `joint_name` | An Existing Joint | Specifies the translational, revolute, or cylindrical joint associated with this entity. |
| `type_of_freedom` | Coupler_freedom | Specifies whether cylindrical joints transfer translational or rotational motion. |
| `motion_multipliers` | Real | Specifies the relative motion of the joints you identify with JOINTS |
| `first_angular_scale_factor` | Angle | Specifies the angular motion of the first joint you identify with JOINT_NAME relative to the motion of the second and third joints you identify with JOINT_NAME. |
| `first_scale_factor` | Real | Specifies the non-angular motion of the first joint you identify with JOINT_NAME relative to the motion of the second and third joints you identify with JOINT_NAME. |
| `second_angular_scale_factor` | Angle | Specifies the angular motion of the second joint you identify with JOINT_NAME relative to the motion of the first and third joints you identify with JOINT_NAME |
| `second_scale_factor` | Real | Specifies the non-angular motion of the second joint you identify with JOINT_NAME relative to the motion of the first and third joints you identify with JOINT_NAME. |
| `third_angular_scale_factor` | Angle | Specifies the angular motion of the third joint you identify with JOINT_NAME relative to the motion of the first and second joints you identify with JOINT_NAME. |
| `third_scale_factor` | Real | Specifies the non-angular motion of the third joint you identify with JOINT_NAME relative to the motion of the first and second joints you identify with JOINT_NAME. |
| `user_function` | Real | Specifies up to 30 values for Adams to pass to a userwritten subroutine. |

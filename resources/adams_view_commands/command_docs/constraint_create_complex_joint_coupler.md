# constraint create complex_joint coupler

Allows the creation of a coupler.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `coupler_name` | A New Coupler | Specifies the name of the new coupler. You may use this name later to refer to this coupler. |
| `adams_id` | Adams_id | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `joint_name` | An Existing Joint | Specifies the translational, revolute, or cylindrical joint associated with this entity. Some entities constrain motion at, or are otherwise associated with, specific joints. You use this parameter to identify that joint. |
| `type_of_freedom` | Coupler_freedom | Specifies whether cylindrical joints transfer translational or rotational motion. |
| `motion_multipliers` | Real | Specifies the relative motion of the joints you identify with joints |
| `first_angular_scale_factor` | Angle | Specifies the angular motion of the first joint you identify with JOINT_NAME relative to the motion of the second and third joints you identify with Joint_Name. |
| `first_scale_factor` | Real | Specifies the non-angular motion of the first joint you identify with JOINT_NAME relative to the motion of the second and third joints you identify with Joint_Name. |
| `second_angular_scale_factor` | Angle | Specifies the angular motion of the second joint you identify with Joint_Name relative to the motion of the first and third joints you identify with JOINT_NAME |
| `second_scale_factor` | Real | Specifies the non-angular motion of the second joint you identify with Joint_Name relative to the motion of the first and third joints you identify with Joint_Name. |
| `third_angular_scale_factor` | Angle | Specifies the angular motion of the third joint you identify with Joint_Name relative to the motion of the first and second joints you identify with Joint_Name. |
| `third_scale_factor` | Real | Specifies the non-angular motion of the third joint you identify with Joint_Name relative to the motion of the first and second joints you identify with Joint_Name. |
| `user_function` | Real | Specifies up to 30 values for Adams to pass to a userwritten subroutine. See the Adams User's Manual for information on writing user-written subroutines. |

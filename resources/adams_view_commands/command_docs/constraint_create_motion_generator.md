# constraint create motion_generator

Allows the creation of a motion generator in a model.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `motion_name` | New Motion Name | Specifies the name of the new motion generator. You may use this name later to refer to this motion generator. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `joint_name` | Existing Joint | Specifies the translational, revolute, or cylindrical joint associated with this entity. Some entities constrain motion at, or are otherwise associated with, specific joints. You use this parameter to identify that joint. |
| `type_of_freedom` | Translational/rotational | Specifies translational or a rotational motion if you attach this motion generator to a cylindrical joint. |
| `i_marker_name` | Existing Marker | Specify an existing I marker |
| `j_marker_name` | Existing Marker | Specify an existing J marker |
| `axis` | X/y/ Z/ B1/ B2/ B3 | Allows you to create and modify additional axes on a plot to effect multiple axis plotting. |
| `function` | Function | Specifies an expression or defines and passes constants to a user-written subroutine to define the motion. |
| `user_function` | Real | Specifies up to 30 values for Adams to pass to a user-written subroutine. |
| `routine` | String | String |
| `time_derivative` | Velocity/displacement/acceleration | Specifies that the FUNCTION argument defines the motion displacement, velocity, or acceleration. |
| `displacement_ic` | Length | Specifies the initial displacement of the motion, when the motion is defined in terms of velocity or acceleration. |
| `velocity_ic` | Velocity | Specifies the initial velocity of the motion, when the motion is defined in terms of acceleration. |
| `rotational_displacement_ic` | Angle | Specifies the rotational displacement. |
| `rotational_velocity_ic` | Real | Specifies the rotational velocity. |

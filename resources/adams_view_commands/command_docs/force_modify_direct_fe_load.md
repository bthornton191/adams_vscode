# force modify direct fe_load

Allows you to modify an existing finite element load.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `feload_name` | An Existing FE Load | Specifies the name of the FE load to modify. |
| `new_feload_name` | A New FE Load | Specifies a new name for the FE load. |
| `ref_fe_part` | An Existing FE Part | Specifies the FE part to which the load is applied. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `ref_orientation_marker` | An Existing Marker | Specifies a marker that defines the coordinate system for the load components. |
| `fx` | Function | Specifies the X component of the translational force as a function expression. |
| `fy` | Function | Specifies the Y component of the translational force as a function expression. |
| `fz` | Function | Specifies the Z component of the translational force as a function expression. |
| `tx` | Function | Specifies the X component of the torque as a function expression. |
| `ty` | Function | Specifies the Y component of the torque as a function expression. |
| `tz` | Function | Specifies the Z component of the torque as a function expression. |
| `user_function` | Real | Specifies up to 30 values for Adams to pass to a user-written subroutine. |
| `routine` | String | Specifies the name of the user-written subroutine. |
| `force_display` | On/Off | Specifies whether to display the force graphics in the Adams View model. |

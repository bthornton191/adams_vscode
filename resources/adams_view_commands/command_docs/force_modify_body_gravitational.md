# force modify body gravitational

Allows modification of the gravitational body object.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `gravity_field_name` | An Existing Gravity Field | Specifies the gravity field to modify. You use this parameterto identify the existing gravity field to affect with thiscommand. |
| `new_gravity_field_name` | A New Gravity Field | Specifies the name of the new gravity field. You may use this name later to refer to this gravity field. Adams Viewwill not allow you to have two gravity fields with the same full name, so you must provide a unique name. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `units_consistency_factor` | Real | Specifies a conversion factor to make your force, mass, length, and time units consistent. If you do not specify UNITS_CONSISTENCY_FACTOR, or specify it as zero, Adams View will calculate it for you when it writes theAdams data set. |
| `x_component_gravity` | Acceleration | Specifies the x component of gravitational acceleration with respect to the ground reference frame |
| `y_component_gravity` | Acceleration | Specifies the y component of gravitational acceleration with respect to the ground reference frame |
| `z_component_gravity` | Acceleration | Specifies the z component of gravitational acceleration with respect to the ground reference frame |

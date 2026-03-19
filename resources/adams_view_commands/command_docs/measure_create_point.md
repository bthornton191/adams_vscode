# measure create point

This is a predefined measure that lets you capture and investigate Characteristics of a point, such as its location relative to the global coordinate system or the sum of forces acting on it.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `measure_name` | New point measure | Specifies the name of the new point measure. You can use this name later to refer to this measure. |
| `component` | X_COMPONENT, Y_COMPONENT, Z_COMPONENT, MAG_COMPONENT, R_COMPONENT, RHO_COMPONENT, THETA_COMPONENT, PHI_COMPONENT | Specifies the component in which you are interested. The components available depend on the coordinate system. |
| `motion_rframe` | Existing marker | Specifies existing marker |
| `coordinate_rframe` | Existing marker | Specifies existing marker |
| `characteristic` | TOTAL_FORCE_ON_POINT, TOTAL_TORQUE_ON_POINT, TOTAL_FORCE_AT_LOCATION, TOTAL_TORQUE_AT_LOCATION, TRANSLATIONAL_DEFORMATION, ANGULAR_DEFORMATION_VELOCITY, TRANSLATIONAL_DEFORMATION_VELOCITY, TRANSLATIONAL_DISPLACEMENT, TRANSLATIONAL_VELOCITY, TRANSLATIONAL_ACCELERATION, ANGULAR_VELOCITY, ANGULAR_DEFORMATION, ANGULAR_ACCELERATION | Specifies the kinematic and characteristic to be measured. |
| `point` | Existing marker | Enter the marker or point to measure. |
| `legend` | String | Specifies the text that will appear in the top of the measure window. |
| `comments` | String | Specifies any comments on this measure. |
| `create_measure_display` | Yes/No | Specifies yes if you want to display a strip chart of the measure. |

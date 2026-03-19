# measure create pt2pt

This is a predefined measure that lets you capture and investigate kinematic characteristics of a point relative to another point, such as the relative velocity or acceleration. For example, you can use a point-to-point measure to calculate the global y-component of distance between any two specified markers.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `measure_name` | New point-point measure | Specifies the name of the new point-to-point measure.You can use this name later to refer to this measure. |
| `component` | X_COMPONENT, Y_COMPONENT, Z_COMPONENT, MAG_COMPONENT, R_COMPONENT, RHO_COMPONENT, THETA_COMPONENT, PHI_COMPONENT | Specifies the component in which you are interested. The components available depend on the coordinate system. |
| `motion_rframe` | Existing marker | Specifies existing marker |
| `coordinate_rframe` | Existing marker | Specifies existing marker |
| `characteristic` | TRANSLATIONAL_DISPLACEMENT, TRANSLATIONAL_VELOCITY, TRANSLATIONAL_ACCELERATION, ANGULAR_VELOCITY, ANGULAR_ACCELERATION | Specifies the kinematic characteristic to be measured. The values you enter next in the command depend on whether you select a translational or angular characteristics. |
| `from_point` | Existing marker | Enter the marker or point from which to measure. |
| `to_point` | Existing marker | Enter the marker or point to which to measure |
| `legend` | String | Specifies the text that will appear in the top of the measure window. |
| `comments` | String | Specifies any comments on this measure. |
| `create_measure_display` | Yes/No | Specifies yes if you want to display a strip chart of the measure. |

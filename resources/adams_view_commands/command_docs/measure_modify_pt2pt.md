# measure modify pt2pt

Allows you to modify an existing point-to-point measure.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `measure_name` | Existing point-point measure | Specifies the name of an existing point-to-point measure to be modified. |
| `new_measure_name` | New name for the measure | Specifies the new name for the measure. You can use this name later to refer to this measure. |
| `component` | X_component, Y_component, Z_component, Mag_component, R_component, Rho_component, Theta_component, Phi_component | Specifies the component in which you are interested. The components available depend on the coordinate system. |
| `motion_rframe` | Existing Marker | Specifies existing marker |
| `coordinate_rframe` | Existing Marker | Specifies existing marker |
| `characteristic` | Translational_displacement, Translational_velocity, Translational_acceleration, Angular_velocity, Angular_acceleration | Specifies the kinematic characteristic to be measured. The values you enter next in the command depend on whether you select a translational or angular characteristics. |
| `from_point` | Existing Marker | Enter the marker or point from which to measure. |
| `to_point` | Existing Marker | Enter the marker or point to which to measure |
| `legend` | String | Specifies the text that will appear in the top of the measure window. |
| `comments` | String | Specifies any comments on this measure. |
| `create_measure_display` | Yes/No | Specifies yes if you want to display a strip chart of the measure. |

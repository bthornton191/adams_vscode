# measure modify point

Allows you to modify an existing point measure.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `measure_name` | Existing point measure | Specifies the name of an existing point measure to be modified. |
| `new_measure_name` | New name for the measure | Specifies the new name for the measure. You can use this name later to refer to this measure. |
| `component` | X_component, Y_component, Z_component, Mag_component, R_component, Rho_component, Theta_component, Phi_component | Specifies the component in which you are interested. The components available depend on the coordinate system. |
| `motion_rframe` | Existing Marker | Specifies existing marker |
| `coordinate_rframe` | Existing Marker | Specifies existing marker |
| `characteristic` | Total_force_on_point, Total_torque_on_point, Total_force_at_location, Total_torque_at_location, Translational_deformation, Angular_deformation_velocity, Translational_deformation_velocity, Translational_displacement, Translational_velocity, Translational_acceleration, Angular_velocity, Angular_deformation, Angular_acceleration | Specifies the kinematic and characteristic to be measured. |
| `point` | Existing Marker | Enter the marker or point to measure. |
| `legend` | String | Specifies the text that will appear in the top of the measure window. |
| `comments` | String | Specifies any comments on this measure. |
| `create_measure_display` | Yes/no | Specifies yes if you want to display a strip chart of the measure. |

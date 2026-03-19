# measure modify object

Allows you to modify an existing object measure.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `measure_name` | Existing Point Measure | Specifies the name of the existing point measure that has to be modified. |
| `new_measure_name` | New Name For The Point Measure | Specifies the new name for the point measure. You can use this name later to refer to this measure. |
| `component` | X_component, Y_component, Z_component, Mag_component, R_component, Rho_component, Theta_component, Phi_component | Specifies the component in which you are interested. The components available depend on the coordinate system. |
| `motion_rframe` | Existing Marker | Specifies existing marker |
| `coordinate_rframe` | Existing Marker | Specifies existing marker |
| `characteristic` | Angular_acceleration, Angular_deformation, Angular_deformation_velocity, Angular_kinetic_energy, Angular_momentum_about_cm, Angular_velocity, Ax_ay_az_projection_angles, Cm_acceleration, cm_angular_acceleration, Cm_angular_displacement, Euler_angles, Cm_angular_velocity, Cm_position, Cm_position_relative_to_body, Cm_velocity, Contact_point_location, Element_force, Element_torque, Integrator_order, Integrator_stepsize, Integrator_time_step, Iterator_steps, Iteration_count, Kinetic_energy, Potential_energy_delta, Power_consumption, Pressure_angle, Static_imbalance, Strain_kinetic_energy, Translational_acceleration, Translational_deformation, Translational_deformation_velocity, Translational_displacement, Translational_kinetic_energy, Translational_momentum, Translational_velocity | Specifies the object characteristic to be measured. |
| `object` | Existing Object In Adams | Enter the object to measure. |
| `legend` | String | Specifies the text that will appear in the top of the measure window. |
| `comments` | String | Specifies any comments on this measure. |
| `create_measure_display` | Yes/no | Specifies yes if you want to display a strip chart of the measure. |

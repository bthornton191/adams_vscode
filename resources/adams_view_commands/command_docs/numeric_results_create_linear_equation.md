# numeric_results create linear_equation

Allows you to multiply two components of a result set, either real or complex. The two components must:

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `a_multiplier` | Real | The A_MULTIPLIER parameter is used as a constant coefficient in the linear_equation operation for manipulating numeric results. The linear equation is of the form: |
| `b_multiplier` | Real | The B_MULTIPLIER parameter is used as a constant coefficient in the linear_equation operation for manipulating numeric results. The linear equation is of the form: |
| `new_result_set_component_name` | New Result Set Name | Identifies the new result set component. |
| `result_set_component_names` | Existing Result Set Components | Identifies two result set components on which to perform the operation. |
| `units` | No_units, Calculate, Length, Angle, Mass, Density, Time, Area, Volume, Velocity, Acceleration, Angular_velocity, Angular_acceleration, Inertia, Area_inertia, Damping, Stiffness, Torsion_stiffness, Torsion_damping, Force, Torque, Pressure, Force_time, Torque_time | Specifies the type of units to be used for the new result set component. Once you set the unit type, Adams View can perform the proper unit conversion on the data. |

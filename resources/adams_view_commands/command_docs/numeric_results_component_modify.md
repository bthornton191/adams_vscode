# numeric_results component modify

Allows you to modify a result set component.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `result_set_component_name` | Existing Result Set Name | Specifies an existing result set name. |
| `new_result_set_component_name` | New Result Set Name | Identifies the new result set component. |
| `values` | Real | Specifies the real values to be stored in the result set component. The values can be a list of numbers, or an expression defining an array of values. |
| `units` | No_units, Calculate, Length, Angle, Mass, Density, Time, Area, Volume, Velocity, Acceleration, Angular_velocity, Angular_acceleration, Inertia, Area_inertia, Damping, Stiffness, Torsion_stiffness, Torsion_damping, Force, Torque, Pressure, Force_time, Torque_time | Specifies the type of units to be used for the new result set component. Once you set the unit type, Adams View can perform the proper unit conversion on the data. |

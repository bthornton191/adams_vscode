# numeric_results modify

Allows you to change the units of an existing result set component. You can reverse modifications using the undo command.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `result_set_component_names` | Existing Result Set Components | Identifies two result set components on which to perform the operation. |
| `units` | no_units, calculate, length, angle, mass, density, time, area, volume, velocity, acceleration, angular_velocity, angular_acceleration, inertia, area_inertia, damping, stiffness, torsion_stiffness, torsion_damping, force, torque, pressure, force_time, torque_time | Specifies the type of units to be used for the new result set component. Once you set the unit type, Adams View can perform the proper unit conversion on the data. |

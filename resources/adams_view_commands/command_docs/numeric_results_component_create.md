# numeric_results component create

Allows you to create a result set component. It is the same as using numeric_results create value.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `new_result_set_component_name` | New Result Set Name | Identifies the new result set component. |
| `values` | Real | Specifies the real values to be stored in the result set component. The values can be a list of numbers, or an expression defining an array of values. |
| `units` | no_units, calculate, length, angle, mass, density, time, area, volume, velocity, acceleration, angular_velocity, angular_acceleration, inertia, area_inertia, damping, stiffness, torsion_stiffness, torsion_damping, force, torque, pressure, force_time, torque_time | Specifies the type of units to be used for the new result set component. Once you set the unit type, Adams View can perform the proper unit conversion on the data. |

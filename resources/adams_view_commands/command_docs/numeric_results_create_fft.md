# numeric_results create fft

Allows you to use FFT (Fast Fourier Transform) to change a result set component from the time domain to the frequency domain, and back.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `new_result_set_component_name` | New Result Set Name | Identifies the new result set component. |
| `result_set_component_names` | Existing Result Set Components | Identifies two result set components on which to perform the operation. |
| `interpolate_type` | Linear, Cubic, Akima, Cspline | Specifies the method to interpolate the result set component. |
| `number_of_points` | Integer | Specifies the number of interpolation points used in the fitting of data contained in a result set component. You might want to use this curve-fitting operation in preparation for an FFT operation, and so on. |
| `units` | No_units, Calculate, Length, Angle, Mass, Density, Time, Area, Volume, Velocity, Acceleration, Angular_velocity, Angular_acceleration, Inertia, Area_inertia, Damping, Stiffness, Torsion_stiffness, Torsion_damping, Force, Torque, Pressure, Force_time, Torque_time | Specifies the type of units to be used for the new result set component. Once you set the unit type, Adams View can perform the proper unit conversion on the data. |

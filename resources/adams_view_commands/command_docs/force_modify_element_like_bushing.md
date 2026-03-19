# force modify element_like bushing

Allows you to modify of the bushing object.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `bushing_name` | An Existing Bushing | Specifies the name of the existing bushing. |
| `new_bushing_name` | A New Bushing | Specifies the name of the new bushing. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `damping` | Damping | Specifies three viscous damping coefficients for the bushing force. The three coefficients multiply the translational velocity components of the I marker along the x-axis, the y-axis, and the z-axis of the J marker. The force due to damping is zero when there is no relative translational velocity between the two markers. DAMPING must be in units of force per unit of displacement per unit of time. |
| `stiffness` | Stiffness | Specifies three stiffness coefficients for the bushing force. |
| `force_preload` | Force | Specifies a vector of three constant terms for the bushing force. These terms are the constant force components along the x-axis, the y-axis, and the z-axis of the J marker. |
| `tdamping` | Torsion_damp | Specifies three viscous damping coefficients for the bushing torque. |
| `tstiffness` | Torsion_stiff | Specifies three stiffness coefficients for the bushing torque. The three coefficients multiply the three rotational displacement components of the body in which the I marker is fixed about the x-axis, the y-axis, and the z-axis of the J marker. |
| `torque_preload` | Torque | Specifies a vector of three constant terms for the bushing torque. These terms are the constant torque components about the x-axis, the y-axis, and the z-axis of the J marker. |
| `i_marker_name` | An Existing Marker | Specifies a marker on the first of two parts connected by this force element. Adams View connects this element to one part at the I marker and to the other at the J marker. |
| `j_marker_name` | An Existing Marker | Specifies a marker on the second of two parts connected by this force element. Adams View connects this element to one part at the I marker and to the other at the J marker. |

# view rotate

The ROTATE command is use to control the rotational positioning of the model displayed in a view. Rotations can also be effectively performed using the control panel. The rotate command is useful in the creation of repeatable macros (See the "file command" and "file log_file" commands).

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `view_name` | An Existing View | Specifies an existing view |
| `screen_angles` | Angle | For rotation, SCREEN_ANGLES infers the direction of the axes about which to perform the rotations. |
| `object_angles` | AngleE | The OBJECT_ANGLES parameter refers to the number of theta, phi, and psi degrees to rotate about an object fixed coordinate system. |

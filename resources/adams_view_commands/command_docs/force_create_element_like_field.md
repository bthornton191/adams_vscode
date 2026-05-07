# force create element_like field

Allows you to create a field element. A field element applies up to six coupled force and torque components between two parts as a linear function of relative displacement and velocity, defined by 6x6 stiffness and damping matrices.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `field_name` | A New Field | Specifies the name of the new field element. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `i_part_name` | An Existing Body | Specifies the part that is the first of two parts connected by this force element. |
| `j_part_name` | An Existing Body | Specifies the part that is the second of two parts connected by this force element. |
| `location` | Location | Specifies the locations to be used to define the position of the force element during its creation. |
| `orientation` | Orientation | Specifies the orientation of the J marker using three rotation angles. |
| `along_axis_orientation` | Location | Specifies the orientation of a coordinate system by directing one of the axes. Adams View will assign an arbitrary rotation about the axis. |
| `in_plane_orientation` | Location | Specifies the orientation of a coordinate system by directing one of the axes and locating one of the coordinate planes. |
| `relative_to` | An Existing Model, Part Or Marker | Specifies the coordinate system that location coordinates and orientation angles are with respect to. |
| `i_marker_name` | An Existing Marker | Specifies a marker on the first of two parts connected by this force element. |
| `j_marker_name` | An Existing Marker | Specifies a marker on the second of two parts connected by this force element. |
| `translation_at_preload` | Length (3 values) | Specifies the translational displacement (x, y, z) at which the preload forces are applied. |
| `rotation_at_preload` | Angle (3 values) | Specifies the rotational displacement (a, b, c) at which the preload torques are applied. |
| `force_preload` | Force (3 values) | Specifies the preload force components (Fx, Fy, Fz) applied at the preload displacement. |
| `torque_preload` | Torque (3 values) | Specifies the preload torque components (Tx, Ty, Tz) applied at the preload rotation. |
| `stiffness_matrix` | Real (36 values) | Specifies the 6x6 stiffness matrix defining the coupling between force/torque components and displacement/rotation. |
| `damping_ratio` | Time | Specifies a damping ratio used to compute the damping matrix from the stiffness matrix. |
| `matrix_of_damping_terms` | Real (36 values) | Specifies the 6x6 damping matrix directly, as an alternative to using the damping ratio. |
| `user_function` | Real | Specifies up to 30 values for Adams to pass to a user-written subroutine. |
| `routine` | String | Specifies the name of the user-written subroutine. |
| `formulation` | Field Formulation | Specifies the theory used to define the force. Options include linear (default) and nonlinear formulations. |
| `length_tolerance` | Real | Specifies the length tolerance used during formulation computations. |

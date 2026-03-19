# force create element_like rotational_spring_damper

Allows you to create a rotational spring damper object.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `spring_damper_name` | String | Specifies the name of the new spring damper force. You may use this name later to refer to this spring damper. |
| `adams_id` | Geom_id | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `damping` | Real number | Specifies the viscous damping coefficient for the spring damper. |
| `stiffness` | Real number | Specifies the spring stiffness coefficient for the spring damper. |
| `preload` | Real | Specifies the reference force or torque for the spring. This is the force the spring exerts when the displacement between the I and J markers is equal to DISPLACEMENT_AT_PRELOAD (the reference length of the spring). |
| `displacement_at_preload` | real | Specifies the reference length for the spring. If PRELOAD (the reference force of the spring) is zero, DISPLACEMENT_AT_PRELOAD equals the free length. |
| `i_part_name` | Existing body | Specifies the part that is the first of two parts that this force acts between. Adams View applies the force on one part at the I marker and the other at the J marker. These markers are automatically generated using this method of force creation. |
| `j_part_name` | Existing body | Specifies the part that is the second of the two parts that this force acts between. Adams View applies the force on one part at the J marker and the other at the I marker. These markers are automatically generated using this method of force creation. |
| `location` | Location | Specifies the locations to be used to define the position of a force during its creation. The I and J markers will be automatically created at this location on the I_PART_NAME and J_PART_NAME respectively. |
| `orientation` | orientation | Specifies the orientation of the J marker for the force being created using three rotation angles. The I marker is oriented based on the J marker orientation and the requirements of the particular force being created. These markers are created automatically. |
| `along_axis_orientation` | location | Specifies the orientation of a coordinate system (e.g. marker or part) by directing one of the axes. Adams View will assign an arbitrary rotation about the axis. |
| `in_plane_orientation` | Location | Specifies the orientation of a coordinate system (e.g. marker or part) by directing one of the axes and locating one of the coordinate planes. |
| `relative_to` | An existing model, part or marker | Specifies the coordinate system that location coordinates and orientation angles correspond to. |
| `i_marker_name` | An existing marker | Specifies a marker on the first of the two parts connected by this force element. Adams View connects this element to one part at the I marker and to the other at the J marker. |
| `j_marker_name` | An existing marker | Specifies a marker on the second of two parts connected by this force element. Adams View connects this element to one part at the I marker and to the other at the J marker. |

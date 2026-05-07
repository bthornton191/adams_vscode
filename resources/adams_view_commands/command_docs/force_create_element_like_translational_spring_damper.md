# force create element_like translational_spring_damper

Allows you to create a translational spring-damper element between two parts.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `spring_damper_name` | A New Spring-Damper | Specifies the name of the new translational spring-damper. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `damping` | Damping | Specifies the damping coefficient of the spring-damper element. |
| `stiffness` | Stiffness | Specifies the stiffness coefficient of the spring-damper element. |
| `preload` | Force | Specifies the preload force applied when the spring is at its free length. |
| `displacement_at_preload` | Length | Specifies the displacement of the spring from its natural free length at which the preload is applied. |
| `i_part_name` | An Existing Body | Specifies the part that is the first of two parts connected by this spring-damper. |
| `j_part_name` | An Existing Body | Specifies the part that is the second of two parts connected by this spring-damper. |
| `location` | Location | Specifies the locations to be used to define the position of the force element during its creation. |
| `orientation` | Orientation | Specifies the orientation of the J marker using three rotation angles. |
| `along_axis_orientation` | Location | Specifies the orientation of a coordinate system by directing one of the axes. Adams View will assign an arbitrary rotation about the axis. |
| `in_plane_orientation` | Location | Specifies the orientation of a coordinate system by directing one of the axes and locating one of the coordinate planes. |
| `relative_to` | An Existing Model, Part Or Marker | Specifies the coordinate system that location coordinates and orientation angles are with respect to. |
| `i_marker_name` | An Existing Marker | Specifies a marker on the first of two parts connected by this spring-damper. |
| `j_marker_name` | An Existing Marker | Specifies a marker on the second of two parts connected by this spring-damper. |

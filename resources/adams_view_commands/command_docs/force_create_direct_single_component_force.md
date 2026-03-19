# force create direct single_component_force

Allows you to create a single component force object.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `single_component_force_name` | New single_component force | Specifies the name of the new single_component_force. You may use this name later to refer to this single_component_force. |
| `adams_id` | Geom_id | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `type_of_freedom` | Rotational/Translational | Specifies the type of force (rotation or translation) to be applied.ROTATIONAL designates a rotational force, i.e. a torque.TRANSLATIONAL designates a translational force. |
| `action_only` | On/Off | Specifies whether the force is action-only or action-reaction. For an action-reaction force, Adams applies a force between the I and J markers. For an action-only force, Adams applies a force on the I marker directed by the Z axis of the J marker, but does not apply a reaction force at the J marker. |
| `function` | Function | Specifies the function expression definition that is used to compute the value of this variable. To enter a function expression, you enter a series of quoted strings. |
| `user_function` | Real | Specifies up to 30 values for Adams to pass to a user-written subroutine. See the Adams User's Manual for information on writing user-written subroutines. |
| `routine` | String | String |
| `error` | Real | Currently not in use. |
| `i_part_name` | Existing body | Specifies the part, that is the first of the two parts that this force acts between. Adams View applies the force on one part at the I marker and the other at the J marker. These markers are automatically generated using this method of force creation. |
| `j_part_name` | Existing body | Specifies the part, that is the second of the two parts that this force acts between. Adams View applies the force on one part at the J marker and the other at the I marker. These markers are automatically generated using this method of force creation. |
| `location` | Location | Specifies the locations to be used to define the position of a force during its creation. |
| `orientation` | Orientation | Specifies the orientation of the J marker for the force being created using three rotation angles. The I marker is oriented based on the J marker orientation and the requirements of the particular force being created. These markers are created automatically. |
| `along_axis_orientation` | Location | Specifies the orientation of a coordinate system (e.g. marker or part) by directing one of the axes. Adams View will assign an arbitrary rotation about the axis. |
| `in_plane_orientation` | Location | Specifies the orientation of a coordinate system (e.g. marker or part) by directing one of the axes and locating one of the coordinate planes. |
| `relative_to` | AN EXISTING MODEL, PART OR MARKER | Specifies the coordinate system that location coordinates and orientation angles correspond to. |
| `i_marker_name` | Existing marker | Specifies a marker on the first of the two parts connected by this force element. Adams View connects this element to one part at the I marker and to the other at the J marker. |
| `j_marker_name` | Existing marker | Specifies a marker on the second of two parts connected by this force element. Adams View connects this element to one part at the I marker and to the other at the J marker. |

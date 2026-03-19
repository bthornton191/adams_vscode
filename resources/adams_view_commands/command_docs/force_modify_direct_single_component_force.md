# force modify direct single_component_force

Allows modification of the single component force object.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `single_component_force_name` | AN EXISTING SINGLE-COMPONENT FORCE | Specifies the single_component_force to modify. |
| `new_single_component_force_name` | A NEW SINGLE-COMPONENT FORCE | Specifies the name of the new single_component_force. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `type_of_freedom` | translational/rotational | Specifies what type of force (rotation or translation) to apply. |
| `action_only` | On/off | Specifies whether the force is action-only or action-reaction. |
| `function` | Function | Specifies the function expression definition that is used to compute the value of this variable. |
| `user_function` | Real | Specifies up to 30 values for Adams to pass to a user-written subroutine. See the Adams User's Manual for information on writing user-written subroutines. |
| `i_marker_name` | Existing marker | Specifies a marker on the first of two parts connected by this force element. Adams View connects this element to one part at the I marker and to the other at the J marker. |
| `j_marker_name` | Existing marker | Specifies a marker on the second of two parts connected by this force element. Adams View connects this element to one part at the I marker and to the other at the J marker. |
| `error` | Real | Real |
| `routine` | String | String |

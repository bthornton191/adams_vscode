# constraint modify joint screw

Allows the modification of an existing screw joint.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `joint_name` | An Existing Joint | Specifies the joint to modify. |
| `new_joint_name` | A New Joint | Specifies the name of the new joint. You may use this name later to refer to this joint. |
| `adams_id` | Adams_id | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `i_marker_name` | An Existing Marker | Specifies a marker on the first of two parts connected by this joint. Adams View connects one part at the I marker to the other at the J marker. |
| `j_marker_name` | An Existing Marker | Specifies a marker on the second of two parts connected by this joint. Adams View connects one part at the I marker to the other at the J marker. |
| `pitch` | Length | Specifies the pitch of the scew joint. |

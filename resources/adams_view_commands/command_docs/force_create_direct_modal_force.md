# force create direct modal_force

Allows you to create a modal force applied to a flexible body. The load may be defined by a scale function applied to a precomputed load case or by a user-written subroutine.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `modal_force_name` | A New Modal Force | Specifies the name of the new modal force. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `flex_body` | An Existing Flexible Body | Specifies the flexible body to which the modal force is applied. |
| `case_index` | Integer | Specifies the index of the load case defined in the flexible body's modal neutral file. |
| `scale` | Function | Specifies a function expression used to scale the load case over time. |
| `user_function` | Real | Specifies up to 30 values for Adams to pass to a user-written subroutine that defines the modal force. |
| `routine` | String | Specifies the name of the user-written subroutine for the scale factor. |
| `force_function` | Real | Specifies up to 30 values for Adams to pass to a user-written subroutine that defines the modal force directly. |
| `j_floating_marker_name` | An Existing Floating Marker | Specifies the floating marker on the J part. |
| `j_part_name` | An Existing Part | Specifies the part on which Adams View creates a floating marker. |
| `j_marker_id` | Integer | Specifies the Adams ID for the floating marker automatically created on the J part. |

# force modify direct modal_force

Allows you to modify an existing modal force applied to a flexible body.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `modal_force_name` | An Existing Modal Force | Specifies the name of the existing modal force to modify. |
| `new_modal_force_name` | A New Modal Force | Specifies a new name for the modal force. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `flex_body` | An Existing Flexible Body | Specifies the flexible body to which the modal force is applied. |
| `case_index` | Integer | Specifies the index of the load case defined in the flexible body's modal neutral file. |
| `scale` | Function | Specifies a function expression used to scale the load case over time. |
| `user_function` | Real | Specifies up to 30 values for Adams to pass to a user-written subroutine that defines the modal force. |
| `routine` | String | Specifies the name of the user-written subroutine. |
| `force_function` | Real | Specifies up to 30 values for Adams to pass to a user-written subroutine that defines the modal force directly. |
| `j_floating_marker_name` | An Existing Floating Marker | Specifies the floating marker on the J part. |
| `j_part_name` | An Existing Part | Specifies the part on which Adams View creates a floating marker. |

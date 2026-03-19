# part modify external_system name_and_position

Allows you to modify an external system part’s name and position.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `external_system_name` | Existing external system | Specifies the name of an existing external system to be modified. |
| `new_external_system_name` | New external system | Specifies the name of the external system. |
| `type` | Nastran, Marc, user | The type of external system. Defaults to 'nastran', if not specified. |
| `adams_id` | Integer | Assigns a unique ID number to the part. |
| `comments` | String | Adds comments about the part to help you manage and identify it. |
| `view_name` | Existing View | Specifies the view in which to display this part. |
| `input_file_name` | String | File containing the input source parameters for the external system. |
| `modal_neutral_file_name` | String | An optional (rigid only) MNF, if a visual representation of the external system is required. |
| `md_db_file_name` | String | An optional MD DB, if a visual representation of the external system is required. |
| `index_in_database` | Integer | Index of the body in the specified MD DB. Valid only if the parameter md_db_file_name is specified. |
| `user_function` | Real | Specifies up to 30 values for Adams Solver to pass to a user-written subroutine. Valid only if the type is 'user'. |
| `interface_routines` | Function | Specifies an alternative library and subroutine names for the user subroutines EXTSYS_DERIV, EXTSYS_UPDATE, EXTSYS_OUTPUT, EXTSYS_SAMP, EXTSYS_SET_NS, EXTSYS_SET_ND, EXTSYS_SENSUB, EXTSYS_SET_STATIC_HOLD, EXTSYS_SET_SAMPLE_OFFSET, respectively. |
| `location` | Location | Specifies x, y, and z coordinates defining the flexible body's location in a given reference frame defined in the parameter relative_to. |
| `orientation` | Orientation | Specifies the orientation method |
| `along_axis_orientation` | Location | Specifies the orientation method |
| `in_plane_orientation` | Location | Specifies the in_plane orientation method |
| `relative_to` | Existing model, part or marker | Specifies a reference frame relative to which the location and orientation are defined. Leave blank or enter model name to use the global coordinate system. |
| `exact_coordinates` | exact_coordinates | Specifies as many as six part coordinates that Adams View is not to change as it solves for the initial conditions. |
| `hide_warnings` | boolean | Hide warnings that may be generated in the modification operation. Defaults to false. |

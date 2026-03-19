# constraint modify general_constraint

The GCON statement introduces a constraint equation that must be satisfied by Adams Solver (C++) during the simulation. This allows you to specify both holonomic and non-holonomic constraints.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `general_constraint_name` | Existing GCON name | Specify a name of the GCON to be modified |
| `new_general_constraint_name` | New GCON name | Specify the new name for the GCON |
| `adams_id` | integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `i_marker_name` | Existing marker | Specify an existing marker name. |
| `function` | Function | Specifies an expression or defines and passes constants to a user-written subroutine to define the motion. |

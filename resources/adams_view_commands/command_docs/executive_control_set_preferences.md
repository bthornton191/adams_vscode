# executive_control set preferences

This command allows you to set preferences for Adams Solver.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_name` | Existing Model Name | Specifies an existing model. |
| `status_message` | on/off | Specifies the status message to be on or off. |
| `contact_geometry_library` | default_library/parasolid | Specifies the geometry library to be used for contact operations. |
| `contact_faceting_tolerance` | Real | Specifies the resolution of the mesh that is to be created from the solid geometries in the model. |
| `thread-count` | Integer | Specifies the number of parallel threads that Adams Solver (C++) will use when performing the simulation. |
| `library_path` | String | Specifies a colon-separated list of directories which are to be searched for user subroutine plug-in libraries before searching in the default locations. |
| `flex_limit_check` | none/skin/selnod | Specifies flexible body linear limit checking on all the flexible bodies. |
| `flex_limit_check_action` | halt/return/message_only | Specifies what action Adams Solver (C++) should take if a flexible body exceeds its linear limit. |

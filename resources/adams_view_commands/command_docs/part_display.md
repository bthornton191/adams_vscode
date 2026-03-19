# part display

Allows you to display the part (rigid body, flexible body, or point mass) in the specified view. If you do not specify a view, Adams View displays the model in the active view. This command can be useful when the entire part is no longer visible in the current view space because it fits the model into the current view.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `part_name` | Existing part | Specifies the name of the rigid body to be displayed |
| `flexible_body_name` | Existing flex body | Specifies the name of the flexible body to be displayed |
| `point_mass_name` | Existing point mass | Specifies the name of the point mass to be displayed |
| `fe_part_name` | Existing FE part | Specifies the name of the FE part to be displayed |
| `view_name` | Existing view | Specifies the view in which to display this model. |
| `fit_to_view` | Yes/No | Controls whether or not to compute the extents of the model or part before displaying the model or part in a view. This parameter is optional and has a default value of on. |

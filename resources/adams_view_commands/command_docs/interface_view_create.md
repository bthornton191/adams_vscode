# interface view create

Allows you to create a new view with user defined location and orientation

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `view_name` | A New View | Specifies the name for a new view |
| `enabled` | Boolean | Activates the view |
| `help_text` | String | Specifies the help text |
| `documentation_text` | String | Specifies the documentation text |
| `units` | Int_units | Specifies the view size as pixel or relative to Adams or custom window |
| `horiz_resizing` | Int_h_resize | Specifies the attachment and scaling option for the view |
| `vert_resizing` | Int_v_resize | Specifies the attachment and scaling option for the view |
| `location` | Real | Specifies the location of the view on the dialog box |
| `height` | Real | Specifies the height of the view in terms of relative units or pixel |
| `width` | Real | Specifies the width of the view field in terms of relative units or pixel |
| `eye` | Location | Specifies the camera position and orientation |
| `target` | Location | Specifies the target location which should be centered on the view window |
| `up_vector` | Location | Specifies the upward vector for the view window to describe inclination |

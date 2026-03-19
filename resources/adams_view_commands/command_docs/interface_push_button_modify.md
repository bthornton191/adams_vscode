# interface push_button modify

Allows you to modify an existing push button.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `push_button_name` | A New GI_push_btn | Specifies the name of an existing push button |
| `new_push_button_name` | A New GI_push_btn | Specifies a new name for an existing push button |
| `enabled` | Boolean | Activates the push button |
| `help_text` | String | Specifies the help text |
| `documentation_text` | String | Specifies the documentation text |
| `units` | Int_units | Specifies the push button size in pixels or units relative to Adams window |
| `horiz_resizing` | Int_H_Resize | Specifies the attachment and scaling option for push button |
| `vert_resizing` | Int_V_Resize | Specifies the attachment and scaling option for push button |
| `location` | Real | Specifies the location of the push button |
| `height` | Real | Specifies the height of the push button in terms of relative units or pixels |
| `width` | Real | Specifies the width of the push button in terms of relative units or pixels |
| `label` | String | Specifies label of the push button |
| `icon_file` | String | Specifies the name and location of the image for icon |
| `commands` | String | Specifies the command to be executed with a single click |
| `dbl_commands` | String | Specifies the command name to be executed with a double-click |
| `default` | True_False | Set the current status for parameter ‘dbl_command’ |

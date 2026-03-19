# interface push_button create

Allows creation of a push button.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `push_button_name` | A New GI_Push_BTN | Specifies the name of a new push button |
| `enabled` | Boolean | Activates the push button |
| `help_text` | String | Specifies the help text |
| `documentation_text` | String | Specifies the documentation text |
| `units` | INT_Units | Specifies the push button size as pixel or relative to Adams window |
| `horiz_resizing` | INT_H_Resize | Specifies the attachment and scaling option for push button |
| `vert_resizing` | INT_V_Resize | Specifies the attachment and scaling option for push button |
| `location` | Real | Specifies the location of the push button |
| `height` | Real | Specifies the height of the push button in terms of relative units or pixel |
| `width` | Real | Specifies the width of the push button in terms of relative units or pixel |
| `label` | String | Specifies label for the push button |
| `icon_file` | String | Specifies the name and location of the image for icon |
| `commands` | String | Specifies the command to be executed with single click |
| `dbl_commands` | String | Specifies the command name to be executed with double click |
| `default` | True_False | Set the current status for parameter ‘dbl_command’ |

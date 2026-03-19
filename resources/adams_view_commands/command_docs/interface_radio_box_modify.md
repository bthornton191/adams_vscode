# interface radio_box modify

Allows modifying an existing radio box

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `radio_box_name` | An Existing GI_radio Box | Specifies the name of an existing radio box |
| `new_radio_box_name` | A New GI_radio_box | Specifies a new name for an existing radio box |
| `enabled` | Boolean | Activates the radio box |
| `help_text` | String | Specifies the help text |
| `documentation_text` | String | Specifies the documentation text |
| `units` | Int_units | Specifies the radio box size as pixel or relative to Adams window |
| `horiz_resizing` | Int_h_resize | Specifies the attachment and scaling option for radio box |
| `vert_resizing` | Int_v_resize | Specifies the attachment and scaling option for radio box |
| `location` | Real | Specifies the location of the radio box |
| `height` | Real | Specifies the height of the radio box in terms of relative units or pixel |
| `width` | Real | Specifies the width of the radio box in terms of relative units or pixel |
| `choices` | String | Specifies labels of the choices to be displayed for the radio box |
| `values` | String | Specifies the real values to be stored in result component |
| `commands` | String | Specifies the command to be executed by the radio box |
| `current choice` | String | Specifies the default choice to be executed by the radio box |

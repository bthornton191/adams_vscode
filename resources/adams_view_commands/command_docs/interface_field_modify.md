# interface field modify

Allows you to modify an already existing field.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `field _name` | An Existing GI_field | Specifies the name of a new field |
| `new_field_name` | A New GI_field | Specifies a new name for an existing field |
| `enabled` | Boolean | Activates the field |
| `help_text` | String | Specifies the help text |
| `documentation_text` | String | Specifies the documentation text |
| `units` | Int_units | Specifies the field size as pixel or relative to Adams window |
| `horiz_resizing` | Int_h_resize | Specifies the attachment and scaling option for the filed |
| `vert_resizing` | Int_v_resize | Specifies the attachment and scaling option for the field |
| `location` | Real | Specifies the location of the field on the dialog box |
| `height` | Real | Specifies the height of the field in terms of relative units or pixel |
| `width` | Real | Specifies the width of the field in terms of relative units or pixel |
| `preload strings` | String | Specifies the initial text to be displayed |
| `commands` | String | Specifies the command to be executed after exiting the field |
| `scrollable` | Boolean | Specifies the scroll bar option of the field |
| `editable` | Boolean | Allows editing the field contents |
| `required` | Boolean | Specifies whether field is required or optional |
| `execute_cmds_on_exit` | Boolean | Sets the BOOLEAN parameter for execution of command after exiting field |
| `number_of_values` | Integer | Specifies the number of values allowed in the field |
| `string_type add_quotes` | Add_quotes | Specifies addition of quotes to the string |
| `object_type` | New_old_any | Specifies the object allowed in the field |
| `type_filter` | Ent | Specifies the types of objects allowed |
| `name_filter` | String | Specifies the name_filter for the object |
| `numeric_type` | Num_type | Specifies the type of numeric objects allowed |
| `lower_check` | Low_check | Specifies the applicability of lower check |
| `lower_limit` | Real | Specifies lower limit for lower check of numeric value |
| `upper_check` | Upp_check | Specifies the applicability of upper check |
| `upper_limit` | Real | Specifies upper limit for upper check of numeric value |
| `file_type` | New_old_any | Specifies the types of file allowed in the field |
| `directory` | String | Specifies the directory for the file |
| `filter` | String | Tests each value of the component |
| `alert_on_overwrite` | Boolean | Sets alert for file overwrite |
| `browse_action` | Open_save | Specifies if the button in the file browser window should be labelled "Open" or "Save". |
| `word_wrap` | Boolean | If set to "yes" text longer than the field width will wrap onto the next line. By default the behavior is as if this is set to "yes" and therefore text longer than the field width will remain on a single line and run beyond the field border. |

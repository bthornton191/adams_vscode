# interface window modify

Allows modification of a window. Windows and dialog boxes look similar, although they are quite different. Windows usually stay on the screen for some time as you work in them, while dialog boxes come and go as you need to enter data or access controls. Windows can contain toolbars and menu bars. Both windows and dialog boxes contain other interface objects such as buttons, labels, and so on.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `window_name` | String | Specify the name of the new window created. |
| `enabled` | Yes/no | Specify whether the window created will be enabled or not. |
| `help_text` | String | Specify the string that should be displayed on the Adams View status bar when the mouse cursor is over the window created. |
| `documentation_text` | String | Specify the documentation text associated with this window. |
| `units` | Relative/Pixel | Specify whether the units used for the window measurements will be in pixels or relative. |
| `horiz_resizing,` | ATTACH_LEFT/ATTACH_RIGHT/SCALE_CENTER/EXPAND/ SCALE_ALL | Specify where the horizontal resizing should occur from. |
| `vert_resizing` | ATTACH_TOP/ATTACH_BOTTOM/SCALE_CENTER/EXPAND/SCALE_ALL | Specify where the vertical resizing should occur from. |
| `location` | Real | The real number should be greater than or equal to zero. |
| `height` | Real | Specify a height for the info window. The value should be a real number between 0.0 and 2.0, where 2.0 represents the height of the Adams View window. Therefore, a value of 1.0 will set the info window to be one half as high as the Adams View window. |
| `width` | Real | Specify a width for the info window. The value should be a real number between 0.0 and 2.0, where 2.0 represents the width of the Adams View window. Therefore, a value of 1.0 will set the info window to be one half as wide as the Adams View window. |
| `title` | String | This parameter allows the specification of the window title. |
| `icon_label` | String | Specify the label for the icon. |
| `start_commands` | String | Specify the commands to be executed at the start of the window creation. |
| `finish_commands` | String | Specify the commands to be executed at the end of the window creation. |
| `decorate` | Yes/No | Yes/No |
| `resizable` | Yes/No | Specify whether this window can be resizable or not. |
| `width_minimum` | Real | Specify the minimum width beyond which the window should not be allowed to resize. |
| `width_maximum` | Real | Specify the maximum width beyond which the window should not be allowed to resize |
| `height_minimum` | Real | Specify the minimum height beyond which the window should not be allowed to resize |
| `height_maximum` | Real | Specify the maximum height beyond which the window should not be allowed to resize |
| `grab_all_input` | Yes/No | Default value will be No. |

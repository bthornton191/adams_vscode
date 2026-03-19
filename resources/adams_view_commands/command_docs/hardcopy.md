# hardcopy

Allows you to send screen output to hard copy file. The user may specify the view_name to be sent to the desired hard copy file name. The FILE_NAME parameter provides a means to specify the name of the hard copy file the screen image(s) selected by the user will be written to. The FILE_NAME is an optional parameter, and if not entered, a default name will be constructed. If entered, the file name must be enclosed in quotes.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `window_name` | Existing Gi_window | Specifies an existing window name whose screen output is required |
| `view_name` | Existing View_name | Specifies existing view name |
| `page_name` | Existing Page_name | Specifies existing page name |
| `file_name` | String | Specifies the name of the hard copy file the screen image(s) selected by the user will be written to |
| `orientation` | Portrait/landscape | Specifies how the image sent to a hardcopy file is to be oriented |
| `paper_type` | Default, Eight_by_eleven, A0, A1, A2, A3, A4, B5, B, C, D, E, F | Specifies the size of paper that needs to be used |
| `send_to_printer` | Boolean | Specifies if a printout of the screen output is required |
| `language` | BMP, XPM, JPG, TIFF and PNG | Specifies the plotting language to be used for the image sent to a hardcopy file |
| `image_width_height` | Real,real | Specifies the size of the hardcopy output in the format ( x, y ) |
| `print_control_panel` | On/off | Allows the user to print the control panel graphics when screen output is sent to a hard copy file. |
| `force_black_and_white` | Boolean | Specifies whether or not to override all color specifications in a scene and produce a hardcopy image which is solely black and white. |
| `include_toolbar` | Boolean | Specifies whether the toolbar is to be included in the screen output |

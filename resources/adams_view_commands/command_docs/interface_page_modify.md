# interface page modify

Allows modifying an existing page.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `page_name` | An Existing Page | Specifies the name of an existing page |
| `layout_type` | Layout_type | Specifies the layout of the plot page |
| `expanded` | Boolean | Specifies the page display parameters |
| `header_left_text` | String | Specifies the header text to be displayed |
| `header_center_text` | String | Specifies the header text to be displayed |
| `header_right_text` | String | Specifies the header text to be displayed |
| `footer_left_text` | String | Specifies the footer text to be displayed |
| `footer_center_text` | String | Specifies the footer text to be displayed |
| `footer_right_text` | String | Specifies the footer text to be displayed |
| `header_left_image_file` | String | Specifies the image to be displayed at the header space |
| `header_left_image_file` | String | Specifies the image to be displayed at the header space |
| `header_center_image_file` | String | Specifies the image to be displayed at the header space |
| `header_right_image_file` | String | Specifies the image to be displayed at the header space |
| `footer_left_image_file` | String | Specifies the image to be displayed at the footer space |
| `footer_center_image_file` | String | Specifies the image to be displayed at the footer space |
| `footer_right_image_file` | String | Specifies the image to be displayed at the footer space |
| `display` | Boolean | Specifies the page display parameter |
| `color` | An Existng Color | Specifies the color of the plot page |
| `set_contents` | Boolean | Specifies the contents of the plot page |
| `page_type` | Plot_page | Specifies the page type |
| `adjoined` | yes_no | Specifies whether the plots on a page are to be separated by margins or otherwise. The default value is no (spacing exists between the plots). Applicable to page1x2, page1x3, page1x4 and page1x5 layouts only |
| `relative_widths` | REAL numbers | Specify the relative widths (as percentages) for each plot of a 1xn configuration. Partial values are supported. In that case, the rest of the plots will be equally distributed over the remaining width. For example for a page1x4 layout, if the relative_widths parameter is specified as 15, 25 then the first column will occupy 15% of the page width, the second 25% and the rest of the two will occupy 30% each. |
| `sync_axis` | [none, vertical, horizontal] | Specifies the axis to sync the zoom on, for all plots on a page. The pre-requisite to this functionality to work is that there should be only one axis in the specified direction for all plots on the page and that the units must be identical.The default is none (no zoom syncing) |
| `sync_legends` | yes_no | Sync the legend heights across all plot legends on the specified page. The parameter is applicable only to page1x2, page1x3, page1x4 and page1x5 layouts and when all legends have the placement specified as 'plot'. |

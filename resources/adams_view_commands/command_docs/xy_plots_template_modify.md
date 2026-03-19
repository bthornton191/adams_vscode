# xy_plots template modify

Allows you to modify an XY plot template.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `plot_name` | An Existing Plot | A plot name is a string of characters that identifies a plot |
| `new_plot_name` | A New Plot | Specifies the new name of the new plot template |
| `title` | String | This parameter allows the specification of the XY plot title |
| `subtitle` | String | This parameter allows the specification of the XY plot subtitle |
| `vlabel` | String | This parameter allows you to specify a text string that will be displayed to the left of the vertical axis. |
| `vscale_type` | Axis_Units | This parameter allows you to specify the type of scale that is displayed on the vertical axis. |
| `vdivs` | Integer | This parameter is used to set the number of divisions on the vertical axis of an xy plot |
| `vinc` | Real | This parameter is used to set the tic mark increment on the vertical axis. |
| `vlim` | Real | This parameter is used to set the minimum and maximum limits to be displayed on the vertical axis. This parameter accepts two (2) values separated by a comma (,) |
| `hlabel` | String | This parameter allows you to specify a text string that will be displayed below the horizontal axis |
| `hscale_type` | Axis_Units | This parameter allows you to specify the type of scale that is displayed on the horizontal axis |
| `hdiv` | Integer | This parameter is used to set the number of divisions on the horizontal axis of an xy plo |
| `hinc` | Real | This parameter is used to set the tic mark increment on the horizontal axis |
| `hlim` | Real | This parameter is used to set the minimum and maximum limits to be displayed on the horizontal axis |
| `dependent_axis_type` | Dependant_Axis | Determines where the dependent axis on the plot will be placed (vertical or horizontal). |
| `grid_lines` | On_Off | This parameter controls the visibility of the plot grid lines |
| `secondary_grid_lines` | On_Off | Controls the visibility of secondary grid lines, which appear at specified intervals between the primary grid lines |
| `time_limits` | Real | This parameter allows you to fit the plot to the data corresponding to a certain range of time |
| `legend` | Boolean | This parameter controls the visibility of the XY plot legend |
| `primary_haxis` | An Existing Axis | This parameter controls the visibility of the XY plot legend |
| `primary_vaxis` | An Existing Axis | Specifies the primary vertical axis for a plot |
| `auto_graph_area` | Boolean | Determines whether or not Adams View automatically fits the plot border to the view (yes or no). |
| `auto_position` | Boolean | Boolean |

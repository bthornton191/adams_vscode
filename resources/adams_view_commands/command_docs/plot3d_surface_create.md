# plot3d surface create

Creates a new 3D surface plot from simulation result data.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `surface_name` | String | Name for the new 3D surface. |
| `x_data` | String | Result set component to use for the X axis. |
| `x_analysis` | String | Analysis name for the X axis data. |
| `y_data` | String | Result set component to use for the Y axis. |
| `y_analysis` | String | Analysis name for the Y axis data. |
| `z_data` | String | Result set component to use for the Z axis. |
| `z_components` | Array | Components of the Z data to plot. |
| `color_components` | Array | Components used to determine surface color. |
| `x_units` | String | Units for the X axis data. |
| `y_units` | String | Units for the Y axis data. |
| `z_units` | String | Units for the Z axis data. |
| `color_units` | String | Units for the color data. |
| `data_invert` | Boolean | Whether to invert the data orientation. |
| `stacked_curves` | Boolean | Whether to display the Z data as stacked curves. |
| `skip_x` | Integer | Number of X data points to skip between plotted points. |
| `skip_y` | Integer | Number of Y data points to skip between plotted points. |
| `use_interpolated_colors` | Boolean | Whether to use interpolated color shading on the surface. |
| `color` | String | Explicit color for the surface when not using interpolated colors. |
| `fit_plot` | Boolean | Whether to auto-fit the plot view after creation. |
| `legend_placement` | String | Location of the color legend on the plot. |
| `run_name` | String | Name of the simulation run to use as data source. |

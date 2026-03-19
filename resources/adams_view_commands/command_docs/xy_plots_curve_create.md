# xy_plots curve create

Allows you to add new curves to an existing plot template, or create a new template and curves at the same time.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `plot_name` | A New Or Existing Plot | A plot name is a string of characters that identifies a plot |
| `curve_name` | A New Curve | A curve name is string of characters that identifies a curve |
| `vaxis_data` | An Existing Component | Identifies the set of values that will be used for the vertical axis data when creating a curve on an xy plot. |
| `vmeasure` | An Existing Measure | An Existing Measure |
| `y_expression_text` | String | String |
| `y_values` | Real | Specifies numeric values for the y curve data |
| `ddata` | An Existing Component | Identifies the set of values to be used for the dependent (vertical) axis data |
| `dmeasure` | An Existing Measure | Identifies the measures to be used for the data displayed in the dependent axis. |
| `dvalues` | Real | Specifies numeric values for the dependent axis data |
| `haxis_data` | An Existing Component | Identifies the set of values that will be used for the horizontal axis data when creating a curve on an xy plot |
| `hmeasure` | An Existing Measure | An Existing Measure |
| `x_expression_text` | String | String |
| `x_values,` | Real | Specifies numeric values for the x curve data |
| `idata` | An Existing Component | Identifies the set of values to be used for the independent (horizontal by default) axis data when creating a curve on an xy plot. |
| `imeasure` | An Existing Measure | Identifies the measures to be used for the data displayed in the independent axis. |
| `iexpression_text` | String | String defining the independent axis data |
| `ivalues` | Real | Specifies numeric values for the independent curve data |
| `x_units` | String | String |
| `y_units` | String | String |
| `d_units` | String | Specifies the units for the curve's dependent data values. |
| `i_units` | String | Specifies the units for the curve's independent data values. |
| `run_name` | An Existing Analysis | Indicates an existing analysis where the measure results are to be found. |
| `vertical_axis_name` | An Existing Axis | Specifies the name of a vertical axis. |
| `auto_vertical_axis` | Boolean | Boolean |
| `auto_axis` | Auto_axis | Identifies one of the following: units , curve , none |
| `calculate_axis_limits` | Boolean | Identifies either: yes - Recalculates axis limits to fit curve (if axes are automatically scaled). no - Does not recalculate axis limits. |
| `horizontal_axis_name` | An Existing Axis | Specifies the name of the horizontal axis for the curve |
| `legend_text` | String | The text string to use for the plot curve's legend. |
| `auto_color` | Boolean | Specifies whether or not Adams View automatically selects a color for the curve (YES or NO). |
| `color` | An Existing Color | Specifies the COLOR of a graphic object |
| `line_type` | Line_style | This parameter allows the selection of the line type for a curve |
| `thickness` | Real | This parameter allows the specification of the thickness of the curve. |
| `increment_symbol` | Integer | If the curve has a symbol, indicates the interval at which they are displayed |
| `symbol_type` | Plot_symbols | This parameter identifies the shape of the symbol used to mark data points on an xy_plot. |
| `frozen` | Boolean | Boolean |
| `create_page` | Boolean | Creates a new page for the plot. Set it to yes or no. |
| `display_page` | Boolean | If a new page was created, displays the new page. Set it to yes or no. |
| `page_name` | String | Specifies the name of the new page. |
| `allow_hotpoints` | Hotpoint_motion | When you enable the ALLOW_HOTPOINTS attribute on a curve, you can then modify the curve using click and drag |

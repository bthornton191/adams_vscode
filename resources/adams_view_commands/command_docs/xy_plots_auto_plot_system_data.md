# xy_plots auto_plot system_data

Allows you to control the results set components that are used by the automatic plot generator to create plots.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `analysis_name` | Existing Analysis | Specifies an existing analysis from which the plot generator uses results sets to generate plots. |
| `units_filter` | Filter_Units | Specifies the types of units (dimensions) for results set components that the plot generator uses to create plots. |
| `object_names` | Existing adams object | Specifies objects for which Adams writes results sets into the results file, and which the plot generator uses to create plots. |
| `result_set_names` | Existing result set | Specifies result sets to be plotted. |
| `class_filter` | Filter Class | Specifies the classes of objects for which Adams writes results sets into the results file, and which the plot generator uses to create plots. |
| `type_filter` | Plot_filter_type | Specifies the types of objects for which Adams writes results sets into the results file, and which the plot generator uses to create plots. |

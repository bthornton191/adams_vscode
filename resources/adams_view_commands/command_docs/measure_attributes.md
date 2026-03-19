# measure attributes

Allows you can set the attributes for a strip chart, including creating a legend, setting axis limits, and setting the color and line type for the curve.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `measure_name` | Existing measure | Specifies an existing measure whose attributes have to be modified. |
| `comment` | String | Specifies any comments. |
| `legend` | String | Enter text that describes the data that the curve in the strip chart represents. |
| `axis_lower` | Real | Parameter not supported. |
| `axis_upper` | Real | Parameter not supported. |
| `axis_label` | String | Parameter not supported. |
| `axis_type` | Linear/logar/db/default | Select the type of plot to be displayed in Adams PostProcessor when you transfer the strip chart to it for plotting. |
| `curve_color` | Existing color | Enter color of the curve. |
| `curve_line_type` | SOLID, DASH, DOTDASH, DOT, NONE | Sets curve_Line Type to the type of line style for the curve. For example, you can select a line that alternates between dots and dashes. |
| `curve_thickness` | Real | Changes the weight of the curve line. Weight values range from 1 to 5 screen pixels. |

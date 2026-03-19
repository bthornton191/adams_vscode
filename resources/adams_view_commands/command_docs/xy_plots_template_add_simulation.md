# xy_plots template add_simulation

Allows you to add a set of simulation results to the xy plot. You can distinguish the new simulation results from the existing one using one of the following:

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `plot_name` | Existing Plot Name | Specifies a string of characters that identifies an existing plot |
| `distinguish_by_color` | Boolean | Select yes to have Adams View automatically choose colors to distinguish the new simulation results from the old. |
| `old_color` | Existing Color | Specifies a color to indicate the existing simulation data. |
| `new_color` | Existing Color | Specifies an existing color to use to indicate the new simulation data. |
| `distinguish_by_line_type` | Boolean | Select yes to have Adams View automatically choose line thickness to distinguish the new simulation results from the old. |
| `old_line_type` | Line Style | Selects a line type to indicate the existing simulation data. |
| `new_line_type` | Line Style | Select a line type to indicate the existing simulation data. |
| `distinguish_by_thickness` | Boolean | Select yes to have Adams View automatically choose line thickness to distinguish the new simulation results from the old. |
| `old_thickness` | Real | Specifies a real number indicating the thickness of the line representing the existing simulation data. The weight values are in screen pixels. |
| `new_thickness` | Real | Specifies a real number indicating the thickness of the line representing the new simulation data. The weight values are in screen pixels. |
| `old_run_name` | Existing Analysis | Sets the name of the simulation containing the existing simulation results that the curves you want operated on reference. |
| `new_run_name` | Existing Analysis | Sets the name of the simulation containing the simulation results to be added. |

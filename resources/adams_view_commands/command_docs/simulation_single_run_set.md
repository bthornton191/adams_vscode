# simulation single_run set

Allows you to set the parameters that are needed for simulation.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `update` | None, End, Output_step, Time_step Or Iteration | Sets simulation related options |
| `monitor` | None, Output_step, Time_step Or Iteration | This information helps you monitor the simulation process and to locate the source of the error if there is a problem. |
| `time_delay` | Real | Specifies the number of seconds to temporarily halt command processing. |
| `alert` | Yes/No | Specifies whether or not to alert the user before reading the binary file if there is data that has been modified since the last save operation. The alert box provides the user with the options to continue with the read or to cancel the read. |
| `icon_visibility` | On/Off | Specifies whether or not to display icons during the animation. |
| `save_analyses` | Yes/No | Specifies whether or not the analysis is to be saved. |
| `analysis_prefix` | String | After selecting Save Analysis, enter the name you want to use for each analysis object. |

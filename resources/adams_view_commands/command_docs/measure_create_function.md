# measure create function

An Adams Solver function measure allows you to create a measure in Adams View that Adams Solver evaluates during simulations. Because Adams Solver function measures are only evaluated during simulations, function measures remain unevaluated until you run a simulation. The Adams Solver function measure is convenient because it lets you reference any user-defined Adams Solver function or subroutine. Function measures are built from Adams Solver run-time functions.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `measure_name` | New name for measure | Specifies the name of the measure. |
| `function` | Function | Specifies function to be evaluated during the simulation. |
| `user_function` | Real | Specifies a real number |
| `routine` | String | Specifies a string for the routine. |
| `units` | String | Specifies any units that have to be associated. |
| `create_measure_display` | Yes/No | Specifies yes if the strip chart of the measure needs to be displayed. |
| `legend` | String | Specifies the text that will appear on the top of the measure dialog. |
| `comments` | String | Specifies any comments about the function measure. |

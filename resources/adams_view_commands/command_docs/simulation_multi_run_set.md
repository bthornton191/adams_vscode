# simulation multi_run set

Allows you to set the parameters for the multi-run simulation.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `load_analysis` | Yes/No | Specifies yes or no. |
| `save_analysis` | Yes/No | Set to Yes to automatically copies the parametric analysis results to a permanent location when the analysis is complete |
| `analysis_prefix` | String | Enters the name you want to use for each analysis object. |
| `stop_on_error` | Yes/No | Set to Yes to stop the parametric analysis if Adams Solver encounters an error during a simulation. If you set it to No, Adams Solver continues running simulations even if a simulation fails or another error occurs. |
| `save_curves` | Yes/No | Clears all displayed measures at the beginning of the parametric analysis and automatically saves the curve from each trial or iteration. |
| `chart_ objectives` | Yes/No | Enter yes or no. See extended definition for more details. |
| `chart_variables` | Yes/No | Displays a strip chart for each design variable, plotting its value versus the trial or iteration number. Adams View updates the strip chart every trial or iteration. Set it to yes or no accordingly. |
| `show_summary` | Yes/No | Yes/No |
| `opt_algorithm` | Algorithm | Specify optimization algorithm. See extended definition for more details. |
| `opt_maximum_ iterations` | Integer | Maximum iterations tells the optimization algorithm how many iterations it should take before it admits failure. Note that a single iteration can have an arbitrarily large number of analysis runs |
| `opt_ convergence_ tolerance` | Real | Convergence tolerance is the limit below which subsequent differences of the objective must fall before an optimization is considered successful. |
| `opt_ differencing_ tecnique` | Centered_difference/forward_difference | The differencing technique controls how the optimizer computes gradients for the design functions. |
| `opt_scaled_ perturbation` | Integer | The size of the perturbation can reduce the effect of errors in the analysis. |
| `opt_user_parameter` | Integer | Adams View passes the user parameters to a user-written optimization algorithm. |
| `opt_rescale_iteration` | Real | Rescale iteration is the number of iterations after which the design variable values are rescaled. If you set the value to -1, scaling is turned off. |
| `opt_slp_convergence_iter` | Real | The number of consecutive iterations for which the absolute or relative convergence criteria must be met to indicate convergence in the DOT Sequential Linear Programming method. |
| `opt_debug` | On/Off | Turning on debugging output sends copious optimizer diagnostics to the window that launched Adams View. |

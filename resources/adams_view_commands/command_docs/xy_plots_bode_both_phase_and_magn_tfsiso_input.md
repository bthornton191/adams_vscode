# xy_plots bode both_phase_and_magn tfsiso_input

Allows you to define a Bode plot (phase, magnitude, or both, depending on the command) using a transfer function.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `plot_name` | Existing Plot | Specifies the name of the Bode plot to be updated. |
| `page_name` | Existing Page | Specifies the name of the Bode page that the plot is on. |
| `transfer_function` | Existing TFSISO | Specifies the transfer function to be plotted. |
| `start_frequency and end_frequency` | Real | Defines the frequency sweep by entering the starting and ending frequencies for the bode plot and selecting the frequency step, which you define using one of next three parameters. |
| `frequency_step` | Real | Specifies the interval between frequencies. |
| `log_samples` | Integer | Specifies the number of log-spaced frequencies. |
| `samples` | Integer | Specifies the number of linear-spaced frequencies. |

# xy_plots bode both_phase_and_magn lse_input

Allows you to defines the Bode plot (phase, magnitude, or both, depending on the command) using ABCD matrices encapsulated in an Adams linear state equation system element.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `plot_name` | Existing plot | Specifies the name of the Bode plot to updated. |
| `page_name` | Existing page | Specifies the name of the Bode page that the plot is on. |
| `linear_state_equation` | Existing LSE | Specifies the linear state equation to be plotted. |
| `inputs and outputs` | Integer | Specifies the input and output results you would like to use for bode plot calculations. If you do not select any inputs or outputs, Adams View computes all combinations. |
| `start_frequency and end frequency` | Real | Defines the frequency sweep by entering the starting and ending frequencies for the bode plot and selecting the frequency step, which you define using one of the next three parameters. |
| `frequency_step` | Real | Specifies the interval between frequencies. |
| `log_samples` | Integer | Specifies the number of log-spaced frequencies. |
| `samples` | Integer | Specifies the number of linear-spaced frequencies. |

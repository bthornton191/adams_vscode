# xy_plots bode phase_plot coefficient_input

Allows you to define a Bode plot (phase, magnitude, or both, depending on the command) using coefficients.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `plot_name` | Existing Plot | Specifies the name of the Bode plot to be updated. |
| `page_name` | Existing Page | Specifies the name of the Bode page that the plot is on. |
| `numerator_coefficients and denominator_coefficients` | Real | Defines the numerator and denominator coefficients. |
| `start_frequency and end_frequency` | Real | Defines the frequency sweep by entering the starting and ending frequencies for the Bode plot and selecting the frequency step, which you define using one of the next three parameters. |
| `frequency_step` | Real | Specifies the interval between frequencies. |
| `log_samples` | Integer | Specifies the number of log-spaced frequencies. |
| `samples` | integer | Specifies the number of linear-spaced frequencies. |

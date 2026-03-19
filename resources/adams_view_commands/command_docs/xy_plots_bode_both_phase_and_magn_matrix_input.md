# xy_plots bode both_phase_and_magn matrix_input

Allows you to define the Bode plot (phase, magnitude, or both, depending on the command) using matrices.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `plot_name` | Existing plot name | Specifies the name of the Bode phase plot to updated. |
| `page_name` | Existing page name | Specifies the name of the Bode page that the phase plot is on. |
| `a, b, c, d` | Existing Adams Matrix | Specifies the A through D matrices that define the state matrix. |
| `inputs` | Integer | Defines the input results you want to use for Bode-plot calculations. If you do not select any inputs, Adams PostProcessor computes all combinations. |
| `outputs` | Integer | Defines the output results you want to use for Bode-plot calculations. If you do not select any outputs, Adams PostProcessor computes all combinations. |
| `start_frequency and end_frequency` | Real | Defines the frequency sweep by entering the starting and ending frequencies for the Bode plot and selecting the frequency step, which you define using one of the next three parameters. |
| `frequency_step` | Real | Specifies the interval between frequencies. |
| `log_samples` | Integer | Specifies the number of log-spaced frequencies. |
| `samples` | integer | Specifies the number of linear-spaced frequencies. |

# xy_plots bode phase_plot state_matrix_input

Allows you to define a Bode plot (phase, magnitude, or both, depending on the command) using linear state matrices generated through a linearization of an Adams model using Adams Linear, an optional module to Adams.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `plot_name` | Existing Plot | Specifies the name of the Bode phase plot to be updated. |
| `page_name` | Existing Page | Specifies the name of the Bode page that the phase plot is on. |
| `state_matrices` | Existing State Matrices | Specifies the state matrices. |
| `inputs` | Integer | Defines the input results you want to use for Bode-plot calculations. If you do not select any inputs, Adams PostProcessor computes all combinations. |
| `outputs` | Integer | Defines the output results you want to use for Bode-plot calculations. If you do not select any outputs, Adams PostProcessor computes all combinations. |
| `start_frequency and end_frequency` | Real | Defines the frequency sweep by entering the starting and ending frequencies for the Bode plot and selecting the frequency step, which you define using one of the next three parameters. |
| `frequency_step` | Real | Specifies the interval between frequencies. |
| `log_samples(mutually exclusive with frequency_step and samples)` | Integer | Specifies the number of log-spaced frequencies. |
| `samples` | Integer | Specifies the number of linear-spaced frequencies. |

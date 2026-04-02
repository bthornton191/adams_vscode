# xy_plots bode magnitude_plot state_matrix_input

Creates a Bode magnitude plot from state matrix inputs, computing frequency response over a defined range.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `plot_name` | String | Name for the Bode magnitude plot. |
| `page_name` | String | Name of the page on which to place the plot. |
| `state_matrices` | Array | Names of the state matrices to use. |
| `inputs` | Array | Input channel indices or names. |
| `outputs` | Array | Output channel indices or names. |
| `start_frequency` | Real | Starting frequency for the Bode plot (Hz). |
| `end_frequency` | Real | Ending frequency for the Bode plot (Hz). |
| `frequency_step` | Real | Frequency increment between computed points. |
| `log_samples` | Boolean | Whether to space frequency samples logarithmically. |
| `samples` | Integer | Number of frequency samples to compute. |

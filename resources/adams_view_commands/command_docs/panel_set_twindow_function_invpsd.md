# panel set twindow_function invpsd

The INVPSD (Inverse Power Spectral Density) function regenerates a time signal from a power spectral density description

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `x` | Function | Specifies a real variable that is the independent variable of the function |
| `spline_name` | An Existing Spline | You identify a spline by typing its name. |
| `min_frequency` | Real | A real variable that specifies the lowest frequency to be regenerated. |
| `max_frequency` | Real | A real variable that specifies the highest frequency to be regenerated |
| `num_frequencies` | Real | An integer that specifies the number of frequencies. This number is supposed to be larger than 1 and less than 200 |
| `use_logarithmic` | Boolean | An integer variable that acts as a flag indicating whether the PSD data points are interpolated in the linear or logarithmic domain. |
| `random_number_seed` | Real | A real variable that specifies a seed for a random number generator, used to calculate the phase shifts |

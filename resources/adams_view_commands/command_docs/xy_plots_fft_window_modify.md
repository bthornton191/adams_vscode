# xy_plots fft_window modify

Modifies an existing FFT window definition.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `window_name` | Object | Name of the FFT window to modify. |
| `start_time` | Real | Start time of the data range to transform. |
| `end_time` | Real | End time of the data range to transform. |
| `use_power_of_two` | Boolean | Whether to restrict the FFT sample count to a power of two. |
| `window_location` | String | Determines where the FFT result plot is placed. |
| `curve_name` | String | Name of the source curve to transform. |
| `window_size` | Integer | Number of samples in the FFT window. |
| `is3d` | Boolean | Whether to generate a 3D waterfall FFT plot. |
| `slice_size` | Integer | Number of samples per time slice for a 3D FFT. |
| `window_type` | String | Type of windowing function (e.g., `Hanning`, `Rectangular`). |
| `y_axis` | String | Quantity to plot on the Y axis (e.g., `magnitude`, `phase`). |
| `detrend` | Boolean | Whether to remove the mean (DC component) before transforming. |
| `segment_length` | Integer | Length of each segment for Welch/averaged FFT methods. |
| `overlap` | Real | Fractional overlap between segments (0.0–1.0). |
| `output_points` | Integer | Number of output frequency points. |
| `zfunct` | String | Function applied to Z values in a 3D FFT. |
| `fftstack` | Boolean | Whether to stack multiple FFT results. |
| `overlap_percent` | Real | Percentage overlap between segments (0–100). |

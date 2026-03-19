# graphic_results single_frame_display

Allows you to display the model geometry based on Adams simulation results, one frame at a time. These frames correspond to "simulation output time steps".

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `analysis_name` | An Existing Analysys | This parameter specifies the name of an analysis name. |
| `view_name` | An Existing View | Specifies the view for the display |
| `frame_number` | Integer | The FRAME_NUMBER parameter is used to specify the frame number (Adams simulation output time step) at which to configure a model during the single_frame_display command. |
| `time` | Time | The TIME parameter allows you to identify the frame number (Adams simulation output time step) at which to configure the model in the SINGLE_FRAME_DISPLAY command. |
| `configuration` | Display_Frame | This parameter is used to specify what output frame, or output time step, of the simulation results is to be displayed for the single_frame_display command. |
| `base_marker` | An Existing Marker | This parameter is used to specify a marker whose position will be frozen in the view as the model animates. |
| `camera_ref_marker` | An Existing Marker | This parameter is used to identify a marker which specifies the viewing direction as the model animates. |
| `offset` | Location | Specifies the offset of the axis line from the plot border. |
| `colors` | An Existing Color | Modifies the red, green, and blue components of existing colors. |
| `contour_plots` | on/off | on/off |

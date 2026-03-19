# graphic_results animate

Allows you to view a pseudo dynamic representation of the model motion simulated with Adams.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `analysis_name` | An Existing Analysis | This parameter specifies an analysis name. When Adams View reads a graphics file (.GRA), a request file (.REQ), or a results file (.RES) an analysis name is created. By default, the name of the analysis is the file name excluding the extension. |
| `view_name` | An Existing View | Specifies the view for the display |
| `number_of_cycles` | Integer | Parameter used to specify the number of complete cycles to animate. This means, based on this parameter, the animation will continuously run through all the specified frames, the specified number of times. |
| `increment_frame_by` | Integer | Parameter used to specify the number of frames to skip between each animation step. This allows the user to speed up the viewing of motions that take many frames to develop (that move slowly). If a negative value is entered, the animation will play in reverse. |
| `time_range` | Time | Parameter to specify the analysis output Adams simulation output time steps at which to start and stop the animation (in that respective order). |
| `frame_range` | Integer | Parameter to specify the analysis frame number (output time step) at which to start and stop the animation (in that respective order). |
| `superimposed` | On_Off | Parameter used with the animation command to specify whether or not to show each frame of the animation individually or superimposed on top of one another. |
| `base_marker` | An Existing Marker | This parameter is used to specify a marker whose position will be frozen in the view as the model animates |
| `camera_ref_marker` | An Existing Marker | This parameter is used to identify a marker which specifies the viewing direction as the model animates. |
| `point_trace_marker` | An Existing Marker | This parameter is used to specify marker(s) whose position will be traced in the view as the model animates. |
| `icon_visibility` | On_Off | Specifies whether or not to display icons during an animation. |
| `offset` | Location | Specifies the offset of the axis line from the plot border. |
| `colors` | An Existing Color | Modify the red, green, and blue components of existing colors. |
| `fullscreen_animation` | On_Off | Specifies the animation should be done using the entire application window. |
| `bitmap_animation` | Bitmap_Opts | Specifies options regarding generating and replaying a bitmap animation. |
| `record_to_laser_disc` | On_Off | Causes a single video frame to be recorded on the laser disc. |
| `animate_page` | Boolean | Boolean |

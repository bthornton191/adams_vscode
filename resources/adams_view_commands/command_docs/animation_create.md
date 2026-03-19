# animation create

Allows you to create a model

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `animation_name` | A New Animation | Specifies the name of a new animation |
| `analysis_name` | An Existing Analysis | Specifies the name of an existing analysis |
| `view_name` | An Existing View | Specifies the name of the view that you would like to view the animation from |
| `number_of_cycles` | Integer | Specifies the number of complete cycles to be animated |
| `time_range` | Time | Specifies the analysis output Adams simulation output time steps at which to start and stop the animation (in that order). |
| `frame_range` | Integer | Specifies the analysis frame number (output time step) at which to start and stop the animation (in that order). |
| `frame_number` | Integer | Specifies the frame number (adams simulation output time step) at which to configure a model during the single_frame_display command. |
| `time` | Time | Specifies the time as a real number greater than or equal to zero |
| `configuration` | Display_frame | Specifies what output frame, or output time step, of the simulation results is to be displayed for the single_frame_display command |
| `increment_frame_by` | Integer | Specifies the number of frames to skip between each animation step |
| `superimposed` | On_off | Parameter used with the animation command to specify whether or not to show each frame of the animation individually or superimposed on top of another |
| `base_marker` | An Existing Marker | Specifies a marker whose position will be frozen in the view as the model gets animated |
| `camera_ref_marker` | An Existing Marker | Identifies a marker which specifies the viewing direction as the model gets animated |
| `point_trace_marker` | An Existing Marker | Specifies marker(s) whose position will be traced in the view as the model animates |
| `icon_visibility` | On_off | Specifies whether or not to display icons during an animation |
| `offset` | Location | Specifies the offset of the axis line from the plot border |
| `colors` | An Existing Color | Modifies the red, green, and blue components of existing colors. |

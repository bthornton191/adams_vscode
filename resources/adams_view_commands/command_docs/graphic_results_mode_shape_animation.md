# graphic_results mode_shape_animation

Allows you to view the model oscillating at one of its natural frequencies.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `eigen_solution_name` | An Existing Eigen | Specifies an existing eigen_solution.You may identify a eigen_solution by typing its name. |
| `view_name` | An Existing View | Specifies an existing view |
| `mode_number` | Integer | Specifies which mode shape of the EIGEN_SOLUTION is to be used to calculate the deformation of the model. |
| `frequency` | Real | The FREQUENCY parameter is used to determine which mode shape of the EIGEN_SOLUTION is to be used to calculate the deformation of the model. |
| `translation_maximum` | Length | Specifies the maximum amount the parts will translate to from their undeformed position. |
| `rotation_maximum` | Angle | Specifies the maximum amount the parts are allowed to rotate from their undeformed position. |
| `show_time_decay` | Boolean | Specifies whether the amplitudes of the deformations are to remain constant or decay due to the damping factor calculated in the EIGEN_SOLUTION. |
| `frames_per_cycle` | Integer | Specifies the number of frames to be displayed for each cycle for this MODE_SHAPE_ANIMATION. |
| `number_of_cycles` | Integer | Parameter used to specify the number of complete cycles to animate. This means, based on this parameter, the animation will continuously run through all the specified frames the specified number of times. |
| `superimposed` | On_Off | Parameter used with the animation command to specify whether or not to show each frame of the animation individually or superimposed on top of one another. |
| `icon_visibility` | On_Off | Specifies whether or not to display icons during an animation. Entering 'ON' will cause Adams View to display the iconsduring animation. This will cause slower animation times. For this reason, 'OFF' is the default value. |
| `fullscreen_animation` | On_Off | Specifies the animation should be done using the entire application window. |
| `bitmap_animation` | Bitmap_Opts | Bitmap_Opts |
| `record_to_laser_disc` | On_Off | Causes a single video frame to be recorded on the laser disc. |

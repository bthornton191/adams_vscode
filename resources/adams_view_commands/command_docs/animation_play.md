# animation play

Allows you to play an animation.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `animation_name` | An Existing Animation | Specifies an existing animation name that has to be run |
| `page_name` | An Existing Page | Specifies the page in the Adams Postprocessor that is to be run |
| `type` | [time_marker, advancing_curve] | Specifies the type of the animation to play on a plot. The default is time_marker animation. In order to specify an animation where the curves advance on the plot with the animation time, specify the advancing_curve option |
| `time_window` | Real value | This parameter is applicable only to the advancing_curve animation option and controls the width of the moving time window on the plot, as the animation proceeds. When one of the axes on the plot is time, then the axis limits change with each frame of the animation according to the time_window specified. For data vs data plots, the axis limits stay unchanged during the animation and only the time-sliced portion of the curve advances on the plot. |

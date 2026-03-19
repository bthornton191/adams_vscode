# numeric_results transform

Allows you to get results to return at locations other than the positions reported in the result file. The transform command only transforms the results in the part result sets (these are the result sets denoted by names of the form xxx_XFORM, where xxx is the part name). The transform command is needed because the result file only gives displacement, velocity, and acceleration results of the local part reference frame (LPRF) origin position relative to ground.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `result_set_name` | Existing Result Set | Allows you to identify a result set name. |
| `new_result_set_name` | New Result Set | Allows you to identify the new result set name to be created with this operation. |
| `marker_name` | Existing Marker | The MARKER_NAME parameter specifies a marker whose coordinates are to be used as the reference position for transformation. The reference position is fixed relative to the part indicated by the RESULTS_SET_NAME parameter throughout the simulation. |
| `lprf_coords` | Real | The LPRF_COORDS parameter provides the coordinates of a point where information in a "part result set" should be transformed. |
| `global_coords` | Real | The GLOBAL_COORDS parameter provides the coordinates of a point where information in a "part result set" should be transformed. |

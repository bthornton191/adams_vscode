# list_info measure

Lists the distance between a marker and ground, or between two markers. The magnitude, X, Y, and Z components are listed.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `i_marker_name` | Existing marker | Specify the first of a pair of markers involved in the distance calculation. |
| `j_marker_name` | Existing marker | Specify the second of a pair of markers involved in the distance calculation. |
| `r_marker_name` | Existing marker | Specify a marker the distance calculation is to be relative to. |
| `model_name` | Existing model | Specify an existing model name. |
| `analysis_name` | Existing analysis | Specify an existing analysis name. |
| `configuration` | Display frame | Specify the configuration of the model at which measurements are to be taken. |
| `time` | Real | Specify the time at which measurements are to be taken. |
| `frame_number` | Integer | Specify the frame number at which measurements are to be taken. |
| `brief` | On/Off | Specifies whether to use the brief form (default) or an extended form of the requested information to be displayed. |
| `write_to_terminal` | On/Off | Specify if the information requested is to be sent to the informational window or not. |
| `file_name` | String | Specify that the information requested is to be sent to a file with the name specified with the parameter. |

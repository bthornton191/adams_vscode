# file fea_loads write

Allows you to export FEA load information in your model from Adams View after a simulation completes. This technique does not require you to set up requests before the simulation.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `marker_name` | Existing marker (required) | Only for rigid body. This parameter is mutually exclusive to the flexible body name. It specifies name of existing marker on rigid body which all load information will be relative. |
| `flexible_body_name` | Existing flexible body (required) | This parameter is mutually exclusive to the marker name. It specifies name of existing flexible body and all load information will be relative to the origin of the flexible body. |
| `analysis_name` | Existing analysis (required) | Specifies the name of the analysis. |
| `file_name` | String (required) | Specifies the name of the file that is to be written. |
| `header` | String (Optional) | Only for adams_fem file format. It specifies the strings of the header written in the exported file. |
| `no_inertia` | yes/no | Select to write inertia loads in addition to external loads or not. Inertia loads include linear acceleration, angular acceleration, and angular velocity of the flexible body. Reaction loads include applied and reaction forces acting on the body. The default is yes (Inertia loads are not included). |
| `node_id` | Integers (Optional) | Specifies node IDs to assign to the load points and it’s useful for rigid body because no node ID is defined at each markers. For flexible body, Adams View automatically assigns node IDs to the load points based on the actual node IDs of the flexible body at these load locations. |
| `locations` | Locations (Optional) | Specified the locations corresponding to node IDs above to find out the marker which has the same location. The number of locations and node IDs have to be identical. |
| `start_time` | Real (Optional) | Only for DAC/RPC file format. It specifies the start time to be written. The default is 0.0. |
| `end_time` | Real (Optional) | Only for DAC/RPC file format. It specifies the end time to be written. The default is the end time of the analysis. |
| `time` | Reals (Optional) | For other than DAC/RPC file format. It specifies the times separated by commas (,) to be written. All time steps are written if leave this blank. |
| `tolerance` | Real (Optional) | For other than DAC/RPC file format. It specifies the time range to write loads at each times above. For example, if you requested output at time steps 2 and 5 with a tolerance of 0.1, Adams View write for all output steps between 1.9 and 2.1 and 4.9 and 5.1. The default value is 0.0 and the loads at times are only written. |
| `format` | ansys/nastran/abaqus/adams_fem/dac/rpc/marc | Select the file format for the loads file that you want Adams View to write. The default is adams_fem. |

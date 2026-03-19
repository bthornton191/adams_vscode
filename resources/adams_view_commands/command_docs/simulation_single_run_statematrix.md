# simulation single_run statematrix

Allows you to get details related to the statematrix for the simulation.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_name` | An Existing Model | Specifies an existing model. |
| `state_matrices_name` | New State_matrices | Specifies the new name for the matrix data element that defines the state transition matrix for the linear system. |
| `plant_input_name` | Existing Plant_input | Specifies the plant input that Adams View uses as plant inputs in the state matrices computation. |
| `plant_output_name` | Existing Plant_output | Specifies the plant output that Adams View uses as plant outputs in the state matrices computation |
| `plant_state_name` | Existing Plant_state | Specifies a plant state to be used to define a set of states that are to be used in the linearization scheme. |
| `reference_marker` | An Existing Marker | Specifies an existing marker for reference |
| `matrix_format` |  | Specifies the matrix format to be used |
| `file_name` | Any File | Specify the name of the software in whose input format Adams View is to output the state matrices. |

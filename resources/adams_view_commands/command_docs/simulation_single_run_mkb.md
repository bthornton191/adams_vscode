# simulation single_run mkb

Specifies that Adams Solver (C++) calculates the M, K, B, C and D matrices for the Adams model. These matrices are used as inputs to an MSC Nastran model.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_name` | Existing Model | Specifies an existing model. |
| `mkb_matrices_name` | New Linear Result | Specifies the name of a new linear result. |
| `plant_input_name` | Existing Plant Input | Specifies the plant input that Adams View uses as plant inputs in the state matrices computation. If you do not specify a plant input, Adams View does not give the B and D matrices as output. |
| `plant_output_name` | Existing Plant Output | Specifies the plant output that Adams View uses as plant outputs in the state matrices computation. If you do not specify a plant output, Adams View does not give the C and D matrices as output. |
| `plant_state_name` | Existing Plant_state | Specifies a plant state to be used to define a set of states that are to be used in the linearization scheme. |
| `reference_marker` | Existing Marker | Specifies the reference marker. |
| `matrix_format` | Matrix_x/matlab | Currently, two software formats are supported: |
| `file_name` | Any File | Specifies the name of the software in whose input format Adams View is to give the state matrices as output. |

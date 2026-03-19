# simulation single_run vibration solve

Vibration analysis is a frequency domain simulation of Adams models. This simulation can be a normal modes analysis in which the Eigenvalues and mode shapes for the model are computed. The frequency domain simulation can also be a forced response analysis using the input and output channels along with the vibration.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_name` | Existing Model | Specifies an existing model. |
| `eigen_name` | New Eigen | Enter the name of an eigensolution. The eigensolution must be in a new eigen. |
| `state_matrices_name` | New State_matrices | Enter a new name for the matrix data element that defines the state transition matrix for the linear system. |
| `plant_input_name` | Existing Plant_input | Specifies the plant input that Adams View uses as plant inputs in the state matrices computation. |
| `plant_output_name` | Existing Plant_output | Specifies the plant output that Adams View uses as plant outputs in the state matrices computation. If you do not specify a plant output, Adams View does not output the C and D matrices. |
| `plant_state_name` | Existing Plant_state | Specifies a plant state to be used to define a set of states that are to be used in the linearization scheme. |
| `reference_marker` | Existing Marker | Specifies the reference marker |
| `number_of_modes` | Integer | If you do not specify the number of modes you want to compute, Adams Vibration automatically chooses a suitable number of modes based on the model size. |

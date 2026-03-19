# executive_control set solver_parameters

This command provides a means to select between the harwel, calahan, umf and auto integration solvers in Adams. This selection is made on a model by model basis.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_name` | String | Specifies the model to be modified. You use this parameter to identify the existing model to be affected with this command. |
| `solver_type` | String | Specifies that the HARWELL, CALAHAN, UMF or AUTO integration solvers is to be used in Adams for simulation of the model specified in the MODEL_NAME parameter. Each time you submit the model to be analyzed, the chosen solver will be used until this command is used to select the alternative. |

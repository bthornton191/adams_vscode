# output_control set madata

MADATA generates a modal file. This file serves as input to the Adams Modal program. Adams Modal is an auxiliary program marketed and supported by Mechanical Dynamics, Inc.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_name` | String | Specifies the model to be modified. You use this parameter to identify the existing model to be affected with this command. |
| `statistics` | Yes/No | Specifies that the modal data is to be dumped from the first static equilibrium analysis and writes it to the modal file. |
| `time` | Real Number greater than 0 | Dumps the modal data at up to thirty time steps (r1[,...,r30]) from the next quasi-static equilibrium analysis or from the next dynamic analysis and writes it to the modal file. |
| `comment` | String | Specifies a comment for request, mrequest, madata, and results entities. |

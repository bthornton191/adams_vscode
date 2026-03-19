# output_control set debug

Allows you to output data for debugging your data set. You can instruct Adams toprint out information using the following parameters:

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_name` | String | Specifies the model to be modified. You use this parameter to identify the existing model to be affected with this command. |
| `eprint` | On/Off | Specifies that a block of information will be printed for each kinematic, static, or dynamic step. |
| `verbose` | On/Off | Specifies that Adams will output additional information in the diagnostic messages and send it to the screen during an analysis. |
| `jmdump` | On/Off | Specifies that the Jacobian matrix will be dumped after each iteration. JMDUMP is useful only when you request a dynamic analysis. |
| `reqdump` | On/Off | Specifies that data from the REQUEST and MREQUEST statements is to be output at each iteration. |
| `rhsdump` | On/Off | Specifies that data from the YY array (state vector), the RHS array (error terms), and the DELTA array (increment to state vector) is to be dumped at each iteration. |
| `dump` | On/Off | Specifies that Adams will write the internal representation of your data set in the tabular output file after Adams reads and checks the input. |
| `topology` | On/Off | Specifies that Adams will print topological data in the message file. |
| `dof` | On/Off | Specifies that a degree-of-freedom table will be printed in the tabular output file. |

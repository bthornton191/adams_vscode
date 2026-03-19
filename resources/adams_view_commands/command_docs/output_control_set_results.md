# output_control set results

RESULTS is used to create the results file. This all-purpose file can contain all the simulation output from Adams. You can use the results file as an input file to Adams View. The results file may contain any combination of system displacements, velocities, accelerations, forces, variables defined through user-written differential equations, and user-written requests.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_name` | Existing model | Specifies the model to be modified. You use this parameter to identify the existing model to be affected with this command. |
| `create_results_file` | On/Off | Specifies whether or not Adams is to create a results file which contains all simulation output from Adams. For more information about the contents and format of the results file, see Appendix F in the Adams View Reference file. |
| `formatted` | On/Off | Specifies that the results file is to be a formatted file. The default is an unformatted (or binary) file. The formatted file is a sequential ASCII text file, and the unformatted file is a direct access binary file. You can understand a formatted file if you write it to the screen or print it. An unformatted binary file will read into a postprocessing program faster. |
| `applied_forces` | On/off | Specifies whether the results file is to include output from applied_forces. ON indicates that the results file will include the desired output. OFF indicates that the results file will not include the applied_forces output. |
| `displacements` | On/off | Specifies whether the results file is to include output from part displacements. ON indicates that the results file will include the desired output. OFF indicates that the results file will not include the part displacements output. |
| `reaction_forces` | On/off | Specifies whether the results file is to include output of reaction_forces. ON indicates that the results file will include the desired output. OFF indicates that the results file will not include the reaction_forces output. |
| `velocities` | On/off | Specifies whether the results file is to include output from part velocities. ON indicates that the results file will include the desired output. OFF indicates that the results file will not include the part velocity output. |
| `data_structures` | On/off | Specifies whether the results file is to include output from data_elements. These elements include: curves, splines, variables, arrays, matrices, plants, and strings. ON indicates that the results file will include the desired output. OFF indicates that the results file will not include the data_elements output. |
| `system_elements` | On/off | Specifies whether the results file is to include output from system_elements. These elements include LINEAR_STATE_EQUATIONs, GENERAL_STATE_EQUATIONs, and TRANSFER_FUNCTIONs. ON indicates that the results file will include the desired output. OFF indicates that the results file will not include the system_element output. |
| `linear` | On/off | Specifies whether the results file is to include output from an Adams linear analysis. ON indicates that the results file will include the desired output. OFF indicates that the results file will not include the linear analysis output. |
| `floating_markers` | On/off | Specifies whether the results file is to include output from floating_markers. ON indicates that the results file will include the desired output. OFF indicates that the results file will not include the floating_markers output. |
| `comment` | String | Specifies a comment for request, mrequest, madata, and results entities. |
| `accelerations` | On/off | Specifies whether the results file is to include part accelerations. |

# simulation set

Allows you to set the type of Adams Solver to be run.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `solver_preference` | Solver_pref | Selects the solver for the simulation |
| `save_file` | Yes/No | Set to Yes to create Adams Solver analysis files in the directory from which you ran Adams View. Adams View saves the files after each simulation. |
| `file_prefix` | String | After setting Save Files to Yes, enter the prefix you want added to the name of each saved analysis file to help identify it |
| `load_analysis` | Yes/No | Yes/No |
| `user_solver_executable` | String | Set it to use the standard Adams Solver executable (leave it blank) or a user-defined or customized Adams Solver library. |
| `remote_compute` | Yes/No | (Linux only parameter) Enter the name of the remote host where you run Adams Solver or leave blank to use local machine. The option you select depends on where the Adams Solver is licensed at your site. |
| `node_name` | String | Enter the node ID of the remote computer |
| `mdi_directory_remote` | String | Enter the name of the Adams Solver installation directory on the remote machine. |
| `directory_remote` | String | Specifies a directory that Adams Solver uses to write out its files and search for input files |
| `verify_first` | Yes/No | Set to yes to verify your model before running a simulation |
| `show_all_messages` | Yes/No | If you are running Adams Solver externally, set to Yes to display the messages that Adams Solver generates into an Information window |
| `hold_solver_license` | Yes/No | Set whether or not the Adams Solver license is checked back in once the simulation is complete. |
| `model_update` | On_off_auto | Select when the model is updated during simulation |
| `choice_for_solver` | Fortran/cplusplus | Select from one of the available solver versions |

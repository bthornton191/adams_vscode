# output_control set output

OUTPUT controls the generation of request, graphics, and initial conditions files. In addition, it controls the form, format, coordinates, filtering, and scaling of request data in the tabular output file. Specifically, OUTPUT controls the following:

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_name` | String | Specifies the model to be modified. You use this parameter to identify the existing model to be affected with this command. |
| `chart` | On/off | Specifies that Adams will produce x-y charts of the request data in the tabular output file. If you do not specify CHART=ON, Adams does not produce charts of the request data for the tabular output file. A value of ON for this parameter will produce a chart, and a value of OFF will not produce a chart. |
| `reqsave` | On/off | Specifies that Adams will save request output in the request file so that you can use Adams View to display x-y plots. If you do not specify REQSAVE=ON, Adams does not save the request output in the request file. The default value for this parameter is OFF. |
| `dacsave` | On/off | On/off |
| `rpcsave` | On/off | On/off |
| `print` | On/off | Specifies whether or not Adams will print time-response-request tables in the Adams Tabular Output File. If you specify ON, Adams will write tables for each request and mrequest in your model. If you specify OFF, Adams will not write the tables. |
| `fixed` | On/off | Specifies numerical output in fixed-point notation format. A value of FIXED=ON will force output to fixed-point notation. Any values that are too small or too large for fixed-point notation are output in scientific notation. If you specify FIXED=OFF, Adams formats numerical output in scientific notation. |
| `osformat` | On/off | Specifies that output-step-request (OS) tables will be written to the tabular output file immediately after completion of each output step for dynamic, kinematic, or quasi-static equilibrium analysis. If you specify OSFORMAT=ON, Adams outputs an output-step-request (OS) table at each output time step during simulation. If you specify OSFORMAT=OFF, Adams does not output request data in this form for these analysis types. |
| `ypr` | On/off | Specifies that rotational values are to be OUTPUT in yaw, pitch, and roll coordinates, rather than in psi, theta, and phi coordinates. |
| `separator` | On/off | Specifies whether or not Adams will write separators to the Request, Graphics, Results, and Tabular Output Files when you modify the model topology in the middle of a simulation. |
| `icsave` | On/off | Specifies that the state vector at every output time step will be saved. |
| `teletype` | On/off | Specifies Adams to format tabular output for printers with 72 columns per line, rather than for printers with 132 columns per line (this is done with the value TELETYPE=ON). A value of TELETYPE=OFF instructs Adams to format tabular output in 132 columns. |
| `grsave` | On/off | Specifies that Adams is to save graphic output in a graphics file. This file can then be read into Adams View, and the graphics can be displayed. A value of GRSAVE=ON will instruct Adams to write graphics data to the graphics file. If GRSAVE=OFF is specified, Adams does not save graphics output. |
| `dscale` | Real | Specifies the scale factor applied to translational and rotational displacements Adams outputs. Dscale accepts two REAL numbers(r1, r2). Define r1 to scale the translational displacements. Define r2 to scale the rotational displacements. Both r1 and r2 default to 1.0. |
| `dzero` | Real | Specifies that output displacements less than the value of this parameter, in magnitude, are to be set equal to zero. The value of DZERO must be greater than zero. The value of DZERO defaults to 1.0E-07 in scientific notation and to 0.001 in fixed-point notation. |
| `vscale` | Real | Specifies scale factors to apply to the translational and rotational velocities Adams outputs. VSCALE accepts two REAL numbers(r1, r2). Define r1 to scale the translational velocities. Define r2 to scale the rotational velocities. Both r1 and r2 default to 1.0. |
| `vzero` | Real | Specifies that output velocities less than the value of this parameter, in magnitude, are to be set equal to zero. The value of VZERO must be greater than zero. The value of VZERO defaults to 1.0E-07 for output in scientific notation and to 0.001 for output in fixed-point notation. |
| `ascale` | Real | Specifies a scale factor which is applied to the translational and the rotational accelerations that Adams outputs. |
| `azero` | Real | Specifies that output accelerations that have a magnitude less than the value of this parameter are to be set equal to zero. The value given must be greater than zero. The value defaults to 1.0E-07 for output in scientific notation and to 0.001 for output in fixed-point notation. |
| `fscale` | Real | Specifies a scale factor which is applied to the translational and the rotational forces Adams outputs. FSCALE accepts two REAL numbers (r1, r2. Define r1 to scale the translational forces. Define r2 to scale the rotational forces. Both r1 and r2 default to 1.0E+00 in scientific notation and to 1.0 in fixed-point notation. |
| `fzero` | Real | Specifies that output forces less than the value of this parameter, in magnitude, are to be set equal to zero. The value of FZERO must be greater than zero. The value of FZERO defaults to 1.0E-07 for output in scientific notation and to 0.001 for output in fixed-point notation. |
| `loads` | none/dac/nastran/generic/rpc/ansys/abaqus/marc | none/dac/nastran/generic/rpc/ansys/abaqus/marc |
| `modal_deformation` | none/generic/nastran/dac/punch/rpc/ansys/femfat | none/generic/nastran/dac/punch/rpc/ansys/femfat |
| `nodal_deformation` | none/generic/nastran/ansys/abaqus | none/generic/nastran/ansys/abaqus |
| `stress` | none/dac/generic/rpc | none/dac/generic/rpc |
| `strain` | none/dac/generic/rpc | none/dac/generic/rpc |

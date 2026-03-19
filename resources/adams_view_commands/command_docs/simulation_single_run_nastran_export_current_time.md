# simulation single_run nastran_export current_time

Export a linearized NASTRAN model from Adams at the current time operating point.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_name` | an existing model | The model to be exported. |
| `type` | open_box/closed_box | The type of export, that is low fidelity (open box) or high fidelity (closed box) |
| `config_file` | string | A configuration file to control the export |
| `output_file_prefix` | string | The file prefix to be used for the exported Nastran file(s). |
| `write_to_terminal` | on/off | Specify whether the output file is to be displayed in the info window after the export operation |
| `reset_after_export` | yes/no | Specify if the simulation has to be reset automatically after the export operation |
| `export_all_graphics` | on/off | Specify if you would like to export or not export all the graphics |

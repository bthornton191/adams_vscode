# file geometry write

Allows you to export CAD data (IGES, STEP, or Parasolid). See Manage Geometry Options for more information.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `type_of_geometry(required)` | Geometry_file_type | Specifies the type of geometry that is to have its rendering mode modified. |
| `file_name(required)` | String | Specifies the name of the file that is to be read, written, or executed. |
| `option_file_name` | String | Specifies the name of the file that contains translation options specific to the geometry format under consideration. Note the options file is specific to either the import or the export operation and to the designated geometry format. |
| `explode(optional)` | Boolean | Values are: yes and no. |
| `model_name(required)` | An Existing Model | Specifies the Adams View model to be written to the CAD file. Adams View places each rigid body in the model on a separate level. |
| `analysis_name(required)` | An Existing Analysis | Specifies a model at a particular simulation frame (time) of a particular analysis. |
| `frame_number(required)` | Integer | Specifies the frame number (simulation output time step) at which to configure a model during the file geometry write command |
| `part_name(required)` | An Existing Body | Specifies the name of the Adams part from which the geometry is written to the iges file. |
| `display_summary` | Boolean | Values: Yes or no |
| `active_only` | Boolean | Values: Yes or no |

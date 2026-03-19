# file iges read

Allows you to read an IGES geometry file.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `file_name` | String | Specifies the name of the IGES file containing the geometry, to be imported into Adams View for the FILE IGES READ command, or the name of the IGES file to be generated for the FILE IGES WRITE command. |
| `option_file_name` | String | Specifies the name of the file that contains translation options specific to the geometry format under consideration. Note the options file is specific to either the import or the export operation and to the designated geometry format. |
| `part_name` | An Existing Part | Specifies the name of an existing Adams View PART onto which the translated geometry will be placed. |
| `geometry_type` | Iges_geometry_type | Specifies the type of geometric entities to be translated from the IGES file to Adams View. |
| `blanked_entities` | Boolean | Specifies if invisible geometry is to be converted. |
| `level` | Integer | Note: This argument has been deprecated and no longer has any influence. |
| `create_geometry` | Iges_create_type | Note: This argument has been deprecated and no longer has any influence. |
| `scale` | Real | Specifies the scale factor to be applied to the size of the geometry created in Adams View |
| `mesh_density` | Integer | Note: This argument has been deprecated and no longer has any influence. |
| `tolerance` | Real | Note: This argument has been deprecated and no longer has any influence. |
| `single_shell` | Shell_opt | Shell_opt |
| `location` | Location | Specifies the translational position where the geometry in the IGES file is to be located relative to the Adams View part lprf. |
| `orientation` | Orientation | Specifies the angular position where the geometry in the IGES file is to be oriented relative to the Adams View part lprf. |
| `relative_to` | An Existing Model, Part Or Marker | Specifies the coordinate system that location coordinates and orientation angles correspond to. |
| `clean_on_import(optional)` | yes/no | Enables an automatic geometry scanner and cleaner behind-the-scenes during import of parasolid files. This process looks for small imperfections in the geometry that would render in not "watertight" and therefore cause problems with mass property calculations based on geometry and density/material. In some cases, this may slow down import speed of certain geometry. If disabling this option, be sure to verify that the volume Adams View calculates is still sufficiently accurate enough. Yes is the default. |

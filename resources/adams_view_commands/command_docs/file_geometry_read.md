# file geometry read

Allows you to import CAD geometry (CatiaV4, CatiaV5, CatiaV6, Inventor, Acis, PROE, Solidworks, Unigraphics, VDA, IGES, STEP or Parasolid). See Manage Geometry Options for more information.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `type_of_geometry` | Geometry_file_type | Specifies the type of geometry that is to have its rendering mode modified. |
| `file_name` | String | Specifies the name of the file that is to be read, written, or executed. |
| `option_file_name` | String | Specifies the name of the file that contains translation options specific to the geometry format under consideration. Note the options file is specific to either the import or the export operation and to the designated geometry format. |
| `part_name` | An Existing Part | Specifies the name of the part with which you want to associate the imported geometry. |
| `model_name` | An existing model | This parameter is mutually exclusive to the 'part_name' parameter and is valid only for Interop based translations. |
| `geometry_type` | Iges_geometry_type | Specifies the type of geometric entities to be translated from the IGES file to View. |
| `blanked_entities` | Boolean | Specifies if invisible geometry is to be converted. |
| `level` | Integer | Note: This argument has been deprecated and no longer has any influence. |
| `create_geometry` | Geom_create_type | Note: This argument has been deprecated and no longer has any influence. |
| `scale` | Real | Enter the factor by which you want to scale the size of the geometry created. |
| `mesh_density` | Integer | Note: This argument has been deprecated and no longer has any influence. |
| `tolerance` | Real | Note: This argument has been deprecated and no longer has any influence. |
| `single_shell` | Shell_opt | Values are: yes, no, and wireframe_only. |
| `location` | Location | Specifies the translational position where the geometry in the CAD file is to be located, relative to the MSC. part coordinate system. |
| `orientation` | Orientation | Specifies the angular position where the geometry in the CAD file is to be oriented, relative to the MSC. part coordinate system. |
| `relative_to` | An Existing Model, Part Or Marker | Specifies the coordinate system relative to which the location coordinates and orientation angles exist. |
| `clean_on_import(optional)` | yes/no | Enables an automatic geometry scanner and cleaner behind-the-scenes during import of parasolid files. This process looks for small imperfections in the geometry that would render in not "watertight" and therefore cause problems with mass property calculations based on geometry and density/material. In some cases, this may slow down import speed of certain geometry. If disabling this option, be sure to verify that the volume Adams View calculates is still sufficiently accurate enough. Yes is the default. |
| `assembly_retain` | Boolean | When specified to true, the import operation will create sub-models as necessary, in order to maintain the hierarchy in the input CAD model. Note that the parameter is only supported in Adams Modeler. If specified in traditional Adams, the parameter will be ignored. |
| `display_summary` | Boolean | Values: Yes or no |
| `ref_markers` | global/local | Upon import Adams creates reference markers to correspond with each piece of geometry created in the Adams model. These markers are typically automatically named with the prefix PSMAR. These reference markers are usually located and oriented at the origin of the Adams model. However, sometimes the geometry in the CAD file was created in such a way in the CAD system that it has a location/orientation transformation value relative to the CAD assembly/part origin.For example, the geometry was created via a copy/paste/move action performed on an original piece of geometry, or an assembly is composed of a number of parts/sub-assemblies re-located relative to the origins about which they were originally modelled. In these scenarios, setting the option Reference Markers to “Local” will locate/orient the Adams-created reference markers by applying the same location/orientation transformation value used in construction in the CAD system to the marker relative to the Adams model origin. Setting the option Reference Markers to “Global” will locate/orient all reference markers at the origin of the Adams model. |

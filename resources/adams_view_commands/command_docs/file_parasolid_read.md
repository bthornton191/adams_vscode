# file parasolid read

Imports Parasolids geometry. See Manage Geometry Options for more information.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `file_name(required)` | String | Specifies the name of the file that is to be read. |
| `type(optional)` | Ascii/binary/neutral | Specifies the internal format. The options are: ASCII, binary, and neutral. |
| `model_name(required)` | New Or Existing Model | Enter the model name under which you want to store the geometry. |
| `part_name(required)` | New Or Existing Body | Enter the part name under which you want to store the geometry. |
| `location(optional)` | Location | Specifies the translational position where the geometry in the imported file is to be located relative to the Adams View part lprf. |
| `orientation(optional)` | Orientation | Specifies the angular position where the geometry in the imported file is to be oriented relative to the Adams View part lprf. |
| `relative_to(optional)` | Existing Body,part Or Marker | Specifies the coordinate system relative to which the location coordinates and orientation angles exist. |
| `explode_assemblies(optional)` | yes/no | Specifies whether or not each geometric entity in an assembly is created as a separate marker (yes) or consolidated into one (no). no is the default. |
| `clean_on_import(optional)` | yes/no | Enables an automatic geometry scanner and cleaner behind-the-scenes during import of parasolid files. This process looks for small imperfections in the geometry that would render in not "watertight" and therefore cause problems with mass property calculations based on geometry and density/material. In some cases, this may slow down import speed of certain geometry. If disabling this option, be sure to verify that the volume Adams View calculates is still sufficiently accurate enough. Yes is the default. |
| `ref_markers` | global/local | Upon import Adams creates reference markers to correspond with each piece of geometry created in the Adams model. These markers are typically automatically named with the prefix PSMAR. These reference markers are usually located and oriented at the origin of the Adams model. However, sometimes the geometry in the CAD file was created in such a way in the CAD system that it has a location/orientation transformation value relative to the CAD assembly/part origin.For example, the geometry was created via a copy/paste/move action performed on an original piece of geometry, or an assembly is composed of a number of parts/sub-assemblies re-located relative to the origins about which they were originally modelled. In these scenarios, setting the option Reference Markers to “Local” will locate/orient the Adams-created reference markers by applying the same location/orientation transformation value used in construction in the CAD system to the marker relative to the Adams model origin. Setting the option Reference Markers to “Global” will locate/orient all reference markers at the origin of the Adams model.The default is "Global". |

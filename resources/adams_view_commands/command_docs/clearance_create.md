# clearance create

Creates a new clearance study. There are two kinds of clearances in Adams, Run-time clearances and Post-processing clearances. Use the menu items Tools → Clearance→ Create in Adams PostProcessor, to create a clearance study for post-processing clearance.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `clearance_name` | String | Specifies the name of the clearance study. |
| `comments` | String | Any accompanying extra information that the user wishes to store with the clearance study. |
| `i_geometry` | Existing Geometry | The first selected entity if it is a geometry. |
| `i_part` | Existing Part | The first selected entity if it is a part. This option is only available for post-processing clearances. |
| `i_flex` | Existing Flexible Body | The first selected entity if it is a flexible body |
| `j_geometry` | Existing Geometry | The second selected entity if it is a geometry |
| `j_part` | Existing Part | The second selected entity if it is a part. This option is only available for post-processing clearances.. |
| `j_flex` | Existing Flexible Body | The first selected entity if it is a flexible body |
| `i_region` | Existing Matrix | If the i_flex parameter is specified, then i_region parameter specifies the list of matrices to be excluded/included in the clearance computations. This option is only available for post-processing clearances. |
| `j_region` | Existing Matrix | If the j_flex parameter is specified, then j_region parameter specifies the list of matrices to be excluded/included in the clearance computations. This option is only available for post-processing clearances. |
| `i_exclude` | Boolean | A list of Boolean values that specifies whether the regions listed in the i_region parameter are to be excluded from the clearance computation. This option is only available for run-time clearances. |
| `j_exclude` | Boolean | A list of Boolean values that specifies whether the regions listed in the j_region parameter are to be excluded from the clearance computation. This option is only available for run-time clearances. |
| `maximum` | Real | To reduce the calculations in the clearance study, you can also define a maximum distance above which Adams PostProcessor does not calculate the clearance |
| `threshold` | Real | For run-time clearances, specifies the threshold distance. When the clearance distance exceeds the threshold value, the precise check is skipped and the gross clearance value is returned. |
| `method` | Selection List | The calculation method used by the Adams PostProcessor for clearance studies. |
| `run_time` | Boolean | Specifies whether the clearance is a run-time clearance or not. If this parameter is not specified then the clearance is treated as a post-processing clearance. |

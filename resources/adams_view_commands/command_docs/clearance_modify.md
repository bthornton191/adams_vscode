# clearance modify

Enables the user to modify an existing clearance study.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `clearance_name` | Existing Clearance | Specifies the name of an existing clearance study |
| `new_clearance_name` | New Clearance | Specifies the name of a new clearance study |
| `comments` | String | Comment string |
| `maximum` | Real Value | To reduce the calculations in the clearance study, you can also define a maximum distance above which Adams PostProcessor does not calculate the clearance. This parameter can be specified only for post-processing clearances. |
| `threshold` | Real Value | For run-time clearances, specifies the threshold distance. When the clearance distance exceeds the threshold value, the precise check is skipped and the gross clearance value is returned. |
| `method` | Selection List | Specifies the calculation method for the clearance study. This parameter can be specified only for post-processing clearances. |

# output_control attributes mrequest

Allows you to change the color and visibility of an mrequest icon.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `mrequest_name` | String | Specifies the mrequest to be modified. You use this parameter to identify the existing mrequest to be affected with this command. |
| `visibility` | String | Specifies the visibility of graphic entities. The visibility parameter is used to control whether graphic entities, such as markers, joints, and parts, are to be drawn in an Adams View viewport. |
| `color` | String | Specifies the color the modeling entity should be drawn in. |
| `active` | On/Off/No_opinion | When you set ACTIVE=NO, that element is written to the data set as a comment. |
| `dependents_active` | On/Off/No_opinion | The DEPENDENTS_ACTIVE parameter acts in the same fashion as that of the ‘active’ parameter, but sets the ACTIVE attribute for the dependents, all the way down the dependency chain. |

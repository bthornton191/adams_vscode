# file mnfxform rotate

Allows you to rotate a flexible body. You need to specify an existing Flexible Body / Modal Neutral File (MNF) / MD DB file, an axis for rotation and angle. The flexible body will be rotated about the specified axis by specified angle. You can also specify offset/ new interface node ids which will increment/replace the current interface node ids of the flexible body respectively. You can also optimize the MNF by using the option MNF Write Option, which corresponds to the parameters in the MDI_MNFWRITE_OPTIONS environment variable. For more information on the MDI_MNFWRITE_OPTIONS, see Setting Up Translation Options through the MNF Toolkit.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `flexible_body_name` | Existing flexible body | This parameter is mutually exclusive to the MNF file and MD DB File. Specifies the flexible body that needs to be rotated. |
| `modal_neutral_file_name` | String | This parameter is mutually exclusive to the flexible body name and MD DB File. It specifies the name of the MNF file name to be rotated. |
| `md_db_file_name` | String | This parameter is mutually exclusive to the MNF file and flexible body name. It specifies the name of the MD DB file to rotate. |
| `index_in_database` | Integer | This parameter applies only, when the user has selected md_ db_ file_name for rotating a flexible body. This parameter specifies the index of the flexible body in the specified MD DB. It is optional. If not specified, it is assumed to have the value 1. |
| `output_file_type` | mnf, md db | Specifies what kind of output file will be created either MNF/ MD DB. |
| `output_file_name` | String | Specifies the name of MNF/MD DB file to be created after rotation. |
| `orientation` | Global X, Global Y, Global Z, X Axis,Y Axis, Z Axis, User Defined | Specifies orientation for rotation. If orientation is X Axis, Y Axis or Z Axis then marker needs to be specified as these axis are marker's axis. If orientation is user defined then you need to enter user_input. |
| `marker` | Existing Model, Marker | Specifies an existing marker on the model. This option is only available when orientation is X Axis, Y Axis, Z Axis. |
| `user_input` | Orientation | Specifies any arbitrary orientation about which you want to rotate the flexible body. |
| `location` | location | Specifies the location for rotation. |
| `pl_point_1` | location | This parameter and the next parameters (pl_point_2 and pl_point_3) are mutually exclusive to the parameters (orientation, marker and location). It specifies x, y, and z coordinates of first point that lies on a plane. |
| `pl_point_2` | location | Specifies x, y, and z coordinates of second point that lies on a plane. |
| `pl_point_3` | location | Specifies x, y, and z coordinates of third point that lies on a plane. |
| `point_1` | location | This parameter and the next parameters (point_2) are mutually exclusive to the parameters (orientation, marker, location, pl_point_1, pl_point_2 and pl_point_3). It specifies x, y, and z coordinates of one of the end points. |
| `point_2` | location | Specifies x, y, and z coordinates of one of the end points. |
| `angle` | real | Specifies the angle for rotation. |
| `node_number_offset` | integer | This parameter is mutually exclusive to the id_list. Specifies offset value by which the current interface node ids will be incremented. It is optional parameter. |
| `id_list` | integer array | This parameter is mutually exclusive to the node_number_offset. It specifies a list of new interface node ids that will replace the current interface node ids. It is optional parameter. |
| `mnfwrite_options` | parameters in MDI_MNFWRITE_OPTIONS environmental variable | Specifies a list of parameters in MDI_MNFWRITE_OPTIONS environment variable. |

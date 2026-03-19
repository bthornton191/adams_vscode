# measure modify orient

Allows you to modify an orientation measure. Orientation measures capture the orientation characteristics of one part or marker relative to another coordinate system in a specified convention. For example, you could use orientation measures to determine the:

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `measure_name` | New mea_orient | Specifies name for the measure to be created |
| `component` | Angle_1_component, Angle_2_component, Angle_3_component, Param_1_component, Param_2_component, Param_3_component, Param_4_component, Mat_1_1_component, Mat_1_2_component, Mat_1_3_component, Mat_2_1_component, Mat_2_2_component, Mat_2_3_component, Mat_3_1_component, Mat_3_2_component, Mat_3_3_component | Specifies the rotational component you want to measure. PARAM_i_COMPONET stands for the i th component of the Euler parameters when characteristic=EULER_PARAMETERS. MAT_i_j_COMPONET stands for the entry of the direction cosine matrix where i is the row number and j is the column number when characteristic=DIRECTION_COSINES. And ANGLE_i_COMPONET stands for the i th component of the angles when characteristic is assigned to other value types. |
| `characteristic` | Euler_angles, Yaw_pitch_roll, Ax_ay_az_projection_angles, Bryant_angles, Body_1_2_3, Body_2_3_1, Body_3_1_2, Body_1_3_2, Body_2_1_3, Body_3_2_1, Body_1_2_1, Body_1_3_1, Body_2_1_2, Body_2_3_2, Body_3_1_3, Body_3_2_3, Space_1_2_3, Space_2_3_1, Space_3_1_2, Space_1_3_2, Space_2_1_3, Space_3_2_1, Space_1_2_1, Space_1_3_1, Space_2_1_2, Space_2_3_2, Space_3_1_3, Space_3_2_3, Euler_parameters, Rodriguez_parameters, Direction_cosines | Specifies the Characteristic convention with which to associate the component. |
| `to_frame` | Existing model, part or marker | Enter the coordinate system to which to measure |
| `from_frame` | Existing Model, Part Or Marker | Enter the coordinate system from which to measure. |
| `create_measure_display` | Yes/no | Specifies yes if you want to display the strip chart. |
| `legend` | String | Specifies the text that will appear at the top of the created measure. |

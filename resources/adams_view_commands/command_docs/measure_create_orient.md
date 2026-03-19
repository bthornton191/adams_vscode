# measure create orient

Creates an orientation measure. Orientation measures capture the orientation characteristics of one part or marker relative to another coordinate system in a specified convention. For example, you could use orientation measures to determine the:

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `measure_name` | New mea_orient | Specifies name for the measure to be created |
| `component` | ANGLE_1_COMPONENT, ANGLE_2_COMPONENT, ANGLE_3_COMPONENT, PARAM_1_COMPONENT, PARAM_2_COMPONENT, PARAM_3_COMPONENT, PARAM_4_COMPONENT, MAT_1_1_COMPONENT, MAT_1_2_COMPONENT, MAT_1_3_COMPONENT, MAT_2_1_COMPONENT, MAT_2_2_COMPONENT, MAT_2_3_COMPONENT, MAT_3_1_COMPONENT, MAT_3_2_COMPONENT, MAT_3_3_COMPONENT | Specifies the rotational component you want to measure. PARAM_i_COMPONET stands for the i th component of the Euler parameters when characteristic=EULER_PARAMETERS. MAT_i_j_COMPONET stands for the entry of the direction cosine matrix where i is the row number and j is the column number when characteristic=DIRECTION_COSINES. And ANGLE_i_COMPONET stands for the i th component of the angles when characteristic is assigned to other value types. |
| `characteristic` | EULER_ANGLES, YAW_PITCH_ROLL, AX_AY_AZ_PROJECTION_ANGLES, BRYANT_ANGLES, BODY_1_2_3, BODY_2_3_1, BODY_3_1_2, BODY_1_3_2, BODY_2_1_3, BODY_3_2_1, BODY_1_2_1, BODY_1_3_1, BODY_2_1_2, BODY_2_3_2, BODY_3_1_3, BODY_3_2_3, SPACE_1_2_3, SPACE_2_3_1, SPACE_3_1_2, SPACE_1_3_2, SPACE_2_1_3, SPACE_3_2_1, SPACE_1_2_1, SPACE_1_3_1, SPACE_2_1_2, SPACE_2_3_2, SPACE_3_1_3, SPACE_3_2_3, EULER_PARAMETERS, RODRIGUEZ_PARAMETERS, DIRECTION_COSINES | Specifies the Characteristic convention with which to associate the component. |
| `to_frame` | Existing model, part or marker | Enter the coordinate system to which to measure |
| `from_frame` | Existing model, part or marker | Enter the coordinate system from which to measure. |
| `create_measure_display` | Yes/No | Specifies yes if you want to display the strip chart. |
| `legend` | String | Specifies the text that will appear at the top of the created measure. |

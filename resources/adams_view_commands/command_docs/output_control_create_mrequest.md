# output_control create mrequest

Allows you to create mrequest files. The MREQUEST statement specifies multiple sets of data that you want Adams Solver (FORTRAN) to write in the tabular output file and request file. You can request sets of displacements, velocities, accelerations, or forces for system elements such as parts, joints, joint primitives, or applied forces in the system.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `mrequest_name` | String | Specifies the name of the mrequest to be created. You use this parameter to identify the existing mrequest to be affected with this command. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `j_marker_name` | String | Specifies a single base marker for measuring the displacements, velocities, or accelerations of the center-of-mass of the parts. Adams Solver (FORTRAN) makes all measurements for parts on the center-of-mass marker on each part with respect to the J marker you specify. The J marker defaults to the ground coordinate system (GCS). |
| `r_marker_name` | String | Identifies the reference marker with respect to which you want to resolve information. RM defaults to zero, which causes Adams Solver (FORTRAN) to resolve components in the ground coordinate system (GCS). |
| `comment` | String | Specifies a title for the top of each set of information the MREQUEST statement outputs. The entire comment must be on one line. Because the COMMENT argument can be only eighty characters long at most, the title can be from seventy-two characters long (if you do not abbreviate COMMENT=) to seventy-eight characters long (if you abbreviate COMMENT= to C=). Blank spaces and all alphanumeric characters can be used. However, the comma (,), the semicolon (;), the ampersand (&), and the exclamation point (!) cannot be used. |
| `output_type` | DISPLACEMENT/VELOCITY/ACCELERATION/FORCE | See extended definition for details on each output_type |
| `part_name` | String | Specifies names of part with which you want to output displacements, velocities, or accelerations. |
| `joint_name` | String | Specifies name of joint with which you want to output displacements, velocities, or accelerations. |
| `jprim_name` | String | Specifies name of joint primitive with which you want to output displacements, velocities, or accelerations. |
| `force_name` | String | Specifies name of force or a list of forces with which you want to output displacements, velocities, or accelerations. |
| `all` | Parts/joints/jprims/forces | Specifies that Adams is to output data for all parts, joints, joint primitives, or forces. Rather than entering each name individually, you may use this parameter to request data for all entities of a particular type. |

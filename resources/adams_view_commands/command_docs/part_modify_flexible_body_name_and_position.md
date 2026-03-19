# part modify flexible_body name_and_position

Allows you to create or modify a flexible body. You specify a modal neutral file (MNF) or a MD DB file or a BDF file name, and Adams View creates the necessary Adams View geometry for displaying the flexible body. It also creates a mesh on the flexible body representing the flexible body nodes.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `flexible_body_name` | Existing Flex Body | Specifies the name of the flexible body to be modified |
| `new_flexible_body_name` | New Flex_body Name | Specifies the new name of the flexible body. |
| `adams_id` | Integer | Assigns a unique ID number to the part. |
| `comments` | String | Adds comments about the part to help you manage and identify it. |
| `view_name` | Existing View | Specifies the view in which to display the part. You may identify a view by typing its name or by picking it from the screen. In most cases, you can enter the special view name all, which means all the views currently displayed. You must separate multiple view names by commas. You need not separate multiple view picks by commas. |
| `modal_neutral_file_name` | String | This parameter is mutually exclusive to the MD DB file and BDF files. Specifies the name of the MNF. |
| `md_db_ file` | String | This parameter is mutually exclusive to the MNF and BDF files. Specifies the name of the MD DB file to create the flex body from. |
| `bdf_file_name` | String | This parameter is mutually exclusive to the MD DB and MNF files. Specifies the name of the Nastran BDF file to create the non-linear flex body from. |
| `index_in_database` | Integer | The parameter applies only, when the user is creating a flexible body out of the MD DB. The parameter specifies the index of the flexible body in the specified MD DB. The parameter is optional. If not specified, it is assumed to have the value 1. |
| `matrices` | Existing Matrix | Specifies the names of seventeen matrices for the modal representation of the flexible body. |
| `damping_ratio` | Function | Specifies the damping ratio to be used. |
| `damping_routine` | String | Specifies the path to user-written subroutine to be used to define modal damping. |
| `generalized_damping` | Off, full, internal_only | Sets generalized damping: |
| `g` | Real | Specifies the structural damping coefficient. Is a Real Value with default value of 0.0. |
| `alpha1` | Real | Specifies the scale factor for mass portion of Rayleigh damping. Is a Real Value with default value of 0.0. |
| `alpha2` | Real | Specifies the scale factor for stiffness portion of Rayleigh damping. Is a Real Value with default value of 0.0. |
| `gefact` | Real | Specifies the Scale factor for material damping. Is a Real value that defaults to 1.0. |
| `w3` | Real | Specifies the average frequency for calculation of structural damping in a transient response. Is a Real value that is >= 0 and defaults to value 0.0. |
| `w4` | Real | Specifies the average frequency for calculation of material damping in a transient response. Is a Real value that is >= 0 and defaults to value 0.0. |
| `dynamic_limit` | Real | Specifies the threshold frequency for quasi-static modes. |
| `location` | Location | Specifies x, y, and z coordinates defining the flexible body's location in a given reference frame defined in the parameter relative_to. |
| `orientation` | Orientation | Specifies the orientation method |
| `along_axis_orientation` | Location | Specifies the orientation method |
| `in_plane_orientation` | Location | Specifies the in_plane orientation method |
| `relative_to` | Existing Model, Part or Marker | Specifies a reference frame relative to which the location and orientation are defined. Leave blank or enter model name to use the global coordinate system. |
| `exact_coordinates` | X, Y, Z, PSI, THETA, PHI, NONE, ALL | Specifies as many as six part coordinates that Adams View is not to change as it solves for the initial conditions. |
| `invariants` | Yes, No | Lists nine on/off values used to control the invariants |
| `characteristic_length` | Real | Specifies the characteristic length of the flexible body for linear limit check. This should be in the model length unit. The linear limit is defined as 10% of this length. |
| `hide_warnings` | No/Yes | Sets the option of displaying the warnings to yes or no. |
| `representation` | RIGID, MODAL, NFORCE, NONE | Specifies the representation of the flexible body and if it is eligible for runtime type switching between MODAL (linear) and RIGID representation during a simulation. If MODAL, the flex body will be treated as a linear flex body initially and can be switched to rigid body using the FLEX_BODY Solver command. If RIGID, the flex body will be treated as a rigid body initially and can be switched to linear flexible formulation during the simulation. These two options provide dual representation capability of the flex body during the simulation.If representation is NFORCE, NONE or not specified, the flex body is not eligible for runtime switching.If NFORCE, the flex body's modal representation is Simplified. Its modal representation is converted to a semi-equivalent multi_point_force representation with rigid_body. The stiffness and damping matrix of the multi_point_force is derived from the modal stiffness matrix and modal damping settings. The properties of the rigid_body are derived from the mass invariants of the flexible_body. |
| `stability_factor` | Real | Specifies the amount of damping needed to add to the quasi-static modes in order to help stabilize the simulation. |
| `fea_mem_settings` | Real | Specifies the amount of open core memory to allocate. The memory size is specified in MB. If no value is specified, the MAXIMUM memory setting would be used, which is 8GB for windows and linux platforms. |
| `self_contact` | Yes, No | Select to enable self-contact for this flex body during the simulation. Default is off. Contact could increase the solution time so only use this option if you think the flexible body may come in contact with itself. |
| `nlfe_stress` | Yes, No | This option controls the stress output to the Nastran result file (.op2 file) during the simulation. If this option is not set, no stress will be computed during the simulation for this flexible body, and you will not be able to post-process them. |
| `nlfe_strain` | Yes, No | This option controls the strain output to the Nastran result file (.op2 file) during the simulation. If this option is not set, no strains will be computed during the simulation for this flexible body, and you will not be able to post-process them. |
| `select_loads` | integer_number | Specifies the list of load case ids that are to be selected in the BDF file that will be sent to the Nastran Solver during simulation. |
| `number_of_threads` | Integer_number >= 0 | Specifies the number of threads to be used on each nonlinear flexible body individually. |
| `buffer_size` | b_auto, b_8193, b_16385, b_32769, b_65537 | Specifies the number of words in a physical record. If "b_auto" is selected, then the Buffer Size is computed internally based upon the degrees of freedom of the Non-Linear flexible body. See Extended Definition for more details. |

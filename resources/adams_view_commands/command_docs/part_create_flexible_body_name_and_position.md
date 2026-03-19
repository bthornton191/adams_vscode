# part create flexible_body name_and_position

Allows you to create or modify a flexible body. You specify a modal neutral file (MNF) or a Nastran MD DB file or a Nastran Bulk Data File (BDF), and Adams View creates the necessary Adams View geometry for displaying the flexible body. It also creates a mesh on the flexible body representing the flexible body nodes.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `flexible_body_name` | New Flex Body | Specifies the name of the flexible body to be created or modified |
| `adams_id` | Integer | Assigns a unique ID number to the part. |
| `comments` | String | Adds comments about the part to help you manage and identify it. |
| `view_name` | Existing View | Specifies the view in which to display the part. You may identify a view by typing its name or by picking it from the screen. In most cases, you can enter the special view name all, which means, all the views currently displayed. |
| `modal_neutral_file_name` | String | This parameter is mutually exclusive to the MD DB and BDF file arguments. Specifies the name of the MNF. |
| `md_db_file_name` | String | This parameter is mutually exclusive to the MNF and BDF file arguments. Specifies the name of the MD DB file to create one or more flex bodies. |
| `bdf_file_name` | String | This parameter is mutually exclusive to the MNF and MD DB file arguments. Specifies the name of the Nastran BDF. |
| `unit_of_length` | String | Specifies the length unit of data contained in the BDF if not explicitly specified in the BDF. A valid length unit option is km, m, cm, mm, mi, ft, in, um, nm, ang, yd, mil, or uin. |
| `unit_of_mass` | String | Specifies the mass unit of data contained in the BDF if not explicitly specified in the BDF. A valid mass unit option is kg, lbm, slug, gram, ozm, klbm, mgg, sinch, ug, ng, or uston. |
| `unit_of_force` | String | Specifies the force unit of data contained in the BDF if not explicitly specified in the BDF. A valid force unit option is n, lbf, kgf, ozf, dyne, kn, klbf, mn, un, or nn. |
| `unit_of_time` | String | Specifies the time unit of data contained in the BDF if not explicitly specified in the BDF. A valid time unit option is h, min, s, ms, us, nanosec, or d. |
| `index_in_database` | Integer | The parameter applies only, when the user is creating a flexible body out of the MD DB. The parameter specifies the index of the flexible body in the specified MD DB. The parameter is optional. If not specified, it is assumed to have the value 1. |
| `matrices` | Existing Matrix | Specifies the names of seventeen matrices for the modal representation of the flexible body. |
| `damping_ratio` | Function | Specifies the damping ratio to be used. |
| `damping_routine` | String | Specifies the path to user-written subroutine to be used to define modal damping. |
| `generalized_damping` | Off, full, internal_only | Sets generalized damping: |
| `dynamic_limit` | Real | Specifies the threshold frequency for quasi-static modes. |
| `location` | Location | Specifies x, y, and z coordinates defining the flexible body's location in a given reference frame defined in the parameter relative_to. |
| `orientation` | Orientation | Specifies the orientation method |
| `along_axis_orientation` | Location | Specifies the orientation method. |
| `in_plane_orientation` | Location | Specifies the in_plane orientation method |
| `relative_to` | Existing Model, Part or Marker | Specifies a reference frame relative to which the location and orientation are defined. Leave blank or enter model name to use the global coordinate system. |
| `exact_coordinates` | X, Y, Z, PSI, THETA,PHI, NONE, ALL | Specifies as many as six part coordinates that Adams View is not to change as it solves for the initial conditions. |
| `invariants` | Yes, No | Lists nine on/off values used to control the invariants |
| `characteristic_length` | Real | Specifies the characteristic length of the flexible body for linear limit check. This should be in the model length unit. The linear limit is defined as 10% of this length. |
| `representation` | RIGID, MODAL, NFORCE, NONE | Specifies the representation of the flexible body and if it is eligible for runtime type switching between MODAL (linear) and RIGID representation during a simulation. If MODAL, the flex body will be treated as a linear flex body initially and can be switched to rigid body using the FLEX_BODY Solver command. If RIGID, the flex body will be treated as a rigid body initially and can be switched to linear flexible formulation during the simulation. These two options provide dual representation capability of the flex body during the simulation.If representation is NFORCE, NONE or not specified, the flex body is not eligible for runtime switching.If NFORCE, the flex body's modal representation is Simplified. Its modal representation is converted to a semi-equivalent multi_point_force representation with rigid_body. The stiffness and damping matrix of the multi_point_force is derived from the modal stiffness matrix and modal damping settings. The properties of the rigid_body are derived from the mass invariants of the flexible_body. |
| `stability_factor` | Real | Specifies the amount of damping needed to add to the quasi-static modes to stabilize the simulation. |

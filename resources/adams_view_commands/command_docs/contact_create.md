# contact create

Allows you to create a contact force between two geometries. You will need to specify the two parts/geometries/flexible bodies using their marker, geometry or flexible body names.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `contact_name` | A New Contact | Specifies the name of the contact to be created. |
| `adams_id` | Integer | If this ID is not entered, Adams View will automatically create an Adams ID for the contact. |
| `comments` | String | Enters any relevant comments to describe the contact. |
| `type` | String | Specifies contact type as: |
| `i_marker_name` | An Existing Marker | Either the I marker or the I geometry name needs to be specified to indicate the geometry participating in the contact. |
| `i_geometry_name` | An Existing Geometry | Specifies the name of the geometry participating in the contact. |
| `j_geometry_name` | An Existing Geometry | Specifies the name of the other geometry participating in the contact. |
| `i_flex` | An Existing Flexible Body | Specifies the name of the first flexible body participating in the contact. This parameter should be used only with Adams Solver (C++). |
| `j_flex` | An Existing Flexible Body | Specifies the name of the other flexible body participating in the contact. This parameter can only exist if the I_flex parameter is specified and used with Adams Solver (C++). |
| `i_edge` | An Existing edge on Flexible Body | Specifies the name of the edge on the first flexible body participating in the contact. This parameter should be used only with Adams Solver C++. |
| `j_edge` | An Existing edge on Flexible Body | Specifies the name of the edge on the other flexible body participating in the contact. This parameter can only exist if the i_edge parameter is specified and used with Adams Solver C++. |
| `i_edge_index` | An Existing edge index | Specifies edge index of the first edge participating in the contact. This parameter can only exist if the i_edge parameter is specified and used with Adams Solver C++. |
| `j_edge_index` | An Existing edge index | Specifies edge index of the other edge participating in the contact. This parameter can only exist if the j_edge parameter is specified and used with Adams Solver C++. |
| `i_flip_normal` | String | Boolean value, specifying whether the normal is to be flipped or not. Takes values, Yes or No. |
| `j_flip_normal` | String | Boolean value, specifying whether the normal is to be flipped or not. Takes values, Yes or No. |
| `i_flip_geometry_name` | Existing Contact_curve | Specifies the geometry name at which the contact should be flipped on the I body. |
| `j_flip_geometry_name` | Existing Contact_curve | Specifies the geometry name at which the contact should be flipped on the J body. |
| `face_contact_bottom` | True/False | Specific to cylinder-to-cylinder contacts where one of the cylinders is using its internal surface for contact (that is, i/j_flip_normal = yes). “Bottom” face is defined as the one on which the cylinder geometry’s reference marker is located. If set to “true” then this face will enforce contact. |
| `face_contact_top` | True/False | Specific to cylinder-to-cylinder contacts where one of the cylinders is using its internal surface for contact (that is, i/j_flip_normal = yes). “Top” face is defined as the one on which the cylinder geometry’s reference marker is NOT located. If set to “true” then this face will enforce contact. |
| `geometry_routines` | String | Takes a string value |
| `stiffness` | Real | Specifies a material stiffness that you can use to calculate the normal force for the impact model. |
| `damping` | Real | Used when you specify the IMPACT model for calculating normal forces. DAMPING defines the damping properties of the contacting material. You should set the damping coefficient to about one percent of the stiffness coefficient.Range: DAMPING >0 |
| `dmax` | Real | Used when you specify the IMPACT model for calculating normal forces. Range: DMAX > 0 |
| `exponent` | Real | Used when you specify the IMPACT model for calculating normal forces. Range: EXPONENT >1 |
| `penalty` | Real | Used when you specify a restitution model for calculating normal forces. PENALTY defines the local stiffness properties between the contacting material. |
| `restitution_coefficient` | Real | The coefficient of restitution models the energy loss during contact. This field is not available when I_flex and J_flex parameters are specified. Range: 0 < RESTITUTION_COEFFICIENT < 1 |
| `normal_function` | Real | Specifies up to thirty user-defined constants to compute the contact normal force components in a user-defined subroutine |
| `normal_routine` | String | Specifies a library and a user-written subroutine in that library that calculates the contact normal force. |
| `augmented_lagrangian_formulation` | Boolean | Refines the normal force between two sets of rigid geometries that are in contact. |
| `coulomb_friction` | Real | Models friction effects at the contact locations using the Coulomb friction model to compute the frictional forces. |
| `mu_static` | Real | Specifies the coefficient of friction at a contact point when the slip velocity is smaller than the STICTION_TRANSITION_VELOCITY. Range: MU_STATIC > 0 |
| `mu_dynamic` | Real | Specifies the coefficient of friction at a contact point when the slip velocity is larger than the FRICTION_TRANSITION_VELOCITY. Range:0 < MU_DYNAMIC < MU_STATIC |
| `friction_transition_velocity` | Real | Used in the COULOMB_FRICTION model for calculating frictional forces at the contact locations. Range:FRICTION_TRANSITION_VELOCITY > STICTION_TRANSITION_VELOCITY > 0 |
| `friction_function` | Real | Specifies up to thirty user-defined constants to compute the contact friction force components in a user-defined subroutine |
| `friction_routine` | String | Specifies a library and a user-written subroutine in that library that calculates the contact friction force. |
| `no_friction` | True | Will take Boolean values of true or false, based on whether friction is present or not. |
| `stiction_transition_velocity` | Real | Used in the COULOMB_FRICTION model for calculating frictional forces at the contact locations. Range: 0 < STICTION_TRANSITION_VELOCITY < FRICTION_TRANSITION_VELOCITY |
| `stiction` | Boolean | Models friction effects at the contact locations using the Stiction and Sliding friction model to compute the frictional forces. The coefficient of friction will be Mu_static at and around zero. A max relative displacement will be used to determine when the friction force transitions from stiction to sliding friction.{off, on} |
| `max_stiction_deformation` | Real | This argument can be defined even if stiction is missing or off; This argument can be missing even if stiction = on, a default of 0.01 should be assumed in that case. |

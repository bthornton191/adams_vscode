# force modify element_like friction

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `friction_name` | An existing friction | An existing friction |
| `new_friction_name` | New friction name | New friction name |
| `adams_id` | Adams_id | Adams_id |
| `formulation` | original/lugre | Specifies the friction formulation. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `joint_name` | Existing joint name | Specifies the translational, revolute, or cylindrical joint associated with this entity. Some entities constrain motion at, or are otherwise associated with, specific joints. You use this parameter to identify that joint. |
| `yoke` | I_yoke/J_yoke | I_yoke/J_yoke |
| `mu_static` | Real | Specify a real number greater than zero. |
| `mu_dynamic` | Real | Specify a real number greater than zero. |
| `reaction_arm` | Real | Specify a real number greater than zero. |
| `friction_arm` | Real | Specify a real number greater than zero. |
| `initial_overlap` | Real | Real |
| `pin_radius` | Real | Specify a real number greater than zero. |
| `ball_radius` | Real | Specify a real number greater than zero. |
| `bending_factor` | Real | Specifies a real number greater than zero. |
| `stiction_transition_velocity` | Real | Specify a real number greater than zero. |
| `max_stiction_deformation` | Real | Specify a real number greater than zero. |
| `friction_force_preload` | Real | Specify a real number greater than or equal to zero. |
| `friction_torque_preload` | Real | Specify a real number greater than or equal to zero. |
| `max_friction_force` | Real | Specify a real number greater than zero. |
| `max_friction_torque` | Real | Specify a real number greater than zero. |
| `transition_velocity_coefficient` | Real | Specify a real number greater than zero. |
| `overlap_delta` | INCREASE, DECREASE, CONSTANT | Can take the values INCREASE, DECREASE, CONSTANT |
| `bristle_stiffness_coefficient` | Real | Specifies a real number greater than zero. |
| `damping_coefficient` | Real | Specifies a real number greater than zero. |
| `viscous_friction_coefficient` | Real | Specifies a real number greater than zero. |
| `velocity_threshold_stribeck` | Real | Specifies a real number greater than zero. |
| `decay_exponent_stribeck` | Real | Specifies a real number greater than zero. |
| `effect` | ALL, STICTION, SLIDING | Specifies the friction effect required. |
| `smooth` | Real | Specifies a real number greater than zero. |
| `torsional_moment` | On/Off | On/Off |
| `bending_moment` | On/Off | On/Off |
| `preload` | On/Off | On/Off |
| `reaction_force` | On/Off | On/Off |

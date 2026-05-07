# defaults contact

The defaults contact command is used to set the default contact force parameters used when creating new contact elements.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `augmented_lagrangian` | On/Off | Specifies whether the augmented Lagrangian contact method is used by default. |
| `normal_force` | String | Specifies the default normal force model type (e.g., impact or restitution). |
| `stiffness` | Real | Specifies the default contact stiffness coefficient. |
| `damping` | Real | Specifies the default contact damping coefficient. |
| `exponent` | Real | Specifies the default force exponent for the contact stiffness. |
| `dmax` | Length | Specifies the default penetration depth at which full damping is applied. |
| `penalty` | Real | Specifies the default penalty factor used in the augmented Lagrangian method. |
| `restitution_coefficient` | Real | Specifies the default coefficient of restitution for impact-based contact. |
| `coulomb_friction` | On/Off | Specifies whether Coulomb friction is enabled by default for contact. |
| `mu_static` | Real | Specifies the default static coefficient of friction. |
| `mu_dynamic` | Real | Specifies the default dynamic coefficient of friction. |
| `stiction_transition_velocity` | Velocity | Specifies the default velocity at which the transition from static to dynamic friction begins. |
| `friction_transition_velocity` | Velocity | Specifies the default velocity at which the full dynamic friction coefficient is applied. |

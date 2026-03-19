# constraint modify higher_pair_contact curve_curve

Allows you to modify a curve_curve constraint.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `curve_curve_name` | New ccurve | Specifies the name of an existing curve_curve |
| `new_curve_curve_name` | New ccurve name | Specifies the name of the new curve_curve. You may use this name later to refer to this curve_curve. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data File. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `i_curve_name` | Existing Acurve name | Specifies the name of a CURVE from which Adams constructs the first Curve |
| `j_curve_name` | Existing acurve | Specifies the name of a CURVE from which Adams constructs the second curve. |
| `i_ref_marker_name` | Existing marker | Specifies the name of a fixed MARKER on the part containing I_CURVE. |
| `j_ref_marker_name` | Existing marker | Specifies the name of a fixed MARKER on the part containing J_CURVE. |
| `i_floating_marker_name` | Existing marker | Specify an existing floating marker. |
| `j_floating_marker_name` | Existing marker | Specify an existing floating marker. |
| `i_displacement_ic` | Length | Specifies the initial point of contact on the first curve. |
| `j_displacement_ic` | Length | Specifies the initial point of contact on the second curve. |
| `no_i_displacement_ic` | True | Specifies that if an I_DISPLACEMENT_IC has been set via any means, to "UNSET" the displacement initial condition. |
| `no_j_displacement_ic` | True | Specifies that if an J_DISPLACEMENT_IC has been set via any means, to "UNSET" the displacement initial condition. |
| `i_velocity_ic` | Velocity | Specifies the initial velocity of the contact point along I_CURVE. |
| `j_velocity_ic` | Velocity | Specifies the initial velocity of the contact point along J_CURVE. |
| `no_i_velocity_ic` | True | Specifies that if an I_VELOCITY_IC has been set via any means, to "UNSET" the velocity initial condition. |
| `no_j_velocity_ic` | True | Specifies that if an J_VELOCITY_IC has been set via any means, to "UNSET" the velocity initial condition. |
| `i_ic_ref_marker_name` | An existing marker | Specifies the name of a fixed MARKER defining the coordinate system in which the values for I_DISPLACEMENT_IC are defined. The I_IC_REF_MARKER must be on the same part as the I_REF_MARKER. |
| `j_ic_ref_marker_name` | An existing marker | Specifies the name of a fixed MARKER defining the co ordinate system in which the values for J_DISPLACEMENT_IC are defined. The J_IC_REF_MARKER must be on the same part as the J_REF_MARKER. |

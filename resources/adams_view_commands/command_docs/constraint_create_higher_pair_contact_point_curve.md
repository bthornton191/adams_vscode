# constraint create higher_pair_contact point_curve

Allows you to create a point_curve.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `point_curve_name` | New Pcurve | Specifies the name of the new point_curve. You may use this name later to refer to this point_curve. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `curve_name` | Existing Acurve name | Specifies the name of a CURVE that defines the contour or shape on which the fixed marker can move. |
| `i_part_name` | Existing body | Specifies the name of the part which will have a point location constrained to lie on the curve defined by CURVE and REF_MARKER. |
| `location` | Location | Specifies the point location on the i part that will be constrained to lie on the curve defined by CURVE and REF_MARKER. |
| `relative_to` | Existing part, body or marker | Specifies the coordinate system that location coordinates and orientation angles are with respect to. |
| `i_marker_name` | Existing marker name | Specifies the name of a fixed MARKER that Adams constrains to lie on the curve defined by CURVE and REF_MARKER. |
| `j_floating_marker_name` | Existing floating marker name | Specify an existing floating marker name. |
| `j_marker_id` | Integer | Specifies the Adams ID for the floating marker which is automatically created on the J part by Adams View. This allows you to reference the floating marker in a request or function by the id you specify, instead of letting Adams View generate one. |
| `ref_marker_name` | Existing marker | Specifies the name of a MARKER fixed on the part containing the curve on which the I_MARKER must move. |
| `displacement_ic` | Length | Specifies the initial point of contact on the curve. |
| `no_displacement_ic` | true | Specifies that if a DISPLACEMENT_IC has been set via any means, to "UNSET" the displacement initial condition. |
| `velocity_ic` | Velocity | Specifies the initial tangential velocity of the I_MARKER along the curve. |
| `no_velocity_ic` | True | Specifies that if a VELOCITY_IC has been set via any means, to "UNSET" the velocity initial condition. |
| `ic_ref_marker_name` | Existing marker | Specifies the name of a the fixed MARKER defining the coordinate system in which the values for DISPLACEMENT_IC values are specified. |

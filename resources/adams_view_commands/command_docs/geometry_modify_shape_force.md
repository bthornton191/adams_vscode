# geometry modify shape force

Allows you to modify a force graphic on an element. Force graphics are arrows whose magnitudes and directions reflect the scaled relative magnitudes and directions of the force vectors acting on your model during a simulation.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `force_name` | Existing Force Symbol | Specifies the name of the force graphic to be modified |
| `new_force_name` | New Name For Force Symbol | Specifies the new name of the force symbol. |
| `adams_id` | Integer | Specifies a new name for the geometry. Assigns a unique ID number to the geometry. |
| `comments` | String | Adds comments about the geometry to help you manage and identify it. |
| `force_element_name` | Existing Force | Specifies the name of the force element whose force is to be displayed by the force graphic. |
| `joint_name` | Existing Joint | Specifies the name of the joint element whose force is to be displayed by the force graphic. |
| `jprim_name` | Existing Primitive Joint | Specifies the name of the joint primitive element whose force the force graphic is to be displayed. |
| `curve_curve_name` | Existing Ccurve | Specifies the name of the curve_curve element whose force the force graphic is to be displayed. |
| `point_curve_name` | Existing Pcurve | Specifies the name of the point_curve element whose force the force graphic is to be displayed. |
| `all_force_elements` | True | Specifies that all the forces from all the force elements acting on the marker that applied_at_marker_name specifies are summed together to determine the force that the force graphic displays. The only value allowed is true. There must be at least one force element acting on the marker. |
| `applied_at_marker_name` | Existing Triad | Specifies the name of the marker where Adams View displays the force graphic. |

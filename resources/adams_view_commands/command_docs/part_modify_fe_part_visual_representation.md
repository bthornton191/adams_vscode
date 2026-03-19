# part modify fe_part visual_representation

Allows you to modify the parameters associated with the animation of a FE Part.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `fe_part_name` | string | Specifies the name of the fe part to be modified. |
| `datum_node` | Existing fe_node | Deformation is computed as the relative displacement of the shell locations on the fe_part from the datum_node. By default the fe_node with s=0 is treated as the datum_node. The datum_node can be changed by selecting any fe_node that lies on the fe_part. |
| `contour_plots` | yes/no | Specify YES if the animation should be viewed as a contour plot, NO otherwise. |

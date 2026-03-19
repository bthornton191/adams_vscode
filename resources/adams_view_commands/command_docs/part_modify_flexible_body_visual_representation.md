# part modify flexible_body visual_representation

Allows you to change the amount by which Adams Flex deforms a mode. You can exaggerate deformations so you can see deformations that might otherwise be too subtle to see, or you can limit the deformations. The default scale factor is 1.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `flexible_body_name` | Existing Flex Body | Specifies the flexible body that needs to be modified. |
| `scale_factor` | Real | Specifies the amount by which the deformations should be exaggerated. |
| `color_contours` | Off/On/by_deformation | Specifies whether this has to be turned On,Off or by_deformation. |
| `mnf_graphics` | Yes/No | Specifies ON to turn on the viewing of the full MNF graphics; OFF to turn off the viewing. |
| `outline_graphics` | Yes/No | Specifies ON to see the outline graphics. |
| `datum_node_for_deformation` | Integer | Set the datum node for which you want deformation color changes to be relative to using Adams Flex. |
| `contour_plots` | Yes/no | You can select to animate the deformations, modal forces (MFORCEs), or the stresses and strain acting on the flexible body as contour or vector plots or both. Specify YES if the animation should be viewed as a contour plot, NO otherwise. |
| `vector_plots` | Yes/No | You can select to animate the deformations, modal forces (MFORCEs), or the stresses and strain acting on the flexible body as contour or vector plots or both. Specify YES if the animation should be viewed as a contour plot, NO otherwise. |
| `mode_filter` | None/ Deformation/ Percentage/ Frequency | Select a filter type, as explained in the extended definition. |
| `filter_value` | Real | Enter the frequency, minimum displacement, or percentage for the specified filter. |
| `render` | Flat/ Smooth/ Precision | Set the flexible body rendering to flat, smooth or precision. |

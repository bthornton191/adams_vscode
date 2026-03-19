# graphic_results deformed_mode_shape

Allows you to display the model at maximum deformation from the operating point of the requested natural frequency of the EIGEN_SOLUTION.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `eigen_solution_name` | An Existing Eigen | Specifies an existing eigen_solution.You may identify an eigen_solution by typing its name. |
| `view_name` | An Existing View | Specifies an existing view |
| `mode_number` | Integer | Specifies which mode shape of the EIGEN_SOLUTION is to be used to calculate the deformation of the model. |
| `frequency` | Real | The FREQUENCY parameter is used to determine which mode shape of the EIGEN_SOLUTION is to be used to calculate the deformation of the model. |
| `translation_maximum` | Length | Specifies the maximum amount the parts will translate from their undeformed position. |
| `rotation_maximum` | Angle | Specifies the maximum amount the parts are allowed to rotate from their undeformed position. |
| `display_undeformed_shape` | Boolean | Specifies whether the undeformed model is to be displayed with the deformed shape superimposed on top of it. YES indicates that the undeformed model will be displayed. |
| `color_of_undeformed_shape` | An Existing Color | Specifies the color of the undeformed model. If no color is specified, the undeformed model will be displayed with the same color as the deformed mode. |

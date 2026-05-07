# numeric_results create modal_polyline

Allows you to create a modal polyline from eigensolution data for visualization of mode shapes.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `polyline_name` | An Existing Polyline | Specifies the polyline to use for the modal visualization. |
| `vertex` | Integer | Specifies the vertex index on the polyline used as the reference point for the mode shape. |
| `linear_state_equation_name` | An Existing Linear State Equation | Specifies the linear state equation data set containing the eigensolution. |
| `general_state_equation_name` | An Existing General State Equation | Specifies the general state equation data set containing the eigensolution. |
| `matrix_name` | An Existing Matrix | Specifies the matrix containing the mode shape data. |
| `relative_to` | An Existing Model, Part Or Marker | Specifies the coordinate system for the mode shape visualization. |
| `x_component` | Integer | Specifies the state vector index used as the X displacement component. |
| `y_component` | Integer | Specifies the state vector index used as the Y displacement component. |
| `z_component` | Integer | Specifies the state vector index used as the Z displacement component. |
| `eigen_solution_name` | An Existing Eigensolution | Specifies the eigensolution data from which the mode is taken. |
| `mode_number` | Integer | Specifies the mode number to visualize. |
| `frequency` | Frequency | Specifies the frequency of the mode shape animation. |
| `frames_per_cycle` | Integer | Specifies the number of animation frames per cycle of the mode shape. |
| `translation_maximum` | Length | Specifies the maximum translational displacement amplitude for the mode shape animation. |
| `rotation_maximum` | Angle | Specifies the maximum rotational displacement amplitude for the mode shape animation. |
| `show_time_decay` | Boolean | Specifies whether time decay is shown in the mode shape animation. |

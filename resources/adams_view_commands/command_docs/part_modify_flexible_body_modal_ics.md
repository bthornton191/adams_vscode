# part modify flexible_body modal_ics

Allows you to set the initial conditions parameters on a flexible body, including the selected modes, the initial displacements and velocities and the modal exact coordinates for selected modes.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `flexible_body_name` | Existing flex_body | Specifies the name of the flexible body |
| `selected_modes` | Real | Specifies which modes to include when computing the modal integrals for use by Adams Solver. |
| `initial_modal_displacements` | real | Specifies the initial displacements for the selected modes. |
| `initial_modal_velocities` | Real | Specifies the initial velocities for the selected modes. |
| `modal_exact_coordinates` | Integer | Specifies integers that correspond to the modal coordinates you want held exact during initial conditions displacement analysis. |
| `set_ic_modes` | Integer | Specifies a list of modes to use when setting modal_IC_displacement or modal_IC_velocities. |
| `modal_ic_displacements` | Real | Specifies a displacement IC to use for the modes specified in set_IC_modes. |
| `modal_ic_velocities` | Real | Specifies a velocity to use for the modes specified in set_IC_modes. |

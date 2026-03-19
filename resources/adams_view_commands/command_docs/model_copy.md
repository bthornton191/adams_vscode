# model copy

Allows you to create a replica model.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_name` | An Existing Model | Specifies an existing model |
| `new_model_name` | A New Model | Specifies the name of the new model. You may use this name later to refer to this model. |
| `analysis_name` | An Existing Analysis | Specifies the name of an analysis. |
| `frame_number` | Integer | Specifies the frame number (Adams simulation output time step) at which to configure the new model. |
| `time` | Time | Allows you to identify the frame number (Adams simulation output time step) at which to configure the new model. |
| `view_name` | An Existing View | Specifies the view in which to display this model. |
| `include_contact_steps` | Integer | Integer |
| `more_results` | Boolean | Set to "yes" or "no". If unspecified, Adams View will assume "no". In addition to the positions of bodies, nearly all the states of the model at the output step of "time" for "analysis_name" will be applied as initial conditions in the ensuing model. For example, displacements and velocities of bodies, values of state variables and initial loads of force elements will be defined as initial conditions in the new model. The following entities' states are preserved when using this argument. body, gse, lse, differential_equation, motion, joint, pcurve, ccurve, marker, general_force, force_vector, torque_vector, single_component_force, modal_force, gcon, variable, request, sensor, ude_instanceTo learn more, see Saving a Simulation State as New Model. |
| `index_time` | Boolean | Set to "yes" or "no". If unspecified, Adams View will assume "no". Time variables in Adams Solver (aka, "runtime") functions will shift to the value specified in the "time" argument. |

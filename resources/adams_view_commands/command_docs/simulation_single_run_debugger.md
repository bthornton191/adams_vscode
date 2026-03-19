# simulation single_run debugger

Provides both graphical and tabular feedback on how hard Adams View is working to simulate your model. For example, during a simulation, the Simulation Debugger provides a table of those objects with the greatest simulation error.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `enable_debugger` | On_off | Enables or disables the debugger |
| `track_model_element` | Ssim_element | Sets the track |
| `show_table` | Boolean | Shows/hides the debug table |
| `highlight_objects` | Boolean | Highlights (or turns highlighting off for) those objects experiencing the most error or the most change, force, or acceleration, depending on the element you select to track |
| `step_size_measure` | On_off | Displays the integrator step size (units of model time), as the simulation progresses, on a logarithmic scale. |
| `iterations_per_step_measure` | On_off | Displays the number of iterations that Adams Solver needed to successfully progress to the next integration time step, over the course of a simulation |
| `integrator_order_measure` | On_off | Displays the order of the polynomial that Adams Solver uses during the predictor phase of integration. |
| `static_imbalance_measure` | On_off | Displays the current imbalance in the equilibrium equations that Adams Solver computes during a static equilibrium simulation. |

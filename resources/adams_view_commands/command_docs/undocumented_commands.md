# Undocumented Adams View Commands

These 183 commands exist in `structured.json` but have no corresponding `.md` file in `command_docs/`.
Adding a `<command_name>.md` file (using underscores in place of spaces) will automatically enable hover documentation for that command — no code changes needed.

## Assembly (15)
- `assembly attributes`
- `assembly auto_connect`
- `assembly build`
- `assembly connect`
- `assembly copy`
- `assembly create definition`
- `assembly create instance`
- `assembly delete`
- `assembly disassemble`
- `assembly disconnect`
- `assembly modify definition`
- `assembly modify instance`
- `assembly replace instance`
- `assembly replace type_of_instance`
- `assembly sync`

## Colors (2)
- `colors create`
- `colors modify`

## Constraint (6)
- `constraint create joint rigid`
- `constraint create primitive_joint point_point`
- `constraint modify joint convel`
- `constraint modify joint rigid`
- `constraint modify primitive_joint at_point`
- `constraint modify primitive_joint inline`

## Defaults (16)
- `defaults animation_settings`
- `defaults contact`
- `defaults container`
- `defaults file_cache_purge`
- `defaults function_references`
- `defaults graphics`
- `defaults icon_naming`
- `defaults interface`
- `defaults lights`
- `defaults nlfe_nastran_files`
- `defaults note_attributes`
- `defaults page_attributes`
- `defaults plot_builder`
- `defaults plotting`
- `defaults results`
- `defaults stereo`

## Executive Control (8)
- `executive_control deactivate advanced`
- `executive_control delete advanced`
- `executive_control set advanced`
- `executive_control set dynamics_parameters bdf_parameters`
- `executive_control set initial_conditions_parameters`
- `executive_control set integrator_parameters gstiff`
- `executive_control set integrator_parameters wstiff`

## File (15)
- `file adams_data_set read`
- `file cache purge`
- `file csv write`
- `file enhanced_data_set read`
- `file enhanced_data_set write`
- `file iges write`
- `file notebook new`
- `file notebook read`
- `file notebook write`
- `file python read`
- `file python write`
- `file romax read`
- `file vrml write`

## Force (7)
- `force create direct fe_load`
- `force create direct modal_force`
- `force create element_like field`
- `force create element_like translational_spring_damper`
- `force modify direct fe_load`
- `force modify direct modal_force`
- `force modify direct multi_point_force`
- `force modify direct torque_vector`

## Geometry (9)
- `geometry create shape csg`
- `geometry create shape cylinder`
- `geometry create shape face`
- `geometry create shape link`
- `geometry create shape solid`
- `geometry modify curve nurb_curve`
- `geometry modify shape csg`
- `geometry modify shape face`
- `geometry modify shape solid`

## Group (1)
- `group objects attributes`

## Interface (31)
- `interface clearance window create`
- `interface clearance window modify`
- `interface clearance window open`
- `interface clearance window update`
- `interface command_builder`
- `interface cursor warp`
- `interface data_table execute_cell`
- `interface generic`
- `interface help`
- `interface model_browser set`
- `interface model_browser show`
- `interface object_table set synthesize`
- `interface plot window set_mode`
- `interface record`
- `interface replay`
- `interface ribbon create`
- `interface ribbon display`
- `interface ribbon read`
- `interface ribbon undisplay`
- `interface standard_toolbar display`
- `interface standard_toolbar undisplay`
- `interface status_toolbar display`
- `interface status_toolbar undisplay`
- `interface tree_navigator`
- `interface wizard create`
- `interface wizard delete`
- `interface wizard display`
- `interface wizard execute`
- `interface wizard modify`
- `interface wizard page delete`
- `interface wizard page modify`
- `interface wizard save`
- `interface wizard undisplay`

## Macro (3)
- `macro begin_record`
- `macro debug`
- `macro end_record`

## Miscellaneous (2)
- `mdi gui_utl_alert_box_1`
- `multi_run_analysis create`
- `multi_run_analysis delete`
- `multi_run_analysis modify`

## Numeric Results (2)
- `numeric_results create modal_polyline`
- `numeric_results create sqrt_sum_of_the_squares`

## Optimize (8)
- `optimize constraint create`
- `optimize constraint delete`
- `optimize constraint modify`
- `optimize objective create`
- `optimize objective delete`
- `optimize objective evaluate`
- `optimize objective modify`
- `optimize simple_optimization`

## Panel (15)
- `panel set acf_twindow initial_conditions`
- `panel set acf_twindow linear_solver`
- `panel set acf_twindow mkb_matrix`
- `panel set acf_twindow nastran_export`
- `panel set acf_twindow transient_simulation`
- `panel set twindow_function _cosine_fourier_series`
- `panel set twindow_function _sine_fourier_series`
- `panel set twindow_function array_value`
- `panel set twindow_function cim`
- `panel set twindow_function contact`
- `panel set twindow_function delay`
- `panel set twindow_function dz`
- `panel set twindow_function force_vector`
- `panel set twindow_function fz`
- `panel set twindow_function haversine`
- `panel set twindow_function output_value_for_plant`
- `panel set twindow_function tx`
- `panel set twindow_function wm`
- `panel set twindow_function yaw`

## Part (11)
- `part create elastic_body`
- `part create fe_part name_position_section`
- `part create fe_part node_create`
- `part create fly_wheel`
- `part create particle`
- `part create stress_body`
- `part modify elastic_body`
- `part modify external_system initial_velocity`
- `part modify fe_part node_modify`
- `part modify fly_wheel`
- `part modify particle`
- `part modify rigid_body initial_velocity`
- `part modify stress_body`

## Plot3D / Plotcurve3D (12)
- `plot3d replace_simulation`
- `plot3d surface create`
- `plot3d surface modify`
- `plotcurve3d curve create`
- `plotcurve3d curve delete`
- `plotcurve3d curve modify`
- `plotcurve3d plot clear`
- `plotcurve3d plot create`
- `plotcurve3d plot delete`
- `plotcurve3d plot modify`

## Runtime Function (3)
- `runtime_function create`
- `runtime_function delete`
- `runtime_function modify`

## Section (1)
- `section modify`

## Simulation (1)
- `simulation multi_run update_variables`

## UDE (1)
- `ude auto_connect`

## View (1)
- `view management superimpose`

## XY Plots (6)
- `xy_plots attributes`
- `xy_plots bode magnitude_plot state_matrix_input`
- `xy_plots bode phase_plot result_set_input`
- `xy_plots fft_window create`
- `xy_plots fft_window modify`
- `xy_plots template pan`
- `xy_plots visibility`

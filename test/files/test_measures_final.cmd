!
!-------------------------- Default Units for Model ---------------------------!
!
!
defaults units  &
   length = mm  &
   angle = deg  &
   force = newton  &
   mass = kg  &
   time = sec
!
defaults units  &
   coordinate_system_type = cartesian  &
   orientation_type = body313
!
!------------------------ Default Attributes for Model ------------------------!
!
!
defaults attributes  &
   inheritance = bottom_up  &
   icon_visibility = on  &
   grid_visibility = off  &
   size_of_icons = 50.0  &
   spacing_for_grid = 1000.0
!
!------------------------------ Adams View Model ------------------------------!
!
!
model create  &
   model_name = model_1
!
!--------------------------------- Materials ----------------------------------!
!
!
material create  &
   material_name = .model_1.steel  &
   adams_id = 1  &
   youngs_modulus = 2.07E+005  &
   poissons_ratio = 0.29  &
   density = 7.801E-006
!
!-------------------------------- Rigid Parts ---------------------------------!
!
! Create parts and their dependent markers and graphics
!
!----------------------------------- ground -----------------------------------!
!
!
! ****** Ground Part ******
!
defaults model  &
   part_name = ground
!
defaults coordinate_system  &
   default_coordinate_system = .model_1.ground
!
! ****** Markers for current part ******
!
marker create  &
   marker_name = .model_1.ground.MAR_1  &
   adams_id = 1  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
part create rigid_body mass_properties  &
   part_name = .model_1.ground  &
   material_type = .model_1.steel
!
part attributes  &
   part_name = .model_1.ground  &
   name_visibility = off
!
model display  &
   model_name = model_1
!
!----------------------------------- PART_1 -----------------------------------!
!
!
defaults coordinate_system  &
   default_coordinate_system = .model_1.ground
!
part create rigid_body name_and_position  &
   part_name = .model_1.PART_1  &
   adams_id = 2  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
defaults coordinate_system  &
   default_coordinate_system = .model_1.PART_1
!
! ****** Markers for current part ******
!
marker create  &
   marker_name = .model_1.PART_1.MAR_1  &
   adams_id = 2  &
   location = 0.0, 0.0, 0.0  &
   orientation = 261.8698976458d, 0.0d, 0.0d
!
marker create  &
   marker_name = .model_1.PART_1.MAR_2  &
   adams_id = 3  &
   location = -50.0, -300.0, 0.0  &
   orientation = 261.8698976458d, 0.0d, 0.0d
!
marker create  &
   marker_name = .model_1.PART_1.cm  &
   adams_id = 4  &
   location = -25.0, -150.0, 0.0  &
   orientation = 350.537677792d, 0.0d, 0.0d
!
marker create  &
   marker_name = .model_1.PART_1.MAR_3  &
   adams_id = 5  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .model_1.PART_1.MAR_4  &
   adams_id = 6  &
   location = -50.0, -300.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
part create rigid_body mass_properties  &
   part_name = .model_1.PART_1  &
   mass = 0.0  &
   center_of_mass_marker = .model_1.PART_1.cm  &
   ixx = 0.0  &
   iyy = 0.0  &
   izz = 0.0  &
   ixy = 0.0  &
   izx = 0.0  &
   iyz = 0.0
!
! ****** Graphics for current part ******
!
geometry create shape link  &
   link_name = .model_1.PART_1.LINK_1  &
   i_marker = .model_1.PART_1.MAR_1  &
   j_marker = .model_1.PART_1.MAR_2  &
   width = 35.3553390593  &
   depth = 17.6776695297
!
part attributes  &
   part_name = .model_1.PART_1  &
   color = RED  &
   name_visibility = off
!
model display  &
   model_name = model_1
!
!----------------------------------- PART_2 -----------------------------------!
!
!
defaults coordinate_system  &
   default_coordinate_system = .model_1.ground
!
part create rigid_body name_and_position  &
   part_name = .model_1.PART_2  &
   adams_id = 3  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
defaults coordinate_system  &
   default_coordinate_system = .model_1.PART_2
!
! ****** Markers for current part ******
!
marker create  &
   marker_name = .model_1.PART_2.MAR_1  &
   adams_id = 7  &
   location = -50.0, -300.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .model_1.PART_2.cm  &
   adams_id = 8  &
   location = -50.0, -300.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .model_1.PART_2.MAR_2  &
   adams_id = 9  &
   location = -50.0, -300.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
part create rigid_body mass_properties  &
   part_name = .model_1.PART_2  &
   mass = 15.0  &
   center_of_mass_marker = .model_1.PART_2.cm  &
   ixx = 1.5E+004  &
   iyy = 1.5E+004  &
   izz = 1.5E+004  &
   ixy = 0.0  &
   izx = 0.0  &
   iyz = 0.0
!
! ****** Graphics for current part ******
!
geometry create shape ellipsoid  &
   ellipsoid_name = .model_1.PART_2.SPHERE_1  &
   center_marker = .model_1.PART_2.MAR_1  &
   x_scale_factor = 100.0  &
   y_scale_factor = 100.0  &
   z_scale_factor = 100.0
!
part attributes  &
   part_name = .model_1.PART_2  &
   color = GREEN  &
   name_visibility = off
!
model display  &
   model_name = model_1
!
!-------------------------------- Data storage --------------------------------!
!
!
!----------------------------------- Joints -----------------------------------!
!
!
constraint create joint revolute  &
   joint_name = .model_1.JOINT_1  &
   adams_id = 1  &
   i_marker_name = .model_1.PART_1.MAR_3  &
   j_marker_name = .model_1.ground.MAR_1  &
   delta_v = 1.0E-002  &
   maximum_deformation = 1.0E-002  &
   mu_dyn_rot = 0.3  &
   mu_stat_rot = 0.4  &
   max_fric_rot = 0.0  &
   preload_radial = 0.0  &
   preload_axial = 0.0  &
   inner_radius = 1.0  &
   outer_radius = 1.1
!
constraint attributes  &
   constraint_name = .model_1.JOINT_1  &
   name_visibility = off
!
constraint create joint fixed  &
   joint_name = .model_1.JOINT_2  &
   adams_id = 2  &
   i_marker_name = .model_1.PART_2.MAR_2  &
   j_marker_name = .model_1.PART_1.MAR_4
!
constraint attributes  &
   constraint_name = .model_1.JOINT_2  &
   name_visibility = off
!
!----------------------------------- Forces -----------------------------------!
!
!
!---------------------------------- Accgrav -----------------------------------!
!
!
force create body gravitational  &
   gravity_field_name = gravity  &
   x_component_gravity = 0.0  &
   y_component_gravity = -9806.65  &
   z_component_gravity = 0.0
!
!----------------------------- Analysis settings ------------------------------!
!
!
!---------------------------------- Measures ----------------------------------!
!
!
measure create object  &
   measure_name = .model_1.ADAMS_KE  &
   from_first = yes  &
   object = .model_1.PART_2  &
   characteristic = kinetic_energy  &
   component = mag_component

!
measure create function  &
   measure_name = .model_1.MY_KE  &
   function =   &
              "0.5*wz(.model_1.PART_2.cm)**2*(15*(50**2 + 300**2) + 15000)/1000"  &
   units = no_units
!
measure create computed  &
   measure_name = .model_1.PERCENT_ERROR  &
   text_of_expression =   &
                        "(100 * (.model_1.ADAMS_KE - .model_1.MY_KE) / 322.6)"  &
   units = no_units
!
measure create range  &
   measure_name = .model_1.MY_AVERAGE  &
   type = average  &
   of_measure_name = .model_1.MY_KE
!
!----------------------------- Simulation Scripts -----------------------------!
!
!
simulation script create  &
   sim_script_name = .model_1.Last_Sim  &
   commands =   &
              "simulation single_run transient type=auto_select end_time=2.0 number_of_steps=50 model_name=.model_1 initial_static=no"
!
!---------------------------- Function definitions ----------------------------!
!
!
!--------------------------- Expression definitions ---------------------------!
!
!
defaults coordinate_system  &
   default_coordinate_system = ground
!
geometry modify shape link  &
   link_name = .model_1.PART_1.LINK_1  &
   width = (35.3553390593mm)  &
   depth = (17.6776695297mm)
!
geometry modify shape ellipsoid  &
   ellipsoid_name = .model_1.PART_2.SPHERE_1  &
   x_scale_factor = (2 * 50.0mm)  &
   y_scale_factor = (2 * 50.0mm)  &
   z_scale_factor = (2 * 50.0mm)
!
material modify  &
   material_name = .model_1.steel  &
   youngs_modulus = (2.07E+011(Newton/meter**2))  &
   density = (7801.0(kg/meter**3))
!
measure modify computed  &
   measure_name = .model_1.PERCENT_ERROR  &
   text_of_expression =   &
      "(100 * (.model_1.ADAMS_KE - .model_1.MY_KE) / 322.6)"

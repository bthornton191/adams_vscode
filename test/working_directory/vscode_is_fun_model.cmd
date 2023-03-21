!
!-------------------------- Default Units for Model ---------------------------!
!
!
defaults units  &
   length = inch  &
   angle = deg  &
   force = pound_force  &
   mass = pound_mass  &
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
   size_of_icons = 1.968503937  &
   spacing_for_grid = 39.3700787402
!
!------------------------------ Adams View Model ------------------------------!
!
!
model create  &
   model_name = vscode_is_fun_model
!
view erase
!
!--------------------------------- Materials ----------------------------------!
!
!
material create  &
   material_name = .vscode_is_fun_model.steel  &
   density = 0.2818290049  &
   youngs_modulus = 3.002281171E+07  &
   poissons_ratio = 0.29
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
   default_coordinate_system = .vscode_is_fun_model.ground
!
!----------------------------------- PART_2 -----------------------------------!
!
!
defaults coordinate_system  &
   default_coordinate_system = .vscode_is_fun_model.ground
!
part create rigid_body name_and_position  &
   part_name = .vscode_is_fun_model.PART_2  &
   adams_id = 2  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
defaults coordinate_system  &
   default_coordinate_system = .vscode_is_fun_model.PART_2
!
! ****** Markers for current part ******
!
marker create  &
   marker_name = .vscode_is_fun_model.PART_2.MARKER_1  &
   adams_id = 1  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .vscode_is_fun_model.PART_2.cm  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
part create rigid_body mass_properties  &
   part_name = .vscode_is_fun_model.PART_2  &
   material_type = .vscode_is_fun_model.steel
!
! ****** Graphics for current part ******
!
geometry create shape ellipsoid  &
   ellipsoid_name = .vscode_is_fun_model.PART_2.ELLIPSOID_1  &
   center_marker = .vscode_is_fun_model.PART_2.MARKER_1  &
   x_scale_factor = 26.4102517028  &
   y_scale_factor = 26.4102517028  &
   z_scale_factor = 26.4102517028
!
part attributes  &
   part_name = .vscode_is_fun_model.PART_2  &
   color = RED  &
   name_visibility = off
!
!----------------------------- Analysis settings ------------------------------!
!
!
!--------------------------- Expression definitions ---------------------------!
!
!
defaults coordinate_system  &
   default_coordinate_system = ground
!
geometry modify shape ellipsoid  &
   ellipsoid_name = .vscode_is_fun_model.PART_2.ELLIPSOID_1  &
   x_scale_factor = (2 * 13.2051258514inch)  &
   y_scale_factor = (2 * 13.2051258514inch)  &
   z_scale_factor = (2 * 13.2051258514inch)
!
material modify  &
   material_name = .vscode_is_fun_model.steel  &
   density = (7801.0(kg/meter**3))  &
   youngs_modulus = (2.07E+11(Newton/meter**2))
!
model display  &
   model_name = vscode_is_fun_model

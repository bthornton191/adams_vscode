! CMD Version:2
! Version 2 enables expanded acceptable characters for object names.
! If unspecified, set to 1 or set to an invalid value, Adams View assumes traditional naming requirements.
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
   size_of_icons = 2000.0  &
   spacing_for_grid = 1000.0
!
!------------------------------ Adams View Model ------------------------------!
!
!
model create  &
   model_name = wind_turbine
!
view erase
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
   default_coordinate_system = .wind_turbine.ground
!
! ****** Markers for current part ******
!
marker create  &
   marker_name = .wind_turbine.ground.tower_base_mkr  &
   adams_id = 1  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.ground.tower_top_mkr  &
   adams_id = 2  &
   location = 0.0, 0.0, 8.0E+04  &
   orientation = 0.0d, 0.0d, 0.0d
!
! ****** Graphics for current part ******
!
geometry create shape frustum  &
   frustum_name = .wind_turbine.ground.tower  &
   adams_id = 3  &
   center_marker = .wind_turbine.ground.tower_base_mkr  &
   angle_extent = 360.0  &
   length = 8.0E+04  &
   top_radius = 1500.0  &
   bottom_radius = 2500.0  &
   side_count_for_body = 32  &
   segment_count_for_ends = 0
!
!---------------------------------- nacelle -----------------------------------!
!
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.ground
!
part create rigid_body name_and_position  &
   part_name = .wind_turbine.nacelle  &
   adams_id = 2  &
   location = 0.0, 0.0, 8.0E+04  &
   orientation = 0.0d, 0.0d, 0.0d
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.nacelle
!
! ****** Markers for current part ******
!
marker create  &
   marker_name = .wind_turbine.nacelle.mass_cm  &
   adams_id = 3  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.nacelle.fix_mkr  &
   adams_id = 4  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.nacelle.corner_mkr  &
   adams_id = 5  &
   location = -5000.0, -1500.0, -1500.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.nacelle.hub_axis_mkr  &
   adams_id = 6  &
   location = 5000.0, 0.0, 0.0  &
   orientation = 90.0d, 90.0d, 0.0d
!
part create rigid_body mass_properties  &
   part_name = .wind_turbine.nacelle  &
   mass = 2.5E+04  &
   center_of_mass_marker = .wind_turbine.nacelle.mass_cm  &
   ixx = 3.75E+10  &
   iyy = 2.27083E+11  &
   izz = 2.27083E+11  &
   ixy = 0.0  &
   izx = 0.0  &
   iyz = 0.0
!
! ****** Graphics for current part ******
!
geometry create shape block  &
   block_name = .wind_turbine.nacelle.nacelle_body  &
   adams_id = 1  &
   corner_marker = .wind_turbine.nacelle.corner_mkr  &
   diag_corner_coords = 1.0E+04, 3000.0, 3000.0
!
!------------------------------------ hub -------------------------------------!
!
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.ground
!
part create rigid_body name_and_position  &
   part_name = .wind_turbine.hub  &
   adams_id = 3  &
   location = 5000.0, 0.0, 8.0E+04  &
   orientation = 0.0d, 0.0d, 0.0d
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.hub
!
! ****** Markers for current part ******
!
marker create  &
   marker_name = .wind_turbine.hub.mass_cm  &
   adams_id = 7  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.hub.pin_mkr  &
   adams_id = 8  &
   location = 0.0, 0.0, 0.0  &
   orientation = 90.0d, 90.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.hub.vis_mkr  &
   adams_id = 9  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.hub.blade_1_attach_mkr  &
   adams_id = 10  &
   location = 0.0, 0.0, 2000.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.hub.blade_2_attach_mkr  &
   adams_id = 11  &
   location = 0.0, 1732.0508075689, -1000.0  &
   orientation = 180.0d, 120.0d, 180.0d
!
marker create  &
   marker_name = .wind_turbine.hub.blade_3_attach_mkr  &
   adams_id = 12  &
   location = 0.0, -1732.0508075689, -1000.0  &
   orientation = 0.0d, 120.0d, 0.0d
!
part create rigid_body mass_properties  &
   part_name = .wind_turbine.hub  &
   mass = 1.0E+04  &
   center_of_mass_marker = .wind_turbine.hub.mass_cm  &
   ixx = 1.6E+10  &
   iyy = 1.6E+10  &
   izz = 1.6E+10  &
   ixy = 0.0  &
   izx = 0.0  &
   iyz = 0.0
!
! ****** Graphics for current part ******
!
geometry create shape ellipsoid  &
   ellipsoid_name = .wind_turbine.hub.hub_sphere  &
   adams_id = 2  &
   center_marker = .wind_turbine.hub.vis_mkr  &
   x_scale_factor = 2000.0  &
   y_scale_factor = 2000.0  &
   z_scale_factor = 2000.0
!
!------------------------------- blade_1_seg_1 --------------------------------!
!
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.ground
!
part create rigid_body name_and_position  &
   part_name = .wind_turbine.blade_1_seg_1  &
   adams_id = 4  &
   location = 5000.0, 0.0, 8.45E+04  &
   orientation = 0.0d, 0.0d, 0.0d
!
part create rigid_body initial_velocity  &
   part_name = .wind_turbine.blade_1_seg_1  &
   vx = 0.0  &
   vy = -5654.8667764616  &
   vz = 0.0  &
   wx = 1.2566370614  &
   wy = 0.0  &
   wz = 0.0
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.blade_1_seg_1
!
! ****** Markers for current part ******
!
marker create  &
   marker_name = .wind_turbine.blade_1_seg_1.mass_cm  &
   adams_id = 13  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_1_seg_1.inboard_mkr  &
   adams_id = 14  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_1_seg_1.beam_mkr  &
   adams_id = 15  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 90.0d, 90.0d, 90.0d
!
part create rigid_body mass_properties  &
   part_name = .wind_turbine.blade_1_seg_1  &
   mass = 500.0  &
   center_of_mass_marker = .wind_turbine.blade_1_seg_1.mass_cm  &
   ixx = 1.04167E+09  &
   iyy = 1.04167E+09  &
   izz = 5.0625E+07  &
   ixy = 0.0  &
   izx = 0.0  &
   iyz = 0.0
!
! ****** Graphics for current part ******
!
geometry create shape frustum  &
   frustum_name = .wind_turbine.blade_1_seg_1.blade_geom  &
   adams_id = 4  &
   center_marker = .wind_turbine.blade_1_seg_1.inboard_mkr  &
   angle_extent = 360.0  &
   length = 5000.0  &
   top_radius = 675.0  &
   bottom_radius = 750.0  &
   side_count_for_body = 16  &
   segment_count_for_ends = 0
!
!------------------------------- blade_1_seg_2 --------------------------------!
!
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.ground
!
part create rigid_body name_and_position  &
   part_name = .wind_turbine.blade_1_seg_2  &
   adams_id = 5  &
   location = 5000.0, 0.0, 8.95E+04  &
   orientation = 0.0d, 0.0d, 0.0d
!
part create rigid_body initial_velocity  &
   part_name = .wind_turbine.blade_1_seg_2  &
   vx = 0.0  &
   vy = -1.1938052084E+04  &
   vz = 0.0  &
   wx = 1.2566370614  &
   wy = 0.0  &
   wz = 0.0
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.blade_1_seg_2
!
! ****** Markers for current part ******
!
marker create  &
   marker_name = .wind_turbine.blade_1_seg_2.mass_cm  &
   adams_id = 16  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_1_seg_2.inboard_mkr  &
   adams_id = 17  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_1_seg_2.beam_mkr  &
   adams_id = 18  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 90.0d, 90.0d, 90.0d
!
part create rigid_body mass_properties  &
   part_name = .wind_turbine.blade_1_seg_2  &
   mass = 500.0  &
   center_of_mass_marker = .wind_turbine.blade_1_seg_2.mass_cm  &
   ixx = 1.04167E+09  &
   iyy = 1.04167E+09  &
   izz = 5.0625E+07  &
   ixy = 0.0  &
   izx = 0.0  &
   iyz = 0.0
!
! ****** Graphics for current part ******
!
geometry create shape frustum  &
   frustum_name = .wind_turbine.blade_1_seg_2.blade_geom  &
   adams_id = 5  &
   center_marker = .wind_turbine.blade_1_seg_2.inboard_mkr  &
   angle_extent = 360.0  &
   length = 5000.0  &
   top_radius = 600.0  &
   bottom_radius = 675.0  &
   side_count_for_body = 16  &
   segment_count_for_ends = 0
!
!------------------------------- blade_1_seg_3 --------------------------------!
!
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.ground
!
part create rigid_body name_and_position  &
   part_name = .wind_turbine.blade_1_seg_3  &
   adams_id = 6  &
   location = 5000.0, 0.0, 9.45E+04  &
   orientation = 0.0d, 0.0d, 0.0d
!
part create rigid_body initial_velocity  &
   part_name = .wind_turbine.blade_1_seg_3  &
   vx = 0.0  &
   vy = -1.8221237391E+04  &
   vz = 0.0  &
   wx = 1.2566370614  &
   wy = 0.0  &
   wz = 0.0
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.blade_1_seg_3
!
! ****** Markers for current part ******
!
marker create  &
   marker_name = .wind_turbine.blade_1_seg_3.mass_cm  &
   adams_id = 19  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_1_seg_3.inboard_mkr  &
   adams_id = 20  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_1_seg_3.beam_mkr  &
   adams_id = 21  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 90.0d, 90.0d, 90.0d
!
part create rigid_body mass_properties  &
   part_name = .wind_turbine.blade_1_seg_3  &
   mass = 500.0  &
   center_of_mass_marker = .wind_turbine.blade_1_seg_3.mass_cm  &
   ixx = 1.04167E+09  &
   iyy = 1.04167E+09  &
   izz = 5.0625E+07  &
   ixy = 0.0  &
   izx = 0.0  &
   iyz = 0.0
!
! ****** Graphics for current part ******
!
geometry create shape frustum  &
   frustum_name = .wind_turbine.blade_1_seg_3.blade_geom  &
   adams_id = 6  &
   center_marker = .wind_turbine.blade_1_seg_3.inboard_mkr  &
   angle_extent = 360.0  &
   length = 5000.0  &
   top_radius = 525.0  &
   bottom_radius = 600.0  &
   side_count_for_body = 16  &
   segment_count_for_ends = 0
!
!------------------------------- blade_1_seg_4 --------------------------------!
!
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.ground
!
part create rigid_body name_and_position  &
   part_name = .wind_turbine.blade_1_seg_4  &
   adams_id = 7  &
   location = 5000.0, 0.0, 9.95E+04  &
   orientation = 0.0d, 0.0d, 0.0d
!
part create rigid_body initial_velocity  &
   part_name = .wind_turbine.blade_1_seg_4  &
   vx = 0.0  &
   vy = -2.4504422698E+04  &
   vz = 0.0  &
   wx = 1.2566370614  &
   wy = 0.0  &
   wz = 0.0
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.blade_1_seg_4
!
! ****** Markers for current part ******
!
marker create  &
   marker_name = .wind_turbine.blade_1_seg_4.mass_cm  &
   adams_id = 22  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_1_seg_4.inboard_mkr  &
   adams_id = 23  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_1_seg_4.beam_mkr  &
   adams_id = 24  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 90.0d, 90.0d, 90.0d
!
part create rigid_body mass_properties  &
   part_name = .wind_turbine.blade_1_seg_4  &
   mass = 500.0  &
   center_of_mass_marker = .wind_turbine.blade_1_seg_4.mass_cm  &
   ixx = 1.04167E+09  &
   iyy = 1.04167E+09  &
   izz = 5.0625E+07  &
   ixy = 0.0  &
   izx = 0.0  &
   iyz = 0.0
!
! ****** Graphics for current part ******
!
geometry create shape frustum  &
   frustum_name = .wind_turbine.blade_1_seg_4.blade_geom  &
   adams_id = 7  &
   center_marker = .wind_turbine.blade_1_seg_4.inboard_mkr  &
   angle_extent = 360.0  &
   length = 5000.0  &
   top_radius = 450.0  &
   bottom_radius = 525.0  &
   side_count_for_body = 16  &
   segment_count_for_ends = 0
!
!------------------------------- blade_1_seg_5 --------------------------------!
!
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.ground
!
part create rigid_body name_and_position  &
   part_name = .wind_turbine.blade_1_seg_5  &
   adams_id = 8  &
   location = 5000.0, 0.0, 1.045E+05  &
   orientation = 0.0d, 0.0d, 0.0d
!
part create rigid_body initial_velocity  &
   part_name = .wind_turbine.blade_1_seg_5  &
   vx = 0.0  &
   vy = -3.0787608005E+04  &
   vz = 0.0  &
   wx = 1.2566370614  &
   wy = 0.0  &
   wz = 0.0
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.blade_1_seg_5
!
! ****** Markers for current part ******
!
marker create  &
   marker_name = .wind_turbine.blade_1_seg_5.mass_cm  &
   adams_id = 25  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_1_seg_5.inboard_mkr  &
   adams_id = 26  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_1_seg_5.beam_mkr  &
   adams_id = 27  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 90.0d, 90.0d, 90.0d
!
part create rigid_body mass_properties  &
   part_name = .wind_turbine.blade_1_seg_5  &
   mass = 500.0  &
   center_of_mass_marker = .wind_turbine.blade_1_seg_5.mass_cm  &
   ixx = 1.04167E+09  &
   iyy = 1.04167E+09  &
   izz = 5.0625E+07  &
   ixy = 0.0  &
   izx = 0.0  &
   iyz = 0.0
!
! ****** Graphics for current part ******
!
geometry create shape frustum  &
   frustum_name = .wind_turbine.blade_1_seg_5.blade_geom  &
   adams_id = 8  &
   center_marker = .wind_turbine.blade_1_seg_5.inboard_mkr  &
   angle_extent = 360.0  &
   length = 5000.0  &
   top_radius = 375.0  &
   bottom_radius = 450.0  &
   side_count_for_body = 16  &
   segment_count_for_ends = 0
!
!------------------------------- blade_1_seg_6 --------------------------------!
!
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.ground
!
part create rigid_body name_and_position  &
   part_name = .wind_turbine.blade_1_seg_6  &
   adams_id = 9  &
   location = 5000.0, 0.0, 1.095E+05  &
   orientation = 0.0d, 0.0d, 0.0d
!
part create rigid_body initial_velocity  &
   part_name = .wind_turbine.blade_1_seg_6  &
   vx = 0.0  &
   vy = -3.7070793312E+04  &
   vz = 0.0  &
   wx = 1.2566370614  &
   wy = 0.0  &
   wz = 0.0
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.blade_1_seg_6
!
! ****** Markers for current part ******
!
marker create  &
   marker_name = .wind_turbine.blade_1_seg_6.mass_cm  &
   adams_id = 28  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_1_seg_6.inboard_mkr  &
   adams_id = 29  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_1_seg_6.beam_mkr  &
   adams_id = 30  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 90.0d, 90.0d, 90.0d
!
part create rigid_body mass_properties  &
   part_name = .wind_turbine.blade_1_seg_6  &
   mass = 500.0  &
   center_of_mass_marker = .wind_turbine.blade_1_seg_6.mass_cm  &
   ixx = 1.04167E+09  &
   iyy = 1.04167E+09  &
   izz = 5.0625E+07  &
   ixy = 0.0  &
   izx = 0.0  &
   iyz = 0.0
!
! ****** Graphics for current part ******
!
geometry create shape frustum  &
   frustum_name = .wind_turbine.blade_1_seg_6.blade_geom  &
   adams_id = 9  &
   center_marker = .wind_turbine.blade_1_seg_6.inboard_mkr  &
   angle_extent = 360.0  &
   length = 5000.0  &
   top_radius = 300.0  &
   bottom_radius = 375.0  &
   side_count_for_body = 16  &
   segment_count_for_ends = 0
!
!------------------------------- blade_1_seg_7 --------------------------------!
!
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.ground
!
part create rigid_body name_and_position  &
   part_name = .wind_turbine.blade_1_seg_7  &
   adams_id = 10  &
   location = 5000.0, 0.0, 1.145E+05  &
   orientation = 0.0d, 0.0d, 0.0d
!
part create rigid_body initial_velocity  &
   part_name = .wind_turbine.blade_1_seg_7  &
   vx = 0.0  &
   vy = -4.335397862E+04  &
   vz = 0.0  &
   wx = 1.2566370614  &
   wy = 0.0  &
   wz = 0.0
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.blade_1_seg_7
!
! ****** Markers for current part ******
!
marker create  &
   marker_name = .wind_turbine.blade_1_seg_7.mass_cm  &
   adams_id = 31  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_1_seg_7.inboard_mkr  &
   adams_id = 32  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_1_seg_7.beam_mkr  &
   adams_id = 33  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 90.0d, 90.0d, 90.0d
!
part create rigid_body mass_properties  &
   part_name = .wind_turbine.blade_1_seg_7  &
   mass = 500.0  &
   center_of_mass_marker = .wind_turbine.blade_1_seg_7.mass_cm  &
   ixx = 1.04167E+09  &
   iyy = 1.04167E+09  &
   izz = 5.0625E+07  &
   ixy = 0.0  &
   izx = 0.0  &
   iyz = 0.0
!
! ****** Graphics for current part ******
!
geometry create shape frustum  &
   frustum_name = .wind_turbine.blade_1_seg_7.blade_geom  &
   adams_id = 10  &
   center_marker = .wind_turbine.blade_1_seg_7.inboard_mkr  &
   angle_extent = 360.0  &
   length = 5000.0  &
   top_radius = 225.0  &
   bottom_radius = 300.0  &
   side_count_for_body = 16  &
   segment_count_for_ends = 0
!
!------------------------------- blade_1_seg_8 --------------------------------!
!
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.ground
!
part create rigid_body name_and_position  &
   part_name = .wind_turbine.blade_1_seg_8  &
   adams_id = 11  &
   location = 5000.0, 0.0, 1.195E+05  &
   orientation = 0.0d, 0.0d, 0.0d
!
part create rigid_body initial_velocity  &
   part_name = .wind_turbine.blade_1_seg_8  &
   vx = 0.0  &
   vy = -4.9637163927E+04  &
   vz = 0.0  &
   wx = 1.2566370614  &
   wy = 0.0  &
   wz = 0.0
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.blade_1_seg_8
!
! ****** Markers for current part ******
!
marker create  &
   marker_name = .wind_turbine.blade_1_seg_8.mass_cm  &
   adams_id = 34  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_1_seg_8.inboard_mkr  &
   adams_id = 35  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_1_seg_8.beam_mkr  &
   adams_id = 36  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 90.0d, 90.0d, 90.0d
!
part create rigid_body mass_properties  &
   part_name = .wind_turbine.blade_1_seg_8  &
   mass = 500.0  &
   center_of_mass_marker = .wind_turbine.blade_1_seg_8.mass_cm  &
   ixx = 1.04167E+09  &
   iyy = 1.04167E+09  &
   izz = 5.0625E+07  &
   ixy = 0.0  &
   izx = 0.0  &
   iyz = 0.0
!
! ****** Graphics for current part ******
!
geometry create shape frustum  &
   frustum_name = .wind_turbine.blade_1_seg_8.blade_geom  &
   adams_id = 11  &
   center_marker = .wind_turbine.blade_1_seg_8.inboard_mkr  &
   angle_extent = 360.0  &
   length = 5000.0  &
   top_radius = 150.0  &
   bottom_radius = 225.0  &
   side_count_for_body = 16  &
   segment_count_for_ends = 0
!
!------------------------------- blade_2_seg_1 --------------------------------!
!
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.ground
!
part create rigid_body name_and_position  &
   part_name = .wind_turbine.blade_2_seg_1  &
   adams_id = 12  &
   location = 5000.0, 3897.11431703, 7.775E+04  &
   orientation = 180.0d, 120.0d, 180.0d
!
part create rigid_body initial_velocity  &
   part_name = .wind_turbine.blade_2_seg_1  &
   vx = 0.0  &
   vy = 2827.4333882308  &
   vz = 4897.2582834324  &
   wx = 1.2566370614  &
   wy = 0.0  &
   wz = 0.0
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.blade_2_seg_1
!
! ****** Markers for current part ******
!
marker create  &
   marker_name = .wind_turbine.blade_2_seg_1.mass_cm  &
   adams_id = 37  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_2_seg_1.inboard_mkr  &
   adams_id = 38  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_2_seg_1.beam_mkr  &
   adams_id = 39  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 90.0d, 90.0d, 90.0d
!
part create rigid_body mass_properties  &
   part_name = .wind_turbine.blade_2_seg_1  &
   mass = 500.0  &
   center_of_mass_marker = .wind_turbine.blade_2_seg_1.mass_cm  &
   ixx = 1.04167E+09  &
   iyy = 1.04167E+09  &
   izz = 5.0625E+07  &
   ixy = 0.0  &
   izx = 0.0  &
   iyz = 0.0
!
! ****** Graphics for current part ******
!
geometry create shape frustum  &
   frustum_name = .wind_turbine.blade_2_seg_1.blade_geom  &
   adams_id = 12  &
   center_marker = .wind_turbine.blade_2_seg_1.inboard_mkr  &
   angle_extent = 360.0  &
   length = 5000.0  &
   top_radius = 675.0  &
   bottom_radius = 750.0  &
   side_count_for_body = 16  &
   segment_count_for_ends = 0
!
!------------------------------- blade_2_seg_2 --------------------------------!
!
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.ground
!
part create rigid_body name_and_position  &
   part_name = .wind_turbine.blade_2_seg_2  &
   adams_id = 13  &
   location = 5000.0, 8227.2413359522, 7.525E+04  &
   orientation = 180.0d, 120.0d, 180.0d
!
part create rigid_body initial_velocity  &
   part_name = .wind_turbine.blade_2_seg_2  &
   vx = 0.0  &
   vy = 5969.0260418206  &
   vz = 1.0338656376E+04  &
   wx = 1.2566370614  &
   wy = 0.0  &
   wz = 0.0
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.blade_2_seg_2
!
! ****** Markers for current part ******
!
marker create  &
   marker_name = .wind_turbine.blade_2_seg_2.mass_cm  &
   adams_id = 40  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_2_seg_2.inboard_mkr  &
   adams_id = 41  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_2_seg_2.beam_mkr  &
   adams_id = 42  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 90.0d, 90.0d, 90.0d
!
part create rigid_body mass_properties  &
   part_name = .wind_turbine.blade_2_seg_2  &
   mass = 500.0  &
   center_of_mass_marker = .wind_turbine.blade_2_seg_2.mass_cm  &
   ixx = 1.04167E+09  &
   iyy = 1.04167E+09  &
   izz = 5.0625E+07  &
   ixy = 0.0  &
   izx = 0.0  &
   iyz = 0.0
!
! ****** Graphics for current part ******
!
geometry create shape frustum  &
   frustum_name = .wind_turbine.blade_2_seg_2.blade_geom  &
   adams_id = 13  &
   center_marker = .wind_turbine.blade_2_seg_2.inboard_mkr  &
   angle_extent = 360.0  &
   length = 5000.0  &
   top_radius = 600.0  &
   bottom_radius = 675.0  &
   side_count_for_body = 16  &
   segment_count_for_ends = 0
!
!------------------------------- blade_2_seg_3 --------------------------------!
!
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.ground
!
part create rigid_body name_and_position  &
   part_name = .wind_turbine.blade_2_seg_3  &
   adams_id = 14  &
   location = 5000.0, 1.2557368355E+04, 7.275E+04  &
   orientation = 180.0d, 120.0d, 180.0d
!
part create rigid_body initial_velocity  &
   part_name = .wind_turbine.blade_2_seg_3  &
   vx = 0.0  &
   vy = 9110.6186954104  &
   vz = 1.5780054469E+04  &
   wx = 1.2566370614  &
   wy = 0.0  &
   wz = 0.0
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.blade_2_seg_3
!
! ****** Markers for current part ******
!
marker create  &
   marker_name = .wind_turbine.blade_2_seg_3.mass_cm  &
   adams_id = 43  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_2_seg_3.inboard_mkr  &
   adams_id = 44  &
   location = 0.0, -1.4210854715E-11, -2500.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_2_seg_3.beam_mkr  &
   adams_id = 45  &
   location = 0.0, -1.4210854715E-11, -2500.0  &
   orientation = 90.0d, 90.0d, 90.0d
!
part create rigid_body mass_properties  &
   part_name = .wind_turbine.blade_2_seg_3  &
   mass = 500.0  &
   center_of_mass_marker = .wind_turbine.blade_2_seg_3.mass_cm  &
   ixx = 1.04167E+09  &
   iyy = 1.04167E+09  &
   izz = 5.0625E+07  &
   ixy = 0.0  &
   izx = 0.0  &
   iyz = 0.0
!
! ****** Graphics for current part ******
!
geometry create shape frustum  &
   frustum_name = .wind_turbine.blade_2_seg_3.blade_geom  &
   adams_id = 14  &
   center_marker = .wind_turbine.blade_2_seg_3.inboard_mkr  &
   angle_extent = 360.0  &
   length = 5000.0  &
   top_radius = 525.0  &
   bottom_radius = 600.0  &
   side_count_for_body = 16  &
   segment_count_for_ends = 0
!
!------------------------------- blade_2_seg_4 --------------------------------!
!
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.ground
!
part create rigid_body name_and_position  &
   part_name = .wind_turbine.blade_2_seg_4  &
   adams_id = 15  &
   location = 5000.0, 1.6887495374E+04, 7.025E+04  &
   orientation = 180.0d, 120.0d, 180.0d
!
part create rigid_body initial_velocity  &
   part_name = .wind_turbine.blade_2_seg_4  &
   vx = 0.0  &
   vy = 1.2252211349E+04  &
   vz = 2.1221452562E+04  &
   wx = 1.2566370614  &
   wy = 0.0  &
   wz = 0.0
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.blade_2_seg_4
!
! ****** Markers for current part ******
!
marker create  &
   marker_name = .wind_turbine.blade_2_seg_4.mass_cm  &
   adams_id = 46  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_2_seg_4.inboard_mkr  &
   adams_id = 47  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_2_seg_4.beam_mkr  &
   adams_id = 48  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 90.0d, 90.0d, 90.0d
!
part create rigid_body mass_properties  &
   part_name = .wind_turbine.blade_2_seg_4  &
   mass = 500.0  &
   center_of_mass_marker = .wind_turbine.blade_2_seg_4.mass_cm  &
   ixx = 1.04167E+09  &
   iyy = 1.04167E+09  &
   izz = 5.0625E+07  &
   ixy = 0.0  &
   izx = 0.0  &
   iyz = 0.0
!
! ****** Graphics for current part ******
!
geometry create shape frustum  &
   frustum_name = .wind_turbine.blade_2_seg_4.blade_geom  &
   adams_id = 15  &
   center_marker = .wind_turbine.blade_2_seg_4.inboard_mkr  &
   angle_extent = 360.0  &
   length = 5000.0  &
   top_radius = 450.0  &
   bottom_radius = 525.0  &
   side_count_for_body = 16  &
   segment_count_for_ends = 0
!
!------------------------------- blade_2_seg_5 --------------------------------!
!
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.ground
!
part create rigid_body name_and_position  &
   part_name = .wind_turbine.blade_2_seg_5  &
   adams_id = 16  &
   location = 5000.0, 2.1217622393E+04, 6.775E+04  &
   orientation = 180.0d, 120.0d, 180.0d
!
part create rigid_body initial_velocity  &
   part_name = .wind_turbine.blade_2_seg_5  &
   vx = 0.0  &
   vy = 1.5393804003E+04  &
   vz = 2.6662850654E+04  &
   wx = 1.2566370614  &
   wy = 0.0  &
   wz = 0.0
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.blade_2_seg_5
!
! ****** Markers for current part ******
!
marker create  &
   marker_name = .wind_turbine.blade_2_seg_5.mass_cm  &
   adams_id = 49  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_2_seg_5.inboard_mkr  &
   adams_id = 50  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_2_seg_5.beam_mkr  &
   adams_id = 51  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 90.0d, 90.0d, 90.0d
!
part create rigid_body mass_properties  &
   part_name = .wind_turbine.blade_2_seg_5  &
   mass = 500.0  &
   center_of_mass_marker = .wind_turbine.blade_2_seg_5.mass_cm  &
   ixx = 1.04167E+09  &
   iyy = 1.04167E+09  &
   izz = 5.0625E+07  &
   ixy = 0.0  &
   izx = 0.0  &
   iyz = 0.0
!
! ****** Graphics for current part ******
!
geometry create shape frustum  &
   frustum_name = .wind_turbine.blade_2_seg_5.blade_geom  &
   adams_id = 16  &
   center_marker = .wind_turbine.blade_2_seg_5.inboard_mkr  &
   angle_extent = 360.0  &
   length = 5000.0  &
   top_radius = 375.0  &
   bottom_radius = 450.0  &
   side_count_for_body = 16  &
   segment_count_for_ends = 0
!
!------------------------------- blade_2_seg_6 --------------------------------!
!
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.ground
!
part create rigid_body name_and_position  &
   part_name = .wind_turbine.blade_2_seg_6  &
   adams_id = 17  &
   location = 5000.0, 2.5547749412E+04, 6.525E+04  &
   orientation = 180.0d, 120.0d, 180.0d
!
part create rigid_body initial_velocity  &
   part_name = .wind_turbine.blade_2_seg_6  &
   vx = 0.0  &
   vy = 1.8535396656E+04  &
   vz = 3.2104248747E+04  &
   wx = 1.2566370614  &
   wy = 0.0  &
   wz = 0.0
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.blade_2_seg_6
!
! ****** Markers for current part ******
!
marker create  &
   marker_name = .wind_turbine.blade_2_seg_6.mass_cm  &
   adams_id = 52  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_2_seg_6.inboard_mkr  &
   adams_id = 53  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_2_seg_6.beam_mkr  &
   adams_id = 54  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 90.0d, 90.0d, 90.0d
!
part create rigid_body mass_properties  &
   part_name = .wind_turbine.blade_2_seg_6  &
   mass = 500.0  &
   center_of_mass_marker = .wind_turbine.blade_2_seg_6.mass_cm  &
   ixx = 1.04167E+09  &
   iyy = 1.04167E+09  &
   izz = 5.0625E+07  &
   ixy = 0.0  &
   izx = 0.0  &
   iyz = 0.0
!
! ****** Graphics for current part ******
!
geometry create shape frustum  &
   frustum_name = .wind_turbine.blade_2_seg_6.blade_geom  &
   adams_id = 17  &
   center_marker = .wind_turbine.blade_2_seg_6.inboard_mkr  &
   angle_extent = 360.0  &
   length = 5000.0  &
   top_radius = 300.0  &
   bottom_radius = 375.0  &
   side_count_for_body = 16  &
   segment_count_for_ends = 0
!
!------------------------------- blade_2_seg_7 --------------------------------!
!
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.ground
!
part create rigid_body name_and_position  &
   part_name = .wind_turbine.blade_2_seg_7  &
   adams_id = 18  &
   location = 5000.0, 2.9877876431E+04, 6.275E+04  &
   orientation = 180.0d, 120.0d, 180.0d
!
part create rigid_body initial_velocity  &
   part_name = .wind_turbine.blade_2_seg_7  &
   vx = 0.0  &
   vy = 2.167698931E+04  &
   vz = 3.754564684E+04  &
   wx = 1.2566370614  &
   wy = 0.0  &
   wz = 0.0
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.blade_2_seg_7
!
! ****** Markers for current part ******
!
marker create  &
   marker_name = .wind_turbine.blade_2_seg_7.mass_cm  &
   adams_id = 55  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_2_seg_7.inboard_mkr  &
   adams_id = 56  &
   location = 0.0, -1.4210854715E-11, -2500.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_2_seg_7.beam_mkr  &
   adams_id = 57  &
   location = 0.0, -1.4210854715E-11, -2500.0  &
   orientation = 90.0d, 90.0d, 90.0d
!
part create rigid_body mass_properties  &
   part_name = .wind_turbine.blade_2_seg_7  &
   mass = 500.0  &
   center_of_mass_marker = .wind_turbine.blade_2_seg_7.mass_cm  &
   ixx = 1.04167E+09  &
   iyy = 1.04167E+09  &
   izz = 5.0625E+07  &
   ixy = 0.0  &
   izx = 0.0  &
   iyz = 0.0
!
! ****** Graphics for current part ******
!
geometry create shape frustum  &
   frustum_name = .wind_turbine.blade_2_seg_7.blade_geom  &
   adams_id = 18  &
   center_marker = .wind_turbine.blade_2_seg_7.inboard_mkr  &
   angle_extent = 360.0  &
   length = 5000.0  &
   top_radius = 225.0  &
   bottom_radius = 300.0  &
   side_count_for_body = 16  &
   segment_count_for_ends = 0
!
!------------------------------- blade_2_seg_8 --------------------------------!
!
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.ground
!
part create rigid_body name_and_position  &
   part_name = .wind_turbine.blade_2_seg_8  &
   adams_id = 19  &
   location = 5000.0, 3.4208003449E+04, 6.025E+04  &
   orientation = 180.0d, 120.0d, 180.0d
!
part create rigid_body initial_velocity  &
   part_name = .wind_turbine.blade_2_seg_8  &
   vx = 0.0  &
   vy = 2.4818581963E+04  &
   vz = 4.2987044932E+04  &
   wx = 1.2566370614  &
   wy = 0.0  &
   wz = 0.0
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.blade_2_seg_8
!
! ****** Markers for current part ******
!
marker create  &
   marker_name = .wind_turbine.blade_2_seg_8.mass_cm  &
   adams_id = 58  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_2_seg_8.inboard_mkr  &
   adams_id = 59  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_2_seg_8.beam_mkr  &
   adams_id = 60  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 90.0d, 90.0d, 90.0d
!
part create rigid_body mass_properties  &
   part_name = .wind_turbine.blade_2_seg_8  &
   mass = 500.0  &
   center_of_mass_marker = .wind_turbine.blade_2_seg_8.mass_cm  &
   ixx = 1.04167E+09  &
   iyy = 1.04167E+09  &
   izz = 5.0625E+07  &
   ixy = 0.0  &
   izx = 0.0  &
   iyz = 0.0
!
! ****** Graphics for current part ******
!
geometry create shape frustum  &
   frustum_name = .wind_turbine.blade_2_seg_8.blade_geom  &
   adams_id = 19  &
   center_marker = .wind_turbine.blade_2_seg_8.inboard_mkr  &
   angle_extent = 360.0  &
   length = 5000.0  &
   top_radius = 150.0  &
   bottom_radius = 225.0  &
   side_count_for_body = 16  &
   segment_count_for_ends = 0
!
!------------------------------- blade_3_seg_1 --------------------------------!
!
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.ground
!
part create rigid_body name_and_position  &
   part_name = .wind_turbine.blade_3_seg_1  &
   adams_id = 20  &
   location = 5000.0, -3897.11431703, 7.775E+04  &
   orientation = 0.0d, 120.0d, 0.0d
!
part create rigid_body initial_velocity  &
   part_name = .wind_turbine.blade_3_seg_1  &
   vx = 0.0  &
   vy = 2827.4333882308  &
   vz = -4897.2582834324  &
   wx = 1.2566370614  &
   wy = 0.0  &
   wz = 0.0
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.blade_3_seg_1
!
! ****** Markers for current part ******
!
marker create  &
   marker_name = .wind_turbine.blade_3_seg_1.mass_cm  &
   adams_id = 61  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_3_seg_1.inboard_mkr  &
   adams_id = 62  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_3_seg_1.beam_mkr  &
   adams_id = 63  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 90.0d, 90.0d, 90.0d
!
part create rigid_body mass_properties  &
   part_name = .wind_turbine.blade_3_seg_1  &
   mass = 500.0  &
   center_of_mass_marker = .wind_turbine.blade_3_seg_1.mass_cm  &
   ixx = 1.04167E+09  &
   iyy = 1.04167E+09  &
   izz = 5.0625E+07  &
   ixy = 0.0  &
   izx = 0.0  &
   iyz = 0.0
!
! ****** Graphics for current part ******
!
geometry create shape frustum  &
   frustum_name = .wind_turbine.blade_3_seg_1.blade_geom  &
   adams_id = 20  &
   center_marker = .wind_turbine.blade_3_seg_1.inboard_mkr  &
   angle_extent = 360.0  &
   length = 5000.0  &
   top_radius = 675.0  &
   bottom_radius = 750.0  &
   side_count_for_body = 16  &
   segment_count_for_ends = 0
!
!------------------------------- blade_3_seg_2 --------------------------------!
!
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.ground
!
part create rigid_body name_and_position  &
   part_name = .wind_turbine.blade_3_seg_2  &
   adams_id = 21  &
   location = 5000.0, -8227.2413359522, 7.525E+04  &
   orientation = 0.0d, 120.0d, 0.0d
!
part create rigid_body initial_velocity  &
   part_name = .wind_turbine.blade_3_seg_2  &
   vx = 0.0  &
   vy = 5969.0260418206  &
   vz = -1.0338656376E+04  &
   wx = 1.2566370614  &
   wy = 0.0  &
   wz = 0.0
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.blade_3_seg_2
!
! ****** Markers for current part ******
!
marker create  &
   marker_name = .wind_turbine.blade_3_seg_2.mass_cm  &
   adams_id = 64  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_3_seg_2.inboard_mkr  &
   adams_id = 65  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_3_seg_2.beam_mkr  &
   adams_id = 66  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 90.0d, 90.0d, 90.0d
!
part create rigid_body mass_properties  &
   part_name = .wind_turbine.blade_3_seg_2  &
   mass = 500.0  &
   center_of_mass_marker = .wind_turbine.blade_3_seg_2.mass_cm  &
   ixx = 1.04167E+09  &
   iyy = 1.04167E+09  &
   izz = 5.0625E+07  &
   ixy = 0.0  &
   izx = 0.0  &
   iyz = 0.0
!
! ****** Graphics for current part ******
!
geometry create shape frustum  &
   frustum_name = .wind_turbine.blade_3_seg_2.blade_geom  &
   adams_id = 21  &
   center_marker = .wind_turbine.blade_3_seg_2.inboard_mkr  &
   angle_extent = 360.0  &
   length = 5000.0  &
   top_radius = 600.0  &
   bottom_radius = 675.0  &
   side_count_for_body = 16  &
   segment_count_for_ends = 0
!
!------------------------------- blade_3_seg_3 --------------------------------!
!
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.ground
!
part create rigid_body name_and_position  &
   part_name = .wind_turbine.blade_3_seg_3  &
   adams_id = 22  &
   location = 5000.0, -1.2557368355E+04, 7.275E+04  &
   orientation = 0.0d, 120.0d, 0.0d
!
part create rigid_body initial_velocity  &
   part_name = .wind_turbine.blade_3_seg_3  &
   vx = 0.0  &
   vy = 9110.6186954104  &
   vz = -1.5780054469E+04  &
   wx = 1.2566370614  &
   wy = 0.0  &
   wz = 0.0
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.blade_3_seg_3
!
! ****** Markers for current part ******
!
marker create  &
   marker_name = .wind_turbine.blade_3_seg_3.mass_cm  &
   adams_id = 67  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_3_seg_3.inboard_mkr  &
   adams_id = 68  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_3_seg_3.beam_mkr  &
   adams_id = 69  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 90.0d, 90.0d, 90.0d
!
part create rigid_body mass_properties  &
   part_name = .wind_turbine.blade_3_seg_3  &
   mass = 500.0  &
   center_of_mass_marker = .wind_turbine.blade_3_seg_3.mass_cm  &
   ixx = 1.04167E+09  &
   iyy = 1.04167E+09  &
   izz = 5.0625E+07  &
   ixy = 0.0  &
   izx = 0.0  &
   iyz = 0.0
!
! ****** Graphics for current part ******
!
geometry create shape frustum  &
   frustum_name = .wind_turbine.blade_3_seg_3.blade_geom  &
   adams_id = 22  &
   center_marker = .wind_turbine.blade_3_seg_3.inboard_mkr  &
   angle_extent = 360.0  &
   length = 5000.0  &
   top_radius = 525.0  &
   bottom_radius = 600.0  &
   side_count_for_body = 16  &
   segment_count_for_ends = 0
!
!------------------------------- blade_3_seg_4 --------------------------------!
!
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.ground
!
part create rigid_body name_and_position  &
   part_name = .wind_turbine.blade_3_seg_4  &
   adams_id = 23  &
   location = 5000.0, -1.6887495374E+04, 7.025E+04  &
   orientation = 0.0d, 120.0d, 0.0d
!
part create rigid_body initial_velocity  &
   part_name = .wind_turbine.blade_3_seg_4  &
   vx = 0.0  &
   vy = 1.2252211349E+04  &
   vz = -2.1221452562E+04  &
   wx = 1.2566370614  &
   wy = 0.0  &
   wz = 0.0
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.blade_3_seg_4
!
! ****** Markers for current part ******
!
marker create  &
   marker_name = .wind_turbine.blade_3_seg_4.mass_cm  &
   adams_id = 70  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_3_seg_4.inboard_mkr  &
   adams_id = 71  &
   location = 0.0, 1.4210854715E-11, -2500.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_3_seg_4.beam_mkr  &
   adams_id = 72  &
   location = 0.0, 1.4210854715E-11, -2500.0  &
   orientation = 90.0d, 90.0d, 90.0d
!
part create rigid_body mass_properties  &
   part_name = .wind_turbine.blade_3_seg_4  &
   mass = 500.0  &
   center_of_mass_marker = .wind_turbine.blade_3_seg_4.mass_cm  &
   ixx = 1.04167E+09  &
   iyy = 1.04167E+09  &
   izz = 5.0625E+07  &
   ixy = 0.0  &
   izx = 0.0  &
   iyz = 0.0
!
! ****** Graphics for current part ******
!
geometry create shape frustum  &
   frustum_name = .wind_turbine.blade_3_seg_4.blade_geom  &
   adams_id = 23  &
   center_marker = .wind_turbine.blade_3_seg_4.inboard_mkr  &
   angle_extent = 360.0  &
   length = 5000.0  &
   top_radius = 450.0  &
   bottom_radius = 525.0  &
   side_count_for_body = 16  &
   segment_count_for_ends = 0
!
!------------------------------- blade_3_seg_5 --------------------------------!
!
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.ground
!
part create rigid_body name_and_position  &
   part_name = .wind_turbine.blade_3_seg_5  &
   adams_id = 24  &
   location = 5000.0, -2.1217622393E+04, 6.775E+04  &
   orientation = 0.0d, 120.0d, 0.0d
!
part create rigid_body initial_velocity  &
   part_name = .wind_turbine.blade_3_seg_5  &
   vx = 0.0  &
   vy = 1.5393804003E+04  &
   vz = -2.6662850654E+04  &
   wx = 1.2566370614  &
   wy = 0.0  &
   wz = 0.0
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.blade_3_seg_5
!
! ****** Markers for current part ******
!
marker create  &
   marker_name = .wind_turbine.blade_3_seg_5.mass_cm  &
   adams_id = 73  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_3_seg_5.inboard_mkr  &
   adams_id = 74  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_3_seg_5.beam_mkr  &
   adams_id = 75  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 90.0d, 90.0d, 90.0d
!
part create rigid_body mass_properties  &
   part_name = .wind_turbine.blade_3_seg_5  &
   mass = 500.0  &
   center_of_mass_marker = .wind_turbine.blade_3_seg_5.mass_cm  &
   ixx = 1.04167E+09  &
   iyy = 1.04167E+09  &
   izz = 5.0625E+07  &
   ixy = 0.0  &
   izx = 0.0  &
   iyz = 0.0
!
! ****** Graphics for current part ******
!
geometry create shape frustum  &
   frustum_name = .wind_turbine.blade_3_seg_5.blade_geom  &
   adams_id = 24  &
   center_marker = .wind_turbine.blade_3_seg_5.inboard_mkr  &
   angle_extent = 360.0  &
   length = 5000.0  &
   top_radius = 375.0  &
   bottom_radius = 450.0  &
   side_count_for_body = 16  &
   segment_count_for_ends = 0
!
!------------------------------- blade_3_seg_6 --------------------------------!
!
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.ground
!
part create rigid_body name_and_position  &
   part_name = .wind_turbine.blade_3_seg_6  &
   adams_id = 25  &
   location = 5000.0, -2.5547749412E+04, 6.525E+04  &
   orientation = 0.0d, 120.0d, 0.0d
!
part create rigid_body initial_velocity  &
   part_name = .wind_turbine.blade_3_seg_6  &
   vx = 0.0  &
   vy = 1.8535396656E+04  &
   vz = -3.2104248747E+04  &
   wx = 1.2566370614  &
   wy = 0.0  &
   wz = 0.0
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.blade_3_seg_6
!
! ****** Markers for current part ******
!
marker create  &
   marker_name = .wind_turbine.blade_3_seg_6.mass_cm  &
   adams_id = 76  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_3_seg_6.inboard_mkr  &
   adams_id = 77  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_3_seg_6.beam_mkr  &
   adams_id = 78  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 90.0d, 90.0d, 90.0d
!
part create rigid_body mass_properties  &
   part_name = .wind_turbine.blade_3_seg_6  &
   mass = 500.0  &
   center_of_mass_marker = .wind_turbine.blade_3_seg_6.mass_cm  &
   ixx = 1.04167E+09  &
   iyy = 1.04167E+09  &
   izz = 5.0625E+07  &
   ixy = 0.0  &
   izx = 0.0  &
   iyz = 0.0
!
! ****** Graphics for current part ******
!
geometry create shape frustum  &
   frustum_name = .wind_turbine.blade_3_seg_6.blade_geom  &
   adams_id = 25  &
   center_marker = .wind_turbine.blade_3_seg_6.inboard_mkr  &
   angle_extent = 360.0  &
   length = 5000.0  &
   top_radius = 300.0  &
   bottom_radius = 375.0  &
   side_count_for_body = 16  &
   segment_count_for_ends = 0
!
!------------------------------- blade_3_seg_7 --------------------------------!
!
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.ground
!
part create rigid_body name_and_position  &
   part_name = .wind_turbine.blade_3_seg_7  &
   adams_id = 26  &
   location = 5000.0, -2.9877876431E+04, 6.275E+04  &
   orientation = 0.0d, 120.0d, 0.0d
!
part create rigid_body initial_velocity  &
   part_name = .wind_turbine.blade_3_seg_7  &
   vx = 0.0  &
   vy = 2.167698931E+04  &
   vz = -3.754564684E+04  &
   wx = 1.2566370614  &
   wy = 0.0  &
   wz = 0.0
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.blade_3_seg_7
!
! ****** Markers for current part ******
!
marker create  &
   marker_name = .wind_turbine.blade_3_seg_7.mass_cm  &
   adams_id = 79  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_3_seg_7.inboard_mkr  &
   adams_id = 80  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_3_seg_7.beam_mkr  &
   adams_id = 81  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 90.0d, 90.0d, 90.0d
!
part create rigid_body mass_properties  &
   part_name = .wind_turbine.blade_3_seg_7  &
   mass = 500.0  &
   center_of_mass_marker = .wind_turbine.blade_3_seg_7.mass_cm  &
   ixx = 1.04167E+09  &
   iyy = 1.04167E+09  &
   izz = 5.0625E+07  &
   ixy = 0.0  &
   izx = 0.0  &
   iyz = 0.0
!
! ****** Graphics for current part ******
!
geometry create shape frustum  &
   frustum_name = .wind_turbine.blade_3_seg_7.blade_geom  &
   adams_id = 26  &
   center_marker = .wind_turbine.blade_3_seg_7.inboard_mkr  &
   angle_extent = 360.0  &
   length = 5000.0  &
   top_radius = 225.0  &
   bottom_radius = 300.0  &
   side_count_for_body = 16  &
   segment_count_for_ends = 0
!
!------------------------------- blade_3_seg_8 --------------------------------!
!
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.ground
!
part create rigid_body name_and_position  &
   part_name = .wind_turbine.blade_3_seg_8  &
   adams_id = 27  &
   location = 5000.0, -3.4208003449E+04, 6.025E+04  &
   orientation = 0.0d, 120.0d, 0.0d
!
part create rigid_body initial_velocity  &
   part_name = .wind_turbine.blade_3_seg_8  &
   vx = 0.0  &
   vy = 2.4818581963E+04  &
   vz = -4.2987044932E+04  &
   wx = 1.2566370614  &
   wy = 0.0  &
   wz = 0.0
!
defaults coordinate_system  &
   default_coordinate_system = .wind_turbine.blade_3_seg_8
!
! ****** Markers for current part ******
!
marker create  &
   marker_name = .wind_turbine.blade_3_seg_8.mass_cm  &
   adams_id = 82  &
   location = 0.0, 0.0, 0.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_3_seg_8.inboard_mkr  &
   adams_id = 83  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 0.0d, 0.0d, 0.0d
!
marker create  &
   marker_name = .wind_turbine.blade_3_seg_8.beam_mkr  &
   adams_id = 84  &
   location = 0.0, 0.0, -2500.0  &
   orientation = 90.0d, 90.0d, 90.0d
!
part create rigid_body mass_properties  &
   part_name = .wind_turbine.blade_3_seg_8  &
   mass = 500.0  &
   center_of_mass_marker = .wind_turbine.blade_3_seg_8.mass_cm  &
   ixx = 1.04167E+09  &
   iyy = 1.04167E+09  &
   izz = 5.0625E+07  &
   ixy = 0.0  &
   izx = 0.0  &
   iyz = 0.0
!
! ****** Graphics for current part ******
!
geometry create shape frustum  &
   frustum_name = .wind_turbine.blade_3_seg_8.blade_geom  &
   adams_id = 27  &
   center_marker = .wind_turbine.blade_3_seg_8.inboard_mkr  &
   angle_extent = 360.0  &
   length = 5000.0  &
   top_radius = 150.0  &
   bottom_radius = 225.0  &
   side_count_for_body = 16  &
   segment_count_for_ends = 0
!
!----------------------------------- Joints -----------------------------------!
!
!
constraint create joint fixed  &
   joint_name = .wind_turbine.fix_nacelle  &
   adams_id = 1  &
   i_marker_name = .wind_turbine.nacelle.fix_mkr  &
   j_marker_name = .wind_turbine.ground.tower_top_mkr
!
constraint create joint revolute  &
   joint_name = .wind_turbine.rev_hub  &
   adams_id = 2  &
   i_marker_name = .wind_turbine.hub.pin_mkr  &
   j_marker_name = .wind_turbine.nacelle.hub_axis_mkr
!
constraint create joint fixed  &
   joint_name = .wind_turbine.fix_blade_1_root  &
   adams_id = 3  &
   i_marker_name = .wind_turbine.blade_1_seg_1.inboard_mkr  &
   j_marker_name = .wind_turbine.hub.blade_1_attach_mkr
!
constraint create joint fixed  &
   joint_name = .wind_turbine.fix_blade_2_root  &
   adams_id = 4  &
   i_marker_name = .wind_turbine.blade_2_seg_1.inboard_mkr  &
   j_marker_name = .wind_turbine.hub.blade_2_attach_mkr
!
constraint create joint fixed  &
   joint_name = .wind_turbine.fix_blade_3_root  &
   adams_id = 5  &
   i_marker_name = .wind_turbine.blade_3_seg_1.inboard_mkr  &
   j_marker_name = .wind_turbine.hub.blade_3_attach_mkr
!
!----------------------------------- Forces -----------------------------------!
!
!
force create element_like beam  &
   beam_name = .wind_turbine.beam_b1_s1_2  &
   adams_id = 1  &
   i_marker_name = .wind_turbine.blade_1_seg_1.beam_mkr  &
   j_marker_name = .wind_turbine.blade_1_seg_2.beam_mkr  &
   length = 5000.0  &
   area_of_cross_section = 1.5E+04  &
   y_shear_area_ratio = 0.0  &
   z_shear_area_ratio = 0.0  &
   youngs_modulus = 2.5E+04  &
   shear_modulus = 1.0E+04  &
   ixx = 4.0E+08  &
   iyy = 2.0E+08  &
   izz = 8.0E+08  &
   damping_ratio = 2.0E-02
!
force create element_like beam  &
   beam_name = .wind_turbine.beam_b1_s2_3  &
   adams_id = 2  &
   i_marker_name = .wind_turbine.blade_1_seg_2.beam_mkr  &
   j_marker_name = .wind_turbine.blade_1_seg_3.beam_mkr  &
   length = 5000.0  &
   area_of_cross_section = 1.5E+04  &
   y_shear_area_ratio = 0.0  &
   z_shear_area_ratio = 0.0  &
   youngs_modulus = 2.5E+04  &
   shear_modulus = 1.0E+04  &
   ixx = 4.0E+08  &
   iyy = 2.0E+08  &
   izz = 8.0E+08  &
   damping_ratio = 2.0E-02
!
force create element_like beam  &
   beam_name = .wind_turbine.beam_b1_s3_4  &
   adams_id = 3  &
   i_marker_name = .wind_turbine.blade_1_seg_3.beam_mkr  &
   j_marker_name = .wind_turbine.blade_1_seg_4.beam_mkr  &
   length = 5000.0  &
   area_of_cross_section = 1.5E+04  &
   y_shear_area_ratio = 0.0  &
   z_shear_area_ratio = 0.0  &
   youngs_modulus = 2.5E+04  &
   shear_modulus = 1.0E+04  &
   ixx = 4.0E+08  &
   iyy = 2.0E+08  &
   izz = 8.0E+08  &
   damping_ratio = 2.0E-02
!
force create element_like beam  &
   beam_name = .wind_turbine.beam_b1_s4_5  &
   adams_id = 4  &
   i_marker_name = .wind_turbine.blade_1_seg_4.beam_mkr  &
   j_marker_name = .wind_turbine.blade_1_seg_5.beam_mkr  &
   length = 5000.0  &
   area_of_cross_section = 1.5E+04  &
   y_shear_area_ratio = 0.0  &
   z_shear_area_ratio = 0.0  &
   youngs_modulus = 2.5E+04  &
   shear_modulus = 1.0E+04  &
   ixx = 4.0E+08  &
   iyy = 2.0E+08  &
   izz = 8.0E+08  &
   damping_ratio = 2.0E-02
!
force create element_like beam  &
   beam_name = .wind_turbine.beam_b1_s5_6  &
   adams_id = 5  &
   i_marker_name = .wind_turbine.blade_1_seg_5.beam_mkr  &
   j_marker_name = .wind_turbine.blade_1_seg_6.beam_mkr  &
   length = 5000.0  &
   area_of_cross_section = 1.5E+04  &
   y_shear_area_ratio = 0.0  &
   z_shear_area_ratio = 0.0  &
   youngs_modulus = 2.5E+04  &
   shear_modulus = 1.0E+04  &
   ixx = 4.0E+08  &
   iyy = 2.0E+08  &
   izz = 8.0E+08  &
   damping_ratio = 2.0E-02
!
force create element_like beam  &
   beam_name = .wind_turbine.beam_b1_s6_7  &
   adams_id = 6  &
   i_marker_name = .wind_turbine.blade_1_seg_6.beam_mkr  &
   j_marker_name = .wind_turbine.blade_1_seg_7.beam_mkr  &
   length = 5000.0  &
   area_of_cross_section = 1.5E+04  &
   y_shear_area_ratio = 0.0  &
   z_shear_area_ratio = 0.0  &
   youngs_modulus = 2.5E+04  &
   shear_modulus = 1.0E+04  &
   ixx = 4.0E+08  &
   iyy = 2.0E+08  &
   izz = 8.0E+08  &
   damping_ratio = 2.0E-02
!
force create element_like beam  &
   beam_name = .wind_turbine.beam_b1_s7_8  &
   adams_id = 7  &
   i_marker_name = .wind_turbine.blade_1_seg_7.beam_mkr  &
   j_marker_name = .wind_turbine.blade_1_seg_8.beam_mkr  &
   length = 5000.0  &
   area_of_cross_section = 1.5E+04  &
   y_shear_area_ratio = 0.0  &
   z_shear_area_ratio = 0.0  &
   youngs_modulus = 2.5E+04  &
   shear_modulus = 1.0E+04  &
   ixx = 4.0E+08  &
   iyy = 2.0E+08  &
   izz = 8.0E+08  &
   damping_ratio = 2.0E-02
!
force create element_like beam  &
   beam_name = .wind_turbine.beam_b2_s1_2  &
   adams_id = 8  &
   i_marker_name = .wind_turbine.blade_2_seg_1.beam_mkr  &
   j_marker_name = .wind_turbine.blade_2_seg_2.beam_mkr  &
   length = 5000.0  &
   area_of_cross_section = 1.5E+04  &
   y_shear_area_ratio = 0.0  &
   z_shear_area_ratio = 0.0  &
   youngs_modulus = 2.5E+04  &
   shear_modulus = 1.0E+04  &
   ixx = 4.0E+08  &
   iyy = 2.0E+08  &
   izz = 8.0E+08  &
   damping_ratio = 2.0E-02
!
force create element_like beam  &
   beam_name = .wind_turbine.beam_b2_s2_3  &
   adams_id = 9  &
   i_marker_name = .wind_turbine.blade_2_seg_2.beam_mkr  &
   j_marker_name = .wind_turbine.blade_2_seg_3.beam_mkr  &
   length = 5000.0  &
   area_of_cross_section = 1.5E+04  &
   y_shear_area_ratio = 0.0  &
   z_shear_area_ratio = 0.0  &
   youngs_modulus = 2.5E+04  &
   shear_modulus = 1.0E+04  &
   ixx = 4.0E+08  &
   iyy = 2.0E+08  &
   izz = 8.0E+08  &
   damping_ratio = 2.0E-02
!
force create element_like beam  &
   beam_name = .wind_turbine.beam_b2_s3_4  &
   adams_id = 10  &
   i_marker_name = .wind_turbine.blade_2_seg_3.beam_mkr  &
   j_marker_name = .wind_turbine.blade_2_seg_4.beam_mkr  &
   length = 5000.0  &
   area_of_cross_section = 1.5E+04  &
   y_shear_area_ratio = 0.0  &
   z_shear_area_ratio = 0.0  &
   youngs_modulus = 2.5E+04  &
   shear_modulus = 1.0E+04  &
   ixx = 4.0E+08  &
   iyy = 2.0E+08  &
   izz = 8.0E+08  &
   damping_ratio = 2.0E-02
!
force create element_like beam  &
   beam_name = .wind_turbine.beam_b2_s4_5  &
   adams_id = 11  &
   i_marker_name = .wind_turbine.blade_2_seg_4.beam_mkr  &
   j_marker_name = .wind_turbine.blade_2_seg_5.beam_mkr  &
   length = 5000.0  &
   area_of_cross_section = 1.5E+04  &
   y_shear_area_ratio = 0.0  &
   z_shear_area_ratio = 0.0  &
   youngs_modulus = 2.5E+04  &
   shear_modulus = 1.0E+04  &
   ixx = 4.0E+08  &
   iyy = 2.0E+08  &
   izz = 8.0E+08  &
   damping_ratio = 2.0E-02
!
force create element_like beam  &
   beam_name = .wind_turbine.beam_b2_s5_6  &
   adams_id = 12  &
   i_marker_name = .wind_turbine.blade_2_seg_5.beam_mkr  &
   j_marker_name = .wind_turbine.blade_2_seg_6.beam_mkr  &
   length = 5000.0  &
   area_of_cross_section = 1.5E+04  &
   y_shear_area_ratio = 0.0  &
   z_shear_area_ratio = 0.0  &
   youngs_modulus = 2.5E+04  &
   shear_modulus = 1.0E+04  &
   ixx = 4.0E+08  &
   iyy = 2.0E+08  &
   izz = 8.0E+08  &
   damping_ratio = 2.0E-02
!
force create element_like beam  &
   beam_name = .wind_turbine.beam_b2_s6_7  &
   adams_id = 13  &
   i_marker_name = .wind_turbine.blade_2_seg_6.beam_mkr  &
   j_marker_name = .wind_turbine.blade_2_seg_7.beam_mkr  &
   length = 5000.0  &
   area_of_cross_section = 1.5E+04  &
   y_shear_area_ratio = 0.0  &
   z_shear_area_ratio = 0.0  &
   youngs_modulus = 2.5E+04  &
   shear_modulus = 1.0E+04  &
   ixx = 4.0E+08  &
   iyy = 2.0E+08  &
   izz = 8.0E+08  &
   damping_ratio = 2.0E-02
!
force create element_like beam  &
   beam_name = .wind_turbine.beam_b2_s7_8  &
   adams_id = 14  &
   i_marker_name = .wind_turbine.blade_2_seg_7.beam_mkr  &
   j_marker_name = .wind_turbine.blade_2_seg_8.beam_mkr  &
   length = 5000.0  &
   area_of_cross_section = 1.5E+04  &
   y_shear_area_ratio = 0.0  &
   z_shear_area_ratio = 0.0  &
   youngs_modulus = 2.5E+04  &
   shear_modulus = 1.0E+04  &
   ixx = 4.0E+08  &
   iyy = 2.0E+08  &
   izz = 8.0E+08  &
   damping_ratio = 2.0E-02
!
force create element_like beam  &
   beam_name = .wind_turbine.beam_b3_s1_2  &
   adams_id = 15  &
   i_marker_name = .wind_turbine.blade_3_seg_1.beam_mkr  &
   j_marker_name = .wind_turbine.blade_3_seg_2.beam_mkr  &
   length = 5000.0  &
   area_of_cross_section = 1.5E+04  &
   y_shear_area_ratio = 0.0  &
   z_shear_area_ratio = 0.0  &
   youngs_modulus = 2.5E+04  &
   shear_modulus = 1.0E+04  &
   ixx = 4.0E+08  &
   iyy = 2.0E+08  &
   izz = 8.0E+08  &
   damping_ratio = 2.0E-02
!
force create element_like beam  &
   beam_name = .wind_turbine.beam_b3_s2_3  &
   adams_id = 16  &
   i_marker_name = .wind_turbine.blade_3_seg_2.beam_mkr  &
   j_marker_name = .wind_turbine.blade_3_seg_3.beam_mkr  &
   length = 5000.0  &
   area_of_cross_section = 1.5E+04  &
   y_shear_area_ratio = 0.0  &
   z_shear_area_ratio = 0.0  &
   youngs_modulus = 2.5E+04  &
   shear_modulus = 1.0E+04  &
   ixx = 4.0E+08  &
   iyy = 2.0E+08  &
   izz = 8.0E+08  &
   damping_ratio = 2.0E-02
!
force create element_like beam  &
   beam_name = .wind_turbine.beam_b3_s3_4  &
   adams_id = 17  &
   i_marker_name = .wind_turbine.blade_3_seg_3.beam_mkr  &
   j_marker_name = .wind_turbine.blade_3_seg_4.beam_mkr  &
   length = 5000.0  &
   area_of_cross_section = 1.5E+04  &
   y_shear_area_ratio = 0.0  &
   z_shear_area_ratio = 0.0  &
   youngs_modulus = 2.5E+04  &
   shear_modulus = 1.0E+04  &
   ixx = 4.0E+08  &
   iyy = 2.0E+08  &
   izz = 8.0E+08  &
   damping_ratio = 2.0E-02
!
force create element_like beam  &
   beam_name = .wind_turbine.beam_b3_s4_5  &
   adams_id = 18  &
   i_marker_name = .wind_turbine.blade_3_seg_4.beam_mkr  &
   j_marker_name = .wind_turbine.blade_3_seg_5.beam_mkr  &
   length = 5000.0  &
   area_of_cross_section = 1.5E+04  &
   y_shear_area_ratio = 0.0  &
   z_shear_area_ratio = 0.0  &
   youngs_modulus = 2.5E+04  &
   shear_modulus = 1.0E+04  &
   ixx = 4.0E+08  &
   iyy = 2.0E+08  &
   izz = 8.0E+08  &
   damping_ratio = 2.0E-02
!
force create element_like beam  &
   beam_name = .wind_turbine.beam_b3_s5_6  &
   adams_id = 19  &
   i_marker_name = .wind_turbine.blade_3_seg_5.beam_mkr  &
   j_marker_name = .wind_turbine.blade_3_seg_6.beam_mkr  &
   length = 5000.0  &
   area_of_cross_section = 1.5E+04  &
   y_shear_area_ratio = 0.0  &
   z_shear_area_ratio = 0.0  &
   youngs_modulus = 2.5E+04  &
   shear_modulus = 1.0E+04  &
   ixx = 4.0E+08  &
   iyy = 2.0E+08  &
   izz = 8.0E+08  &
   damping_ratio = 2.0E-02
!
force create element_like beam  &
   beam_name = .wind_turbine.beam_b3_s6_7  &
   adams_id = 20  &
   i_marker_name = .wind_turbine.blade_3_seg_6.beam_mkr  &
   j_marker_name = .wind_turbine.blade_3_seg_7.beam_mkr  &
   length = 5000.0  &
   area_of_cross_section = 1.5E+04  &
   y_shear_area_ratio = 0.0  &
   z_shear_area_ratio = 0.0  &
   youngs_modulus = 2.5E+04  &
   shear_modulus = 1.0E+04  &
   ixx = 4.0E+08  &
   iyy = 2.0E+08  &
   izz = 8.0E+08  &
   damping_ratio = 2.0E-02
!
force create element_like beam  &
   beam_name = .wind_turbine.beam_b3_s7_8  &
   adams_id = 21  &
   i_marker_name = .wind_turbine.blade_3_seg_7.beam_mkr  &
   j_marker_name = .wind_turbine.blade_3_seg_8.beam_mkr  &
   length = 5000.0  &
   area_of_cross_section = 1.5E+04  &
   y_shear_area_ratio = 0.0  &
   z_shear_area_ratio = 0.0  &
   youngs_modulus = 2.5E+04  &
   shear_modulus = 1.0E+04  &
   ixx = 4.0E+08  &
   iyy = 2.0E+08  &
   izz = 8.0E+08  &
   damping_ratio = 2.0E-02
!
!----------------------------- Simulation Scripts -----------------------------!
!
!
simulation script create  &
   sim_script_name = .wind_turbine.run  &
   type = auto_select  &
   initial_static = no  &
   number_of_steps = 1000  &
   end_time = 10.0
!
simulation script create  &
   sim_script_name = .wind_turbine.Last_Sim  &
   commands = "simulation single_run equilibrium model_name=.wind_turbine"
!
!---------------------------------- Motions -----------------------------------!
!
!
constraint create motion_generator  &
   motion_name = .wind_turbine.hub_spin  &
   adams_id = 1  &
   type_of_freedom = rotational  &
   joint_name = .wind_turbine.rev_hub  &
   function = ""
!
!---------------------------------- Accgrav -----------------------------------!
!
!
force create body gravitational  &
   gravity_field_name = gravity  &
   x_component_gravity = 0.0  &
   y_component_gravity = 0.0  &
   z_component_gravity = -9806.65
!
!----------------------------- Analysis settings ------------------------------!
!
!
executive_control set equilibrium_parameters  &
   model_name = wind_turbine  &
   maxit = 2500
!
!---------------------------- Function definitions ----------------------------!
!
!
constraint modify motion_generator  &
   motion_name = .wind_turbine.hub_spin  &
   function = "72.0D * TIME"
!
model display  &
   model_name = wind_turbine

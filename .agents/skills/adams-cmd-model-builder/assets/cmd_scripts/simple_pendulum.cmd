! ============================================================
! Simple Pendulum — Adams CMD example
!
! A single 200 mm rigid link pinned to ground at the top.
! Released from 45° and allowed to swing freely under gravity.
!
! Model structure:
!   .pendulum
!   ├── ground
!   │   └── m_pivot          (pin point on ground)
!   └── link
!       ├── cm               (auto-created by Adams when part modify mass_properties runs)
!       ├── m_pin            (upper end — coincides with m_pivot)
!       └── m_tip            (lower end, 200 mm below pin)
! ============================================================

! --- 1. Model and units ---
model create model_name = pendulum

defaults units &
    length = mm &
    force  = newton &
    mass   = kg &
    time   = sec

! --- 2. Ground marker at the pivot point ---
marker create &
    marker_name = .pendulum.ground.pivot_mkr &
    location    = 0.0, 0.0, 0.0 &
    orientation = 0.0D, 0.0D, 0.0D

! --- 3. Create the link part ---
!     The part origin is at the pin location; link hangs in -Y direction
part create rigid_body name_and_position &
    part_name   = .pendulum.link &
    location    = 0.0, 0.0, 0.0 &
    orientation = 0.0D, 0.0D, 0.0D   ! aligned with global axes

! --- 4. Markers on the link ---
! Set mass properties first — Adams auto-creates .pendulum.link.cm
! Do NOT pass center_of_mass_marker here; .cm doesn't exist yet and Adams will error.
part modify rigid_body mass_properties &
    part_name = .pendulum.link &
    mass      = 1.0 &
    ixx       = 3333.0 &   ! (1/12)*m*L² in kg mm²
    iyy       = 3333.0 &
    izz       = 0.0

! Pin marker at top of link (local position = origin)
marker create &
    marker_name = .pendulum.link.pin_mkr &
    location    = 0.0, 0.0, 0.0 &
    orientation = 0.0D, 0.0D, 0.0D

! Tip marker (200 mm below pin in -Y)
marker create &
    marker_name = .pendulum.link.tip_mkr &
    location    = 0.0, -200.0, 0.0 &
    orientation = 0.0D, 0.0D, 0.0D

! --- 5. Revolute joint at the pivot ---
!     Rotation about the Z-axis of M_PIVOT (global Z)
constraint create joint revolute &
    joint_name    = .pendulum.rev_pivot &
    i_marker_name = .pendulum.link.pin_mkr &
    j_marker_name = .pendulum.ground.pivot_mkr

! --- 6. Set initial conditions (45 deg release) ---
! Rotate the link 45° about Z relative to ground
part modify rigid_body name_and_position &
    part_name   = .pendulum.link &
    orientation = 0.0D, 0.0D, 45.0D

! --- 7. Gravity ---
force create body gravitational &
    gravity_field_name  = .pendulum.gravity &
    x_component_gravity = 0.0 &
    y_component_gravity = -9806.65 &
    z_component_gravity = 0.0

! --- 8. Visualization geometry ---
! Sphere at tip to represent bob
geometry create shape sphere &
    sphere_name   = .pendulum.link.sphere_bob &
    part_name     = .pendulum.link &
    center_marker = .pendulum.link.tip_mkr &
    radius        = 12.0

! Cylinder for the rod body
geometry create shape cylinder &
    cylinder_name  = .pendulum.link.cyl_rod &
    part_name      = .pendulum.link &
    center_marker  = .pendulum.link.pin_mkr &
    length         = 200.0 &
    radius         = 4.0 &
    angle_extent   = 360.0D &
    side_count_for_perimeter = 16

! ============================================================
! End of simple_pendulum.cmd
!
! To simulate: set end time = 2.0 s, step size = 0.001 s
!   simulation single_run transient type=auto_select end_time=2.0 number_of_steps=2000 model_name=.pendulum initial_static=no
! ============================================================

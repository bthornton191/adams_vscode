! ============================================================
! Parametric N-Link Chain — Adams CMD example
!
! Builds N rigid links connected end-to-end by revolute joints.
! The top link is pinned to ground. The number of links is set
! by a single variable N_LINKS and the loop does the rest.
!
! Demonstrates:
!   - variable set / EVAL()
!   - for / end loop
!   - string concatenation with //  and RTOI()
!   - conditional DB_EXISTS check
!   - parameterized marker locations
! ============================================================

! --- 1. Model and units ---
model create model_name = chain

defaults units &
    length = mm &
    force  = newton &
    mass   = kg &
    time   = sec

! --- 2. Parameters ---
variable set variable_name = .chain.n_links    real_value = 5
variable set variable_name = .chain.link_len   real_value = 100.0   ! mm per link
variable set variable_name = .chain.link_mass  real_value = 0.5     ! kg per link

! --- 3. Ground anchor marker ---
marker create &
    marker_name = .chain.ground.top_mkr &
    location    = 0.0, 0.0, 0.0 &
    orientation = 0.0D, 0.0D, 0.0D

! --- 4. Build links in a loop ---
!
! Link i lives at Y = -(i-1)*link_len to -(i)*link_len
! m_top of link i connects to m_bot of link (i-1)  [or to ground for i=1]
!
for variable_name = i  start_value = 1  end_value = (eval(.chain.n_links))

    ! --- Part ---
    part create rigid_body name_and_position &
        part_name   = (eval(".chain.link_" // RTOI(i))) &
        location    = 0.0, (-(i - 1) * eval(.chain.link_len)), 0.0 &
        orientation = 0.0D, 0.0D, 0.0D

    part modify rigid_body mass_properties &
        part_name             = (eval(".chain.link_" // RTOI(i))) &
        mass                  = (eval(.chain.link_mass)) &
        ixx = (eval(.chain.link_mass) * eval(.chain.link_len)**2 / 12.0) &
        iyy = (eval(.chain.link_mass) * eval(.chain.link_len)**2 / 12.0) &
        izz = 0.0

    ! --- Markers ---
    ! Top pin marker (local coords: 0,0,0 = part origin)
    marker create &
        marker_name = (eval(".chain.link_" // RTOI(i) // ".top_mkr")) &
        location    = 0.0, 0.0, 0.0 &
        orientation = 0.0D, 0.0D, 0.0D

    ! Bottom pin marker (local Y = -link_len)
    marker create &
        marker_name = (eval(".chain.link_" // RTOI(i) // ".bot_mkr")) &
        location    = 0.0, (-eval(.chain.link_len)), 0.0 &
        orientation = 0.0D, 0.0D, 0.0D

    ! --- Revolute joint ---
    ! First link connects to ground; others connect to previous link's m_bot
    if condition = (i == 1)
        constraint create joint revolute &
            joint_name    = .chain.rev_0_1 &
            i_marker_name = .chain.link_1.top_mkr &
            j_marker_name = .chain.ground.top_mkr
    end

    if condition = (i > 1)
        constraint create joint revolute &
            joint_name    = (eval(".chain.rev_" // RTOI(i-1) // "_" // RTOI(i))) &
            i_marker_name = (eval(".chain.link_" // RTOI(i) // ".top_mkr")) &
            j_marker_name = (eval(".chain.link_" // RTOI(i-1) // ".bot_mkr"))
    end

    ! --- Cylinder geometry ---
    geometry create shape cylinder &
        cylinder_name  = (eval(".chain.link_" // RTOI(i) // ".cyl")) &
        part_name      = (eval(".chain.link_" // RTOI(i))) &
        center_marker  = (eval(".chain.link_" // RTOI(i) // ".top_mkr")) &
        length         = (eval(.chain.link_len)) &
        radius         = 5.0 &
        angle_extent   = 360.0D

end  ! end for loop

! --- 5. Gravity ---
force create body gravitational &
    gravity_field_name  = .chain.gravity &
    x_component_gravity = 0.0 &
    y_component_gravity = -9806.65 &
    z_component_gravity = 0.0

! ============================================================
! End of parametric_chain.cmd
!
! To change the number of links, edit N_LINKS above and re-run.
!   simulation single_run transient type=auto_select end_time=3.0 number_of_steps=3000 model_name=.chain initial_static=no
! ============================================================

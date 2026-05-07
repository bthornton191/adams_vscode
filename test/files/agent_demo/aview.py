# ============================================================
# Wind Turbine - Adams Python API
#
# Builds a 3-bladed horizontal-axis wind turbine (HAWT) model:
#   - Rigid tower (frustum geometry on ground part)
#   - Rigid nacelle (box geometry, Fixed to ground)
#   - Rigid hub (ellipsoid geometry, Revolute joint to nacelle)
#   - 3 blades, each discretized into N_BLADE_SEGMENTS rigid
#     parts connected by Adams Beam force elements to model
#     structural flexibility (GFRP-like properties)
#
# Coordinate system:
#   X  - rotor axis (into wind / downwind)
#   Y  - lateral (starboard)
#   Z  - vertical (up)
#
# All dimensions in mm, masses in kg, time in seconds.
#
# Blade azimuth is measured from +Z toward +Y in the YZ plane
# (rotor disc):
#   Blade 1  az =   0 deg  ->  pointing straight up  (+Z)
#   Blade 2  az = 120 deg  ->  lower-right quadrant
#   Blade 3  az = 240 deg  ->  lower-left  quadrant
# ============================================================

import Adams
import math


# ==============================================================
# CONSTANTS - edit these to change the model geometry and physics
# ==============================================================

# --- Tower ---
TOWER_HEIGHT        = 80_000.0   # mm  (80 m hub-height class)
TOWER_BASE_RADIUS   =  2_500.0   # mm  outer radius at base
TOWER_TOP_RADIUS    =  1_500.0   # mm  outer radius at top
TOWER_MASS          = 80_000.0   # kg

# --- Nacelle ---
NACELLE_OVERHANG    =  5_000.0   # mm  hub centre distance in +X from tower axis
NACELLE_LENGTH      = 10_000.0   # mm  total length along rotor axis
NACELLE_WIDTH       =  3_000.0   # mm  width (Y direction)
NACELLE_HEIGHT      =  3_000.0   # mm  height (Z direction)
NACELLE_MASS        = 25_000.0   # kg

# --- Hub ---
HUB_RADIUS          =  2_000.0   # mm  sphere radius (geometry and blade-root offset)
HUB_MASS            = 10_000.0   # kg

# --- Blade ---
N_BLADES            = 3          # number of blades
BLADE_SPAN          = 40_000.0   # mm  hub-face to tip (40 m)
N_BLADE_SEGMENTS    = 8          # rigid segments per blade
BLADE_ROOT_RADIUS   =    750.0   # mm  frustum radius at root (segment 0 inboard)
BLADE_TIP_RADIUS    =    150.0   # mm  frustum radius at tip  (segment N-1 outboard)
BLADE_SEGMENT_MASS  =    500.0   # kg  per segment (~4 000 kg total per blade)

# --- Blade beam properties (steel hollow tube section) ---
BEAM_E              = 2.07e5     # N/mm^2  Young's modulus (steel)
BEAM_G              = 8.0e4     # N/mm^2  Shear modulus  (steel)
BEAM_AREA           = 15_000.0   # mm^2    Cross-section area
BEAM_IXX            =  4.0e8     # mm^4   Torsional second moment
BEAM_IYY            =  2.0e8     # mm^4   Flapwise bending
BEAM_IZZ            =  8.0e8     # mm^4   Edgewise bending
BEAM_Y_SHEAR_RATIO  =  1.0       # -      Y shear area ratio
BEAM_Z_SHEAR_RATIO  =  1.0       # -      Z shear area ratio
BEAM_DAMPING        =  1.0e-5    # s      Structural damping (sec units)

# --- Rotor ---
ROTOR_RPM           = 12.0       # rpm  rated speed

# --- Simulation (run is commented out below until model is verified) ---
SIM_END_TIME        = 10.0       # s
SIM_STEPS           = 1_000


# ==============================================================
# DERIVED QUANTITIES
# ==============================================================

SEG_LEN = BLADE_SPAN / N_BLADE_SEGMENTS   # mm, undeformed length per segment

# Rotor angular velocity as a displacement rate for JointMotion:
# ROTOR_RPM rpm * 6 (deg per rpm.s) = deg/s
ROTOR_DEG_PER_SEC = ROTOR_RPM * 6.0      # = 72.0 deg/s at 12 rpm
ROTOR_RAD_PER_SEC = ROTOR_RPM * 2.0 * math.pi / 60.0  # rad/s (for initial conditions)

# Segment inertia (uniform rod, blade axis = local z)
#   ixx, iyy  ~= (1/12) m L^2  (transverse bending)
#   izz       ~= (1/2)  m r^2  (torsional / spin about blade axis)
_R_avg    = (BLADE_ROOT_RADIUS + BLADE_TIP_RADIUS) / 2.0
SEG_IXX   = BLADE_SEGMENT_MASS * SEG_LEN ** 2 / 12.0    # flapwise bending
SEG_IYY   = BLADE_SEGMENT_MASS * SEG_LEN ** 2 / 12.0    # edgewise bending
SEG_IZZ   = 0.5 * BLADE_SEGMENT_MASS * _R_avg ** 2      # spin about blade axis


# ==============================================================
# HELPERS
# ==============================================================

def create_beam(model, name, i_marker, j_marker, length,
                E, G, area, ixx, iyy, izz,
                y_shear=1.0, z_shear=1.0, damp=1.0e-5):
    """
    Create an Adams Beam force element via the CMD bridge.
    The Python API createBeam() does not expose y_shear_ratio / z_shear_ratio;
    those properties are silently ignored, leaving shear ratios at 0 which
    makes the beam numerically singular.  Using execute_cmd guarantees all
    parameters are written correctly.
    """
    Adams.execute_cmd(
        f'force create element_like beam '
        f'beam_name = {model.full_name}.{name} '
        f'i_marker_name = {i_marker.full_name} '
        f'j_marker_name = {j_marker.full_name} '
        f'length = {length:.6g} '
        f'area_of_cross_section = {area:.6g} '
        f'ixx = {ixx:.6g} '
        f'iyy = {iyy:.6g} '
        f'izz = {izz:.6g} '
        f'youngs_modulus = {E:.6g} '
        f'shear_modulus = {G:.6g} '
        f'y_shear_area_ratio = {y_shear:.6g} '
        f'z_shear_area_ratio = {z_shear:.6g} '
        f'damping_ratio = {damp:.6g}'
    )


def seg_radius(seg_idx):
    """
    Linearly interpolated frustum radius at the inboard face of segment seg_idx.
    seg_idx=0  -> BLADE_ROOT_RADIUS
    seg_idx=N  -> BLADE_TIP_RADIUS
    """
    frac = seg_idx / N_BLADE_SEGMENTS
    return BLADE_ROOT_RADIUS + frac * (BLADE_TIP_RADIUS - BLADE_ROOT_RADIUS)


def set_mass_props(part, cm_location, mass, ixx, iyy, izz, orientation=None):
    """
    Create a CM marker on `part` and declare it as the centre-of-mass marker
    via the Adams CMD bridge.  This is required for the Adams Solver to accept
    the model -- setting part.mass/ixx/iyy/izz via Python properties alone
    does NOT write a cm_marker_name into the solver dataset, causing a fatal
    "Missing CM marker" error at simulation time.

    Parameters
    ----------
    part        : Adams Part object
    cm_location : [x, y, z] global position of the CM (mm)
    mass        : total mass (kg)
    ixx, iyy, izz : principal moments of inertia about the CM marker's local
                    x, y, z axes respectively (kg.mm^2).  Pass orientation so
                    that these axes align with the part's structural axes.
    orientation : [psi, theta, phi] ZXZ Euler angles (deg) for the CM marker.
                  Defaults to [0,0,0] (global-aligned) for axis-aligned parts.
                  Pass the part's own orient for angled parts (e.g. blade segs)
                  so Adams applies Ixx/Iyy/Izz in the correct local frame and
                  the inertia box is displayed correctly in Adams View.
    """
    if orientation is None:
        orientation = [0.0, 0.0, 0.0]
    cm_mkr = part.Markers.create(
        name='mass_cm',
        location=cm_location,
        orientation=orientation,
    )
    # The correct Adams CMD to declare mass properties WITH a CM marker is:
    #   part modify rigid_body mass_properties
    #       part_name=... mass=... ixx=... iyy=... izz=...
    #       center_of_mass_marker=...
    # (NOT 'part modify rigid_body ... cm_marker_name=...' which is wrong syntax)
    Adams.execute_cmd(
        f'part modify rigid_body mass_properties '
        f'part_name = {part.full_name} '
        f'mass = {mass:.6g} '
        f'ixx = {ixx:.6g} '
        f'iyy = {iyy:.6g} '
        f'izz = {izz:.6g} '
        f'center_of_mass_marker = {cm_mkr.full_name}'
    )
    return cm_mkr


def blade_orientation(az_deg):
    """
    Adams ZXZ (psi, theta, phi) Euler angles [degrees] that rotate the
    default frame so its local z-axis points along the blade radial direction
    d = [0, sin(az), cos(az)].

    Used for: geometry markers (frustum center), CM markers, part orientation,
              hub attachment markers, and the root Fixed joint i_marker.

    Derivation (ZXZ):
      psi=0, theta=-az:
        z'' = [0, -sin(-az), cos(-az)] = [0, sin(az), cos(az)]  OK
    """
    return [0.0, -az_deg, 0.0]


def beam_marker_orientation(az_deg):
    """
    Adams ZXZ (psi, theta, phi) Euler angles [degrees] that rotate the
    default frame so its local x-axis points along the blade radial direction
    d = [0, sin(az), cos(az)].

    Used exclusively for beam endpoint markers.  Adams Beam uses the x-axis
    of the i_marker as the beam longitudinal axis (the direction along which
    axial stiffness EA acts and from which the I-beam cross-section symbol
    is drawn perpendicular).

    Derivation (ZXZ, psi=90, theta=90):
      local x in global = [0, cos(phi), sin(phi)]
      Set phi = 90 - az:
        local x = [0, sin(az), cos(az)]  OK
    """
    return [90.0, 90.0, 90.0 - az_deg]


# ==============================================================
# 1 - MODEL & UNITS
# ==============================================================

m = Adams.Models.create(name='wind_turbine')

d = Adams.defaults
d.units.length = 'mm'
d.units.mass   = 'kg'
d.units.time   = 'second'
d.units.force  = 'newton'


# ==============================================================
# 2 - GRAVITY  (-Z, standard g in mm units)
# ==============================================================

grav = m.Forces.createGravity(name='gravity')
grav.xyz_component_gravity = [0.0, 0.0, -9806.65]


# ==============================================================
# 3 - TOWER  (frustum geometry on ground_part; no separate part)
#
# The tower base is at the global origin.  The frustum extends
# TOWER_HEIGHT mm in +Z from tower_base_mkr.
# ==============================================================

ground = m.ground_part

tower_base_mkr = ground.Markers.create(
    name='tower_base_mkr',
    location=[0.0, 0.0, 0.0],
    orientation=[0.0, 0.0, 0.0],   # z along global Z -> frustum extends upward
)

ground.Geometries.createFrustum(
    name='tower',
    center_marker=tower_base_mkr,
    bottom_radius=TOWER_BASE_RADIUS,
    top_radius=TOWER_TOP_RADIUS,
    length=TOWER_HEIGHT,
    angle_extent=360.0,
    side_count_for_body=32,
    segment_count_for_ends=0,      # no end caps
)

# Reference marker at tower top - used for the nacelle Fixed joint
tower_top_mkr = ground.Markers.create(
    name='tower_top_mkr',
    location=[0.0, 0.0, TOWER_HEIGHT],
    orientation=[0.0, 0.0, 0.0],
)


# ==============================================================
# 4 - NACELLE  (rigid part, Fixed to ground, box geometry)
#
# The nacelle box spans:
#   X  in  [-(NACELLE_LENGTH - NACELLE_OVERHANG), NACELLE_OVERHANG]
#        = [-5000, +5000] mm  (centred on the tower, hub at front face)
#   Y  in  [-NACELLE_WIDTH/2,  NACELLE_WIDTH/2]
#   Z  in  [TOWER_HEIGHT - NACELLE_HEIGHT/2,  TOWER_HEIGHT + NACELLE_HEIGHT/2]
# ==============================================================

nacelle = m.Parts.createRigidBody(name='nacelle')
nacelle.location = [0.0, 0.0, TOWER_HEIGHT]
# Inertia of a solid box:  I_axis = m/12 * (a^2 + b^2)
set_mass_props(
    nacelle,
    cm_location=[0.0, 0.0, TOWER_HEIGHT],
    mass=NACELLE_MASS,
    ixx=NACELLE_MASS / 12.0 * (NACELLE_WIDTH  ** 2 + NACELLE_HEIGHT ** 2),
    iyy=NACELLE_MASS / 12.0 * (NACELLE_LENGTH ** 2 + NACELLE_HEIGHT ** 2),
    izz=NACELLE_MASS / 12.0 * (NACELLE_LENGTH ** 2 + NACELLE_WIDTH  ** 2),
)

# Fixed joint - nacelle rigidly attached to tower top
nacelle_fix_mkr = nacelle.Markers.create(
    name='fix_mkr',
    location=[0.0, 0.0, TOWER_HEIGHT],
    orientation=[0.0, 0.0, 0.0],
)
m.Constraints.createFixed(
    name='fix_nacelle',
    i_marker=nacelle_fix_mkr,
    j_marker=tower_top_mkr,
)

# Corner marker for the block geometry
# (corner at global [-5000, -1500, 78500]; block extends +x, +y, +z)
nacelle_corner_mkr = nacelle.Markers.create(
    name='corner_mkr',
    location=[
        -(NACELLE_LENGTH - NACELLE_OVERHANG),   # = -5000 mm
        -NACELLE_WIDTH  / 2.0,                  # = -1500 mm
         TOWER_HEIGHT - NACELLE_HEIGHT / 2.0,   # = 78500 mm
    ],
    orientation=[0.0, 0.0, 0.0],
)
nacelle.Geometries.createBlock(
    name='nacelle_body',
    corner_marker=nacelle_corner_mkr,
    x=NACELLE_LENGTH,
    y=NACELLE_WIDTH,
    z=NACELLE_HEIGHT,
)

# Hub-axis marker on nacelle - z-axis along global +X for the revolute joint.
# Adams ZXZ orientation [90, 90, 0]:
#   psi=90  -> X' = [0,1,0]  (new x = global Y)
#   theta=90 about X'=[0,1,0]:  z'' = X'*Z * sin(90) = [1,0,0]  
nacelle_hub_axis_mkr = nacelle.Markers.create(
    name='hub_axis_mkr',
    location=[NACELLE_OVERHANG, 0.0, TOWER_HEIGHT],
    orientation=[90.0, 90.0, 0.0],   # z along global +X (rotor axis)
)


# ==============================================================
# 5 - HUB  (rigid part, revolute joint to nacelle, driven at ROTOR_RPM)
# ==============================================================

# Inertia of a solid sphere: I = (2/5) m r^2
_HUB_I = 0.4 * HUB_MASS * HUB_RADIUS ** 2

hub = m.Parts.createRigidBody(name='hub')
hub.location = [NACELLE_OVERHANG, 0.0, TOWER_HEIGHT]
set_mass_props(
    hub,
    cm_location=[NACELLE_OVERHANG, 0.0, TOWER_HEIGHT],
    mass=HUB_MASS,
    ixx=_HUB_I,
    iyy=_HUB_I,
    izz=_HUB_I,
)

# Hub pin marker - must match nacelle_hub_axis_mkr in position and orientation
hub_pin_mkr = hub.Markers.create(
    name='pin_mkr',
    location=[NACELLE_OVERHANG, 0.0, TOWER_HEIGHT],
    orientation=[90.0, 90.0, 0.0],   # z along global +X
)

rev_hub = m.Constraints.createRevolute(
    name='rev_hub',
    i_marker=hub_pin_mkr,
    j_marker=nacelle_hub_axis_mkr,
)

# Constant-speed rotor motion (displacement function -> vel = ROTOR_DEG_PER_SEC)
m.Constraints.createJointMotion(
    name='hub_spin',
    joint=rev_hub,
    type_of_freedom='rotational',
    time_derivative='displacement',
    function=f'{ROTOR_DEG_PER_SEC}D * TIME',
)

# Ellipsoid for hub visualisation
hub_vis_mkr = hub.Markers.create(
    name='vis_mkr',
    location=[NACELLE_OVERHANG, 0.0, TOWER_HEIGHT],
    orientation=[0.0, 0.0, 0.0],
)
hub.Geometries.createEllipsoid(
    name='hub_sphere',
    center_marker=hub_vis_mkr,
    x_scale_factor=HUB_RADIUS,
    y_scale_factor=HUB_RADIUS,
    z_scale_factor=HUB_RADIUS,
)


# ==============================================================
# 6 - BLADES  (3 * N_BLADE_SEGMENTS rigid parts + Beam forces)
#
# For each blade b (0, 1, 2) at azimuth az = b * 120 deg:
#   - One hub attachment marker at the blade root on the hub part
#   - N_BLADE_SEGMENTS rigid parts (blade segments)
#   - Segment 0 root -> Fixed joint to hub attachment marker
#   - Segments 1..N-1 -> Beam force from the INBOARD marker of the
#     previous segment to the INBOARD marker of this segment.
#     These two markers are physically SEG_LEN apart, so Adams
#     computes zero strain at t=0 (no preload explosion).
#     Adams defines the beam z-axis as the i->j vector, which
#     equals the blade radial direction -- consistent with the
#     marker orientations.
#
# NOTE: connecting prev_out_mkr -> in_mkr (coincident markers)
# with length=SEG_LEN causes 100% axial compression at t=0 and
# segments fly off.  The correct connectivity is inboard->inboard.
# ==============================================================

for b in range(N_BLADES):

    az_deg = b * 120.0
    az_rad = math.radians(az_deg)

    # Blade radial unit vector (YZ plane): d = [0, sin(az), cos(az)]
    d_y = math.sin(az_rad)
    d_z = math.cos(az_rad)

    # Geometry / CM orientation: z along blade
    orient      = blade_orientation(az_deg)
    # Beam endpoint orientation: x along blade (Adams Beam longitudinal axis)
    beam_orient = beam_marker_orientation(az_deg)

    # ----------------------------------------------------------
    # Hub attachment marker for this blade (lives on hub part,
    # rotates with the rotor).  Located at hub face (radius = HUB_RADIUS)
    # along the blade radial direction.
    # ----------------------------------------------------------
    hub_attach_mkr = hub.Markers.create(
        name=f'blade_{b + 1}_attach_mkr',
        location=[
            NACELLE_OVERHANG,
            d_y * HUB_RADIUS,
            TOWER_HEIGHT + d_z * HUB_RADIUS,
        ],
        orientation=orient,  # z along blade, matches root in_mkr
    )

    prev_beam_mkr = None  # beam endpoint marker of the previous segment

    for i in range(N_BLADE_SEGMENTS):

        r_in  = HUB_RADIUS + i       * SEG_LEN   # inboard  distance from hub centre
        r_mid = HUB_RADIUS + (i + 0.5) * SEG_LEN  # CM       distance

        seg_name = f'blade_{b + 1}_seg_{i + 1}'

        # ---- Part ------------------------------------------------
        # Use property setters (not createRigidBody kwargs) for location and
        # orientation so Adams auto-creates the CM marker before user markers
        # are added -- this matches the hub creation pattern and avoids the
        # "no center-of-mass marker" warning that arises when location is
        # passed directly to createRigidBody.
        seg_pos = [
            NACELLE_OVERHANG,
            d_y * r_mid,
            TOWER_HEIGHT + d_z * r_mid,
        ]
        seg = m.Parts.createRigidBody(name=seg_name)
        seg.location    = seg_pos
        seg.orientation = orient
        set_mass_props(
            seg,
            cm_location=seg_pos,
            mass=BLADE_SEGMENT_MASS,
            # CM marker z is along blade axis, so:
            #   ixx, iyy = transverse bending inertia
            #   izz      = spin inertia about blade z-axis
            ixx=SEG_IXX,
            iyy=SEG_IYY,
            izz=SEG_IZZ,
            orientation=orient,  # z along blade
        )

        # ---- Initial conditions (match hub spin rate at t=0) -----
        # All blade segments must start with the same angular velocity as the
        # hub so there is no velocity discontinuity across the beam elements.
        # Angular velocity = ROTOR_RAD_PER_SEC about global X.
        # Linear velocity  = omega x (CM - hub_centre):
        #   vy = -omega * dz * r_mid
        #   vz =  omega * dy * r_mid
        seg.wx = ROTOR_RAD_PER_SEC
        seg.wy = 0.0
        seg.wz = 0.0
        seg.vx = 0.0
        seg.vy = -ROTOR_RAD_PER_SEC * d_z * r_mid
        seg.vz =  ROTOR_RAD_PER_SEC * d_y * r_mid

        # ---- Inboard marker: z along blade (geometry + Fixed constraint) ----
        # Used for: frustum center_marker, root Fixed joint i_marker.
        # z-axis points outboard along the blade so the frustum renders correctly.
        in_mkr = seg.Markers.create(
            name='inboard_mkr',
            location=[
                NACELLE_OVERHANG,
                d_y * r_in,
                TOWER_HEIGHT + d_z * r_in,
            ],
            orientation=orient,  # z along blade
        )

        # ---- Beam marker: x along blade (beam endpoints only) ---------------
        # Coincident with inboard_mkr but rotated so x points along the blade.
        # Adams Beam longitudinal axis = x-axis of i_marker, so this orientation
        # ensures the I-beam cross-section symbol is drawn in the correct plane
        # and axial stiffness is applied along the blade direction.
        beam_mkr = seg.Markers.create(
            name='beam_mkr',
            location=[
                NACELLE_OVERHANG,
                d_y * r_in,
                TOWER_HEIGHT + d_z * r_in,
            ],
            orientation=beam_orient,  # x along blade
        )

        # ---- Constraint / force connecting to previous part ------
        if i == 0:
            # Root segment: Fixed joint to hub attachment marker
            m.Constraints.createFixed(
                name=f'fix_blade_{b + 1}_root',
                i_marker=in_mkr,
                j_marker=hub_attach_mkr,
            )
        else:
            # Beam from prev segment's beam_mkr -> this segment's beam_mkr.
            # Both markers are SEG_LEN apart along the blade -> zero strain at t=0.
            create_beam(
                m,
                name=f'beam_b{b + 1}_s{i}_{i + 1}',
                i_marker=prev_beam_mkr,
                j_marker=beam_mkr,
                length=SEG_LEN,
                E=BEAM_E, G=BEAM_G,
                area=BEAM_AREA,
                ixx=BEAM_IXX, iyy=BEAM_IYY, izz=BEAM_IZZ,
                y_shear=BEAM_Y_SHEAR_RATIO,
                z_shear=BEAM_Z_SHEAR_RATIO,
                damp=BEAM_DAMPING,
            )

        # ---- Frustum geometry (tapered blade section) ------------
        # center_marker z-axis points along blade -> frustum extends outboard.
        seg.Geometries.createFrustum(
            name='blade_geom',
            center_marker=in_mkr,
            bottom_radius=seg_radius(i),
            top_radius=seg_radius(i + 1),
            length=SEG_LEN,
            angle_extent=360.0,
            side_count_for_body=16,
            segment_count_for_ends=0,  # no end caps for performance
        )

        prev_beam_mkr = beam_mkr


# ==============================================================
# 7 - SIMULATION
# ==============================================================

sim = m.Simulations.create(
    name='run',
    end_time=SIM_END_TIME,
    number_of_steps=SIM_STEPS,
    initial_static=False,       # spinning system has no static equilibrium
)
sim.simulate()

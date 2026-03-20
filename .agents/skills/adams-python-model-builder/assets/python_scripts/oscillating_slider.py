# ============================================================
# Oscillating Slider — Adams Python API example
#
# A crank-slider mechanism:
#   ground → crank (revolute, driven by sinusoidal motion)
#         → connecting rod (revolute at both ends)
#         → slider (translational joint on ground)
#
# The crank rotates at 2 rev/s, driving the slider back and
# forth along the X axis. Demonstrates:
#   - Adams.defaults.coordinate_system to set the working CS
#   - Part center_marker property assignment
#   - Using a function string for a JointMotion
#   - Using spline or expression objects
#
# Dimensions (all in mm):
#   crank radius   R = 50 mm
#   rod  length    L = 200 mm
#   slider travel  ~ 100 mm
# ============================================================

import Adams

# --- 1. Model and units ---
m = Adams.models.create(name='oscillating_slider')
d = Adams.defaults
d.units = Adams.DefaultUnits(
    length='mm',
    force='newton',
    mass='kg',
    time='sec',
)

# Working coordinate system aligned with global (default)
d.coordinate_system = m.ground.Markers.create(
    name='global_ref',
    location=[0.0, 0.0, 0.0],
    orientation=[0.0, 0.0, 0.0],
)

# --- 2. Ground reference marker at crank pivot ---
crank_pivot_mkr = m.ground.Markers.create(
    name='crank_pivot_mkr',
    location=[0.0, 0.0, 0.0],
    orientation=[0.0, 0.0, 0.0],
)

# Ground marker at slider guide line (coincident with global origin — same X axis)
slider_guide_mkr = m.ground.Markers.create(
    name='slider_guide_mkr',
    location=[0.0, 0.0, 0.0],
    orientation=[0.0, 0.0, 0.0],  # X axis = slider travel direction
)

# --- 3. Crank (50 mm radius, rotates in XY plane) ---
CRANK_RADIUS = 50.0
crank = m.Parts.createRigidBody(name='crank')
crank.location = [0.0, 0.0, 0.0]
crank.mass = 0.3
crank.ixx = 0.3 * CRANK_RADIUS ** 2 / 2.0
crank.iyy = 0.3 * CRANK_RADIUS ** 2 / 4.0
crank.izz = 0.3 * CRANK_RADIUS ** 2 / 2.0

# Pivot marker (at ground pivot — the revolute will be placed here)
crank_pin_mkr = crank.Markers.create(
    name='pin_mkr',
    location=[0.0, 0.0, 0.0],  # aligns with ground crank_pivot_mkr
    orientation=[0.0, 0.0, 0.0],
)

# Big-end marker at the far end of the crank arm
crank_bigend_mkr = crank.Markers.create(
    name='bigend_mkr',
    location=[CRANK_RADIUS, 0.0, 0.0],  # 50 mm along local X
    orientation=[0.0, 0.0, 0.0],
)

# Cylinder visualisation for crank arm
crank.Geometries.createCylinder(
    name='crank_arm',
    center_marker=crank_pin_mkr,
    length=CRANK_RADIUS,
    radius=5.0,
)

# --- 4. Connecting rod (200 mm, links crank big-end to slider) ---
ROD_LEN = 200.0
rod = m.Parts.createRigidBody(name='rod')
# Place rod CM between crank big-end (50, 0, 0) and initial slider position
rod.location = [CRANK_RADIUS + ROD_LEN / 2.0, 0.0, 0.0]
rod.mass = 0.5
rod.ixx = 0.5 * ROD_LEN ** 2 / 12.0
rod.iyy = 0.5 * ROD_LEN ** 2 / 12.0
rod.izz = 0.0

rod_top_mkr = rod.Markers.create(
    name='top_mkr',
    location=[CRANK_RADIUS, 0.0, 0.0],          # global position; coincides with crank big-end
    orientation=[0.0, 0.0, 0.0],
)
rod_bot_mkr = rod.Markers.create(
    name='bot_mkr',
    location=[CRANK_RADIUS + ROD_LEN, 0.0, 0.0],  # far end at initial slider pin
    orientation=[0.0, 0.0, 0.0],
)

rod.Geometries.createCylinder(
    name='rod_body',
    center_marker=rod_top_mkr,
    length=ROD_LEN,
    radius=4.0,
)

# --- 5. Slider (translates along X) ---
slider = m.Parts.createRigidBody(name='slider')
slider.location = [CRANK_RADIUS + ROD_LEN, 0.0, 0.0]
slider.mass = 1.0
slider.ixx = 1.0
slider.iyy = 1.0
slider.izz = 1.0

slider_pin_mkr = slider.Markers.create(
    name='pin_mkr',
    location=[CRANK_RADIUS + ROD_LEN, 0.0, 0.0],  # rod attachment
    orientation=[0.0, 0.0, 0.0],
)

slider.center_marker = slider.Markers.create(
    name='cm',
    location=[CRANK_RADIUS + ROD_LEN, 0.0, 0.0],
    orientation=[0.0, 0.0, 0.0],
)

slider.Geometries.createBlock(
    name='slider_box',
    corner_marker=slider.center_marker,
    x=30.0,
    y=20.0,
    z=20.0,
)

# --- 6. Joints ---
# Crank pivots on ground (rotation about Z)
rev_crank = m.Constraints.createRevolute(
    name='rev_crank',
    i=crank_pin_mkr,
    j=crank_pivot_mkr,
)

# Crank big-end to rod top (spherical — allows the rod to swing)
m.Constraints.createSpherical(
    name='sph_crank_rod',
    i=crank_bigend_mkr,
    j=rod_top_mkr,
)

# Rod bottom to slider pin (spherical)
m.Constraints.createSpherical(
    name='sph_rod_slider',
    i=rod_bot_mkr,
    j=slider_pin_mkr,
)

# Slider translates along X on ground
m.Constraints.createTranslational(
    name='trans_slider',
    i=slider_pin_mkr,
    j=slider_guide_mkr,
)

# --- 7. Crank motion: 2 rev/s = 720°/s = 4π rad/s ---
motion = m.Constraints.JointMotions.create(
    name='crank_drive',
    joint=rev_crank,
    type='rotational',
)
motion.function = '4.0 * PI * TIME'   # rad (cumulative angle = ω * t)

# --- 8. Gravity in -Y ---
gravity = m.Forces.createGravity(name='gravity')
gravity.x = 0.0
gravity.y = -9806.65
gravity.z = 0.0

# --- 9. Simulate 2 seconds ---
sim = m.Simulations.create(
    name='sim',
    end_time=2.0,
    number_of_steps=2000,
)
sim.simulate()

# --- 10. Quick post-processing: X displacement of slider ---
analysis = m.Analyses['Last_Run']
slider_dx = analysis.results[slider.full_name]['CM Position']['X'].values
print(f'Slider X range: {min(slider_dx):.1f} to {max(slider_dx):.1f} mm')

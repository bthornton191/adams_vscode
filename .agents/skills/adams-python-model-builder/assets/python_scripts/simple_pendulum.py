# ============================================================
# Simple Pendulum — Adams Python API example
#
# A single 200 mm rigid link pinned to ground at the top.
# Released from 45° and allowed to swing freely under gravity.
#
# Model structure:
#   .pendulum
#   ├── ground
#   │   └── pivot_mkr        (pin point on ground)
#   └── link
#       ├── cm               (auto-created by Adams)
#       ├── pin_mkr          (upper end, at part origin)
#       └── tip_mkr          (lower end, 200 mm below pin)
# ============================================================

import Adams

# --- 1. Model and units ---
m = Adams.models.create(name='pendulum')
Adams.defaults.units = Adams.DefaultUnits(
    length='mm',
    force='newton',
    mass='kg',
    time='sec',
)

# --- 2. Ground marker at the pivot point ---
pivot_mkr = m.ground.Markers.create(
    name='pivot_mkr',
    location=[0.0, 0.0, 0.0],
    orientation=[0.0, 0.0, 0.0],
)

# --- 3. Link part ---
link = m.Parts.createRigidBody(name='link')
link.location = [0.0, 0.0, 0.0]

# --- 4. Mass properties ---
# Set before creating additional markers.
# Adams auto-creates link.cm.
link.mass = 1.0
link.ixx = 3333.0  # (1/12)*m*L²  [kg·mm²]
link.iyy = 3333.0
link.izz = 0.0

# --- 5. Markers on the link ---
# Pin at the top (local origin)
pin_mkr = link.Markers.create(
    name='pin_mkr',
    location=[0.0, 0.0, 0.0],
    orientation=[0.0, 0.0, 0.0],
)

# Tip 200 mm below pin in local -Y
tip_mkr = link.Markers.create(
    name='tip_mkr',
    location=[0.0, -200.0, 0.0],
    orientation=[0.0, 0.0, 0.0],
)

# --- 6. Revolute joint at the pivot (rotation about Z) ---
rev_pivot = m.Constraints.createRevolute(
    name='rev_pivot',
    i=pin_mkr,
    j=pivot_mkr,
)

# --- 7. Initial conditions — release from 45° ---
link.orientation = [0.0, 0.0, 45.0]  # degrees

# --- 8. Gravity in -Y ---
gravity = m.Forces.createGravity(name='gravity')
gravity.x = 0.0
gravity.y = -9806.65  # mm/s² (standard g in mm units)
gravity.z = 0.0

# --- 9. Visualization geometry ---
# Small sphere at the tip (bob)
link.Geometries.createSphere(
    name='sphere_bob',
    center_marker=tip_mkr,
    radius=12.0,
)

# Cylinder for the rod
link.Geometries.createCylinder(
    name='cyl_rod',
    center_marker=pin_mkr,
    length=200.0,
    radius=4.0,
)

# --- 10. Simulate 2 seconds ---
sim = m.Simulations.create(
    name='sim',
    end_time=2.0,
    number_of_steps=2000,
)
sim.simulate()

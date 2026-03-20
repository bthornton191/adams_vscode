# ============================================================
# Parametric N-Link Chain — Adams Python API example
#
# Builds N rigid links connected end-to-end by revolute joints.
# The top link is pinned to ground. The number of links and the
# per-link dimensions are set at the top of this file.
#
# Demonstrates:
#   - Python loop instead of Adams CMD for/end construct
#   - Dynamic naming with f-strings
#   - Accessing a marker from a previously-created part
#   - Manager-based object creation
# ============================================================

import Adams

# --- Parameters ---
N_LINKS = 5
LINK_LEN = 100.0   # mm per link
LINK_MASS = 0.5    # kg per link

# --- 1. Model and units ---
m = Adams.models.create(name='chain')
Adams.defaults.units = Adams.DefaultUnits(
    length='mm',
    force='newton',
    mass='kg',
    time='sec',
)

# --- 2. Ground anchor marker ---
top_mkr = m.ground.Markers.create(
    name='top_mkr',
    location=[0.0, 0.0, 0.0],
    orientation=[0.0, 0.0, 0.0],
)

# --- 3. Build N links in a Python loop ---
parts: list = []  # keep references for connecting to previous link

for i in range(1, N_LINKS + 1):
    y_top = -(i - 1) * LINK_LEN  # global Y of this link's top pin

    # Part
    link = m.Parts.createRigidBody(name=f'link_{i}')
    link.location = [0.0, y_top, 0.0]
    link.mass = LINK_MASS
    link.ixx = LINK_MASS * LINK_LEN ** 2 / 12.0
    link.iyy = LINK_MASS * LINK_LEN ** 2 / 12.0
    link.izz = 0.0

    # Markers — local coords relative to the part origin
    top = link.Markers.create(
        name='top_mkr',
        location=[0.0, 0.0, 0.0],
        orientation=[0.0, 0.0, 0.0],
    )
    bot = link.Markers.create(
        name='bot_mkr',
        location=[0.0, -LINK_LEN, 0.0],
        orientation=[0.0, 0.0, 0.0],
    )

    # Revolute joint
    if i == 1:
        # First link pins to ground
        m.Constraints.createRevolute(
            name='rev_0_1',
            i=top,
            j=top_mkr,  # ground marker
        )
    else:
        # Subsequent links connect to the previous link's bottom marker
        prev_bot = parts[i - 2].Markers['bot_mkr']
        m.Constraints.createRevolute(
            name=f'rev_{i - 1}_{i}',
            i=top,
            j=prev_bot,
        )

    # Cylinder visualization
    link.Geometries.createCylinder(
        name='cyl',
        center_marker=top,
        length=LINK_LEN,
        radius=5.0,
    )

    parts.append(link)

# --- 4. Gravity in -Y ---
gravity = m.Forces.createGravity(name='gravity')
gravity.x = 0.0
gravity.y = -9806.65
gravity.z = 0.0

# --- 5. Simulate 3 seconds ---
sim = m.Simulations.create(
    name='sim',
    end_time=3.0,
    number_of_steps=3000,
)
sim.simulate()

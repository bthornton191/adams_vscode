"""Adams Python linting demo - triggers Pylance diagnostics via stub files."""
import Adams

# ============================================================
# ERROR: Accessing non-existent attribute on Adams module
# ============================================================
Adams.NonExistentAttribute

# ============================================================
# ERROR: Wrong argument type - execute_cmd expects str
# ============================================================
Adams.execute_cmd(12345)

# ============================================================
# ERROR: Wrong argument type - evaluate_exp expects str
# ============================================================
Adams.evaluate_exp(None)

# ============================================================
# Setup: Create a model (correct usage for context)
# ============================================================
model = Adams.Models.create(name='demo_model')
ground = model.ground_part

# ============================================================
# ERROR: Accessing non-existent manager on Model
# ============================================================
model.Widgets

# ============================================================
# ERROR: Wrong type for marker location (expects List[float])
# ============================================================
mkr = ground.Markers.create(name='MKR_1', location='not_a_list')

# ============================================================
# ERROR: Wrong type for orientation (expects List[float])
# ============================================================
mkr2 = ground.Markers.create(name='MKR_2', orientation=45.0)

# ============================================================
# ERROR: createRigidBody returns RigidBody, not a Marker
# Assigning mass to a Marker variable is wrong usage
# ============================================================
part = model.Parts.createRigidBody(name='LINK')
part.mass = 'five_kg'  # ERROR: mass expects float, not str

# ============================================================
# ERROR: ixx expects float, not list
# ============================================================
part.ixx = [100, 200, 300]

# ============================================================
# ERROR: Wrong Literal value for type_of_freedom
# ============================================================
sforce = model.Forces.createSingleComponentForce(
    name='BAD_FORCE',
    type_of_freedom='diagonal',  # ERROR: not a valid Literal
)

# ============================================================
# ERROR: Wrong Literal value for formulation on Beam
# ============================================================
i_mkr = part.Markers.create(name='I_MKR', location=[0, 0, 0])
j_mkr = ground.Markers.create(name='J_MKR', location=[100, 0, 0])
beam = model.Forces.createBeam(
    name='BAD_BEAM',
    i_marker=i_mkr,
    j_marker=j_mkr,
)
beam.formulation = 'quadratic'  # ERROR: not 'linear', 'string', or 'nonlinear'

# ============================================================
# ERROR: Gravity xyz_component_gravity expects List[float], not a scalar
# ============================================================
grav = model.Forces.createGravity(name='GRAV')
grav.xyz_component_gravity = -9806.65  # ERROR: expects list, got float

# ============================================================
# ERROR: Simulation number_of_steps expects int, not float
# ============================================================
sim = model.Simulations.create(
    name='run1',
    end_time=5.0,
    number_of_steps=50.5,  # ERROR: expects int
)

# ============================================================
# ERROR: initial_static expects bool, not str
# ============================================================
sim2 = model.Simulations.create(
    name='run2',
    end_time=2.0,
    initial_static='yes',  # ERROR: expects bool
)

# ============================================================
# ERROR: simulate() analysis_name should not be int
# ============================================================
sim.simulate(analysis_name=999)

# ============================================================
# ERROR: Accessing non-existent property on RevoluteJoint
# ============================================================
rev = model.Constraints.createRevolute(
    name='REV_1',
    i_marker=i_mkr,
    j_marker=j_mkr,
)
rev.pitch  # ERROR: RevoluteJoint has no 'pitch' attribute (that's ScrewJoint)

# ============================================================
# ERROR: createMotion - wrong Literal for time_derivative
# ============================================================
motion = model.Constraints.createMotion(
    name='MOT_1',
    joint=rev,
    type_of_freedom='rotational',
    time_derivative='disp',  # ERROR: not 'displacement', 'velocity', or 'acceleration'
    function='360D * TIME',
)

# ============================================================
# ERROR: Wrong type passed to i_marker (expects Marker, got str)
# ============================================================
bad_joint = model.Constraints.createFixed(
    name='FIX_1',
    i_marker='not_an_object',  # ERROR: expects Marker
    j_marker=j_mkr,
)

# ============================================================
# ERROR: stiffness on TranslationalSpringDamper expects float, not list
# ============================================================
spring = model.Forces.createTranslationalSpringDamper(
    name='SPRING_1',
    i_marker=i_mkr,
    j_marker=j_mkr,
)
spring.stiffness = [100, 200, 300]  # ERROR: expects float (it's 1-DOF, not bushing)

# ============================================================
# ERROR: Bushing stiffness expects List[float], not a scalar
# ============================================================
bushing = model.Forces.createBushing(
    name='BUSH_1',
    i_marker=i_mkr,
    j_marker=j_mkr,
)
bushing.stiffness = 5000.0  # ERROR: expects List[float]

# ============================================================
# ERROR: Wrong type for DesignVariable value
# ============================================================
dv = model.DesignVariables.createReal(name='MY_DV', value='not_a_number')

# ============================================================
# ERROR: Calling a method that doesn't exist on the manager
# ============================================================
model.Parts.createFlexible(name='FLEX_1')  # ERROR: no such method

# ============================================================
# ERROR: Using int where str is expected for function expression
# ============================================================
sforce.function = 100  # ERROR: function expects str

import Manager
import Object
from Marker import _i_j_parts_from_markers as _i_j_parts, _loc_ori_provider as _loc_ori
from typing import Any, ItemsView, Iterable, ValuesView

class ForceManager(Manager.SubclassManager):
    def createGravity(self, **kwargs): ...
    def createForceVector(self, **kwargs): ...
    def createTorqueVector(self, **kwargs): ...
    def createRotationalSpringDamper(self, **kwargs): ...
    def createTranslationalSpringDamper(self, **kwargs): ...
    def createBushing(self, **kwargs): ...
    def createSingleComponentForce(self, **kwargs): ...
    def createAppliedTorque(self, **kwargs): ...
    def createAppliedForce(self, **kwargs): ...
    def createBeam(self, **kwargs): ...
    def createField(self, **kwargs): ...
    def createFriction(self, **kwargs): ...
    def createModalForce(self, **kwargs): ...
    def createGeneralForce(self, **kwargs): ...
    def createMultiPointForce(self, **kwargs): ...
    def __getitem__(self, name) -> Force: ...
    def __iter__(self, *args) -> Iterable[str]: ...
    def items(self) -> ItemsView[str, Force]: ...
    def values(self) -> ValuesView[Force]: ...

class _force_i_j_parts(_i_j_parts):
    i_part: Any
    j_part: Any
    i_part_name: Any
    j_part_name: Any

class Force(Object.Object): ...

class Gravity(Force):
    xyz_component_gravity: Any

class ForceVector(Force):
    i_marker_name: Any
    i_marker: Any
    j_floating_marker_name: Any
    j_floating_marker: Any
    ref_marker_name: Any
    ref_marker: Any
    x_force_function: Any
    y_force_function: Any
    z_force_function: Any
    user_function: Any
    routine: Any
    xyz_force_function: Any

class TorqueVector(Force):
    i_marker_name: Any
    i_marker: Any
    j_floating_marker_name: Any
    j_floating_marker: Any
    ref_marker_name: Any
    ref_marker: Any
    x_torque_function: Any
    y_torque_function: Any
    z_torque_function: Any
    user_function: Any
    routine: Any
    xyz_torque_function: Any

class RotationalSpringDamper(Force, _force_i_j_parts, _loc_ori):
    i_marker: Any
    j_marker: Any
    i_marker_name: Any
    j_marker_name: Any
    displacement_at_preload: Any
    torque_preload: Any
    angle: Any
    r_damp: Any
    r_stiff: Any

class TranslationalSpringDamper(Force, _force_i_j_parts, _loc_ori):
    i_marker: Any
    j_marker: Any
    i_marker_name: Any
    j_marker_name: Any
    force_preload: Any
    stiffness: Any
    damping: Any
    displacement_at_preload: Any

class Bushing(Force, _force_i_j_parts, _loc_ori):
    i_marker: Any
    j_marker: Any
    i_marker_name: Any
    j_marker_name: Any
    force_preload: Any
    stiffness: Any
    damping: Any
    tdamping: Any
    tstiffness: Any
    torque_preload: Any

class SingleComponentForce(Force, _force_i_j_parts, _loc_ori):
    i_marker: Any
    j_marker: Any
    i_marker_name: Any
    j_marker_name: Any
    user_function: Any
    function: Any
    action_only: Any
    routine: Any
    type_of_freedom: Any

class Beam(Force, _force_i_j_parts, _loc_ori):
    i_marker: Any
    j_marker: Any
    i_marker_name: Any
    j_marker_name: Any
    length: Any
    damping_ratio: Any
    matrix_of_damping_terms: Any
    shear_modulus: Any
    youngs_modulus: Any
    ixx: Any
    iyy: Any
    izz: Any
    area_of_cross_section: Any
    y_shear_area_ratio: Any
    z_shear_area_ratio: Any
    formulation: Any

class Field(Force, _force_i_j_parts, _loc_ori):
    i_marker: Any
    j_marker: Any
    i_marker_name: Any
    j_marker_name: Any
    force_preload: Any
    torque_preload: Any
    damping_ratio: Any
    matrix_of_damping_terms: Any
    stiffness_matrix: Any
    user_function: Any
    routine: Any
    formulation: Any
    length_tol: Any
    translation_at_preload: Any
    rotation_at_preload: Any

class Friction(Force):
    joint_types: Any
    joint_name: Any
    joint: Any
    mu_static: Any
    mu_dynamic: Any
    yoke: Any
    reaction_arm: Any
    friction_arm: Any
    bending_reaction_arm: Any
    initial_overlap: Any
    pin_radius: Any
    ball_radius: Any
    stiction_transition_velocity: Any
    transition_velocity_coefficient: Any
    max_stiction_deformation: Any
    friction_force_preload: Any
    friction_torque_preload: Any
    max_friction_force: Any
    max_friction_torque: Any
    overlap_delta: Any
    effect: Any
    smooth: Any
    torsional_moment: Any
    bending_moment: Any
    preload: Any
    reaction_force: Any
    inactive_during_static: Any

class ModalForce(Force):
    flexible_body: Any
    flexible_body_name: Any
    reaction_part: Any
    user_function: Any
    routine: Any
    scale_function: Any
    load_case: Any
    force_function: Any

class GeneralForce(Force):
    i_marker_name: Any
    j_floating_marker_name: Any
    ref_marker_name: Any
    i_marker: Any
    j_floating_marker: Any
    ref_marker: Any
    x_force_function: Any
    y_force_function: Any
    z_force_function: Any
    x_torque_function: Any
    y_torque_function: Any
    z_torque_function: Any
    user_function: Any
    routine: Any
    xyz_force_function: Any
    xyz_torque_function: Any

class MultiPointForce(Force):
    i_marker_names: Any
    j_marker_name: Any
    i_markers: Any
    j_marker: Any
    stiffness_matrix_name: Any
    damping_matrix_name: Any
    stiffness_matrix: Any
    damping_matrix: Any
    damping_ratio: Any
    length_matrix_name: Any
    force_matrix_name: Any
    length_matrix: Any
    force_matrix: Any

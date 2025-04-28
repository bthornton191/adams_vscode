import Manager
import Object
from Marker import _i_j_parts_from_markers as _i_j_parts, _loc_ori_provider as _loc_ori, Marker, FloatingMarker
from Marker import FloatingMarker
from typing import Any, ItemsView, Iterable, KeysView, List, ValuesView
from Part import Part, FlexBody


class ForceManager(Manager.SubclassManager):
    def items(self) -> ItemsView[str, Force]: ...
    def values(self) -> ValuesView[Force]: ...
    def keys(self) -> KeysView[str]: ...
    def __getitem__(self, name) -> Force: ...
    def __iter__(self, *args) -> Iterable[str]: ...
    def createGravity(self, **kwargs): ...

    def createForceVector(self,
                          name: str,
                          adams_id: int,
                          comments: str,
                          i_marker: Marker = None,
                          i_marker_name: str = None,
                          j_floating_marker: Marker = None,
                          j_floating_marker_name: str = None,
                          j_part: Part = None,
                          j_part_name: str = None,
                          ref_marker: Marker = None,
                          ref_marker_name: str = None,
                          x_force_function: str = None,
                          y_force_function: str = None,
                          z_force_function: str = None,
                          x_torque_function: str = None,
                          y_torque_function: str = None,
                          z_torque_function: str = None,
                          xyz_force_function: str = None,
                          xyz_torque_function: str = None,
                          user_function: str = None,
                          routine: str = None,
                          **kwargs) -> GeneralForce: ...

    def createTorqueVector(self, **kwargs): ...
    def createRotationalSpringDamper(self, **kwargs): ...
    def createTranslationalSpringDamper(self, **kwargs): ...

    def createBushing(self,
                      i_marker: Marker = None,
                      j_marker: Marker = None,
                      i_marker_name: str = None,
                      j_marker_name: str = None,
                      force_preload: List[float] = None,
                      stiffness: List[float] = None,
                      damping: List[float] = None,
                      tdamping: List[float] = None,
                      tstiffness: List[float] = None,
                      torque_preload: List[float] = None,
                      **kwargs) -> Bushing: ...

    def createSingleComponentForce(self,
                                   name: str,
                                   function: str = '',
                                   i_marker: Marker = None,
                                   j_marker: Marker = None,
                                   i_marker_name: str = None,
                                   j_marker_name: str = None,
                                   i_part: Part = None,
                                   j_part: Part = None,
                                   i_part_name: str = None,
                                   j_part_name: str = None,
                                   action_only: bool = None,
                                   location: List[float] = None,
                                   orientation: List[float] = None,
                                   type_of_freedom: str = 'translational',
                                   relative_to: Marker = None,
                                   **kwargs) -> SingleComponentForce: ...

    def createAppliedTorque(self, **kwargs): ...
    def createAppliedForce(self, **kwargs): ...

    def createBeam(self,
                   name: str,
                   i_marker: Marker = None,
                   j_marker: Marker = None,
                   i_marker_name: str = None,
                   j_marker_name: str = None,
                   length: float = None,
                   damping_ratio: float = None,
                   matrix_of_damping_terms: List[float] = None,
                   shear_modulus: float = None,
                   youngs_modulus: float = None,
                   ixx: float = None,
                   iyy: float = None,
                   izz: float = None,
                   area_of_cross_section: float = None,
                   y_shear_area_ratio: float = None,
                   z_shear_area_ratio: float = None,
                   formulation: str = None,
                   **kwargs) -> Beam: ...

    def createField(self, **kwargs): ...
    def createFriction(self, **kwargs): ...

    def createModalForce(self,
                         name: str = None,
                         flexible_body: FlexBody = None,
                         flexible_body_name: str = None,
                         reaction_part: FloatingMarker = None,
                         reaction_part_name: str = None,
                         user_function: str = None,
                         routine: str = None,
                         scale_function: str = None,
                         load_case=None,
                         force_function: str = None,
                         **kwargs) -> ModalForce: ...

    def createGeneralForce(self,
                           name: str,
                           adams_id: int,
                           comments: str,
                           i_marker: Marker = None,
                           i_marker_name: str = None,
                           j_floating_marker: Marker = None,
                           j_floating_marker_name: str = None,
                           ref_marker: Marker = None,
                           ref_marker_name: str = None,
                           x_force_function: str = None,
                           y_force_function: str = None,
                           z_force_function: str = None,
                           xyz_force_function: str = None,
                           user_function: str = None,
                           routine: str = None,
                           **kwargs) -> ForceVector: ...

    def createMultiPointForce(self, **kwargs): ...
    def __getitem__(self, name) -> Force: ...
    def __iter__(self, *args) -> Iterable[str]: ...
    def items(self) -> ItemsView[str, Force]: ...
    def values(self) -> ValuesView[Force]: ...


class _force_i_j_parts(_i_j_parts):
    i_part: Part
    j_part: Part
    i_part_name: str
    j_part_name: str


class Force(Object.Object):
    ...


class Gravity(Force):
    xyz_component_gravity: List[float]


class ForceVector(Force):
    i_marker_name: str
    i_marker: Marker
    j_floating_marker_name: str
    j_floating_marker: Marker
    ref_marker_name: str
    ref_marker: Marker
    x_force_function: str
    y_force_function: str
    z_force_function: str
    user_function: str
    routine: str
    xyz_force_function: str


class TorqueVector(Force):
    i_marker_name: str
    i_marker: Marker
    j_floating_marker_name: str
    j_floating_marker: Marker
    ref_marker_name: str
    ref_marker: Marker
    x_torque_function: Any
    y_torque_function: Any
    z_torque_function: Any
    user_function: Any
    routine: Any
    xyz_torque_function: Any


class RotationalSpringDamper(Force, _force_i_j_parts, _loc_ori):
    i_marker: Marker
    j_marker: Marker
    i_marker_name: str
    j_marker_name: str
    displacement_at_preload: Any
    torque_preload: Any
    angle: Any
    r_damp: Any
    r_stiff: Any


class TranslationalSpringDamper(Force, _force_i_j_parts, _loc_ori):
    i_marker: Marker
    j_marker: Marker
    i_marker_name: str
    j_marker_name: str
    force_preload: Any
    stiffness: Any
    damping: Any
    displacement_at_preload: Any


class Bushing(Force, _force_i_j_parts, _loc_ori):
    i_marker: Marker
    j_marker: Marker
    i_marker_name: str
    j_marker_name: str
    force_preload: List[float]
    stiffness: List[float]
    damping: List[float]
    tdamping: List[float]
    tstiffness: List[float]
    torque_preload: List[float]


class SingleComponentForce(Force, _force_i_j_parts, _loc_ori):
    i_marker: Marker
    j_marker: Marker
    i_marker_name: str
    j_marker_name: str
    user_function: str
    function: str
    action_only: bool
    routine: str
    type_of_freedom: str


class Beam(Force, _force_i_j_parts, _loc_ori):
    i_marker: Marker
    j_marker: Marker
    i_marker_name: str
    j_marker_name: str
    length: float
    damping_ratio: float
    matrix_of_damping_terms: List[float]
    shear_modulus: float
    youngs_modulus: float
    ixx: float
    iyy: float
    izz: float
    area_of_cross_section: float
    y_shear_area_ratio: float
    z_shear_area_ratio: float
    formulation: str


class Field(Force, _force_i_j_parts, _loc_ori):
    i_marker: Marker
    j_marker: Marker
    i_marker_name: str
    j_marker_name: str
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
    flexible_body: FlexBody
    flexible_body_name: str
    reaction_part: FloatingMarker
    user_function: str
    routine: str
    scale_function: str
    load_case: str
    force_function: str


class GeneralForce(Force):
    i_marker_name: str
    j_floating_marker_name: str
    ref_marker_name: str
    i_marker: Marker
    j_floating_marker: Marker
    ref_marker: Marker
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
    j_marker_name: str
    i_markers: Any
    j_marker: Marker
    stiffness_matrix_name: Any
    damping_matrix_name: Any
    stiffness_matrix: Any
    damping_matrix: Any
    damping_ratio: Any
    length_matrix_name: Any
    force_matrix_name: Any
    length_matrix: Any
    force_matrix: Any

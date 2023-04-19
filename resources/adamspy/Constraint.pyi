import Manager
import Marker
import Object
from typing import Any, ItemsView, Iterable, KeysView, ValuesView

class ConstraintManager(Manager.SubclassManager):
    def createCoupler(self, **kwargs): ...
    def createGear(self, **kwargs): ...
    def createGeneral(self, **kwargs): ...
    def createMotion(self, **kwargs): ...
    def createPointMotion(self, **kwargs): ...
    def createJointMotion(self, **kwargs): ...
    def createMotionT(self, **kwargs): ...
    def createMotionR(self, **kwargs): ...
    def createTranslational(self, **kwargs): ...
    def createRevolute(self, **kwargs): ...
    def createCylindrical(self, **kwargs): ...
    def createUniversal(self, **kwargs): ...
    def createSpherical(self, **kwargs): ...
    def createPlanar(self, **kwargs): ...
    def createConvel(self, **kwargs): ...
    def createFixed(self, **kwargs): ...
    def createHooke(self, **kwargs): ...
    def createRackpin(self, **kwargs): ...
    def createScrew(self, **kwargs): ...
    def createAtPoint(self, **kwargs): ...
    def createInline(self, **kwargs): ...
    def createInLine(self, **kwargs): ...
    def createInPlane(self, **kwargs): ...
    def createOrientation(self, **kwargs): ...
    def createParallel(self, **kwargs): ...
    def createPerpendicular(self, **kwargs): ...
    def createPointPoint(self, **kwargs): ...
    def createPointLine(self, **kwargs): ...
    def createPointPlane(self, **kwargs): ...
    def createLineLine(self, **kwargs): ...
    def createLinePlane(self, **kwargs): ...
    def createPlanePlane(self, **kwargs): ...
    def createPointCurve(self, **kwargs): ...
    def createCurveCurve(self, **kwargs): ...
    def createUserDefined(self, **kwargs): ...
    def createAngle(self, **kwargs): ...
    def switch_type(self, **kwargs): ...
    def items(self) -> ItemsView[str, Constraint]: ...
    def values(self) -> ValuesView[Constraint]: ...
    def keys(self) -> KeysView[str]: ...
    def __getitem__(self, name) -> Constraint: ...
    def __iter__(self, *args) -> Iterable[str]: ...

class Constraint(Object.Object): ...

class _constraint_i_j_parts(_i_j_m):
    i_part: Any
    j_part: Any
    i_part_name: Any
    j_part_name: Any

class Joint(Constraint, _constraint_i_j_parts, Marker._loc_ori_provider):
    def setProperties(self, **kwargs) -> None: ...
    update: Any

class Jprim(Constraint, _constraint_i_j_parts, Marker._loc_ori_provider):
    def setProperties(self, **kwargs) -> None: ...
    update: Any

class TranslationalJoint(Joint):
    maximum_deformation: Any
    delta_v: Any
    i_marker: Any
    j_marker: Any
    i_marker_name: Any
    j_marker_name: Any
    translational_ic: Any
    velocity_ic: Any
    mu_dyn_trans: Any
    mu_stat_trans: Any
    max_fric_trans: Any
    height: Any
    width: Any
    preload_x: Any
    preload_y: Any

class RevoluteJoint(Joint):
    maximum_deformation: Any
    delta_v: Any
    i_marker: Any
    j_marker: Any
    i_marker_name: Any
    j_marker_name: Any
    rotational_ic: Any
    angular_velocity_ic: Any
    mu_dyn_rot: Any
    mu_stat_rot: Any
    max_fric_rot: Any

class CylindricalJoint(Joint):
    i_marker: Any
    j_marker: Any
    i_marker_name: Any
    j_marker_name: Any
    translational_ic: Any
    velocity_ic: Any
    rotational_ic: Any
    angular_velocity_ic: Any

class UniversalJoint(Joint):
    i_marker: Any
    j_marker: Any
    i_marker_name: Any
    j_marker_name: Any

class SphericalJoint(Joint):
    i_marker: Any
    j_marker: Any
    i_marker_name: Any
    j_marker_name: Any

class PlanarJoint(Joint):
    i_marker: Any
    j_marker: Any
    i_marker_name: Any
    j_marker_name: Any

class RackpinJoint(Joint):
    i_marker: Any
    j_marker: Any
    i_marker_name: Any
    j_marker_name: Any
    diameter_of_pitch: Any

class ScrewJoint(Joint):
    i_marker: Any
    j_marker: Any
    i_marker_name: Any
    j_marker_name: Any
    pitch: Any

class ConvelJoint(Joint):
    i_marker: Any
    j_marker: Any
    i_marker_name: Any
    j_marker_name: Any

class FixedJoint(Joint):
    i_marker: Any
    j_marker: Any
    i_marker_name: Any
    j_marker_name: Any

class HookeJoint(Joint):
    i_marker: Any
    j_marker: Any
    i_marker_name: Any
    j_marker_name: Any

class AtPointJPrim(Jprim):
    i_marker: Any
    j_marker: Any
    i_marker_name: Any
    j_marker_name: Any

class InLineJPrim(Jprim):
    i_marker: Any
    j_marker: Any
    i_marker_name: Any
    j_marker_name: Any

class InPlaneJPrim(Jprim):
    i_marker: Any
    j_marker: Any
    i_marker_name: Any
    j_marker_name: Any

class OrientationJPrim(Jprim):
    i_marker: Any
    j_marker: Any
    i_marker_name: Any
    j_marker_name: Any

class ParallelJPrim(Jprim):
    i_marker: Any
    j_marker: Any
    i_marker_name: Any
    j_marker_name: Any

class PerpendicularJPrim(Jprim):
    i_marker: Any
    j_marker: Any
    i_marker_name: Any
    j_marker_name: Any

class PointPointJPrim(Jprim):
    i_marker: Any
    j_marker: Any
    i_marker_name: Any
    j_marker_name: Any
    offset: Any

class PointLineConstraint(Jprim):
    i_marker: Any
    j_marker: Any
    i_marker_name: Any
    j_marker_name: Any
    offset: Any

class PointPlaneConstraint(Jprim):
    i_marker: Any
    j_marker: Any
    i_marker_name: Any
    j_marker_name: Any
    offset: Any

class LineLineConstraint(Jprim):
    i_marker: Any
    j_marker: Any
    i_marker_name: Any
    j_marker_name: Any
    offset: Any

class LinePlaneConstraint(Jprim):
    i_marker: Any
    j_marker: Any
    i_marker_name: Any
    j_marker_name: Any
    offset: Any

class PlanePlaneConstraint(Jprim):
    i_marker: Any
    j_marker: Any
    i_marker_name: Any
    j_marker_name: Any
    offset: Any

class AngleConstraint(Jprim):
    i_marker: Any
    j_marker: Any
    i_marker_name: Any
    j_marker_name: Any
    offset: Any

class PointCurveConstraint(Constraint):
    i_marker_name: Any
    j_floating_marker_name: Any
    ref_marker_name: Any
    i_marker: Any
    j_floating_marker: Any
    ref_marker: Any
    displacement_ic: Any
    velocity_ic: Any
    ic_ref_marker_name: Any
    ic_ref_marker: Any
    curve_name: Any
    curve: Any

class CurveCurveConstraint(Constraint):
    i_floating_marker_name: Any
    i_curve_name: Any
    i_ref_marker_name: Any
    i_floating_marker: Any
    i_curve: Any
    i_ref_marker: Any
    i_displacement_ic: Any
    i_velocity_ic: Any
    i_ic_ref_marker_name: Any
    j_floating_marker_name: Any
    j_curve_name: Any
    j_ref_marker_name: Any
    i_ic_ref_marker: Any
    j_floating_marker: Any
    j_curve: Any
    j_ref_marker: Any
    j_displacement_ic: Any
    j_velocity_ic: Any
    j_ic_ref_marker_name: Any
    j_ic_ref_marker: Any

class UserDefinedConstraint(Constraint):
    user_function: Any
    routine: Any

class CouplerConstraint(Constraint):
    tof_types: Any
    tof_reverse: Any
    joints: Any
    joint_names: Any
    scale_factor: Any
    user_function: Any
    type_of_freedom: Any

class GearConstraint(Constraint):
    joint_1_name: Any
    joint_2_name: Any
    joint_1: Any
    joint_2: Any
    common_velocity_marker: Any
    common_velocity_marker_name: Any

class GeneralConstraint(Constraint):
    i_marker_name: Any
    i_marker: Any
    function: Any

class Motion(Constraint):
    time_derivative: Any
    function: Any
    user_function: Any
    routine: Any

class PointMotion(Motion):
    i_marker: Any
    j_marker: Any
    i_marker_name: Any
    j_marker_name: Any
    axis: Any
    displacement_ic: Any
    velocity_ic: Any
    def setProperties(self, **kwargs) -> None: ...
    update: Any

class JointMotion(Motion):
    __class__: Any
    def setProperties(self, **kwargs): ...
    update: Any
    type_of_freedom: Any
    joint_name: Any
    joint: Any

class TranslationalJointMotion(JointMotion):
    displacement_ic: Any
    velocity_ic: Any

class RotationalJointMotion(JointMotion):
    rotational_displacement_ic: Any
    rotational_velocity_ic: Any

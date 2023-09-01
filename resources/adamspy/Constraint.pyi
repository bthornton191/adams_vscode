import Manager
import Marker
import Object
from typing import Any, ItemsView, Iterable, KeysView, List, ValuesView

class ConstraintManager(Manager.SubclassManager):
    def createCoupler(self,name: str=None, **kwargs): ...
    def createGear(self,name: str=None, **kwargs): ...
    def createGeneral(self,name: str=None, **kwargs): ...
    def createMotion(self,
                     name: str=None, 
                     joint: Joint=None, 
                     joint_name: str=None, 
                     i_marker: Marker.Marker=None,
                     j_marker: Marker.Marker=None,
                     i_marker_name: str=None,
                     j_marker_name: str=None,
                     time_derivative: str=None,
                     function: str='',
                     type_of_freedom: str=None, 
                     **kwargs): 
        """Creates a Motion constraint

        Parameters
        ----------
        type_of_freedom : str
            The type of freedom to be constrained. Can be 'translational' or 'rotational'.
        time_derivative : str
            The time derivative of the constraint. Can be 'displacement' or 'velocity'.
        """
    def createPointMotion(self,name: str=None, **kwargs): ...
    def createJointMotion(self,
                          name: str=None, 
                          joint: Joint=None, 
                          joint_name: str=None, 
                          time_derivative: str=None,
                          function: str='',
                          type_of_freedom: str=None, 
                          **kwargs): 
        """Creates a Motion constraint on a Joint

        Parameters
        ----------
        type_of_freedom : str
            The type of freedom to be constrained. Can be 'translational' or 'rotational'.
        time_derivative : str
            The time derivative of the constraint. Can be 'displacement' or 'velocity'.
        """
    def createMotionT(self,name: str=None, **kwargs): ...
    def createMotionR(self,name: str=None, **kwargs): ...
    def createTranslational(self,name: str=None, **kwargs): ...
    def createRevolute(self,name: str=None, **kwargs): ...
    def createCylindrical(self,name: str=None, **kwargs): ...
    def createUniversal(self,name: str=None, **kwargs): ...
    def createSpherical(self,name: str=None, **kwargs): ...
    def createPlanar(self,name: str=None, **kwargs): ...
    def createConvel(self,name: str=None, **kwargs): ...
    def createFixed(self,name: str=None, **kwargs): ...
    def createHooke(self,name: str=None, **kwargs): ...
    def createRackpin(self,name: str=None, **kwargs): ...
    def createScrew(self,name: str=None, **kwargs): ...
    def createAtPoint(self,name: str=None, **kwargs): ...
    def createInline(self,name: str=None, **kwargs): ...
    def createInLine(self,name: str=None, **kwargs): ...
    def createInPlane(self,name: str=None, **kwargs): ...
    def createOrientation(self,name: str=None, **kwargs): ...
    def createParallel(self,name: str=None, **kwargs): ...
    def createPerpendicular(self,name: str=None, **kwargs): ...
    def createPointPoint(self,name: str=None, **kwargs): ...
    def createPointLine(self,name: str=None, **kwargs): ...
    def createPointPlane(self,name: str=None, **kwargs): ...
    def createLineLine(self,name: str=None, **kwargs): ...
    def createLinePlane(self,name: str=None, **kwargs): ...
    def createPlanePlane(self,name: str=None, **kwargs): ...
    def createPointCurve(self,name: str=None, **kwargs): ...
    def createCurveCurve(self,name: str=None, **kwargs): ...
    def createUserDefined(self,name: str=None, **kwargs): ...
    def createAngle(self,name: str=None, **kwargs): ...
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
    i_part_name: str
    j_part_name: str

class Joint(Constraint, _constraint_i_j_parts, Marker._loc_ori_provider):
    def setProperties(self, **kwargs) -> None: ...
    update: Any

class Jprim(Constraint, _constraint_i_j_parts, Marker._loc_ori_provider):
    def setProperties(self, **kwargs) -> None: ...
    update: Any

class TranslationalJoint(Joint):
    maximum_deformation: float
    delta_v: float
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str
    translational_ic: float
    velocity_ic: float
    mu_dyn_trans: float
    mu_stat_trans: float
    max_fric_trans: float
    height: float
    width: float
    preload_x: float
    preload_y: float

class RevoluteJoint(Joint):
    maximum_deformation: float
    delta_v: float
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str
    rotational_ic: float
    angular_velocity_ic: float
    mu_dyn_rot: float
    mu_stat_rot: float
    max_fric_rot: float

class CylindricalJoint(Joint):
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str
    translational_ic: float
    velocity_ic: float
    rotational_ic: float
    angular_velocity_ic: float

class UniversalJoint(Joint):
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str

class SphericalJoint(Joint):
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str

class PlanarJoint(Joint):
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str

class RackpinJoint(Joint):
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str
    diameter_of_pitch: Any

class ScrewJoint(Joint):
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str
    pitch: Any

class ConvelJoint(Joint):
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str

class FixedJoint(Joint):
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str

class HookeJoint(Joint):
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str

class AtPointJPrim(Jprim):
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str

class InLineJPrim(Jprim):
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str

class InPlaneJPrim(Jprim):
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str

class OrientationJPrim(Jprim):
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str

class ParallelJPrim(Jprim):
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str

class PerpendicularJPrim(Jprim):
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str

class PointPointJPrim(Jprim):
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str
    offset: Any

class PointLineConstraint(Jprim):
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str
    offset: Any

class PointPlaneConstraint(Jprim):
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str
    offset: Any

class LineLineConstraint(Jprim):
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str
    offset: Any

class LinePlaneConstraint(Jprim):
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str
    offset: Any

class PlanePlaneConstraint(Jprim):
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str
    offset: Any

class AngleConstraint(Jprim):
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str
    offset: Any

class PointCurveConstraint(Constraint):
    i_marker_name: str
    j_floating_marker_name: str
    ref_marker_name: str
    i_marker: Marker.Marker
    j_floating_marker: Marker.Marker
    ref_marker: Marker.Marker
    displacement_ic: float
    velocity_ic: float
    ic_ref_marker_name: str
    ic_ref_marker: Marker.Marker
    curve_name: str
    curve: Any

class CurveCurveConstraint(Constraint):
    i_floating_marker_name: str
    i_curve_name: str
    i_ref_marker_name: str
    i_floating_marker: Marker.Marker
    i_curve: Any
    i_ref_marker: Marker.Marker
    i_displacement_ic: float
    i_velocity_ic: float
    i_ic_ref_marker_name: str
    j_floating_marker_name: str
    j_curve_name: str
    j_ref_marker_name: str
    i_ic_ref_marker: Marker.Marker
    j_floating_marker: Marker.Marker
    j_curve: Any
    j_ref_marker: Marker.Marker
    j_displacement_ic: float
    j_velocity_ic: float
    j_ic_ref_marker_name: str
    j_ic_ref_marker: Marker.Marker

class UserDefinedConstraint(Constraint):
    user_function: str
    routine: Any

class CouplerConstraint(Constraint):
    tof_types: Any
    tof_reverse: Any
    joints: List[Constraint]
    joint_names: List[str]
    scale_factor: float
    user_function: str
    type_of_freedom: Any

class GearConstraint(Constraint):
    joint_1_name: str
    joint_2_name: str
    joint_1: Constraint
    joint_2: Constraint
    common_velocity_marker: Marker.Marker
    common_velocity_marker_name: str

class GeneralConstraint(Constraint):
    i_marker_name: str
    i_marker: Marker.Marker
    function: str

class Motion(Constraint):
    time_derivative: Any
    function: str
    user_function: str
    routine: str

class PointMotion(Motion):
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str
    axis: Any
    displacement_ic: float
    velocity_ic: float
    def setProperties(self, **kwargs) -> None: ...
    update: Any

class JointMotion(Motion):
    __class__: Any
    def setProperties(self, **kwargs): ...
    update: Any
    type_of_freedom: Any
    joint_name: str
    joint: Constraint

class TranslationalJointMotion(JointMotion):
    displacement_ic: float
    velocity_ic: float

class RotationalJointMotion(JointMotion):
    rotational_displacement_ic: float
    rotational_velocity_ic: float

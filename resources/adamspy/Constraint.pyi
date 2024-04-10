import Manager
import Marker
import Object
from typing import Any, ItemsView, Iterable, KeysView, List, ValuesView
from Part import Part

class ConstraintManager(Manager.SubclassManager):
    def createCoupler(self,name: str=None, **kwargs)->CouplerConstraint: ...
    def createGear(self,name: str=None, **kwargs)->GearConstraint: ...
    def createGeneral(self,name: str=None, **kwargs)->GeneralConstraint: ...
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
                     **kwargs)->Motion: 
        """Creates a Motion constraint

        Parameters
        ----------
        type_of_freedom : str
            The type of freedom to be constrained. Can be 'translational' or 'rotational'.
        time_derivative : str
            The time derivative of the constraint. Can be 'displacement' or 'velocity'.
        """
    def createPointMotion(self,name: str=None, **kwargs)->PointMotion: ...
    def createJointMotion(self,
                          name: str = None, 
                          joint: Joint = None, 
                          joint_name: str = None, 
                          time_derivative: str = None,
                          function: str = '',
                          type_of_freedom: str = None, 
                          **kwargs) -> JointMotion: 
        """Creates a Motion constraint on a Joint

        Parameters
        ----------
        name : str, optional
            The name of the motion, by default None
        joint : Joint, optional
            The joint object to which the motion is applied, by default None
        joint_name : str, optional
            The name of the joint object to which the motion is applied, by default None
        time_derivative : str, optional
            The time derivative of the constraint. Can be 'displacement' or 'velocity'.
        function : str, optional
            The function defining the joint motion, by default ''
        type_of_freedom : str, optional
            The type of freedom to be constrained. Can be 'translational' or 'rotational'.

        Returns
        -------
        JointMotion
            The created joint motion object
        """
    def createMotionT(self, name: str = None, **kwargs): ...
    def createMotionR(self, name: str = None, **kwargs): ...

    def createTranslational(self, 
                            name: str = None,
                            i_part: Part = None,
                            j_part: Part = None,
                            i_marker: Marker.Marker = None,
                            j_marker: Marker.Marker = None,
                            i_marker_name: str = None,
                            j_marker_name: str = None,
                            location: List[float] = None,
                            orientation: List[float] = None,
                            in_plane_orientation: List[float] = None,
                            along_axis_orientation: List[float] = None,
                            relative_to: Object.Object = None,
                            comments: str = None,
                            adams_id: int = None, 
                            maximum_deformation: float = None,
                            delta_v: float = None,
                            translational_ic: float = None,
                            velocity_ic: float = None,
                            mu_dyn_trans: float = None,
                            mu_stat_trans: float = None,
                            max_fric_trans: float = None,
                            height: float = None,
                            width: float = None,
                            preload_x: float = None,
                            preload_y: float = None,
                            **kwargs) -> TranslationalJoint: 
        ...

    def createRevolute(self,
                       name: str = None,
                       i_part: Part = None,
                       j_part: Part = None,
                       i_marker: Marker.Marker = None,
                       j_marker: Marker.Marker = None,
                       i_marker_name: str = None,
                       j_marker_name: str = None,
                       location: List[float] = None,
                       orientation: List[float] = None,
                       in_plane_orientation: List[float] = None,
                       along_axis_orientation: List[float] = None,
                       relative_to: Object.Object = None,
                       comments: str = None,
                       adams_id: int = None,
                       maximum_deformation: float = None,
                       delta_v: float = None,
                       rotational_ic: float = None,
                       angular_velocity_ic: float = None,
                       mu_dyn_rot: float = None,
                       mu_stat_rot: float = None,
                       max_fric_rot: float = None,
                       **kwargs) -> RevoluteJoint: 
        ...

    def createCylindrical(self,
                          name: str = None,
                          i_part: Part = None,
                          j_part: Part = None,
                          i_marker: Marker.Marker = None,
                          j_marker: Marker.Marker = None,
                          i_marker_name: str = None,
                          j_marker_name: str = None,
                          location: List[float] = None,
                          orientation: List[float] = None,
                          in_plane_orientation: List[float] = None,
                          along_axis_orientation: List[float] = None,
                          relative_to: Object.Object = None,
                          comments: str = None,
                          adams_id: int = None,
                          translational_ic: float = None,
                          velocity_ic: float = None,
                          rotational_ic: float = None,
                          angular_velocity_ic: float = None,
                          **kwargs) -> CylindricalJoint: 
        ...

    def createUniversal(self,
                        name: str = None,
                        i_part: Part = None,
                        j_part: Part = None,
                        i_marker: Marker.Marker = None,
                        j_marker: Marker.Marker = None,
                        i_marker_name: str = None,
                        j_marker_name: str = None,
                        location: List[float] = None,
                        orientation: List[float] = None,
                        in_plane_orientation: List[float] = None,
                        along_axis_orientation: List[float] = None,
                        relative_to: Object.Object = None,
                        comments: str = None,
                        adams_id: int = None,
                        **kwargs): 
        ...

    def createSpherical(self,
                        name: str = None,
                        i_part: Part = None,
                        j_part: Part = None,
                        i_marker: Marker.Marker = None,
                        j_marker: Marker.Marker = None,
                        i_marker_name: str = None,
                        j_marker_name: str = None,
                        location: List[float] = None,
                        orientation: List[float] = None,
                        in_plane_orientation: List[float] = None,
                        along_axis_orientation: List[float] = None,
                        relative_to: Object.Object = None,
                        comments: str = None,
                        adams_id: int = None,
                        **kwargs): 
        ...

    def createPlanar(self,
                     name: str = None,
                     i_part: Part = None,
                     j_part: Part = None,
                     i_marker: Marker.Marker = None,
                     j_marker: Marker.Marker = None,
                     i_marker_name: str = None,
                     j_marker_name: str = None,
                     location: List[float] = None,
                     orientation: List[float] = None,
                     in_plane_orientation: List[float] = None,
                     along_axis_orientation: List[float] = None,
                     relative_to: Object.Object = None,
                     comments: str = None,
                     adams_id: int = None,
                     **kwargs): 
        ...

    def createConvel(self,
                     name: str = None,
                     i_part: Part = None,
                     j_part: Part = None,
                     i_marker: Marker.Marker = None,
                     j_marker: Marker.Marker = None,
                     i_marker_name: str = None,
                     j_marker_name: str = None,
                     location: List[float] = None,
                     orientation: List[float] = None,
                     in_plane_orientation: List[float] = None,
                     along_axis_orientation: List[float] = None,
                     relative_to: Object.Object = None,
                     comments: str = None,
                     adams_id: int = None,
                     **kwargs): 
        ...

    def createFixed(self,
                    name: str = None,
                    i_part: Part = None,
                    j_part: Part = None,
                    i_marker: Marker.Marker = None,
                    j_marker: Marker.Marker = None,
                    i_marker_name: str = None,
                    j_marker_name: str = None,
                    location: List[float] = None,
                    orientation: List[float] = None,
                    in_plane_orientation: List[float] = None,
                    along_axis_orientation: List[float] = None,
                    relative_to: Object.Object = None,
                    comments: str = None,
                    adams_id: int = None,
                    **kwargs) -> FixedJoint: 
        ...

    def createHooke(self,
                    name: str = None,
                    i_marker: Marker.Marker = None,
                    j_marker: Marker.Marker = None,
                    i_marker_name: str = None,
                    j_marker_name: str = None,
                    **kwargs): ...

    def createRackpin(self,
                      name: str = None,
                      i_marker: Marker.Marker = None,
                      j_marker: Marker.Marker = None,
                      i_marker_name: str = None,
                      j_marker_name: str = None,
                      diameter_of_pitch: float = None,
                      **kwargs) -> RackpinJoint: ...

    def createScrew(self,
                    name: str = None,

                    i_marker: Marker.Marker = None,
                    j_marker: Marker.Marker = None,
                    i_marker_name: str = None,
                    j_marker_name: str = None,
                    pitch: float = None,
                    **kwargs) -> ScrewJoint: ...

    def createAtPoint(self,
                      name: str = None,

                      i_marker: Marker.Marker = None,
                      j_marker: Marker.Marker = None,
                      i_marker_name: str = None,
                      j_marker_name: str = None,
                      **kwargs) -> AtPointJPrim: ...

    def createInline(self,
                     name: str = None,

                     i_marker: Marker.Marker = None,
                     j_marker: Marker.Marker = None,
                     i_marker_name: str = None,
                     j_marker_name: str = None,
                     **kwargs) -> InlineJPrim: ...

    def createInLine(self,
                     name: str = None,

                     i_marker: Marker.Marker = None,
                     j_marker: Marker.Marker = None,
                     i_marker_name: str = None,
                     j_marker_name: str = None,
                     **kwargs) -> InLineJPrim: ...

    def createInPlane(self,
                      name: str = None,

                      i_marker: Marker.Marker = None,
                      j_marker: Marker.Marker = None,
                      i_marker_name: str = None,
                      j_marker_name: str = None,
                      **kwargs) -> InPlaneJPrim: ...

    def createOrientation(self,
                          name: str = None,

                          i_marker: Marker.Marker = None,
                          j_marker: Marker.Marker = None,
                          i_marker_name: str = None,
                          j_marker_name: str = None,
                          **kwargs) -> OrientationJPrim: ...

    def createParallel(self,
                       name: str = None,

                       i_marker: Marker.Marker = None,
                       j_marker: Marker.Marker = None,
                       i_marker_name: str = None,
                       j_marker_name: str = None,
                       **kwargs) -> ParallelJPrim: ...

    def createPerpendicular(self,
                            name: str = None,

                            i_marker: Marker.Marker = None,
                            j_marker: Marker.Marker = None,
                            i_marker_name: str = None,
                            j_marker_name: str = None,
                            **kwargs) -> PerpendicularJPrim: ...

    def createPointPoint(self,
                         name: str = None,

                         i_marker: Marker.Marker = None,
                         j_marker: Marker.Marker = None,
                         i_marker_name: str = None,
                         j_marker_name: str = None,
                         **kwargs) -> PointPointJPrim: ...

    def createPointLine(self,
                        name: str = None,

                        i_marker: Marker.Marker = None,
                        j_marker: Marker.Marker = None,
                        i_marker_name: str = None,
                        j_marker_name: str = None,
                        **kwargs) -> PointLineConstraint: ...

    def createPointPlane(self,
                         name: str = None,

                         i_marker: Marker.Marker = None,
                         j_marker: Marker.Marker = None,
                         i_marker_name: str = None,
                         j_marker_name: str = None,
                         **kwargs) -> PointPlaneConstraint: ...

    def createLineLine(self,
                       name: str = None,

                       i_marker: Marker.Marker = None,
                       j_marker: Marker.Marker = None,
                       i_marker_name: str = None,
                       j_marker_name: str = None,
                       **kwargs) -> LineLineConstraint: ...

    def createLinePlane(self,
                        name: str = None,

                        i_marker: Marker.Marker = None,
                        j_marker: Marker.Marker = None,
                        i_marker_name: str = None,
                        j_marker_name: str = None,
                        **kwargs) -> LinePlaneConstraint: ...

    def createPlanePlane(self,
                         name: str = None,

                         i_marker: Marker.Marker = None,
                         j_marker: Marker.Marker = None,
                         i_marker_name: str = None,
                         j_marker_name: str = None,
                         **kwargs) -> PlanePlaneConstraint: ...

    def createPointCurve(self,
                         name: str = None,
                         i_marker: Marker.Marker = None,
                         i_marker_name: str = None,
                         j_floating_marker_name: str = None,
                         j_floating_marker: Marker.Marker = None,
                         ref_marker: Marker.Marker = None,
                         ref_marker_name: str = None,
                         displacement_ic: float = None,
                         velocity_ic: float = None,
                         ic_ref_marker_name: str = None,
                         ic_ref_marker: Marker.Marker = None,
                         curve_name: str = None,
                         curve: Any = None,
                         **kwargs) -> PointCurveConstraint: ...

    def createCurveCurve(self,
                         name: str = None,
                         i_curve: Any = None,
                         i_curve_name: str = None,
                         i_floating_marker: Marker.Marker = None,
                         i_floating_marker_name: str = None,
                         i_ref_marker: Marker.Marker = None,
                         i_ref_marker_name: str = None,
                         i_ic_ref_marker: Marker.Marker = None,
                         i_ic_ref_marker_name: str = None,
                         i_displacement_ic: float = None,
                         i_velocity_ic: float = None,
                         j_curve: Any = None,
                         j_curve_name: str = None,
                         j_floating_marker: Marker.Marker = None,
                         j_floating_marker_name: str = None,
                         j_ref_marker: Marker.Marker = None,
                         j_ref_marker_name: str = None,
                         j_ic_ref_marker: Marker.Marker = None,
                         j_ic_ref_marker_name: str = None,
                         j_displacement_ic: float = None,
                         j_velocity_ic: float = None,
                         **kwargs) -> CurveCurveConstraint: ...
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
    i_part: Part
    j_part: Part
    i_part_name: str
    j_part_name: str

class Joint(Constraint, _constraint_i_j_parts, Marker._loc_ori_provider):
    def setProperties(self, **kwargs) -> None: ...
    update: Any

class Jprim(Constraint, _constraint_i_j_parts, Marker._loc_ori_provider):
    def setProperties(self, **kwargs) -> None: ...
    update: Any

class TranslationalJoint(Joint):
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str
    maximum_deformation: float
    delta_v: float
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
    i_marker: Marker.Marker
    j_floating_marker_name: str
    j_floating_marker: Marker.Marker
    ref_marker: Marker.Marker
    ref_marker_name: str
    displacement_ic: float
    velocity_ic: float
    ic_ref_marker_name: str
    ic_ref_marker: Marker.Marker
    curve_name: str
    curve: Any

class CurveCurveConstraint(Constraint):
    i_curve: Any
    i_curve_name: str
    i_floating_marker: Marker.Marker
    i_floating_marker_name: str
    i_ref_marker: Marker.Marker
    i_ref_marker_name: str
    i_ic_ref_marker: Marker.Marker
    i_ic_ref_marker_name: str
    i_displacement_ic: float
    i_velocity_ic: float
    j_curve: Any
    j_curve_name: str
    j_floating_marker: Marker.Marker
    j_floating_marker_name: str
    j_ref_marker: Marker.Marker
    j_ref_marker_name: str
    j_ic_ref_marker: Marker.Marker
    j_ic_ref_marker_name: str
    j_displacement_ic: float
    j_velocity_ic: float

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

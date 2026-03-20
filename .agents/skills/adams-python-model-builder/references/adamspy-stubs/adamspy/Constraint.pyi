import DataElement
import Manager
import Marker
import Object
from typing import Dict, ItemsView, Iterable, KeysView, List, Literal, ValuesView
from Part import Part


class Constraint(Object.Object):
    ...


class _i_j_m:
    ...


class _constraint_i_j_parts(_i_j_m):
    i_part: Part
    j_part: Part
    i_part_name: str
    j_part_name: str


class Joint(Constraint, _constraint_i_j_parts, Marker._loc_ori_provider):
    def setProperties(self, **kwargs) -> None: ...
    def update(self, **kwargs) -> None: ...


class Jprim(Constraint, _constraint_i_j_parts, Marker._loc_ori_provider):
    def setProperties(self, **kwargs) -> None: ...
    def update(self, **kwargs) -> None: ...


class TranslationalJoint(Joint):
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str
    maximum_deformation: float
    """Maximum deformation allowed in the joint."""
    delta_v: float
    """Velocity below which the joint is considered to be in static friction."""
    translational_ic: float
    """Initial translational displacement."""
    velocity_ic: float
    """Initial translational velocity."""
    mu_dyn_trans: float
    """Dynamic friction coefficient for the translational direction."""
    mu_stat_trans: float
    """Static friction coefficient for the translational direction."""
    max_fric_trans: float
    """Maximum friction force allowed in the translational direction."""
    height: float
    """Height of the translational joint (used in friction calculation)."""
    width: float
    """Width of the translational joint (used in friction calculation)."""
    preload_x: float
    """Preload force in the x direction."""
    preload_y: float
    """Preload force in the y direction."""


class RevoluteJoint(Joint):
    maximum_deformation: float
    """Maximum deformation allowed in the joint."""
    delta_v: float
    """Velocity below which the joint is considered to be in static friction."""
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str
    rotational_ic: float
    """Rotational displacement initial condition (degrees)."""
    angular_velocity_ic: float
    """Angular velocity initial condition."""
    mu_dyn_rot: float
    """Dynamic friction coefficient for the rotational direction."""
    mu_stat_rot: float
    """Static friction coefficient for the rotational direction."""
    max_fric_rot: float
    """Maximum torsional friction torque permitted in the joint."""


class CylindricalJoint(Joint):
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str
    translational_ic: float
    """Initial displacement in the joint."""
    velocity_ic: float
    """Initial translational velocity in the joint."""
    rotational_ic: float
    """Initial angle in the joint (degrees)."""
    angular_velocity_ic: float
    """Initial angular velocity in the joint."""


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
    """Rack and pinion joint. Create via ``model.Constraints.createRackpin()``."""
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str
    diameter_of_pitch: float
    """Pitch diameter that relates the rotational motion of the pinion to the translational motion of the rack."""


class ScrewJoint(Joint):
    """Screw joint. Create via ``model.Constraints.createScrew()``."""
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str
    pitch: float
    """Translational displacement that corresponds to one full revolution of the rotational displacement."""


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
    offset: float
    """Point-to-point distance offset."""


class PointLineConstraint(Jprim):
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str
    offset: float
    """Point-to-line distance offset."""


class PointPlaneConstraint(Jprim):
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str
    offset: float
    """Point-to-plane distance offset."""


class LineLineConstraint(Jprim):
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str
    offset: float
    """Line-to-line distance offset."""


class LinePlaneConstraint(Jprim):
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str
    offset: float
    """Line-to-plane distance offset."""


class PlanePlaneConstraint(Jprim):
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str
    offset: float
    """Plane-to-plane distance offset."""


class AngleConstraint(Jprim):
    """Angle constraint between two markers. Create via ``model.Constraints.createAngle()``."""
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str
    offset: float
    """Angular offset (degrees)."""


class PointCurveConstraint(Constraint):
    i_marker_name: str
    i_marker: Marker.Marker
    j_floating_marker_name: str
    j_floating_marker: Marker.Marker
    ref_marker: Marker.Marker
    ref_marker_name: str
    displacement_ic: float
    """Initial x, y, z coordinates of the point of contact on the curve."""
    velocity_ic: float
    """Initial velocity along the curve."""
    ic_ref_marker_name: str
    ic_ref_marker: Marker.Marker
    curve_name: str
    """Name of the curve data element."""
    curve: DataElement.CurveData
    """Curve data element object."""


class CurveCurveConstraint(Constraint):
    i_curve: DataElement.CurveData
    """I-side curve data element object."""
    i_curve_name: str
    """Name of the I-side curve data element."""
    i_floating_marker: Marker.Marker
    i_floating_marker_name: str
    i_ref_marker: Marker.Marker
    i_ref_marker_name: str
    i_ic_ref_marker: Marker.Marker
    i_ic_ref_marker_name: str
    i_displacement_ic: float
    """Initial x, y, z coordinates of the contact point on the I-side curve."""
    i_velocity_ic: float
    """Initial velocity along the I-side curve."""
    j_curve: DataElement.CurveData
    """J-side curve data element object."""
    j_curve_name: str
    """Name of the J-side curve data element."""
    j_floating_marker: Marker.Marker
    j_floating_marker_name: str
    j_ref_marker: Marker.Marker
    j_ref_marker_name: str
    j_ic_ref_marker: Marker.Marker
    j_ic_ref_marker_name: str
    j_displacement_ic: float
    """Initial x, y, z coordinates of the contact point on the J-side curve."""
    j_velocity_ic: float
    """Velocity along the J-side curve."""


class UserDefinedConstraint(Constraint):
    """User-defined constraint via subroutine. Create via ``model.Constraints.createUserDefined()``."""
    user_function: List[float | int]
    routine: str


class CouplerConstraint(Constraint):
    """Coupler constraint linking two or three joints. Create via ``model.Constraints.createCoupler()``."""
    tof_types: Dict[str, int]
    tof_reverse: Dict[int, str]
    joints: List[Constraint]
    """Joint objects coupled by this coupler."""
    joint_names: List[str]
    """Names of the joints coupled by this coupler."""
    scale_factor: List[float]
    """Scale factors between the coupler displacements."""
    user_function: List[float | int]
    type_of_freedom: List[Literal['translational', 'rotational', 'unknown']]
    """List of freedom types per joint: 'translational', 'rotational', or 'unknown'."""


class GearConstraint(Constraint):
    joint_1_name: str
    """Name of the first joint in this gear constraint."""
    joint_2_name: str
    """Name of the second joint in this gear constraint."""
    joint_1: Constraint
    """First joint object in this gear constraint."""
    joint_2: Constraint
    """Second joint object in this gear constraint."""
    common_velocity_marker: Marker.Marker
    """Common velocity marker object."""
    common_velocity_marker_name: str
    """Name of the common velocity marker."""


class GeneralConstraint(Constraint):
    i_marker_name: str
    i_marker: Marker.Marker
    function: str


class Motion(Constraint):
    time_derivative: Literal['displacement', 'velocity', 'acceleration']
    function: str
    """Specifies an expression or defines and passes constants to a user-written subroutine to define the motion."""
    user_function: List[float | int]
    routine: str


class PointMotion(Motion):
    """Motion constraint between two markers. Create via ``model.Constraints.createPointMotion()``."""
    i_marker: Marker.Marker
    j_marker: Marker.Marker
    i_marker_name: str
    j_marker_name: str
    axis: Literal['x', 'y', 'z', 'b1', 'b2', 'b3']
    """Direction or orientation axis for this motion."""
    displacement_ic: float
    """Initial translational displacement if axis is 'x', 'y', or 'z'; else initial angular displacement."""
    velocity_ic: float
    """Initial translational velocity if axis is 'x', 'y', or 'z'; else initial angular velocity."""

    def setProperties(self, **kwargs) -> None: ...
    update = setProperties


class JointMotion(Motion):
    """Motion constraint on a joint. Create via ``model.Constraints.createJointMotion()``."""

    def setProperties(self, **kwargs) -> None: ...
    update = setProperties
    type_of_freedom: Literal['unspecified', 'translational', 'rotational']
    joint_name: str
    joint: Constraint


class TranslationalJointMotion(JointMotion):
    """Translational motion on a joint. Create via ``model.Constraints.createMotionT()`` or
    ``model.Constraints.createJointMotion(type_of_freedom='translational')``."""
    displacement_ic: float
    """Initial translational displacement."""
    velocity_ic: float
    """Initial translational velocity."""


class RotationalJointMotion(JointMotion):
    """Rotational motion on a joint. Create via ``model.Constraints.createMotionR()`` or
    ``model.Constraints.createJointMotion(type_of_freedom='rotational')``."""
    rotational_displacement_ic: float
    """Initial angular displacement in degrees."""
    rotational_velocity_ic: float
    """Initial angular velocity."""


class ConstraintManager(Manager.SubclassManager):
    def createCoupler(self, name: str = None, **kwargs) -> CouplerConstraint: ...
    def createGear(self, name: str = None, **kwargs) -> GearConstraint: ...
    def createGeneral(self, name: str = None, **kwargs) -> GeneralConstraint: ...

    def createMotion(self,
                     name: str = None,
                     joint: Joint = None,
                     joint_name: str = None,
                     i_marker: Marker.Marker = None,
                     j_marker: Marker.Marker = None,
                     i_marker_name: str = None,
                     j_marker_name: str = None,
                     time_derivative: Literal['displacement', 'velocity', 'acceleration'] = None,
                     function: str = '',
                     type_of_freedom: Literal['translational', 'rotational'] = None,
                     **kwargs) -> Motion:
        """Creates a Motion constraint

        Parameters
        ----------
        type_of_freedom : str
            The type of freedom to be constrained. Can be 'translational' or 'rotational'.
        time_derivative : str
            The time derivative of the constraint. Can be 'displacement' or 'velocity'.
        """

    def createPointMotion(self, name: str = None, **kwargs) -> PointMotion: ...

    def createJointMotion(self,
                          name: str = None,
                          joint: Joint = None,
                          joint_name: str = None,
                          time_derivative: Literal['displacement', 'velocity', 'acceleration'] = None,
                          function: str = '',
                          type_of_freedom: Literal['unspecified', 'translational', 'rotational'] = None,
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
                     **kwargs) -> InLineJPrim: ...

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
                         curve: DataElement.CurveData = None,
                         **kwargs) -> PointCurveConstraint: ...

    def createCurveCurve(self,
                         name: str = None,
                         i_curve: DataElement.CurveData = None,
                         i_curve_name: str = None,
                         i_floating_marker: Marker.Marker = None,
                         i_floating_marker_name: str = None,
                         i_ref_marker: Marker.Marker = None,
                         i_ref_marker_name: str = None,
                         i_ic_ref_marker: Marker.Marker = None,
                         i_ic_ref_marker_name: str = None,
                         i_displacement_ic: float = None,
                         i_velocity_ic: float = None,
                         j_curve: DataElement.CurveData = None,
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

    def createUserDefined(self, name: str = None, **kwargs) -> UserDefinedConstraint: ...
    def createAngle(self, name: str = None, **kwargs) -> AngleConstraint: ...
    def switch_type(self, **kwargs): ...
    def items(self) -> ItemsView[str, Constraint]: ...
    def values(self) -> ValuesView[Constraint]: ...
    def keys(self) -> KeysView[str]: ...
    def __getitem__(self, name) -> Constraint: ...
    def __iter__(self, *args) -> Iterable[str]: ...

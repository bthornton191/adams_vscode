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
    def createCoupler(self,
                      name: str = None,
                      joints: List = None,
                      joint_names: List[str] = None,
                      type_of_freedom: List[str] = None,
                      **kwargs) -> CouplerConstraint:
        """Create a coupler constraint between 2 or 3 joints.

        Parameters
        ----------
        name : str, optional
            Name of the coupler.
        joints : list of Joint, optional
            List of 2-3 joint objects (Translational, Cylindrical, or Revolute).
            Mutually exclusive with ``joint_names``.
        joint_names : list of str, optional
            List of 2-3 joint name strings. Mutually exclusive with ``joints``.
        type_of_freedom : list of str, optional
            Freedom type for each joint: ``'unknown'``, ``'translational'``, or
            ``'rotational'``. Required if any joint is Cylindrical.
        """
        ...

    def createGear(self,
                   name: str = None,
                   joint_1: Joint = None,
                   joint_1_name: str = None,
                   joint_2: Joint = None,
                   joint_2_name: str = None,
                   common_velocity_marker: Marker.Marker = None,
                   common_velocity_marker_name: str = None,
                   **kwargs) -> GearConstraint:
        """Create a gear constraint between two joints.

        Parameters
        ----------
        name : str, optional
            Name of the gear constraint.
        joint_1 : Joint, optional
            First joint object. Mutually exclusive with ``joint_1_name``.
        joint_1_name : str, optional
            Full name of the first joint.
        joint_2 : Joint, optional
            Second joint object. Mutually exclusive with ``joint_2_name``.
        joint_2_name : str, optional
            Full name of the second joint.
        common_velocity_marker : Marker, optional
            Marker defining the common velocity direction.
            Mutually exclusive with ``common_velocity_marker_name``.
        common_velocity_marker_name : str, optional
            Full name of the common velocity marker.
        """
        ...

    def createGeneral(self,
                      name: str = None,
                      i_marker: Marker.Marker = None,
                      i_marker_name: str = None,
                      function: str = None,
                      **kwargs) -> GeneralConstraint:
        """Create a general constraint.

        Parameters
        ----------
        name : str, optional
            Name of the general constraint.
        i_marker : Marker, optional
            Marker on which the constraint acts.
        i_marker_name : str, optional
            Full name of the i marker.
        function : str, optional
            Expression defining the constraint equation.
        """
        ...

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

    def createPointMotion(self,
                          name: str = None,
                          i_marker: Marker.Marker = None,
                          j_marker: Marker.Marker = None,
                          i_marker_name: str = None,
                          j_marker_name: str = None,
                          axis: Literal['x', 'y', 'z', 'b1', 'b2', 'b3'] = None,
                          time_derivative: Literal['displacement', 'velocity', 'acceleration'] = None,
                          function: str = '',
                          **kwargs) -> PointMotion:
        """Create a point motion constraint.

        Parameters
        ----------
        name : str, optional
            Name of the point motion.
        i_marker : Marker, optional
            Action marker.
        j_marker : Marker, optional
            Reaction marker.
        i_marker_name : str, optional
            Full name of the action marker.
        j_marker_name : str, optional
            Full name of the reaction marker.
        axis : str, optional
            Axis of motion: ``'x'``, ``'y'``, ``'z'`` (translational) or
            ``'b1'``, ``'b2'``, ``'b3'`` (rotational).
        time_derivative : str, optional
            ``'displacement'``, ``'velocity'``, or ``'acceleration'``.
        function : str, optional
            Expression defining the motion.
        """
        ...

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

    def createMotionT(self, name: str = None, **kwargs) -> JointMotion:
        """Create a translational joint motion.

        .. deprecated::
            Use :meth:`createJointMotion` with
            ``type_of_freedom='translational'`` instead.

        Parameters
        ----------
        name : str, optional
            Name of the motion.
        """
        ...

    def createMotionR(self, name: str = None, **kwargs) -> JointMotion:
        """Create a rotational joint motion.

        .. deprecated::
            Use :meth:`createJointMotion` with
            ``type_of_freedom='rotational'`` instead.

        Parameters
        ----------
        name : str, optional
            Name of the motion.
        """
        ...

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
        """Create a translational (prismatic) joint between two parts.

        Parameters
        ----------
        name : str, optional
            Name of the joint.
        i_part : Part, optional
            I-part. When provided with ``j_part``, Adams auto-creates I/J markers
            at ``location``. Mutually exclusive with ``i_marker``/``i_marker_name``.
        j_part : Part, optional
            J-part. Mutually exclusive with ``j_marker``/``j_marker_name``.
        i_marker : Marker, optional
            Explicit I-marker. Mutually exclusive with ``i_part``.
        j_marker : Marker, optional
            Explicit J-marker. Mutually exclusive with ``j_part``.
        i_marker_name : str, optional
            Full name of the I-marker.
        j_marker_name : str, optional
            Full name of the J-marker.
        location : list of float, optional
            [x, y, z] coordinates for auto-generated markers (used with ``i_part``/``j_part``).
        orientation : list of float, optional
            [psi, theta, phi] Euler angles defining the joint axis orientation.
        in_plane_orientation : list of float, optional
            Three-component vector defining a vector in the joint plane.
        along_axis_orientation : list of float, optional
            Three-component vector along the joint axis.
        relative_to : Object, optional
            Reference object for ``location`` and orientation vectors.
        comments : str, optional
            Descriptive comments.
        adams_id : int, optional
            Adams numeric ID.
        maximum_deformation : float, optional
            Maximum deformation allowed before joint locks.
        delta_v : float, optional
            Velocity threshold below which friction model switches to static.
        translational_ic : float, optional
            Initial translational displacement.
        velocity_ic : float, optional
            Initial translational velocity.
        mu_dyn_trans : float, optional
            Dynamic friction coefficient (translational).
        mu_stat_trans : float, optional
            Static friction coefficient (translational).
        max_fric_trans : float, optional
            Maximum friction force allowed (translational).
        height : float, optional
            Joint height used in the friction calculation.
        width : float, optional
            Joint width used in the friction calculation.
        preload_x : float, optional
            Preload force in the x direction.
        preload_y : float, optional
            Preload force in the y direction.
        """
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
        """Create a revolute (pin/hinge) joint between two parts.

        Parameters
        ----------
        name : str, optional
            Name of the joint.
        i_part : Part, optional
            I-part. When provided with ``j_part``, Adams auto-creates I/J markers
            at ``location``. Mutually exclusive with ``i_marker``/``i_marker_name``.
        j_part : Part, optional
            J-part. Mutually exclusive with ``j_marker``/``j_marker_name``.
        i_marker : Marker, optional
            Explicit I-marker.
        j_marker : Marker, optional
            Explicit J-marker.
        i_marker_name : str, optional
            Full name of the I-marker.
        j_marker_name : str, optional
            Full name of the J-marker.
        location : list of float, optional
            [x, y, z] coordinates for auto-generated markers.
        orientation : list of float, optional
            [psi, theta, phi] Euler angles defining the joint axis orientation.
        in_plane_orientation : list of float, optional
            Three-component vector in the joint plane.
        along_axis_orientation : list of float, optional
            Three-component vector along the joint axis.
        relative_to : Object, optional
            Reference object for ``location`` and orientation vectors.
        comments : str, optional
            Descriptive comments.
        adams_id : int, optional
            Adams numeric ID.
        maximum_deformation : float, optional
            Maximum deformation allowed before joint locks.
        delta_v : float, optional
            Velocity threshold below which friction model switches to static.
        rotational_ic : float, optional
            Initial rotational displacement (degrees).
        angular_velocity_ic : float, optional
            Initial angular velocity.
        mu_dyn_rot : float, optional
            Dynamic friction coefficient (rotational).
        mu_stat_rot : float, optional
            Static friction coefficient (rotational).
        max_fric_rot : float, optional
            Maximum torsional friction torque permitted.
        """
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
        """Create a cylindrical joint between two parts.

        A cylindrical joint permits both translation and rotation along/about a
        common axis (2 DOF).

        Parameters
        ----------
        name : str, optional
            Name of the joint.
        i_part : Part, optional
            I-part. When provided with ``j_part``, Adams auto-creates I/J markers
            at ``location``. Mutually exclusive with ``i_marker``/``i_marker_name``.
        j_part : Part, optional
            J-part.
        i_marker : Marker, optional
            Explicit I-marker.
        j_marker : Marker, optional
            Explicit J-marker.
        i_marker_name : str, optional
            Full name of the I-marker.
        j_marker_name : str, optional
            Full name of the J-marker.
        location : list of float, optional
            [x, y, z] coordinates for auto-generated markers.
        orientation : list of float, optional
            [psi, theta, phi] Euler angles defining the joint axis.
        in_plane_orientation : list of float, optional
            Three-component vector in the joint plane.
        along_axis_orientation : list of float, optional
            Three-component vector along the joint axis.
        relative_to : Object, optional
            Reference object for ``location`` and orientation vectors.
        comments : str, optional
            Descriptive comments.
        adams_id : int, optional
            Adams numeric ID.
        translational_ic : float, optional
            Initial translational displacement.
        velocity_ic : float, optional
            Initial translational velocity.
        rotational_ic : float, optional
            Initial rotational displacement (degrees).
        angular_velocity_ic : float, optional
            Initial angular velocity.
        """
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
        """Create a universal (Cardan/Hooke) joint between two parts.

        A universal joint transmits rotation between two shafts whose axes
        intersect at a point and allows angular misalignment (2 rotational DOF
        removed, 1 relative rotation permitted per shaft).

        Parameters
        ----------
        name : str, optional
            Name of the joint.
        i_part : Part, optional
            I-part. When provided with ``j_part``, Adams auto-creates I/J markers
            at ``location``. Mutually exclusive with ``i_marker``/``i_marker_name``.
        j_part : Part, optional
            J-part.
        i_marker : Marker, optional
            Explicit I-marker.
        j_marker : Marker, optional
            Explicit J-marker.
        i_marker_name : str, optional
            Full name of the I-marker.
        j_marker_name : str, optional
            Full name of the J-marker.
        location : list of float, optional
            [x, y, z] coordinates for auto-generated markers.
        orientation : list of float, optional
            [psi, theta, phi] Euler angles.
        in_plane_orientation : list of float, optional
            Three-component vector in the joint plane.
        along_axis_orientation : list of float, optional
            Three-component vector along the joint axis.
        relative_to : Object, optional
            Reference object for ``location`` and orientation vectors.
        comments : str, optional
            Descriptive comments.
        adams_id : int, optional
            Adams numeric ID.
        """
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
        """Create a spherical (ball) joint between two parts.

        A spherical joint permits all three rotational DOF while constraining
        all three translational DOF (3 DOF removed).

        Parameters
        ----------
        name : str, optional
            Name of the joint.
        i_part : Part, optional
            I-part. When provided with ``j_part``, Adams auto-creates I/J markers
            at ``location``. Mutually exclusive with ``i_marker``/``i_marker_name``.
        j_part : Part, optional
            J-part.
        i_marker : Marker, optional
            Explicit I-marker.
        j_marker : Marker, optional
            Explicit J-marker.
        i_marker_name : str, optional
            Full name of the I-marker.
        j_marker_name : str, optional
            Full name of the J-marker.
        location : list of float, optional
            [x, y, z] coordinates for auto-generated markers.
        orientation : list of float, optional
            [psi, theta, phi] Euler angles.
        in_plane_orientation : list of float, optional
            Three-component vector in the joint plane.
        along_axis_orientation : list of float, optional
            Three-component vector along the joint axis.
        relative_to : Object, optional
            Reference object for ``location`` and orientation vectors.
        comments : str, optional
            Descriptive comments.
        adams_id : int, optional
            Adams numeric ID.
        """
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
        """Create a planar joint between two parts.

        A planar joint constrains motion to a plane, permitting two translational
        and one rotational DOF (3 DOF removed).

        Parameters
        ----------
        name : str, optional
            Name of the joint.
        i_part : Part, optional
            I-part. When provided with ``j_part``, Adams auto-creates I/J markers
            at ``location``. Mutually exclusive with ``i_marker``/``i_marker_name``.
        j_part : Part, optional
            J-part.
        i_marker : Marker, optional
            Explicit I-marker.
        j_marker : Marker, optional
            Explicit J-marker.
        i_marker_name : str, optional
            Full name of the I-marker.
        j_marker_name : str, optional
            Full name of the J-marker.
        location : list of float, optional
            [x, y, z] coordinates for auto-generated markers.
        orientation : list of float, optional
            [psi, theta, phi] Euler angles.
        in_plane_orientation : list of float, optional
            Three-component vector in the joint plane.
        along_axis_orientation : list of float, optional
            Three-component vector along the joint axis.
        relative_to : Object, optional
            Reference object for ``location`` and orientation vectors.
        comments : str, optional
            Descriptive comments.
        adams_id : int, optional
            Adams numeric ID.
        """
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
        """Create a constant velocity (convel) joint between two parts.

        A constant velocity joint transmits rotation between two shafts at a
        constant angular velocity ratio regardless of the shaft angle.

        Parameters
        ----------
        name : str, optional
            Name of the joint.
        i_part : Part, optional
            I-part. When provided with ``j_part``, Adams auto-creates I/J markers
            at ``location``. Mutually exclusive with ``i_marker``/``i_marker_name``.
        j_part : Part, optional
            J-part.
        i_marker : Marker, optional
            Explicit I-marker.
        j_marker : Marker, optional
            Explicit J-marker.
        i_marker_name : str, optional
            Full name of the I-marker.
        j_marker_name : str, optional
            Full name of the J-marker.
        location : list of float, optional
            [x, y, z] coordinates for auto-generated markers.
        orientation : list of float, optional
            [psi, theta, phi] Euler angles.
        in_plane_orientation : list of float, optional
            Three-component vector in the joint plane.
        along_axis_orientation : list of float, optional
            Three-component vector along the joint axis.
        relative_to : Object, optional
            Reference object for ``location`` and orientation vectors.
        comments : str, optional
            Descriptive comments.
        adams_id : int, optional
            Adams numeric ID.
        """
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
        """Create a fixed joint between two parts.

        A fixed joint rigidly connects two parts, removing all 6 relative DOF.

        Parameters
        ----------
        name : str, optional
            Name of the joint.
        i_part : Part, optional
            I-part. When provided with ``j_part``, Adams auto-creates I/J markers
            at ``location``. Mutually exclusive with ``i_marker``/``i_marker_name``.
        j_part : Part, optional
            J-part.
        i_marker : Marker, optional
            Explicit I-marker.
        j_marker : Marker, optional
            Explicit J-marker.
        i_marker_name : str, optional
            Full name of the I-marker.
        j_marker_name : str, optional
            Full name of the J-marker.
        location : list of float, optional
            [x, y, z] coordinates for auto-generated markers.
        orientation : list of float, optional
            [psi, theta, phi] Euler angles.
        in_plane_orientation : list of float, optional
            Three-component vector in the joint plane.
        along_axis_orientation : list of float, optional
            Three-component vector along the joint axis.
        relative_to : Object, optional
            Reference object for ``location`` and orientation vectors.
        comments : str, optional
            Descriptive comments.
        adams_id : int, optional
            Adams numeric ID.
        """
        ...

    def createHooke(self,
                    name: str = None,
                    i_marker: Marker.Marker = None,
                    j_marker: Marker.Marker = None,
                    i_marker_name: str = None,
                    j_marker_name: str = None,
                    **kwargs) -> HookeJoint:
        """Create a Hooke (universal) joint.

        .. deprecated::
            Use :meth:`createUniversal` instead.

        Parameters
        ----------
        name : str, optional
            Name of the joint.
        i_marker : Marker, optional
            I-marker.
        j_marker : Marker, optional
            J-marker.
        i_marker_name : str, optional
            Full name of the I-marker.
        j_marker_name : str, optional
            Full name of the J-marker.
        """
        ...

    def createRackpin(self,
                      name: str = None,
                      i_marker: Marker.Marker = None,
                      j_marker: Marker.Marker = None,
                      i_marker_name: str = None,
                      j_marker_name: str = None,
                      diameter_of_pitch: float = None,
                      **kwargs) -> RackpinJoint:
        """Create a rack-and-pinion joint.

        Relates the rotational motion of a pinion (revolute joint) to the
        translational motion of a rack (translational joint).

        Parameters
        ----------
        name : str, optional
            Name of the joint.
        i_marker : Marker, optional
            I-marker (on the pinion part).
        j_marker : Marker, optional
            J-marker (on the rack part).
        i_marker_name : str, optional
            Full name of the I-marker.
        j_marker_name : str, optional
            Full name of the J-marker.
        diameter_of_pitch : float, optional
            Pitch diameter of the pinion that relates one full revolution to
            the translational displacement of the rack.
        """
        ...

    def createScrew(self,
                    name: str = None,

                    i_marker: Marker.Marker = None,
                    j_marker: Marker.Marker = None,
                    i_marker_name: str = None,
                    j_marker_name: str = None,
                    pitch: float = None,
                    **kwargs) -> ScrewJoint:
        """Create a screw joint.

        A screw joint couples translation and rotation along a common axis
        such that one full revolution equals a translational displacement of
        ``pitch``.

        Parameters
        ----------
        name : str, optional
            Name of the joint.
        i_marker : Marker, optional
            I-marker.
        j_marker : Marker, optional
            J-marker.
        i_marker_name : str, optional
            Full name of the I-marker.
        j_marker_name : str, optional
            Full name of the J-marker.
        pitch : float, optional
            Translational displacement per full revolution of the screw.
        """
        ...

    def createAtPoint(self,
                      name: str = None,

                      i_marker: Marker.Marker = None,
                      j_marker: Marker.Marker = None,
                      i_marker_name: str = None,
                      j_marker_name: str = None,
                      **kwargs) -> AtPointJPrim:
        """Create an at-point (JPRIM) constraint.

        Constrains the origin of the I-marker to coincide with the origin of
        the J-marker (3 translational DOF removed).

        Parameters
        ----------
        name : str, optional
            Name of the constraint.
        i_marker : Marker, optional
            I-marker.
        j_marker : Marker, optional
            J-marker.
        i_marker_name : str, optional
            Full name of the I-marker.
        j_marker_name : str, optional
            Full name of the J-marker.
        """
        ...

    def createInline(self,
                     name: str = None,

                     i_marker: Marker.Marker = None,
                     j_marker: Marker.Marker = None,
                     i_marker_name: str = None,
                     j_marker_name: str = None,
                     **kwargs) -> InLineJPrim:
        """Create an in-line (JPRIM) constraint.

        Constrains the origin of the I-marker to lie on the z-axis of the
        J-marker (2 translational DOF removed).

        .. deprecated::
            Use :meth:`createInLine` instead.

        Parameters
        ----------
        name : str, optional
            Name of the constraint.
        i_marker : Marker, optional
            I-marker.
        j_marker : Marker, optional
            J-marker (its z-axis defines the line).
        i_marker_name : str, optional
            Full name of the I-marker.
        j_marker_name : str, optional
            Full name of the J-marker.
        """
        ...

    def createInLine(self,
                     name: str = None,

                     i_marker: Marker.Marker = None,
                     j_marker: Marker.Marker = None,
                     i_marker_name: str = None,
                     j_marker_name: str = None,
                     **kwargs) -> InLineJPrim:
        """Create an in-line (JPRIM) constraint.

        Constrains the origin of the I-marker to lie on the z-axis of the
        J-marker (2 translational DOF removed).

        Parameters
        ----------
        name : str, optional
            Name of the constraint.
        i_marker : Marker, optional
            I-marker.
        j_marker : Marker, optional
            J-marker (its z-axis defines the line).
        i_marker_name : str, optional
            Full name of the I-marker.
        j_marker_name : str, optional
            Full name of the J-marker.
        """
        ...

    def createInPlane(self,
                      name: str = None,

                      i_marker: Marker.Marker = None,
                      j_marker: Marker.Marker = None,
                      i_marker_name: str = None,
                      j_marker_name: str = None,
                      **kwargs) -> InPlaneJPrim:
        """Create an in-plane (JPRIM) constraint.

        Constrains the origin of the I-marker to lie in the x-y plane of the
        J-marker (1 translational DOF removed).

        Parameters
        ----------
        name : str, optional
            Name of the constraint.
        i_marker : Marker, optional
            I-marker.
        j_marker : Marker, optional
            J-marker (its x-y plane defines the constraint plane).
        i_marker_name : str, optional
            Full name of the I-marker.
        j_marker_name : str, optional
            Full name of the J-marker.
        """
        ...

    def createOrientation(self,
                          name: str = None,

                          i_marker: Marker.Marker = None,
                          j_marker: Marker.Marker = None,
                          i_marker_name: str = None,
                          j_marker_name: str = None,
                          **kwargs) -> OrientationJPrim:
        """Create an orientation (JPRIM) constraint.

        Constrains the orientation of the I-marker axes to match those of the
        J-marker (3 rotational DOF removed).

        Parameters
        ----------
        name : str, optional
            Name of the constraint.
        i_marker : Marker, optional
            I-marker.
        j_marker : Marker, optional
            J-marker.
        i_marker_name : str, optional
            Full name of the I-marker.
        j_marker_name : str, optional
            Full name of the J-marker.
        """
        ...

    def createParallel(self,
                       name: str = None,

                       i_marker: Marker.Marker = None,
                       j_marker: Marker.Marker = None,
                       i_marker_name: str = None,
                       j_marker_name: str = None,
                       **kwargs) -> ParallelJPrim:
        """Create a parallel-axes (JPRIM) constraint.

        Constrains the z-axis of the I-marker to remain parallel to the z-axis
        of the J-marker (2 rotational DOF removed).

        Parameters
        ----------
        name : str, optional
            Name of the constraint.
        i_marker : Marker, optional
            I-marker.
        j_marker : Marker, optional
            J-marker.
        i_marker_name : str, optional
            Full name of the I-marker.
        j_marker_name : str, optional
            Full name of the J-marker.
        """
        ...

    def createPerpendicular(self,
                            name: str = None,

                            i_marker: Marker.Marker = None,
                            j_marker: Marker.Marker = None,
                            i_marker_name: str = None,
                            j_marker_name: str = None,
                            **kwargs) -> PerpendicularJPrim:
        """Create a perpendicular-axes (JPRIM) constraint.

        Constrains the z-axis of the I-marker to remain perpendicular to the
        z-axis of the J-marker (1 rotational DOF removed).

        Parameters
        ----------
        name : str, optional
            Name of the constraint.
        i_marker : Marker, optional
            I-marker.
        j_marker : Marker, optional
            J-marker.
        i_marker_name : str, optional
            Full name of the I-marker.
        j_marker_name : str, optional
            Full name of the J-marker.
        """
        ...

    def createPointPoint(self,
                         name: str = None,

                         i_marker: Marker.Marker = None,
                         j_marker: Marker.Marker = None,
                         i_marker_name: str = None,
                         j_marker_name: str = None,
                         **kwargs) -> PointPointJPrim:
        """Create a point-to-point distance (JPRIM) constraint.

        Constrains the distance between the origins of the I-marker and
        J-marker to a constant value.

        Parameters
        ----------
        name : str, optional
            Name of the constraint.
        i_marker : Marker, optional
            I-marker.
        j_marker : Marker, optional
            J-marker.
        i_marker_name : str, optional
            Full name of the I-marker.
        j_marker_name : str, optional
            Full name of the J-marker.
        """
        ...

    def createPointLine(self,
                        name: str = None,

                        i_marker: Marker.Marker = None,
                        j_marker: Marker.Marker = None,
                        i_marker_name: str = None,
                        j_marker_name: str = None,
                        **kwargs) -> PointLineConstraint:
        """Create a point-to-line distance (JPRIM) constraint.

        Constrains the perpendicular distance from the origin of the I-marker
        to the z-axis of the J-marker to a constant value.

        Parameters
        ----------
        name : str, optional
            Name of the constraint.
        i_marker : Marker, optional
            I-marker (point).
        j_marker : Marker, optional
            J-marker (its z-axis defines the line).
        i_marker_name : str, optional
            Full name of the I-marker.
        j_marker_name : str, optional
            Full name of the J-marker.
        """
        ...

    def createPointPlane(self,
                         name: str = None,

                         i_marker: Marker.Marker = None,
                         j_marker: Marker.Marker = None,
                         i_marker_name: str = None,
                         j_marker_name: str = None,
                         **kwargs) -> PointPlaneConstraint:
        """Create a point-to-plane distance (JPRIM) constraint.

        Constrains the perpendicular distance from the origin of the I-marker
        to the x-y plane of the J-marker to a constant value.

        Parameters
        ----------
        name : str, optional
            Name of the constraint.
        i_marker : Marker, optional
            I-marker (point).
        j_marker : Marker, optional
            J-marker (its x-y plane defines the constraint plane).
        i_marker_name : str, optional
            Full name of the I-marker.
        j_marker_name : str, optional
            Full name of the J-marker.
        """
        ...

    def createLineLine(self,
                       name: str = None,

                       i_marker: Marker.Marker = None,
                       j_marker: Marker.Marker = None,
                       i_marker_name: str = None,
                       j_marker_name: str = None,
                       **kwargs) -> LineLineConstraint:
        """Create a line-to-line distance (JPRIM) constraint.

        Constrains the perpendicular distance between the z-axes of the
        I-marker and J-marker to a constant value.

        Parameters
        ----------
        name : str, optional
            Name of the constraint.
        i_marker : Marker, optional
            I-marker (its z-axis defines the first line).
        j_marker : Marker, optional
            J-marker (its z-axis defines the second line).
        i_marker_name : str, optional
            Full name of the I-marker.
        j_marker_name : str, optional
            Full name of the J-marker.
        """
        ...

    def createLinePlane(self,
                        name: str = None,

                        i_marker: Marker.Marker = None,
                        j_marker: Marker.Marker = None,
                        i_marker_name: str = None,
                        j_marker_name: str = None,
                        **kwargs) -> LinePlaneConstraint:
        """Create a line-to-plane distance (JPRIM) constraint.

        Constrains the perpendicular distance from the z-axis of the I-marker
        to the x-y plane of the J-marker to a constant value.

        Parameters
        ----------
        name : str, optional
            Name of the constraint.
        i_marker : Marker, optional
            I-marker (its z-axis defines the line).
        j_marker : Marker, optional
            J-marker (its x-y plane defines the constraint plane).
        i_marker_name : str, optional
            Full name of the I-marker.
        j_marker_name : str, optional
            Full name of the J-marker.
        """
        ...

    def createPlanePlane(self,
                         name: str = None,

                         i_marker: Marker.Marker = None,
                         j_marker: Marker.Marker = None,
                         i_marker_name: str = None,
                         j_marker_name: str = None,
                         **kwargs) -> PlanePlaneConstraint:
        """Create a plane-to-plane distance (JPRIM) constraint.

        Constrains the perpendicular distance between the x-y planes of the
        I-marker and J-marker to a constant value.

        Parameters
        ----------
        name : str, optional
            Name of the constraint.
        i_marker : Marker, optional
            I-marker (its x-y plane defines the first plane).
        j_marker : Marker, optional
            J-marker (its x-y plane defines the second plane).
        i_marker_name : str, optional
            Full name of the I-marker.
        j_marker_name : str, optional
            Full name of the J-marker.
        """
        ...

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
                         **kwargs) -> PointCurveConstraint:
        """Create a point-on-curve constraint.

        Constrains the origin of the I-marker to remain on a specified curve.

        Parameters
        ----------
        name : str, optional
            Name of the constraint.
        i_marker : Marker, optional
            I-marker (the constrained point).
        i_marker_name : str, optional
            Full name of the I-marker.
        j_floating_marker : Marker, optional
            Floating J-marker that tracks the contact point on the curve.
        j_floating_marker_name : str, optional
            Full name of the floating J-marker.
        ref_marker : Marker, optional
            Reference marker that defines the curve coordinate system.
            If omitted, Adams derives it from the curve data.
        ref_marker_name : str, optional
            Full name of the reference marker.
        displacement_ic : float, optional
            Initial x, y, z coordinates of the contact point on the curve.
        velocity_ic : float, optional
            Initial velocity along the curve.
        ic_ref_marker : Marker, optional
            Reference marker for initial conditions.
        ic_ref_marker_name : str, optional
            Full name of the IC reference marker.
        curve : CurveData, optional
            Curve data element object.
        curve_name : str, optional
            Full name of the curve data element.
        """
        ...

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
                         **kwargs) -> CurveCurveConstraint:
        """Create a curve-on-curve constraint.

        Constrains a point on the I-side curve to remain in contact with a
        point on the J-side curve.

        Parameters
        ----------
        name : str, optional
            Name of the constraint.
        i_curve : CurveData, optional
            I-side curve data element object.
        i_curve_name : str, optional
            Full name of the I-side curve data element.
        i_floating_marker : Marker, optional
            Floating I-marker that tracks the contact point on the I-side curve.
        i_floating_marker_name : str, optional
            Full name of the floating I-marker.
        i_ref_marker : Marker, optional
            Reference marker for the I-side curve coordinate system.
            If omitted, Adams derives it from the curve data.
        i_ref_marker_name : str, optional
            Full name of the I-side reference marker.
        i_ic_ref_marker : Marker, optional
            Reference marker for I-side initial conditions.
        i_ic_ref_marker_name : str, optional
            Full name of the I-side IC reference marker.
        i_displacement_ic : float, optional
            Initial contact point coordinates on the I-side curve.
        i_velocity_ic : float, optional
            Initial velocity along the I-side curve.
        j_curve : CurveData, optional
            J-side curve data element object.
        j_curve_name : str, optional
            Full name of the J-side curve data element.
        j_floating_marker : Marker, optional
            Floating J-marker that tracks the contact point on the J-side curve.
        j_floating_marker_name : str, optional
            Full name of the floating J-marker.
        j_ref_marker : Marker, optional
            Reference marker for the J-side curve coordinate system.
        j_ref_marker_name : str, optional
            Full name of the J-side reference marker.
        j_ic_ref_marker : Marker, optional
            Reference marker for J-side initial conditions.
        j_ic_ref_marker_name : str, optional
            Full name of the J-side IC reference marker.
        j_displacement_ic : float, optional
            Initial contact point coordinates on the J-side curve.
        j_velocity_ic : float, optional
            Initial velocity along the J-side curve.
        """
        ...

    def createUserDefined(self,
                          name: str = None,
                          user_function: str = None,
                          routine: str = None,
                          **kwargs) -> UserDefinedConstraint:
        """Create a user-defined constraint.

        Parameters
        ----------
        name : str, optional
            Name of the constraint.
        user_function : str, optional
            Array of values passed to the user subroutine.
        routine : str, optional
            Name of the user subroutine.
        """
        ...

    def createAngle(self,
                    name: str = None,
                    i_marker: Marker.Marker = None,
                    j_marker: Marker.Marker = None,
                    i_marker_name: str = None,
                    j_marker_name: str = None,
                    offset: float = None,
                    **kwargs) -> AngleConstraint:
        """Create an angle (JPRIM) constraint.

        Parameters
        ----------
        name : str, optional
            Name of the angle constraint.
        i_marker : Marker, optional
            Action marker.
        j_marker : Marker, optional
            Reaction marker.
        i_marker_name : str, optional
            Full name of the action marker.
        j_marker_name : str, optional
            Full name of the reaction marker.
        offset : float, optional
            Angle offset in degrees.
        """
        ...

    def switch_type(self, **kwargs): ...
    def items(self) -> ItemsView[str, Constraint]: ...
    def values(self) -> ValuesView[Constraint]: ...
    def keys(self) -> KeysView[str]: ...
    def __getitem__(self, name) -> Constraint: ...
    def __iter__(self, *args) -> Iterable[str]: ...

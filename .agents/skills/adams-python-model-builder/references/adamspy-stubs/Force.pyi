import Manager
import Object
import DataElement
from Marker import _i_j_parts_from_markers as _i_j_parts, _loc_ori_provider as _loc_ori, Marker, FloatingMarker
from typing import ItemsView, Iterable, KeysView, List, Literal, ValuesView
from Part import Part, FlexBody


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
    """Force function in the x direction."""
    y_force_function: str
    """Force function in the y direction."""
    z_force_function: str
    """Force function in the z direction."""
    user_function: List[float | int]
    routine: str
    xyz_force_function: str
    """Vector force function for the x, y, and z directions."""


class TorqueVector(Force):
    i_marker_name: str
    i_marker: Marker
    j_floating_marker_name: str
    j_floating_marker: Marker
    ref_marker_name: str
    ref_marker: Marker
    x_torque_function: str
    """Torque function about the x axis."""
    y_torque_function: str
    """Torque function about the y axis."""
    z_torque_function: str
    """Torque function about the z axis."""
    user_function: List[float | int]
    routine: str
    xyz_torque_function: str
    """Vector torque function about the x, y, and z axes."""


class RotationalSpringDamper(Force, _force_i_j_parts, _loc_ori):
    i_marker: Marker
    j_marker: Marker
    i_marker_name: str
    j_marker_name: str
    displacement_at_preload: float
    """Angular displacement at the preload (degrees)."""
    torque_preload: float
    """Torque preload."""
    angle: float
    """Free angle (degrees)."""
    r_damp: float
    """Torsional damping coefficient."""
    r_stiff: float
    """Torsional stiffness coefficient."""


class TranslationalSpringDamper(Force, _force_i_j_parts, _loc_ori):
    i_marker: Marker
    j_marker: Marker
    i_marker_name: str
    j_marker_name: str
    force_preload: float
    """Force preload."""
    stiffness: float
    """Translational stiffness coefficient."""
    damping: float
    """Translational damping coefficient."""
    displacement_at_preload: float
    """Translational displacement at preload."""


class Bushing(Force, _force_i_j_parts, _loc_ori):
    i_marker: Marker
    j_marker: Marker
    i_marker_name: str
    j_marker_name: str
    force_preload: List[float]
    """List of force preloads in the x, y, and z directions."""
    stiffness: List[float]
    """List of translational stiffness values in the x, y, and z directions."""
    damping: List[float]
    """List of translational damping values about the x, y, and z axes."""
    tdamping: List[float]
    """List of rotational damping values about the x, y, and z axes."""
    tstiffness: List[float]
    """List of rotational stiffness values in the x, y, and z directions."""
    torque_preload: List[float]
    """List of torque preloads about the x, y, and z axes."""


class SingleComponentForce(Force, _force_i_j_parts, _loc_ori):
    i_marker: Marker
    j_marker: Marker
    i_marker_name: str
    j_marker_name: str
    user_function: List[float | int]
    function: str
    """Function expression for the single-component force."""
    action_only: bool
    """If True, the force is an action-only force (no reaction on the j part)."""
    routine: str
    type_of_freedom: Literal['translational', 'rotational']
    """Specifies whether the force is translational or rotational."""


class Beam(Force, _force_i_j_parts, _loc_ori):
    i_marker: Marker
    j_marker: Marker
    i_marker_name: str
    j_marker_name: str
    length: float
    """Beam length."""
    damping_ratio: float
    """Damping ratio for the beam."""
    matrix_of_damping_terms: List[float]
    """List of 21 damping matrix terms (upper triangle of the 6x6 matrix)."""
    shear_modulus: float
    """Shear modulus for the beam."""
    youngs_modulus: float
    """Young's modulus for the beam."""
    ixx: float
    """Ixx second moment of area for the beam cross-section."""
    iyy: float
    """Iyy second moment of area for the beam cross-section."""
    izz: float
    """Izz second moment of area for the beam cross-section."""
    area_of_cross_section: float
    """Cross-sectional area of the beam."""
    y_shear_area_ratio: float
    """Y-direction shear area ratio for the beam."""
    z_shear_area_ratio: float
    """Z-direction shear area ratio for the beam."""
    formulation: Literal['linear', 'string', 'nonlinear']
    """Beam formulation type."""


class Field(Force, _force_i_j_parts, _loc_ori):
    i_marker: Marker
    j_marker: Marker
    i_marker_name: str
    j_marker_name: str
    force_preload: List[float]
    """List of force preloads in the x, y, and z directions."""
    torque_preload: List[float]
    """List of torque preloads about the x, y, and z axes."""
    damping_ratio: float
    """Scalar damping ratio; mutually exclusive with matrix_of_damping_terms."""
    matrix_of_damping_terms: List[float]
    """List of 36 terms in the 6x6 damping matrix; mutually exclusive with damping_ratio."""
    stiffness_matrix: List[float]
    """List of 36 terms in the 6x6 stiffness matrix."""
    user_function: List[float | int]
    routine: str
    formulation: Literal['linear', 'nonlinear']
    """Field force formulation type."""
    length_tol: float
    """When using formulation='nonlinear', the geometric stiffness uses the larger of the current length and this length tolerance."""
    translation_at_preload: List[float]
    """Nominal position [x, y, z] of the I marker with respect to the J marker at preload, resolved in the J marker coordinate system."""
    rotation_at_preload: List[float]
    """Rotational displacement [rx, ry, rz] of the I marker axes with respect to the J marker at preload, resolved in the J marker coordinate system."""


class Friction(Force):
    """Joint friction force. Create via ``model.Forces.createFriction()``."""
    joint_types: List[str]
    joint_name: str
    joint: Object.Object
    mu_static: float
    """Coefficient of static friction."""
    mu_dynamic: float
    """Coefficient of dynamic friction."""
    yoke: Literal['yoke_i', 'yoke_j']
    """Specifies the i or j yoke in a Hooke or Universal joint."""
    formulation: Literal['original', 'lugre']
    """Friction formulation of the joint."""
    reaction_arm: float
    """Reaction arm length."""
    friction_arm: float
    """Effective moment arm used to compute the axial component of the friction torque in revolute, hooke, and universal joints."""
    bending_reaction_arm: float
    """Effective moment arm used to compute the contribution of the bending moment on the net friction torque in revolute, hooke, and universal joints."""
    initial_overlap: float
    """Initial overlap of the sliding parts in a translational or cylindrical joint."""
    pin_radius: float
    """Radius of the pin for a revolute, cylindrical, hooke, or universal joint."""
    ball_radius: float
    """Radius of the ball in a spherical joint, used in friction force and torque calculation."""
    stiction_transition_velocity: float
    """Absolute velocity threshold for the transition from dynamic friction to static friction."""
    transition_velocity_coefficient: float
    """Coefficient of velocity threshold for the transition from dynamic friction to static friction."""
    max_stiction_deformation: float
    """Maximum creep that can occur in a joint during the stiction regime."""
    bristle_stiffness_coefficient: float
    """Bristle stiffness coefficient in a joint friction model (LuGre only)."""
    damping_coefficient: float
    """Damping coefficient in a joint friction model (LuGre only)."""
    viscous_friction_coefficient: float
    """Viscous friction coefficient in a joint friction model (LuGre only)."""
    velocity_threshold_stribeck: float
    """Stribeck threshold velocity in a joint friction model (LuGre only)."""
    decay_exponent_stribeck: float
    """Stribeck decay exponent in a joint friction model (LuGre only)."""
    friction_force_preload: float
    """Joint preload frictional force, typically caused by mechanical interference in the assembly of the joint."""
    friction_torque_preload: float
    """Preload friction torque in the joint, typically caused by mechanical interference in the assembly of the joint."""
    max_friction_force: float
    """Maximum friction force, for use in translational or cylindrical joints."""
    max_friction_torque: float
    """Maximum friction torque, for use in revolute, universal, hooke, spherical, or cylindrical joints."""
    overlap_delta: Literal['increase', 'decrease', 'constant']
    """Change in overlap for a translational or cylindrical joint."""
    effect: Literal['all', 'stiction', 'sliding']
    """Frictional effects included in the friction model."""
    smooth: float
    """Smoothing coefficient for the friction model."""
    torsional_moment: bool
    """Whether to include torsional moment contribution in friction (for use with inputs)."""
    bending_moment: bool
    """Whether to include bending moment contribution in friction (for use with inputs)."""
    preload: bool
    """Whether to include preload contribution in friction (for use with inputs)."""
    reaction_force: bool
    """Whether to include reaction force contribution in friction (for use with inputs)."""
    inactive_during_static: bool
    """If True, frictional forces are not calculated during static or quasi-static solutions."""


class ModalForce(Force):
    flexible_body: FlexBody
    """Flexible body that this modal force acts on."""
    flexible_body_name: str
    """Full name of the flexible body that this modal force acts on."""
    reaction_part: FloatingMarker
    reaction_part_name: str
    user_function: List[float | int]
    routine: str
    scale_function: str
    """Expression for the scale factor applied to the load case referenced by load_case."""
    load_case: int
    """Modal load case number that defines the ModalForce."""
    force_function: List[float]
    """Function values specifying the ModalForce."""


class GeneralForce(Force):
    i_marker_name: str
    j_floating_marker_name: str
    ref_marker_name: str
    i_marker: Marker
    j_floating_marker: Marker
    ref_marker: Marker
    x_force_function: str
    """Force function expression in the x direction."""
    y_force_function: str
    """Force function expression in the y direction."""
    z_force_function: str
    """Force function expression in the z direction."""
    x_torque_function: str
    """Torque function expression about the x axis."""
    y_torque_function: str
    """Torque function expression about the y axis."""
    z_torque_function: str
    """Torque function expression about the z axis."""
    user_function: List[float | int]
    routine: str
    xyz_force_function: str
    """Vector force function expression for the x, y, and z directions."""
    xyz_torque_function: str
    """Vector torque function expression about the x, y, and z axes."""


class MultiPointForce(Force):
    i_marker_names: List[str]
    j_marker_name: str
    i_markers: List[Marker]
    j_marker: Marker
    stiffness_matrix_name: str
    """Name of the stiffness matrix data element."""
    damping_matrix_name: str
    """Name of the damping matrix data element."""
    stiffness_matrix: DataElement.Matrix
    """Stiffness matrix data element object."""
    damping_matrix: DataElement.Matrix
    """Damping matrix data element object."""
    damping_ratio: float
    """Scalar damping ratio."""
    length_matrix_name: str
    """Name of the length matrix data element."""
    force_matrix_name: str
    """Name of the force matrix data element."""
    length_matrix: DataElement.Matrix
    """Length matrix data element object."""
    force_matrix: DataElement.Matrix
    """Force matrix data element object."""


class ForceManager(Manager.SubclassManager):
    def items(self) -> ItemsView[str, Force]: ...
    def values(self) -> ValuesView[Force]: ...
    def keys(self) -> KeysView[str]: ...
    def __getitem__(self, name) -> Force: ...
    def __iter__(self, *args) -> Iterable[str]: ...

    def createGravity(self,
                      name: str = None,
                      xyz_component_gravity: List[float] = None) -> Gravity:
        """Create a gravity force.

        Parameters
        ----------
        name : str, optional
            Name of the gravity force.
        xyz_component_gravity : list of float, optional
            Gravity acceleration components [x, y, z].
        """
        ...

    def createForceVector(self,
                          name: str = None,
                          adams_id: int = None,
                          comments: str = None,
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
                          **kwargs) -> GeneralForce:
        """Create a force vector.

        Specify either component functions (``x/y/z_force_function``) or a
        single vector function (``xyz_force_function``), but not both.

        Parameters
        ----------
        name : str, optional
            Name of the force vector.
        adams_id : int, optional
            Adams ID.
        comments : str, optional
            Comments for the force element.
        i_marker : Marker, optional
            Action marker.
        i_marker_name : str, optional
            Full name of the action marker.
        j_floating_marker : Marker, optional
            Reaction floating marker.
        j_floating_marker_name : str, optional
            Full name of the reaction floating marker.
        j_part : Part, optional
            Reaction part (creates floating marker automatically).
        j_part_name : str, optional
            Full name of the reaction part.
        ref_marker : Marker, optional
            Reference frame marker.
        ref_marker_name : str, optional
            Full name of the reference marker.
        x_force_function : str, optional
            Expression for the x-component of force.
        y_force_function : str, optional
            Expression for the y-component of force.
        z_force_function : str, optional
            Expression for the z-component of force.
        x_torque_function : str, optional
            Expression for the x-component of torque.
        y_torque_function : str, optional
            Expression for the y-component of torque.
        z_torque_function : str, optional
            Expression for the z-component of torque.
        xyz_force_function : str, optional
            Single expression for the force vector.
        xyz_torque_function : str, optional
            Single expression for the torque vector.
        user_function : str, optional
            User function values.
        routine : str, optional
            Name of the user subroutine.
        """
        ...

    def createTorqueVector(self,
                           name: str = None,
                           i_marker: Marker = None,
                           i_marker_name: str = None,
                           j_floating_marker: Marker = None,
                           j_floating_marker_name: str = None,
                           ref_marker: Marker = None,
                           ref_marker_name: str = None,
                           x_torque_function: str = None,
                           y_torque_function: str = None,
                           z_torque_function: str = None,
                           xyz_torque_function: str = None,
                           user_function: str = None,
                           routine: str = None,
                           **kwargs) -> TorqueVector:
        """Create a torque vector force.

        Specify either component functions (``x/y/z_torque_function``) or a
        single vector function (``xyz_torque_function``), but not both.

        Parameters
        ----------
        name : str, optional
            Name of the torque vector.
        i_marker : Marker, optional
            Action marker.
        i_marker_name : str, optional
            Full name of the action marker.
        j_floating_marker : Marker, optional
            Reaction floating marker.
        j_floating_marker_name : str, optional
            Full name of the reaction floating marker.
        ref_marker : Marker, optional
            Reference frame marker.
        ref_marker_name : str, optional
            Full name of the reference marker.
        x_torque_function : str, optional
            Expression for the x-component of torque.
        y_torque_function : str, optional
            Expression for the y-component of torque.
        z_torque_function : str, optional
            Expression for the z-component of torque.
        xyz_torque_function : str, optional
            Single expression for the torque vector.
        user_function : str, optional
            User function values.
        routine : str, optional
            Name of the user subroutine.
        """
        ...

    def createRotationalSpringDamper(self,
                                     name: str = None,
                                     i_marker: Marker = None,
                                     j_marker: Marker = None,
                                     i_marker_name: str = None,
                                     j_marker_name: str = None,
                                     torque_preload: float = None,
                                     displacement_at_preload: float = None,
                                     angle: float = None,
                                     r_damp: float = None,
                                     r_stiff: float = None,
                                     **kwargs) -> RotationalSpringDamper:
        """Create a rotational spring-damper force.

        Parameters
        ----------
        name : str, optional
            Name of the rotational spring-damper.
        i_marker : Marker, optional
            Action marker.
        j_marker : Marker, optional
            Reaction marker.
        i_marker_name : str, optional
            Full name of the action marker.
        j_marker_name : str, optional
            Full name of the reaction marker.
        torque_preload : float, optional
            Torque preload value.
        displacement_at_preload : float, optional
            Angular displacement at preload.
        angle : float, optional
            Free angle.
        r_damp : float, optional
            Torsional damping coefficient.
        r_stiff : float, optional
            Torsional stiffness coefficient.
        """
        ...

    def createTranslationalSpringDamper(self,
                                        name: str = None,
                                        i_marker: Marker = None,
                                        j_marker: Marker = None,
                                        i_marker_name: str = None,
                                        j_marker_name: str = None,
                                        force_preload: float = None,
                                        stiffness: float = None,
                                        damping: float = None,
                                        displacement_at_preload: float = None,
                                        **kwargs) -> TranslationalSpringDamper:
        """Create a translational spring-damper force.

        Parameters
        ----------
        name : str, optional
            Name of the translational spring-damper.
        i_marker : Marker, optional
            Action marker.
        j_marker : Marker, optional
            Reaction marker.
        i_marker_name : str, optional
            Full name of the action marker.
        j_marker_name : str, optional
            Full name of the reaction marker.
        force_preload : float, optional
            Force preload value.
        stiffness : float, optional
            Linear stiffness coefficient.
        damping : float, optional
            Linear damping coefficient.
        displacement_at_preload : float, optional
            Length at which the preload acts.
        """
        ...

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
                      **kwargs) -> Bushing:
        """Create a bushing (six-component spring-damper) force.

        Parameters
        ----------
        i_marker : Marker, optional
            Action marker.
        j_marker : Marker, optional
            Reaction marker.
        i_marker_name : str, optional
            Full name of the action marker.
        j_marker_name : str, optional
            Full name of the reaction marker.
        force_preload : list of float, optional
            Translational force preload [fx, fy, fz].
        stiffness : list of float, optional
            Translational stiffness coefficients [kx, ky, kz].
        damping : list of float, optional
            Translational damping coefficients [cx, cy, cz].
        tdamping : list of float, optional
            Torsional damping coefficients [ctx, cty, ctz].
        tstiffness : list of float, optional
            Torsional stiffness coefficients [ktx, kty, ktz].
        torque_preload : list of float, optional
            Torsional torque preload [tx, ty, tz].
        """
        ...

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
                                   **kwargs) -> SingleComponentForce:
        """Create a single-component force or torque.

        Parameters
        ----------
        name : str
            Name of the force.
        function : str, optional
            Expression defining the force/torque magnitude.
        i_marker : Marker, optional
            Action marker. Mutually exclusive with ``i_part``.
        j_marker : Marker, optional
            Reaction marker. Mutually exclusive with ``j_part``.
        i_marker_name : str, optional
            Full name of the action marker.
        j_marker_name : str, optional
            Full name of the reaction marker.
        i_part : Part, optional
            Action part (Adams auto-creates marker). Mutually exclusive with ``i_marker``.
        j_part : Part, optional
            Reaction part. Mutually exclusive with ``j_marker``.
        i_part_name : str, optional
            Full name of the action part.
        j_part_name : str, optional
            Full name of the reaction part.
        action_only : bool, optional
            If True, force acts on the I-part only (no reaction on J).
        location : list of float, optional
            [x, y, z] coordinates for auto-created markers.
        orientation : list of float, optional
            [psi, theta, phi] Euler angles for auto-created markers.
        type_of_freedom : str, optional
            ``'translational'`` (default) or ``'rotational'``.
        relative_to : Marker, optional
            Reference frame for ``location`` and ``orientation``.
        """
        ...

    def createAppliedTorque(self,
                            name: str = None,
                            i_marker: Marker = None,
                            j_marker: Marker = None,
                            i_marker_name: str = None,
                            j_marker_name: str = None,
                            **kwargs) -> AppliedTorque:
        """Create an applied torque force.

        Parameters
        ----------
        name : str, optional
            Name of the applied torque.
        i_marker : Marker, optional
            Action marker.
        j_marker : Marker, optional
            Reaction marker.
        i_marker_name : str, optional
            Full name of the action marker.
        j_marker_name : str, optional
            Full name of the reaction marker.
        """
        ...

    def createAppliedForce(self,
                           name: str = None,
                           i_marker: Marker = None,
                           j_marker: Marker = None,
                           i_marker_name: str = None,
                           j_marker_name: str = None,
                           **kwargs) -> AppliedForce:
        """Create an applied force.

        Parameters
        ----------
        name : str, optional
            Name of the applied force.
        i_marker : Marker, optional
            Action marker.
        j_marker : Marker, optional
            Reaction marker.
        i_marker_name : str, optional
            Full name of the action marker.
        j_marker_name : str, optional
            Full name of the reaction marker.
        """
        ...

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
                   **kwargs) -> Beam:
        """Create a linear beam force element (BEAM).

        Represents the elastic compliance of a slender beam using Euler-Bernoulli
        or Timoshenko beam theory.

        Parameters
        ----------
        name : str
            Name of the beam element.
        i_marker : Marker, optional
            I-marker (attached to the I-end of the beam).
        j_marker : Marker, optional
            J-marker (attached to the J-end of the beam).
        i_marker_name : str, optional
            Full name of the I-marker.
        j_marker_name : str, optional
            Full name of the J-marker.
        length : float, optional
            Unstressed length of the beam. Defaults to the I-J marker distance.
        damping_ratio : float, optional
            Damping ratio. Mutually exclusive with ``matrix_of_damping_terms``.
        matrix_of_damping_terms : list of float, optional
            36-element damping matrix.
        shear_modulus : float, optional
            Shear modulus (G).
        youngs_modulus : float, optional
            Young's modulus (E).
        ixx : float, optional
            Area moment of inertia about the x-axis (torsion).
        iyy : float, optional
            Area moment of inertia about the y-axis (bending).
        izz : float, optional
            Area moment of inertia about the z-axis (bending).
        area_of_cross_section : float, optional
            Cross-sectional area.
        y_shear_area_ratio : float, optional
            Ratio of shear area to total area for y-direction shear.
        z_shear_area_ratio : float, optional
            Ratio of shear area to total area for z-direction shear.
        formulation : str, optional
            ``'timoshenko'`` (includes shear deformation) or ``'euler'`` (default).
        """
        ...

    def createField(self,
                    name: str = None,
                    i_marker: Marker = None,
                    j_marker: Marker = None,
                    i_marker_name: str = None,
                    j_marker_name: str = None,
                    force_preload: List[float] = None,
                    torque_preload: List[float] = None,
                    damping_ratio: float = None,
                    matrix_of_damping_terms: List[float] = None,
                    stiffness_matrix: List[float] = None,
                    user_function: str = None,
                    routine: str = None,
                    formulation: str = None,
                    length_tol: float = None,
                    translation_at_preload: List[float] = None,
                    rotation_at_preload: List[float] = None,
                    **kwargs) -> Field:
        """Create a field force element.

        Parameters
        ----------
        name : str, optional
            Name of the field.
        i_marker : Marker, optional
            Action marker.
        j_marker : Marker, optional
            Reaction marker.
        i_marker_name : str, optional
            Full name of the action marker.
        j_marker_name : str, optional
            Full name of the reaction marker.
        force_preload : list of float, optional
            Force preload [fx, fy, fz].
        torque_preload : list of float, optional
            Torque preload [tx, ty, tz].
        damping_ratio : float, optional
            Damping ratio. Mutually exclusive with ``matrix_of_damping_terms``.
        matrix_of_damping_terms : list of float, optional
            36-element damping matrix. Mutually exclusive with ``damping_ratio``.
        stiffness_matrix : list of float, optional
            36-element stiffness matrix.
        user_function : str, optional
            User function values.
        routine : str, optional
            Name of the user subroutine.
        formulation : str, optional
            ``'linear'`` or ``'nonlinear'``.
        length_tol : float, optional
            Geometric stiffness tolerance (default 1e-5).
        translation_at_preload : list of float, optional
            Translational preload offset [x, y, z].
        rotation_at_preload : list of float, optional
            Rotational preload offset [x, y, z] in degrees.
        """
        ...

    def createFriction(self,
                       name: str = None,
                       joint: 'Constraint' = None,
                       joint_name: str = None,
                       mu_static: float = None,
                       mu_dynamic: float = None,
                       yoke: str = None,
                       pin_radius: float = None,
                       **kwargs) -> Friction:
        """Create a friction force on a joint.

        Parameters
        ----------
        name : str, optional
            Name of the friction element.
        joint : Joint, optional
            Joint object to apply friction to.
        joint_name : str, optional
            Full name of the joint.
        mu_static : float, optional
            Coefficient of static friction.
        mu_dynamic : float, optional
            Coefficient of dynamic friction.
        yoke : str, optional
            ``'yoke_i'`` or ``'yoke_j'`` (for Hooke/Universal joints).
        pin_radius : float, optional
            Pin radius for friction calculation.
        """
        ...

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
                         **kwargs) -> ModalForce:
        """Create a modal force element on a flexible body.

        Parameters
        ----------
        name : str, optional
            Name of the modal force.
        flexible_body : FlexBody, optional
            Flexible body to apply the force to.
        flexible_body_name : str, optional
            Full name of the flexible body.
        reaction_part : FloatingMarker, optional
            Reaction part or floating marker.
        reaction_part_name : str, optional
            Full name of the reaction part.
        user_function : str, optional
            Values passed to the user subroutine.
        routine : str, optional
            Name of the user subroutine.
        scale_function : str, optional
            Expression to scale the modal force.
        load_case : optional
            Load case object or identifier.
        force_function : str, optional
            Expression defining the force magnitude.
        """
        ...

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
                           **kwargs) -> ForceVector:
        """Create a general force vector element.

        Specify either component functions (``x/y/z_force_function``) or a
        single vector function (``xyz_force_function``), but not both.

        Parameters
        ----------
        name : str
            Name of the general force.
        adams_id : int
            Adams ID.
        comments : str
            Comments for the force element.
        i_marker : Marker, optional
            Action marker.
        i_marker_name : str, optional
            Full name of the action marker.
        j_floating_marker : Marker, optional
            Reaction floating marker.
        j_floating_marker_name : str, optional
            Full name of the reaction floating marker.
        ref_marker : Marker, optional
            Reference frame marker for component resolution.
        ref_marker_name : str, optional
            Full name of the reference marker.
        x_force_function : str, optional
            Expression for the x-component of force.
        y_force_function : str, optional
            Expression for the y-component of force.
        z_force_function : str, optional
            Expression for the z-component of force.
        xyz_force_function : str, optional
            Single expression for the full force vector.
        user_function : str, optional
            User function values.
        routine : str, optional
            Name of the user subroutine.
        """
        ...

    def createMultiPointForce(self,
                              name: str = None,
                              i_markers: List[Marker] = None,
                              i_marker_names: List[str] = None,
                              j_marker: Marker = None,
                              j_marker_name: str = None,
                              **kwargs) -> MultiPointForce:
        """Create a multi-point force element.

        Parameters
        ----------
        name : str, optional
            Name of the multi-point force.
        i_markers : list of Marker, optional
            List of action markers (1-350).
            Mutually exclusive with ``i_marker_names``.
        i_marker_names : list of str, optional
            Full names of the action markers.
        j_marker : Marker, optional
            Reaction marker.
        j_marker_name : str, optional
            Full name of the reaction marker.
        """
        ...

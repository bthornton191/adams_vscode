import Manager
import Object
from DBAccess import set_locori_expression as set_locori_expression
from Marker import MarkerManager, Marker
from DesignPoint import DesignPointManager
from Geometry import GeometryManager
from Expression import AdamsExpr as AdamsExpr
from typing import Any, ItemsView, Iterable, KeysView, List, Literal, Optional, ValuesView


class Part(Object.Object):
    Markers: MarkerManager
    DesignPoints: DesignPointManager
    FloatingMarkers: MarkerManager
    Geometries: GeometryManager
    def __init__(self, _DBKey) -> None: ...
    ground_part: bool
    is_flexible: bool
    def destroy(self): ...
    relative_to: Object.Object
    orientation: List[float]
    location: List[float]
    along_axis_orientation: List[float]
    in_plane_orientation: List[float]
    cm: Marker


class RigidBody(Part):
    mass: float
    """Mass of the rigid body."""
    cm: Marker
    """Center of mass marker object."""
    cm_name: str
    """Full name of the center of mass marker."""
    im: Marker
    """Inertial marker object. Inertia tensor components are expressed in this frame."""
    im_name: str
    """Full name of the inertial marker."""
    vx: float
    """Initial translational velocity along the vm marker x axis."""
    vy: float
    """Initial translational velocity along the vm marker y axis."""
    vz: float
    """Initial translational velocity along the vm marker z axis."""
    ixx: float
    """Ixx component of the mass-inertia tensor expressed in the im marker frame."""
    iyy: float
    """Iyy component of the mass-inertia tensor expressed in the im marker frame."""
    izz: float
    """Izz component of the mass-inertia tensor expressed in the im marker frame."""
    ixy: float
    """Ixy component of the mass-inertia tensor expressed in the im marker frame."""
    izx: float
    """Izx component of the mass-inertia tensor expressed in the im marker frame."""
    iyz: float
    """Iyz component of the mass-inertia tensor expressed in the im marker frame."""
    wx: float
    """Initial angular velocity about the wm marker x axis."""
    wy: float
    """Initial angular velocity about the wm marker y axis."""
    wz: float
    """Initial angular velocity about the wm marker z axis."""
    wm: Optional[Marker]
    """Marker about which initial angular velocities are specified."""
    wm_name: str
    """Full name of the angular velocity reference marker."""
    vm: Optional[Marker]
    """Marker along whose axes initial translational velocities are specified."""
    vm_name: str
    """Full name of the translational velocity reference marker."""
    exact_x: bool
    """If True, the x location is held fixed during initial conditions computation."""
    exact_y: bool
    """If True, the y location is held fixed during initial conditions computation."""
    exact_z: bool
    """If True, the z location is held fixed during initial conditions computation."""
    exact_psi: bool
    """If True, the psi (yaw) orientation is held fixed during initial conditions computation."""
    exact_theta: bool
    """If True, the theta (pitch) orientation is held fixed during initial conditions computation."""
    exact_phi: bool
    """If True, the phi (roll) orientation is held fixed during initial conditions computation."""
    planar: bool
    """If True, the rigid body is constrained to 3 degrees of freedom (planar motion)."""
    density: float
    """Density of the rigid body. Mutually exclusive with ``mass`` and ``material_type``."""
    material_type: Object.Object
    """Material object defining mass/inertia properties. Mutually exclusive with ``mass`` and ``density``."""
    Geometries: GeometryManager
    def __init__(self, _DBKey) -> None: ...
    inertia_values: List[float]
    """Inertia tensor as [Ixx, Iyy, Izz, Ixy, Ixz, Iyz]."""
    plane: Literal['xy', 'yz', 'zx']
    """Plane in which a planar rigid body moves."""


class FlexBody(Part):
    vx: float
    """Initial translational velocity along the vm marker x axis."""
    vy: float
    """Initial translational velocity along the vm marker y axis."""
    vz: float
    """Initial translational velocity along the vm marker z axis."""
    wx: float
    """Initial angular velocity about the wm marker x axis."""
    wy: float
    """Initial angular velocity about the wm marker y axis."""
    wz: float
    """Initial angular velocity about the wm marker z axis."""
    vm: Optional[Marker]
    """Marker along whose axes initial translational velocities are specified."""
    vm_name: str
    """Full name of the translational velocity reference marker."""
    wm: Optional[Marker]
    """Marker about which initial angular velocities are specified."""
    wm_name: str
    """Full name of the angular velocity reference marker."""
    md_db_file_name: str
    """Path to the MD DB file containing flexible body properties."""
    index_in_database: int
    """Index of the flexible body in the MD DB file."""
    damping_ratio: Optional[str]
    """Expression for modal damping as a ratio of critical damping."""
    damping_user_function: List[float | int]
    """Up to 30 values passed to the modal damping subroutine DMPSUB."""
    damping_routine: str
    """Name of the user modal damping subroutine DMPSUB."""
    dynamic_limit: float
    """Modes with frequencies above this limit (Hz) are treated as quasi-static modes."""
    exact_x: bool
    """If True, the x location is held fixed during initial conditions computation."""
    exact_y: bool
    """If True, the y location is held fixed during initial conditions computation."""
    exact_z: bool
    """If True, the z location is held fixed during initial conditions computation."""
    exact_psi: bool
    """If True, the psi (yaw) orientation is held fixed during initial conditions computation."""
    exact_theta: bool
    """If True, the theta (pitch) orientation is held fixed during initial conditions computation."""
    exact_phi: bool
    """If True, the phi (roll) orientation is held fixed during initial conditions computation."""
    invariants: List[bool]
    """Nine booleans controlling which Craig-Bampton invariant matrices are used."""
    characteristic_length: float
    """Reference length used to set the linear deformation limit (limit = 10% of this value)."""
    stability_factor: float
    """Adds proportional damping to modes when dynamic_limit is enabled. Default is 10.0."""
    exact_coordinates: List[int]
    """Deprecated. Use ``modal_exact_coordinates`` instead."""
    selected_modes: List[int]
    """List of selected mode numbers to include in the flexible body response."""
    modal_exact_coordinates: List[int]
    """Modal coordinates held fixed during initial conditions computation."""
    initial_modal_displacements: List[float]
    """Initial values of the modal displacement coordinates."""
    initial_modal_velocities: List[float]
    """Initial modal velocities."""
    node_count: int
    """Read-only. Number of nodes in the flexible body."""
    mode_count: int
    """Read-only. Number of modes in the flexible body."""
    modal_neutral_file_name: str
    """Path to the Modal Neutral File (.mnf) defining flexible body properties."""
    bdf_file_name: str
    """Path to the Nastran BDF file defining flexible body properties."""
    generalized_damping: Literal['off', 'full', 'internal_only']
    """Generalized damping formulation for the flexible body."""
    representation: Literal['rigid', 'modal', 'nonlinear', 'nforce']
    """Representation type for the flexible body."""

    def disable_modes_by_strain_energy(self, analysis: Any | None = ..., analysis_name: Any | None = ..., energy_tolerance: float = ...) -> None: ...


class PointMass(Part):
    vx: float
    """Initial translational velocity in the x direction of the vm marker."""
    vy: float
    """Initial translational velocity in the y direction of the vm marker."""
    vz: float
    """Initial translational velocity in the z direction of the vm marker."""
    cm: Marker
    """Center of mass marker object."""
    cm_name: str
    """Full name of the center of mass marker."""
    mass: float
    """Mass of the point mass. Mutually exclusive with ``density`` and ``material_type``."""
    vm: Optional[Marker]
    """Marker along whose axes initial translational velocities are specified."""
    vm_name: str
    """Full name of the translational velocity reference marker."""
    exact_x: bool
    """If True, the x initial velocity is held fixed during initial conditions computation."""
    exact_y: bool
    """If True, the y initial velocity is held fixed during initial conditions computation."""
    exact_z: bool
    """If True, the z initial velocity is held fixed during initial conditions computation."""
    material_type: Object.Object
    """Material object for this point mass. Mutually exclusive with ``mass`` and ``density``."""
    material_type_name: str
    """Full name of the material object for this point mass."""
    density: float
    """Density for this point mass. Mutually exclusive with ``mass`` and ``material_type``."""


class ExternalSystem(Part):
    Markers: MarkerManager
    def __init__(self, _DBKey) -> None: ...
    vx: float
    """Initial translational velocity along the x axis of the ground frame."""
    vy: float
    """Initial translational velocity along the y axis of the ground frame."""
    vz: float
    """Initial translational velocity along the z axis of the ground frame."""
    wx: float
    """Initial rotational velocity about the center-of-mass marker x axis."""
    wy: float
    """Initial rotational velocity about the center-of-mass marker y axis."""
    wz: float
    """Initial rotational velocity about the center-of-mass marker z axis."""
    wm: Optional[Marker]
    """Marker representing the rotational velocity reference frame."""
    wm_name: str
    """Full name of the rotational velocity reference marker."""
    vm: Optional[Marker]
    """Marker representing the translational velocity reference frame."""
    vm_name: str
    """Full name of the translational velocity reference marker."""
    modal_neutral_file_name: str
    """Optional MNF for a visual representation of the external system (rigid only)."""
    md_db_file_name: str
    """Optional MD DB for a visual representation of the external system."""
    index_in_database: int
    """Index of the body in the specified MD DB. Valid only when ``md_db_file_name`` is set."""
    interface_routines: str
    type: str
    """Type of external system (e.g. 'nastran')."""
    input_file_name: str
    """File containing input source parameters for the external system."""


class FEPart(Part):
    def addNode(self, s, **kwargs) -> None: ...
    def addNodeXYZ(self, x, y, z, **kwargs) -> None: ...
    def setUniformSection(self, sec) -> None: ...
    def setUniformAngle(self, ang) -> None: ...
    def evenlyDistributeNodes(self) -> None: ...
    def getNumNodes(self): ...
    def getNodeIndex(self, s): ...
    def modifyNode(self, index, **kwargs) -> None: ...
    def modifyNodeIC(self, index, **kwargs) -> None: ...
    def removeNode(self, index): ...
    i_location: Marker
    j_location: Marker
    material_type: Object.Object
    ref_curve: Object.Object
    cratiok: float
    cratiom: float
    faceting_tolerance: float
    fepart_type: str
    num_nodes: int
    sorted_s: List[float]
    preload: bool
    vm: Optional[Marker]
    vm_name: str
    wm: Optional[Marker]
    wm_name: str
    coordinates: List[float]
    Geometries: GeometryManager
    def __init__(self, _DBKey) -> None: ...


class PartManager(Manager.SubclassManager):
    def createRigidBody(self,
                        name: str = None,
                        location: List[float] = None,
                        orientation: List[float] = None,
                        along_axis_orientation: List[float] = None,
                        in_plane_orientation: List[float] = None,
                        relative_to: Object.Object = None,
                        mass: float = None,
                        cm: Marker = None,
                        cm_name: str = None,
                        im: Marker = None,
                        im_name: str = None,
                        vx: float = None,
                        vy: float = None,
                        vz: float = None,
                        wx: float = None,
                        wy: float = None,
                        wz: float = None,
                        vm: Marker = None,
                        vm_name: str = None,
                        wm: Marker = None,
                        wm_name: str = None,
                        ixx: float = None,
                        iyy: float = None,
                        izz: float = None,
                        ixy: float = None,
                        izx: float = None,
                        iyz: float = None,
                        exact_x: bool = None,
                        exact_y: bool = None,
                        exact_z: bool = None,
                        exact_psi: bool = None,
                        exact_theta: bool = None,
                        exact_phi: bool = None,
                        planar: bool = None,
                        **kwargs) -> RigidBody:
        """Create a rigid body part.

        Parameters
        ----------
        name : str, optional
            Name of the rigid body.
        location : List[float], optional
            Global [x, y, z] location of the part origin.
        orientation : List[float], optional
            [psi, theta, phi] Euler angles in degrees.
        along_axis_orientation : List[float], optional
            Orientation defined by an axis direction vector. Mutually exclusive
            with ``orientation`` and ``in_plane_orientation``.
        in_plane_orientation : List[float], optional
            Orientation defined by an in-plane vector. Mutually exclusive with
            ``orientation`` and ``along_axis_orientation``.
        relative_to : Object, optional
            Reference frame for location and orientation.
        mass : float, optional
            Mass of the rigid body.
        cm : Marker, optional
            Center-of-mass marker.
        cm_name : str, optional
            Full name of the center-of-mass marker.
        im : Marker, optional
            Inertia reference marker.
        im_name : str, optional
            Full name of the inertia reference marker.
        vx : float, optional
            Initial translational velocity along the vm marker x axis.
        vy : float, optional
            Initial translational velocity along the vm marker y axis.
        vz : float, optional
            Initial translational velocity along the vm marker z axis.
        wx : float, optional
            Initial angular velocity about the wm marker x axis.
        wy : float, optional
            Initial angular velocity about the wm marker y axis.
        wz : float, optional
            Initial angular velocity about the wm marker z axis.
        vm : Marker, optional
            Marker along whose axes initial translational velocities are specified.
        vm_name : str, optional
            Full name of the translational velocity reference marker.
        wm : Marker, optional
            Marker about which initial angular velocities are specified.
        wm_name : str, optional
            Full name of the angular velocity reference marker.
        ixx : float, optional
            Moment of inertia about the x axis.
        iyy : float, optional
            Moment of inertia about the y axis.
        izz : float, optional
            Moment of inertia about the z axis.
        ixy : float, optional
            Product of inertia about the xy axes.
        izx : float, optional
            Product of inertia about the zx axes.
        iyz : float, optional
            Product of inertia about the yz axes.
        exact_x : bool, optional
            If True, x position is held fixed during IC computation.
        exact_y : bool, optional
            If True, y position is held fixed during IC computation.
        exact_z : bool, optional
            If True, z position is held fixed during IC computation.
        exact_psi : bool, optional
            If True, psi orientation is held fixed during IC computation.
        exact_theta : bool, optional
            If True, theta orientation is held fixed during IC computation.
        exact_phi : bool, optional
            If True, phi orientation is held fixed during IC computation.
        planar : bool, optional
            If True, the body is constrained to 3-DOF planar motion.
        """
        ...

    def createFlexBody(self,
                       name: str = None,
                       vx: float = None,
                       vy: float = None,
                       vz: float = None,
                       wx: float = None,
                       wy: float = None,
                       wz: float = None,
                       vm: float = None,
                       vm_name: str = None,
                       wm: float = None,
                       wm_name: str = None,
                       md_db_file_name: str = None,
                       index_in_database: int = None,
                       damping_ratio: str = None,
                       damping_user_function: List[float | int] = None,
                       damping_routine: str = None,
                       dynamic_limit: float = None,
                       exact_x: float = None,
                       exact_y: float = None,
                       exact_z: float = None,
                       exact_psi: float = None,
                       exact_theta: float = None,
                       exact_phi: float = None,
                       invariants: List[bool] = None,
                       characteristic_length: float = None,
                       stability_factor: float = None,
                       exact_coordinates: List[int] = None,
                       selected_modes: List[int] = None,
                       modal_exact_coordinates: List[int] = None,
                       initial_modal_displacements: List[float] = None,
                       initial_modal_velocities: List[float] = None,
                       node_count: int = None,
                       mode_count: int = None,
                       modal_neutral_file_name: str = None,
                       bdf_file_name: str = None,
                       generalized_damping: Literal['off', 'full', 'internal_only'] = None,
                       representation: Literal['rigid', 'modal', 'nonlinear', 'nforce'] = None,
                       **kwargs) -> FlexBody:
        """Create a flexible body part from a modal neutral file or BDF file.

        Parameters
        ----------
        name : str, optional
            Name of the flexible body.
        vx, vy, vz : float, optional
            Initial translational velocity components.
        wx, wy, wz : float, optional
            Initial angular velocity components.
        vm : float or Marker, optional
            Reference marker for initial translational velocities.
        vm_name : str, optional
            Full name of the translational velocity reference marker.
        wm : float or Marker, optional
            Reference marker for initial angular velocities.
        wm_name : str, optional
            Full name of the angular velocity reference marker.
        md_db_file_name : str, optional
            Path to an MSC Nastran or modal database (.mdb/.mnf) file.
        index_in_database : int, optional
            Index of the component in the modal database.
        damping_ratio : str, optional
            Modal damping ratio expression.
        damping_user_function : list of float or int, optional
            User function values for damping.
        damping_routine : str, optional
            User subroutine name for damping.
        dynamic_limit : float, optional
            Maximum modal displacement for stability.
        exact_x, exact_y, exact_z : float, optional
            Constrain specific translational DOF during IC analysis.
        exact_psi, exact_theta, exact_phi : float, optional
            Constrain specific rotational DOF during IC analysis.
        invariants : list of bool, optional
            Which modal invariants to use during simulation.
        characteristic_length : float, optional
            Reference length for geometric stiffness (default: auto).
        stability_factor : float, optional
            Multiplier on the geometric stiffness matrix.
        exact_coordinates : list of int, optional
            Generalized coordinates held fixed during IC analysis.
        selected_modes : list of int, optional
            Mode numbers to include (default: all).
        modal_exact_coordinates : list of int, optional
            Modal coordinates held fixed during IC analysis.
        initial_modal_displacements : list of float, optional
            Initial modal displacement values.
        initial_modal_velocities : list of float, optional
            Initial modal velocity values.
        node_count : int, optional
            Number of nodes (informational).
        mode_count : int, optional
            Number of modes included.
        modal_neutral_file_name : str, optional
            Path to a modal neutral file (.mnf).
        bdf_file_name : str, optional
            Path to a Nastran BDF file for CMS flexible body creation.
        generalized_damping : str, optional
            ``'off'``, ``'full'``, or ``'internal_only'``.
        representation : str, optional
            ``'rigid'``, ``'modal'``, ``'nonlinear'``, or ``'nforce'``.
        """
        ...

    def createPointMass(self,
                        name: str = None,
                        location: List[float] = None,
                        orientation: List[float] = None,
                        relative_to: Object.Object = None,
                        mass: float = None,
                        **kwargs) -> PointMass:
        """Create a point mass part.

        Parameters
        ----------
        name : str, optional
            Name of the point mass.
        location : List[float], optional
            Global [x, y, z] location.
        orientation : List[float], optional
            [psi, theta, phi] Euler angles in degrees.
        relative_to : Object, optional
            Reference frame for location and orientation.
        mass : float, optional
            Mass of the point mass.
        """
        ...

    def createExternalSystem(self,
                             name: str = None,
                             location: List[float] = None,
                             orientation: List[float] = None,
                             relative_to: Object.Object = None,
                             **kwargs) -> ExternalSystem:
        """Create an external system part.

        Parameters
        ----------
        name : str, optional
            Name of the external system.
        location : List[float], optional
            Global [x, y, z] location.
        orientation : List[float], optional
            [psi, theta, phi] Euler angles in degrees.
        relative_to : Object, optional
            Reference frame for location and orientation.
        """
        ...

    def createFEPart(self,
                     name: str = None,
                     i_location=None,
                     j_location=None,
                     ref_curve=None,
                     coordinates: List[float] = None,
                     cratiok: float = 1.0,
                     cratiom: float = 1.0,
                     material_type=None,
                     section_label=None,
                     **kwargs) -> FEPart:
        """Create a finite element part.

        Provide one of: (``i_location`` and ``j_location``), ``ref_curve``,
        or ``coordinates``.

        Parameters
        ----------
        name : str, optional
            Name of the FE part.
        i_location : DesignPoint, optional
            Start point of the beam.
        j_location : DesignPoint, optional
            End point of the beam.
        ref_curve : Geometry, optional
            Reference curve defining the beam path.
        coordinates : List[float], optional
            Node coordinates defining the beam path.
        cratiok : float, optional
            Stiffness ratio (default 1.0).
        cratiom : float, optional
            Mass ratio (default 1.0).
        material_type : Material, optional
            Material defining section properties.
        section_label : Section, optional
            Cross-section definition.
        """
        ...

    def __getitem__(self, name) -> Part: ...
    def __iter__(self, *args) -> Iterable[str]: ...
    def items(self) -> ItemsView[str, Part]: ...
    def values(self) -> ValuesView[Part]: ...
    def keys(self) -> KeysView[str]: ...

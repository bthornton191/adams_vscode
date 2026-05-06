import DataElement
import Manager
import Object
import Part
from Geometry import Geometry, GeometrySolid
from DBAccess import MultiTypeObjectName as MultiTypeObjectName, MultiTypeObjectValue as MultiTypeObjectValue
from typing import ItemsView, Iterable, List, Literal, Optional, ValuesView
from Marker import Marker


class Contact(Object.Object):
    solid_types: List[str]
    curve_types: List[str]
    flip_geom_types: List[str]
    contact_type: Literal['solid_to_solid', 'curve_to_curve', 'point_to_curve', 'point_to_plane', 'curve_to_plane', 'sphere_to_plane',
                          'sphere_to_sphere', 'cylinder_to_cylinder', 'flex_to_flex', 'flex_edge_to_curve', 'flex_edge_to_plane', 'flex_edge_to_flex_edge', 'flex_to_solid']
    i_geometry: List[Geometry]
    """I-side geometry objects participating in the contact."""
    i_geometry_name: List[str]
    """Names of the I-side geometry objects participating in the contact."""
    j_geometry: List[Geometry]
    """J-side geometry objects participating in the contact."""
    j_geometry_name: List[str]
    """Names of the J-side geometry objects participating in the contact."""
    i_marker: List[Marker]
    """I-side marker(s) indicating the geometry participating in the contact."""
    i_marker_name: List[str]
    """Names of the I-side marker(s) indicating the geometry participating in the contact."""
    i_flex: Optional[Part.FlexBody]
    """First flexible body participating in the contact."""
    i_flex_name: Optional[str]
    """Name of the first flexible body participating in the contact."""
    i_edge: Optional[DataElement.Matrix]
    """Edge matrix on the first flexible body participating in the contact."""
    i_edge_name: str
    """Name of the edge matrix on the first flexible body participating in the contact."""
    i_edge_index: int
    """Index of the first edge participating in the contact."""
    j_flex: Optional[Part.FlexBody]
    """Second flexible body participating in the contact."""
    j_flex_name: Optional[str]
    """Name of the second flexible body participating in the contact."""
    j_edge: Optional[DataElement.Matrix]
    """Edge matrix on the second flexible body participating in the contact."""
    j_edge_name: str
    """Name of the edge matrix on the second flexible body participating in the contact."""
    j_edge_index: int
    """Index of the second edge participating in the contact."""
    i_flip_normal: List[bool]
    """Whether the surface normal is flipped for each I-side geometry."""
    j_flip_normal: List[bool]
    """Whether the surface normal is flipped for each J-side geometry."""
    i_flip_geometry: List[Geometry]
    """Geometries on the I body at which the contact normal direction is flipped."""
    i_flip_geometry_name: List[str]
    """Names of geometries on the I body at which the contact normal direction is flipped."""
    j_flip_geometry: List[Geometry]
    """Geometries on the J body at which the contact normal direction is flipped."""
    j_flip_geometry_name: List[str]
    """Names of geometries on the J body at which the contact normal direction is flipped."""
    geometry_routines: str
    stiffness: float
    """Material stiffness used to calculate the normal contact force."""
    damping: float
    """Damping coefficient used with the IMPACT model for calculating normal forces."""
    dmax: float
    """Boundary penetration depth used with the impact model for calculating normal forces."""
    exponent: float
    """Force exponent used with the impact model for calculating normal forces."""
    penalty: float
    """Penalty stiffness used with the restitution model for calculating normal forces."""
    restitution_coefficient: float
    """Coefficient of restitution modelling energy loss during contact."""
    normal_function: List[float]
    """Up to 30 user-defined constants passed to the normal force subroutine."""
    normal_routine: str
    """Library and subroutine name for the user-written normal force computation."""
    augmented_lagrangian_formulation: bool
    """If True, refines the normal force between two sets of rigid geometries using augmented Lagrangian formulation."""
    friction_function: List[float]
    """Up to 30 user-defined constants passed to the friction force subroutine."""
    friction_routine: str
    """Library and subroutine name for the user-written friction force computation."""
    coulomb_friction_dict: dict
    coulomb_friction: Literal['off', 'on', 'dynamics_only']
    """Models friction using the Coulomb friction model at contact locations."""
    mu_static: float
    """Coefficient of friction at a contact point when the slip velocity is below the stiction transition velocity."""
    mu_dynamic: float
    """Coefficient of friction at a contact point when the slip velocity is above the friction transition velocity."""
    friction_transition_velocity: float
    """Slip velocity above which the Coulomb friction model uses mu_dynamic."""
    stiction_transition_velocity: float
    """Slip velocity below which the contact is considered in stiction."""
    no_friction: bool
    """If True, friction is not applied at the contact."""
    face_contact_top: bool
    """If True, enables face contact on the top face."""
    face_contact_bottom: bool
    """If True, enables face contact on the bottom face."""
    stiction: str
    """Models friction effects using the Stiction and Sliding friction model."""
    max_stiction_deformation: float
    """Maximum creep that can occur during the stiction regime."""


class ContactManager(Manager.AdamsManager):
    def createSolidToSolid(self,
                           name: str,
                           i_geometry: GeometrySolid,
                           j_geometry: GeometrySolid,
                           stiffness: float,
                           damping: float,
                           dmax: float,
                           exponent: float,
                           **kwargs) -> Contact:
        """Create a solid-to-solid contact.

        Parameters
        ----------
        name : str
            Name of the contact.
        i_geometry : GeometrySolid
            First solid geometry.
        j_geometry : GeometrySolid
            Second solid geometry.
        stiffness : float
            Contact stiffness.
        damping : float
            Contact damping.
        dmax : float
            Maximum penetration depth for full damping.
        exponent : float
            Force exponent for the contact model.
        """
        ...

    def createCurveToCurve(self, name: str = None, **kwargs) -> Contact:
        """Create a curve-to-curve contact.

        Parameters
        ----------
        name : str, optional
            Name of the contact.
        """
        ...

    def createPointToCurve(self, name: str = None, **kwargs) -> Contact:
        """Create a point-to-curve contact.

        Parameters
        ----------
        name : str, optional
            Name of the contact.
        """
        ...

    def createPointToPlane(self, name: str = None, **kwargs) -> Contact:
        """Create a point-to-plane contact.

        Parameters
        ----------
        name : str, optional
            Name of the contact.
        """
        ...

    def createCurveToPlane(self, name: str = None, **kwargs) -> Contact:
        """Create a curve-to-plane contact.

        Parameters
        ----------
        name : str, optional
            Name of the contact.
        """
        ...

    def createSphereToPlane(self, name: str = None, **kwargs) -> Contact:
        """Create a sphere-to-plane contact.

        Parameters
        ----------
        name : str, optional
            Name of the contact.
        """
        ...

    def createSphereToSphere(self, name: str = None, **kwargs) -> Contact:
        """Create a sphere-to-sphere contact.

        Parameters
        ----------
        name : str, optional
            Name of the contact.
        """
        ...

    def createCylinderToCylinder(self, name: str = None, **kwargs) -> Contact:
        """Create a cylinder-to-cylinder contact.

        Parameters
        ----------
        name : str, optional
            Name of the contact.
        """
        ...

    def createFlexToFlex(self, name: str = None, **kwargs) -> Contact:
        """Create a flex-to-flex contact.

        Parameters
        ----------
        name : str, optional
            Name of the contact.
        """
        ...

    def createFlexEdgeToCurve(self, name: str = None, **kwargs) -> Contact:
        """Create a flex-edge-to-curve contact.

        Parameters
        ----------
        name : str, optional
            Name of the contact.
        """
        ...

    def createFlexEdgeToFlexEdge(self, name: str = None, **kwargs) -> Contact:
        """Create a flex-edge-to-flex-edge contact.

        Parameters
        ----------
        name : str, optional
            Name of the contact.
        """
        ...

    def createFlexEdgeToPlane(self, name: str = None, **kwargs) -> Contact:
        """Create a flex-edge-to-plane contact.

        Parameters
        ----------
        name : str, optional
            Name of the contact.
        """
        ...

    def createFlexToSolid(self, name: str = None, **kwargs) -> Contact:
        """Create a flex-to-solid contact.

        Parameters
        ----------
        name : str, optional
            Name of the contact.
        """
        ...

    def __getitem__(self, name) -> Contact: ...
    def __iter__(self, *args) -> Iterable[str]: ...
    def items(self) -> ItemsView[str, Contact]: ...
    def values(self) -> ValuesView[Contact]: ...

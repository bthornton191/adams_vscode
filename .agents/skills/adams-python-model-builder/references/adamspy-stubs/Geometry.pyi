import AppearanceSettings
import Contact
import Feature
import Manager
from Marker import Marker
import Object
from DesignVariable import DesignVariableManager
from DBAccess import MultiTypeObjectValue as MultiTypeObjectValue
from typing import ItemsView, Iterable, KeysView, List, Literal, Optional, Tuple, Union, ValuesView, overload


class GeometryModelManager(Manager.SubclassManager):
    type_map: dict
    def __init__(self, managedClass, parent) -> None: ...

    def createSpringDamper(self,
                           name: str = None,
                           i_marker: Marker = None,
                           i_marker_name: str = None,
                           j_marker: Marker = None,
                           j_marker_name: str = None,
                           **kwargs) -> GeometrySpringDamper:
        """Create a spring-damper graphic.

        Parameters
        ----------
        name : str, optional
            Name of the spring-damper graphic.
        i_marker : Marker, optional
            First endpoint marker.
        i_marker_name : str, optional
            Full name of the first endpoint marker.
        j_marker : Marker, optional
            Second endpoint marker.
        j_marker_name : str, optional
            Full name of the second endpoint marker.
        """
        ...

    def createForce(self,
                    name: str = None,
                    applied_at_marker: Marker = None,
                    applied_at_marker_name: str = None,
                    force_element=None,
                    joint=None,
                    jprim=None,
                    point_curve=None,
                    curve_curve=None,
                    **kwargs) -> GeometryForce:
        """Create a force graphic.

        Parameters
        ----------
        name : str, optional
            Name of the force graphic.
        applied_at_marker : Marker, optional
            Marker at which the force is displayed.
        applied_at_marker_name : str, optional
            Full name of the marker.
        force_element : Force, optional
            Force element to visualize.
        joint : Joint, optional
            Joint to visualize forces for.
        jprim : Jprim, optional
            Jprim to visualize forces for.
        point_curve : PointCurveConstraint, optional
            Point-curve constraint to visualize.
        curve_curve : CurveCurveConstraint, optional
            Curve-curve constraint to visualize.
        """
        ...

    def createGContact(self,
                       name: str = None,
                       contact_element=None,
                       contact_element_name: str = None,
                       adams_id: int = None,
                       **kwargs) -> GeometryGContact:
        """Create a general contact graphic.

        Parameters
        ----------
        name : str, optional
            Name of the contact graphic.
        contact_element : Contact, optional
            Contact element to visualize.
        contact_element_name : str, optional
            Full name of the contact element.
        adams_id : int, optional
            Adams ID for the graphic.
        """
        ...


class Geometry(Object.ObjectComment, AppearanceSettings.GeometryAppearanceSettings):
    adams_id_id: int
    comment_id: int
    DesignVariables: DesignVariableManager
    Features: Feature.FeatureManager
    def __init__(self, _DBKey) -> None: ...


class GeometryLink(Geometry):
    comment_id: int
    depth: float
    width: float
    i_marker: Marker
    i_marker_name: str
    j_marker: Marker
    j_marker_name: str


class GeometryEllipse(Geometry):
    comment_id: int
    adams_id_id: int
    center_marker: Marker
    center_marker_name: str
    start_angle: float
    end_angle: float
    major_radius: float
    minor_radius: float


class GeometryTorus(Geometry, Object.ObjectAdamsId):
    major_radius: float
    minor_radius: float
    angle_extent: float
    side_count_for_perimeter: int
    segment_count: int
    center_marker: Marker
    center_marker_name: str


class GeometryCircle(Geometry, Object.ObjectAdamsId):
    radius: float
    segment_count: int
    center_marker: Marker
    center_marker_name: str
    def setRefMarkerRadius(self, marker): ...
    ref_radius_by_marker: Marker


class GeometryPlane(Geometry):
    x_minimum: float
    x_maximum: float
    y_minimum: float
    y_maximum: float
    ref_marker: Marker
    ref_marker_name: str


class GeometryBSpline(Geometry, Object.ObjectAdamsId):
    segment_count: int
    ref_marker: Marker
    ref_marker_name: str
    ref_curve: Object.Object
    ref_curve_name: str
    def setClosed(self, close): ...
    def getClosed(self): ...
    closed: bool


class GeometryBlock(Geometry):
    x: float
    y: float
    z: float
    corner_marker: Marker
    corner_marker_name: str


class GeometryChain(Geometry):
    comment_id: int
    adams_id_id: int
    objects_in_chain: List[Geometry]


class GeometryCylinder(Geometry, Object.ObjectAdamsId):
    center_marker: Marker
    center_marker_name: str
    angle_extent: float
    length: float
    side_count_for_body: int
    radius: float
    segment_count_for_ends: int
    def setRefMarkerRadius(self, marker): ...
    ref_radius_by_marker: Marker


class GeometryEllipsoid(Geometry):
    x_scale_factor: float
    y_scale_factor: float
    z_scale_factor: float
    center_marker: Marker
    center_marker_name: str


class GeometryForce(Geometry, Object.ObjectAdamsId):
    all_force_elements: bool
    applied_at_marker: Marker
    applied_at_marker_name: str
    force_element: Object.Object
    force_element_name: str
    joint: Object.Object
    joint_name: str
    jprim: Object.Object
    jprim_name: str
    curve_curve: Object.Object
    curve_curve_name: str
    point_curve: Object.Object
    point_curve_name: str


class GeometryGContact(Geometry):
    comment_id: int
    contact_element: Contact.Contact
    adams_id: int
    force_display: str


class GeometryArc(Geometry, Object.ObjectAdamsId):
    center_marker: Marker
    center_marker_name: str
    radius: float
    angle_extent: float
    segment_count: int
    def setRefMarkerRadius(self, marker): ...
    ref_radius_by_marker: Marker
    type_close: dict
    def setClose(self, closure): ...
    def getClose(self): ...
    close: Literal['no', 'sector', 'chorded']


class GeometryFrustum(Geometry, Object.ObjectAdamsId):
    top_radius: float
    bottom_radius: float
    angle_extent: float
    length: float
    side_count_for_body: int
    segment_count_for_ends: int
    center_marker: Marker
    center_marker_name: str


class GeometryOutline(Geometry, Object.ObjectAdamsId):
    visibility_between_markers: Literal['on', 'off']
    marker: Marker
    marker_name: str


class GeometrySpringDamper(Geometry, Object.ObjectAdamsId):
    diameter_of_spring: float
    damper_diameter_at_i: float
    damper_diameter_at_j: float
    coil_count: int
    tip_length_at_i: float
    tip_length_at_j: float
    cup_length_at_i: float
    cup_length_at_j: float
    i_marker: Marker
    i_marker_name: str
    j_marker: Marker
    j_marker_name: str


class GeometryExtrusion(Geometry, Object.ObjectAdamsId):
    def __init__(self, _DBKey) -> None: ...
    analytical: bool
    points_for_profile: List[float]
    length_along_z_axis: float
    path_points: List[float]
    profile_curve: Geometry
    path_curve: Geometry
    reference_marker: Marker
    reference_marker_name: str
    relative_to: Object.Object


class GeometryRevolution(Geometry):
    def __init__(self, _DBKey) -> None: ...
    angle_extent: float
    analytical: bool
    profile_curve: Geometry
    profile_curve_name: str
    reference_marker: Marker
    reference_marker_name: str
    number_of_sides: int
    points_for_profile: List[float]
    relative_to: Object.Object


class GeometryShell(Geometry):
    comment_id: int
    file_name: str
    points: List[Tuple[float, float, float]]
    scale: float
    """Conversion factor to meters"""
    reference_marker: Marker
    reference_marker_name: str
    wireframe_only: bool
    connections: List[List[float]]


class GeometryPlate(Geometry):
    comment_id: int
    markers: List[Marker]
    marker_names: List[str]
    width: float
    radius: float


class GeometryPoint(Geometry):
    ref_marker: Marker
    ref_marker_name: str


class GeometryCsg(Geometry):
    comment_id: int
    adams_id_id: int
    geom_type: List[str]
    def setCsgExplode(self, val): ...
    explode: bool
    base_object: Geometry
    base_object_name: str
    object: Geometry
    object_name: str
    csg_type: Literal['intersection', 'union', 'difference']


class GeometrySolid(Geometry):
    ...


class GeometryExternal(Geometry):
    solid_id: int
    rm: Marker
    ref_marker_name: str
    faceting_tolerance: float
    file: str
    element: str


class GeometryPolyline(Geometry):
    def __init__(self, _DBKey) -> None: ...
    comment_id: int
    geom_type: List[str]
    path_curve: Geometry
    location: List[float]
    """Locations of the points defining the line.
    
    Note
    ----
    When setting this variable, you must use global coordinates. But, **when getting this variable, 
    the coordinates are relative to the parent part**.
    """
    close: bool
    relative_to: Object.Object


class GeometrySheet(Geometry):
    ...


class GeometryNurbCurve(Geometry):
    comment_id: int
    degree: int
    rational: bool
    periodic: bool
    knots: List[float]
    weights: List[float]
    control_points: List[float]


class GeometryManager(Manager.SubclassManager):
    def __init__(self, managedClass, parent) -> None: ...

    def createTorus(
        self,
        *,
        center_marker: Union[Marker, Object.Object],
        name: Optional[str] = ...,
        major_radius: Optional[float] = ...,
        minor_radius: Optional[float] = ...,
        angle_extent: Optional[float] = ...,
        side_count_for_perimeter: Optional[int] = ...,
        segment_count: Optional[int] = ...,
        **kwargs,
    ) -> GeometryTorus:
        """Create a torus geometry.

        Parameters
        ----------
        center_marker : Marker | Object
            Marker at the center of the torus. **Required.**
        name : str, optional
            Name of the geometry. Auto-generated if omitted.
        major_radius : float, optional
            Major radius of the torus.
        minor_radius : float, optional
            Minor radius of the torus.
        angle_extent : float, optional
            Angular extent of the torus.
        side_count_for_perimeter : int, optional
            Number of sides for the perimeter.
        segment_count : int, optional
            Number of segments.
        """
        ...

    def createCylinder(
        self,
        *,
        center_marker: Union[Marker, Object.Object],
        name: Optional[str] = ...,
        radius: Optional[float] = ...,
        length: Optional[float] = ...,
        angle_extent: Optional[float] = ...,
        side_count_for_body: Optional[int] = ...,
        segment_count_for_ends: Optional[int] = ...,
        **kwargs,
    ) -> GeometryCylinder:
        """Create a cylinder geometry.

        Parameters
        ----------
        center_marker : Marker | Object
            Marker at the center of the cylinder. **Required.**
        name : str, optional
            Name of the geometry. Auto-generated if omitted.
        radius : float, optional
            Radius of the cylinder.
        length : float, optional
            Length of the cylinder.
        angle_extent : float, optional
            Angular extent.
        side_count_for_body : int, optional
            Number of sides for the body.
        segment_count_for_ends : int, optional
            Number of segments for the ends.
        """
        ...

    def createCircle(
        self,
        *,
        center_marker: Union[Marker, Object.Object],
        name: Optional[str] = ...,
        radius: Optional[float] = ...,
        segment_count: Optional[int] = ...,
        **kwargs,
    ) -> GeometryCircle:
        """Create a circle geometry.

        Parameters
        ----------
        center_marker : Marker | Object
            Marker at the center of the circle. **Required.**
        name : str, optional
            Name of the geometry. Auto-generated if omitted.
        radius : float, optional
            Radius of the circle.
        segment_count : int, optional
            Number of segments.
        """
        ...

    def createPlane(
        self,
        *,
        x_minimum: float,
        x_maximum: float,
        y_minimum: float,
        y_maximum: float,
        ref_marker: Optional[Union[Marker, Object.Object]] = ...,
        ref_marker_name: Optional[str] = ...,
        name: Optional[str] = ...,
        **kwargs,
    ) -> GeometryPlane:
        """Create a plane geometry.

        Parameters
        ----------
        x_minimum : float
            Minimum x extent. **Required.**
        x_maximum : float
            Maximum x extent. **Required.**
        y_minimum : float
            Minimum y extent. **Required.**
        y_maximum : float
            Maximum y extent. **Required.**
        ref_marker : Marker | Object, optional
            Reference marker. Either ``ref_marker`` or ``ref_marker_name`` must be provided.
        ref_marker_name : str, optional
            Full name of the reference marker.
        name : str, optional
            Name of the geometry. Auto-generated if omitted.
        """
        ...

    def createBSpline(
        self,
        *,
        name: Optional[str] = ...,
        ref_curve: Optional[Object.Object] = ...,
        ref_curve_name: Optional[str] = ...,
        segment_count: int = ...,
        **kwargs,
    ) -> GeometryBSpline:
        """Create a B-spline geometry.

        Parameters
        ----------
        name : str, optional
            Name of the geometry. Auto-generated if omitted.
        ref_curve : Object, optional
            Reference curve object. Either ``ref_curve`` or ``ref_curve_name`` may be provided.
        ref_curve_name : str, optional
            Full name of the reference curve.
        segment_count : int, optional
            Number of segments (default 20).
        """
        ...

    def createBlock(
        self,
        *,
        corner_marker: Union[Marker, Object.Object],
        name: Optional[str] = ...,
        x: Optional[float] = ...,
        y: Optional[float] = ...,
        z: Optional[float] = ...,
        **kwargs,
    ) -> GeometryBlock:
        """Create a block geometry.

        Parameters
        ----------
        corner_marker : Marker | Object
            Marker at the corner of the block. **Required.**
        name : str, optional
            Name of the geometry. Auto-generated if omitted.
        x : float, optional
            X dimension of the block.
        y : float, optional
            Y dimension of the block.
        z : float, optional
            Z dimension of the block.
        """
        ...

    def createEllipsoid(
        self,
        *,
        center_marker: Union[Marker, Object.Object],
        name: Optional[str] = ...,
        x_scale_factor: Optional[float] = ...,
        y_scale_factor: Optional[float] = ...,
        z_scale_factor: Optional[float] = ...,
        **kwargs,
    ) -> GeometryEllipsoid:
        """Create an ellipsoid geometry.

        Parameters
        ----------
        center_marker : Marker | Object
            Marker at the center of the ellipsoid. **Required.**
        name : str, optional
            Name of the geometry. Auto-generated if omitted.
        x_scale_factor : float, optional
            Scale factor along the x-axis.
        y_scale_factor : float, optional
            Scale factor along the y-axis.
        z_scale_factor : float, optional
            Scale factor along the z-axis.
        """
        ...

    def createArc(
        self,
        *,
        center_marker: Union[Marker, Object.Object],
        name: Optional[str] = ...,
        radius: Optional[float] = ...,
        angle_extent: Optional[float] = ...,
        segment_count: Optional[int] = ...,
        close: Optional[Literal['no', 'sector', 'chorded']] = ...,
        **kwargs,
    ) -> GeometryArc:
        """Create an arc geometry.

        Parameters
        ----------
        center_marker : Marker | Object
            Marker at the center of the arc. **Required.**
        name : str, optional
            Name of the geometry. Auto-generated if omitted.
        radius : float, optional
            Radius of the arc.
        angle_extent : float, optional
            Angular extent of the arc.
        segment_count : int, optional
            Number of segments.
        close : ``'no'`` | ``'sector'`` | ``'chorded'``, optional
            Closure type for the arc.
        """
        ...

    def createFrustum(
        self,
        *,
        center_marker: Union[Marker, Object.Object],
        name: Optional[str] = ...,
        top_radius: Optional[float] = ...,
        bottom_radius: Optional[float] = ...,
        length: Optional[float] = ...,
        angle_extent: Optional[float] = ...,
        side_count_for_body: Optional[int] = ...,
        segment_count_for_ends: Optional[int] = ...,
        **kwargs,
    ) -> GeometryFrustum:
        """Create a frustum geometry.

        Parameters
        ----------
        center_marker : Marker | Object
            Marker at the center of the frustum. **Required.**
        name : str, optional
            Name of the geometry. Auto-generated if omitted.
        top_radius : float, optional
            Radius of the top face.
        bottom_radius : float, optional
            Radius of the bottom face.
        length : float, optional
            Length of the frustum.
        angle_extent : float, optional
            Angular extent.
        side_count_for_body : int, optional
            Number of sides for the body.
        segment_count_for_ends : int, optional
            Number of segments for the ends.
        """
        ...

    def createRevolution(
        self,
        *,
        reference_marker: Union[Marker, Object.Object],
        profile_curve: Optional[Geometry] = ...,
        points_for_profile: Optional[List[float]] = ...,
        name: Optional[str] = ...,
        analytical: Optional[bool] = ...,
        number_of_sides: Optional[int] = ...,
        angle_extent: Optional[float] = ...,
        relative_to: Optional[Object.Object] = ...,
        **kwargs,
    ) -> GeometryRevolution:
        """Create a revolution geometry.

        Parameters
        ----------
        reference_marker : Marker | Object
            Reference marker for the revolution. **Required.**
        profile_curve : Geometry, optional
            Curve to revolve. Either ``profile_curve`` or ``points_for_profile`` must be provided.
        points_for_profile : list of float, optional
            Flat list of point coordinates defining the profile.
        name : str, optional
            Name of the geometry. Auto-generated if omitted.
        analytical : bool, optional
            Whether to create an analytical geometry.
        number_of_sides : int, optional
            Number of sides (default 20).
        angle_extent : float, optional
            Angular extent (default 360 degrees).
        relative_to : Object, optional
            Reference frame for point coordinates. Defaults to the current default reference frame.
        """
        ...

    def createExtrusion(
        self,
        *,
        reference_marker: Union[Marker, Object.Object],
        profile_curve: Optional[Geometry] = ...,
        points_for_profile: Optional[List[float]] = ...,
        name: Optional[str] = ...,
        analytical: Optional[bool] = ...,
        path_curve: Optional[Geometry] = ...,
        path_points: Optional[List[float]] = ...,
        relative_to: Optional[Object.Object] = ...,
        **kwargs,
    ) -> GeometryExtrusion:
        """Create an extrusion geometry.

        Parameters
        ----------
        reference_marker : Marker | Object
            Reference marker for the extrusion. **Required.**
        profile_curve : Geometry, optional
            Curve defining the profile. Either ``profile_curve`` or ``points_for_profile`` must
            be provided, but not both.
        points_for_profile : list of float, optional
            Flat list of point coordinates defining the profile.
        name : str, optional
            Name of the geometry. Auto-generated if omitted.
        analytical : bool, optional
            Whether to create an analytical geometry.
        path_curve : Geometry, optional
            Curve defining the extrusion path.
        path_points : list of float, optional
            Flat list of point coordinates defining the extrusion path.
        relative_to : Object, optional
            Reference frame for point coordinates. Defaults to the current default reference frame.
        """
        ...

    def createOutline(
        self,
        *,
        name: Optional[str] = ...,
        marker: Optional[Marker] = ...,
        marker_name: Optional[str] = ...,
        visibility_between_markers: Optional[Literal['on', 'off']] = ...,
        **kwargs,
    ) -> GeometryOutline:
        """Create an outline geometry.

        Parameters
        ----------
        name : str, optional
            Name of the geometry. Auto-generated if omitted.
        marker : Marker, optional
            Marker for the outline.
        marker_name : str, optional
            Full name of the marker.
        visibility_between_markers : ``'on'`` | ``'off'``, optional
            Whether lines between markers are visible.
        """
        ...

    def createSolid(
        self,
        *,
        name: Optional[str] = ...,
        **kwargs,
    ) -> GeometrySolid:
        """Create a solid geometry.

        Parameters
        ----------
        name : str, optional
            Name of the geometry. Auto-generated if omitted.
        """
        ...

    def createExternal(
        self,
        *,
        name: Optional[str] = ...,
        solid_id: Optional[int] = ...,
        rm: Optional[Marker] = ...,
        faceting_tolerance: Optional[float] = ...,
        file: Optional[str] = ...,
        element: Optional[str] = ...,
        **kwargs,
    ) -> GeometryExternal:
        """Create an external geometry.

        Parameters
        ----------
        name : str, optional
            Name of the geometry. Auto-generated if omitted.
        solid_id : int, optional
            ID of the solid.
        rm : Marker, optional
            Reference marker.
        faceting_tolerance : float, optional
            Faceting tolerance.
        file : str, optional
            Path to external geometry file.
        element : str, optional
            Element identifier within the file.
        """
        ...

    @overload
    def createShell(
        self,
        *,
        file_name: str,
        name: Optional[str] = ...,
        reference_marker: Optional[Marker] = ...,
        reference_marker_name: Optional[str] = ...,
        scale: Optional[float] = ...,
        wireframe_only: Optional[bool] = ...,
        **kwargs,
    ) -> GeometryShell:
        """Create a shell geometry from a file."""
        ...

    @overload
    def createShell(
        self,
        *,
        points: List[Tuple[float, float, float]],
        connections: List[List[float]],
        name: Optional[str] = ...,
        reference_marker: Optional[Marker] = ...,
        reference_marker_name: Optional[str] = ...,
        scale: Optional[float] = ...,
        wireframe_only: Optional[bool] = ...,
        **kwargs,
    ) -> GeometryShell:
        """Create a shell geometry from points and connections."""
        ...

    def createShell(
        self,
        *,
        file_name: Optional[str] = ...,
        points: Optional[List[Tuple[float, float, float]]] = ...,
        connections: Optional[List[List[float]]] = ...,
        name: Optional[str] = ...,
        reference_marker: Optional[Marker] = ...,
        reference_marker_name: Optional[str] = ...,
        scale: Optional[float] = ...,
        wireframe_only: Optional[bool] = ...,
        **kwargs,
    ) -> GeometryShell:
        """Create a shell geometry.

        Provide either ``file_name`` **or** ``points`` and ``connections``, but not both.

        Parameters
        ----------
        file_name : str, optional
            Path to the shell geometry file.
        points : list of (float, float, float), optional
            Vertex coordinates.
        connections : list of list of float, optional
            Connectivity data referencing the *points* list.
        name : str, optional
            Name of the geometry. Auto-generated if omitted.
        reference_marker : Marker, optional
            Reference marker for the shell.
        reference_marker_name : str, optional
            Full name of the reference marker.
        scale : float, optional
            Conversion factor to metres.
        wireframe_only : bool, optional
            Whether to display only wireframe.
        """
        ...

    def createPlate(
        self,
        *,
        markers: List[Union[Marker, Object.Object]],
        radius: float,
        width: float,
        name: Optional[str] = ...,
        **kwargs,
    ) -> GeometryPlate:
        """Create a plate geometry.

        Parameters
        ----------
        markers : list of Marker | Object
            List of markers defining the plate outline. **Required.**
        radius : float
            Fillet radius at the corners. **Required.**
        width : float
            Width (thickness) of the plate. **Required.**
        name : str, optional
            Name of the geometry. Auto-generated if omitted.
        """
        ...

    def createLink(
        self,
        *,
        width: float,
        depth: float,
        i_marker: Optional[Union[Marker, Object.Object]] = ...,
        i_marker_name: Optional[str] = ...,
        j_marker: Optional[Union[Marker, Object.Object]] = ...,
        j_marker_name: Optional[str] = ...,
        name: Optional[str] = ...,
        **kwargs,
    ) -> GeometryLink:
        """Create a link geometry.

        Parameters
        ----------
        width : float
            Width of the link. **Required.**
        depth : float
            Depth of the link. **Required.**
        i_marker : Marker | Object, optional
            I-marker. Either ``i_marker`` or ``i_marker_name`` must be provided.
        i_marker_name : str, optional
            Full name of the i-marker.
        j_marker : Marker | Object, optional
            J-marker. Either ``j_marker`` or ``j_marker_name`` must be provided.
        j_marker_name : str, optional
            Full name of the j-marker.
        name : str, optional
            Name of the geometry. Auto-generated if omitted.
        """
        ...

    def createEllipse(
        self,
        *,
        center_marker: Union[Marker, Object.Object],
        name: Optional[str] = ...,
        major_radius: Optional[float] = ...,
        minor_radius: Optional[float] = ...,
        start_angle: Optional[float] = ...,
        end_angle: Optional[float] = ...,
        **kwargs,
    ) -> GeometryEllipse:
        """Create an ellipse geometry.

        Parameters
        ----------
        center_marker : Marker | Object
            Marker at the center of the ellipse. **Required.**
        name : str, optional
            Name of the geometry. Auto-generated if omitted.
        major_radius : float, optional
            Major radius.
        minor_radius : float, optional
            Minor radius.
        start_angle : float, optional
            Start angle.
        end_angle : float, optional
            End angle.
        """
        ...

    def createPolyline(
        self,
        *,
        name: Optional[str] = ...,
        location: Optional[List[float]] = ...,
        close: Optional[bool] = ...,
        relative_to: Optional[Object.Object] = ...,
        path_curve: Optional[Geometry] = ...,
        **kwargs,
    ) -> GeometryPolyline:
        """Create a polyline geometry.

        Parameters
        ----------
        name : str, optional
            Name of the geometry. Auto-generated if omitted.
        location : list of float, optional
            Flat list of point coordinates defining the polyline (global coordinates).
        close : bool, optional
            Whether to close the polyline.
        relative_to : Object, optional
            Reference frame for the coordinates.
        path_curve : Geometry, optional
            Curve to follow.
        """
        ...

    def createChain(
        self,
        *,
        objects_in_chain: List[Geometry],
        name: Optional[str] = ...,
        **kwargs,
    ) -> GeometryChain:
        """Create a chain geometry.

        Parameters
        ----------
        objects_in_chain : list of Geometry
            Geometry objects to include in the chain. **Required.**
        name : str, optional
            Name of the geometry. Auto-generated if omitted.
        """
        ...

    def createPoint(
        self,
        *,
        ref_marker: Optional[Union[Marker, Object.Object]] = ...,
        ref_marker_name: Optional[str] = ...,
        name: Optional[str] = ...,
        **kwargs,
    ) -> GeometryPoint:
        """Create a point geometry.

        Parameters
        ----------
        ref_marker : Marker | Object, optional
            Reference marker. Either ``ref_marker`` or ``ref_marker_name`` must be provided.
        ref_marker_name : str, optional
            Full name of the reference marker.
        name : str, optional
            Name of the geometry. Auto-generated if omitted.
        """
        ...

    def createCsg(
        self,
        *,
        csg_type: Literal['intersection', 'union', 'difference'],
        base_object: Optional[Geometry] = ...,
        base_object_name: Optional[str] = ...,
        object: Optional[Geometry] = ...,
        object_name: Optional[str] = ...,
        name: Optional[str] = ...,
        **kwargs,
    ) -> GeometryCsg:
        """Create a CSG (Constructive Solid Geometry) object.

        Parameters
        ----------
        csg_type : ``'intersection'`` | ``'union'`` | ``'difference'``
            Type of boolean operation. **Required.**
        base_object : Geometry, optional
            Base geometry object. Either ``base_object`` or ``base_object_name`` must be provided.
        base_object_name : str, optional
            Full name of the base geometry object.
        object : Geometry, optional
            Second geometry object. Either ``object`` or ``object_name`` must be provided.
        object_name : str, optional
            Full name of the second geometry object.
        name : str, optional
            Name of the geometry. Auto-generated if omitted.
        """
        ...

    def createSheet(
        self,
        *,
        name: Optional[str] = ...,
        **kwargs,
    ) -> GeometrySheet:
        """Create a sheet geometry.

        Parameters
        ----------
        name : str, optional
            Name of the geometry. Auto-generated if omitted.
        """
        ...

    def createNurbCurve(
        self,
        *,
        degree: int,
        name: Optional[str] = ...,
        rational: Optional[bool] = ...,
        periodic: Optional[bool] = ...,
        knots: Optional[List[float]] = ...,
        weights: Optional[List[float]] = ...,
        control_points: Optional[List[float]] = ...,
        **kwargs,
    ) -> GeometryNurbCurve:
        """Create a NURB curve geometry.

        Parameters
        ----------
        degree : int
            Degree of the NURB curve. **Required.**
        name : str, optional
            Name of the geometry. Auto-generated if omitted.
        rational : bool, optional
            Whether the curve is rational.
        periodic : bool, optional
            Whether the curve is periodic.
        knots : list of float, optional
            Knot vector.
        weights : list of float, optional
            Weights for control points.
        control_points : list of float, optional
            Flat list of control point coordinates.
        """
        ...

    def __getitem__(self, name) -> Geometry: ...
    def __iter__(self, *args) -> Iterable[str]: ...
    def items(self) -> ItemsView[str, Geometry]: ...
    def values(self) -> ValuesView[Geometry]: ...
    def keys(self) -> KeysView[str]: ...

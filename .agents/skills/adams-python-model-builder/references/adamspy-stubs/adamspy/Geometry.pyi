import AppearanceSettings
import Contact
import Feature
import Manager
from Marker import Marker
import Object
from DesignVariable import DesignVariableManager
from DBAccess import MultiTypeObjectValue as MultiTypeObjectValue
from typing import ItemsView, Iterable, KeysView, List, Literal, Tuple, ValuesView


class GeometryModelManager(Manager.SubclassManager):
    type_map: dict
    def __init__(self, managedClass, parent) -> None: ...
    def createSpringDamper(self, **kwargs): ...
    def createForce(self, **kwargs): ...
    def createGContact(self, **kwargs): ...


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
    When setting this variable, you must use global coordinates.
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
    def createTorus(self, **kwargs): ...
    def createCylinder(self, **kwargs): ...
    def createCircle(self, **kwargs): ...
    def createPlane(self, **kwargs): ...
    def createBSpline(self, **kwargs): ...
    def createBlock(self, **kwargs): ...
    def createEllipsoid(self, **kwargs): ...
    def createArc(self, **kwargs): ...
    def createFrustum(self, **kwargs): ...
    def createRevolution(self, **kwargs): ...
    def createExtrusion(self, **kwargs): ...
    def createOutline(self, **kwargs): ...
    def createSolid(self, **kwargs): ...
    def createExternal(self, **kwargs): ...
    def createShell(self, file_name: str, ref_mkr: Marker, **kwargs) -> GeometryShell: ...
    def createPlate(self, **kwargs): ...
    def createLink(self, **kwargs): ...
    def createEllipse(self, **kwargs): ...
    def createPolyline(self, **kwargs): ...
    def createChain(self, **kwargs): ...
    def createPoint(self, **kwargs): ...
    def createCsg(self, **kwargs): ...
    def createSheet(self, **kwargs): ...
    def createNurbCurve(self, **kwargs): ...
    def __getitem__(self, name) -> Geometry: ...
    def __iter__(self, *args) -> Iterable[str]: ...
    def items(self) -> ItemsView[str, Geometry]: ...
    def values(self) -> ValuesView[Geometry]: ...
    def keys(self) -> KeysView[str]: ...

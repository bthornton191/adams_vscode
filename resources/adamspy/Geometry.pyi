import AppearanceSettings
import Manager
from Marker import Marker
import Object
from DesignVariable import DesignVariableManager
from DBAccess import MultiTypeObjectValue as MultiTypeObjectValue
from typing import Any, ItemsView, Iterable, KeysView, List, Tuple, ValuesView

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
    

class GeometryModelManager(Manager.SubclassManager):
    type_map: Any
    def __init__(self, managedClass, parent) -> None: ...
    def createSpringDamper(self, **kwargs): ...
    def createForce(self, **kwargs): ...
    def createGContact(self, **kwargs): ...

class Geometry(Object.ObjectComment, AppearanceSettings.GeometryAppearanceSettings):
    adams_id_id: int
    comment_id: int
    DesignVariables: DesignVariableManager
    Features: Any
    def __init__(self, _DBKey) -> None: ...

class GeometryLink(Geometry):
    comment_id: Any
    depth: Any
    width: Any
    i_marker: Marker
    i_marker_name: str
    j_marker: Marker
    j_marker_name: str

class GeometryEllipse(Geometry):
    comment_id: Any
    adams_id_id: Any
    center_marker: Marker
    center_marker_name: str
    start_angle: Any
    end_angle: Any
    major_radius: Any
    minor_radius: Any

class GeometryTorus(Geometry, Object.ObjectAdamsId):
    major_radius: Any
    minor_radius: Any
    angle_extent: Any
    side_count_for_perimeter: Any
    segment_count: Any
    center_marker: Marker
    center_marker_name: str

class GeometryCircle(Geometry, Object.ObjectAdamsId):
    radius: Any
    segment_count: Any
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
    segment_count: Any
    ref_marker: Marker
    ref_marker_name: str
    ref_curve: Any
    ref_curve_name: str
    def setClosed(self, close): ...
    def getClosed(self): ...
    closed: Any

class GeometryBlock(Geometry):
    x: Any
    y: Any
    z: Any
    corner_marker: Marker
    corner_marker_name: str

class GeometryChain(Geometry):
    comment_id: Any
    adams_id_id: Any
    objects_in_chain: Any

class GeometryCylinder(Geometry, Object.ObjectAdamsId):
    center_marker: Marker
    center_marker_name: str
    angle_extent: Any
    length: Any
    side_count_for_body: Any
    radius: Any
    segment_count_for_ends: Any
    def setRefMarkerRadius(self, marker): ...
    ref_radius_by_marker: Marker

class GeometryEllipsoid(Geometry):
    x_scale_factor: Any
    y_scale_factor: Any
    z_scale_factor: Any
    center_marker: Marker
    center_marker_name: str

class GeometryForce(Geometry, Object.ObjectAdamsId):
    all_force_elements: Any
    applied_at_marker: Marker
    applied_at_marker_name: str
    force_element: Any
    force_element_name: str
    joint: Any
    joint_name: str
    jprim: Any
    jprim_name: str
    curve_curve: Any
    curve_curve_name: str
    point_curve: Any
    point_curve_name: str

class GeometryGContact(Geometry):
    comment_id: Any
    contact_element: Any
    adams_id: Any
    force_display: Any

class GeometryArc(Geometry, Object.ObjectAdamsId):
    center_marker: Marker
    center_marker_name: str
    radius: Any
    angle_extent: Any
    segment_count: Any
    def setRefMarkerRadius(self, marker): ...
    ref_radius_by_marker: Marker
    type_close: Any
    def setClose(self, closure): ...
    def getClose(self): ...
    close: Any

class GeometryFrustum(Geometry, Object.ObjectAdamsId):
    top_radius: Any
    bottom_radius: Any
    angle_extent: Any
    length: Any
    side_count_for_body: Any
    segment_count_for_ends: Any
    center_marker: Marker
    center_marker_name: str

class GeometryOutline(Geometry, Object.ObjectAdamsId):
    visibility_between_markers: Any
    marker: Marker
    marker_name: str

class GeometrySpringDamper(Geometry, Object.ObjectAdamsId):
    diameter_of_spring: Any
    damper_diameter_at_i: Any
    damper_diameter_at_j: Any
    coil_count: Any
    tip_length_at_i: Any
    tip_length_at_j: Any
    cup_length_at_i: Any
    cup_length_at_j: Any
    i_marker: Marker
    i_marker_name: str
    j_marker: Marker
    j_marker_name: str

class GeometryExtrusion(Geometry, Object.ObjectAdamsId):
    def __init__(self, _DBKey) -> None: ...
    analytical: Any
    points_for_profile: Any
    length_along_z_axis: Any
    path_points: Any
    profile_curve: Any
    path_curve: Any
    reference_marker: Marker
    reference_marker_name: str
    relative_to: Any

class GeometryRevolution(Geometry):
    def __init__(self, _DBKey) -> None: ...
    angle_extent: Any
    analytical: Any
    profile_curve: Any
    profile_curve_name: str
    reference_marker: Marker
    reference_marker_name: str
    number_of_sides: Any
    points_for_profile: Any
    relative_to: Any

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
    comment_id: Any
    markers: Any
    width: Any
    radius: Any

class GeometryPoint(Geometry):
    ref_marker: Marker
    ref_marker_name: str

class GeometryCsg(Geometry):
    comment_id: Any
    adams_id_id: Any
    geom_type: Any
    def setCsgExplode(self, val): ...
    explode: Any
    base_object: Any
    base_object_name: str
    object: Any
    object_name: str
    csg_type: Any

class GeometrySolid(Geometry): ...

class GeometryExternal(Geometry):
    solid_id: Any
    rm: Any
    ref_marker_name: str
    faceting_tolerance: Any
    file: Any
    element: Any

class GeometryPolyline(Geometry):
    def __init__(self, _DBKey) -> None: ...
    comment_id: Any
    geom_type: Any
    path_curve: Any
    location: List[float]
    """Locations of the points defining the line.
    
    Note
    ----
    When setting this variable, you must use global coordinates.
    """
    close: Any
    relative_to: Any

class GeometrySheet(Geometry): ...

class GeometryNurbCurve(Geometry):
    comment_id: Any
    degree: Any
    rational: Any
    periodic: Any
    knots: Any
    weights: Any
    control_points: Any

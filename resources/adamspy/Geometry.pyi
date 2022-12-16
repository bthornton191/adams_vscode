import AppearanceSettings
import Manager
from Marker import Marker
import Object
from DesignVariable import DesignVariableManager
from DBAccess import MultiTypeObjectValue as MultiTypeObjectValue
from typing import Any, ItemsView, Iterable, List, Tuple

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
    i_marker: Any
    i_marker_name: Any
    j_marker: Any
    j_marker_name: Any

class GeometryEllipse(Geometry):
    comment_id: Any
    adams_id_id: Any
    center_marker: Any
    center_marker_name: Any
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
    center_marker: Any
    center_marker_name: Any

class GeometryCircle(Geometry, Object.ObjectAdamsId):
    radius: Any
    segment_count: Any
    center_marker: Any
    center_marker_name: Any
    def setRefMarkerRadius(self, marker): ...
    ref_radius_by_marker: Any

class GeometryPlane(Geometry):
    x_minimum: Any
    x_maximum: Any
    y_minimum: Any
    y_maximum: Any
    ref_marker: Any
    ref_marker_name: Any

class GeometryBSpline(Geometry, Object.ObjectAdamsId):
    segment_count: Any
    ref_marker: Any
    ref_marker_name: Any
    ref_curve: Any
    ref_curve_name: Any
    def setClosed(self, close): ...
    def getClosed(self): ...
    closed: Any

class GeometryBlock(Geometry):
    x: Any
    y: Any
    z: Any
    corner_marker: Any
    corner_marker_name: Any

class GeometryChain(Geometry):
    comment_id: Any
    adams_id_id: Any
    objects_in_chain: Any

class GeometryCylinder(Geometry, Object.ObjectAdamsId):
    center_marker: Any
    center_marker_name: Any
    angle_extent: Any
    length: Any
    side_count_for_body: Any
    radius: Any
    segment_count_for_ends: Any
    def setRefMarkerRadius(self, marker): ...
    ref_radius_by_marker: Any

class GeometryEllipsoid(Geometry):
    x_scale_factor: Any
    y_scale_factor: Any
    z_scale_factor: Any
    center_marker: Any
    center_marker_name: Any

class GeometryForce(Geometry, Object.ObjectAdamsId):
    all_force_elements: Any
    applied_at_marker: Any
    applied_at_marker_name: Any
    force_element: Any
    force_element_name: Any
    joint: Any
    joint_name: Any
    jprim: Any
    jprim_name: Any
    curve_curve: Any
    curve_curve_name: Any
    point_curve: Any
    point_curve_name: Any

class GeometryGContact(Geometry):
    comment_id: Any
    contact_element: Any
    adams_id: Any
    force_display: Any

class GeometryArc(Geometry, Object.ObjectAdamsId):
    center_marker: Any
    center_marker_name: Any
    radius: Any
    angle_extent: Any
    segment_count: Any
    def setRefMarkerRadius(self, marker): ...
    ref_radius_by_marker: Any
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
    center_marker: Any
    center_marker_name: Any

class GeometryOutline(Geometry, Object.ObjectAdamsId):
    visibility_between_markers: Any
    marker: Any
    marker_name: Any

class GeometrySpringDamper(Geometry, Object.ObjectAdamsId):
    diameter_of_spring: Any
    damper_diameter_at_i: Any
    damper_diameter_at_j: Any
    coil_count: Any
    tip_length_at_i: Any
    tip_length_at_j: Any
    cup_length_at_i: Any
    cup_length_at_j: Any
    i_marker: Any
    i_marker_name: Any
    j_marker: Any
    j_marker_name: Any

class GeometryExtrusion(Geometry, Object.ObjectAdamsId):
    def __init__(self, _DBKey) -> None: ...
    analytical: Any
    points_for_profile: Any
    length_along_z_axis: Any
    path_points: Any
    profile_curve: Any
    path_curve: Any
    reference_marker: Any
    reference_marker_name: Any
    relative_to: Any

class GeometryRevolution(Geometry):
    def __init__(self, _DBKey) -> None: ...
    angle_extent: Any
    analytical: Any
    profile_curve: Any
    profile_curve_name: Any
    reference_marker: Any
    reference_marker_name: Any
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
    ref_marker: Any
    ref_marker_name: Any

class GeometryCsg(Geometry):
    comment_id: Any
    adams_id_id: Any
    geom_type: Any
    def setCsgExplode(self, val): ...
    explode: Any
    base_object: Any
    base_object_name: Any
    object: Any
    object_name: Any
    csg_type: Any

class GeometrySolid(Geometry): ...

class GeometryExternal(Geometry):
    solid_id: Any
    rm: Any
    ref_marker_name: Any
    faceting_tolerance: Any
    file: Any
    element: Any

class GeometryPolyline(Geometry):
    def __init__(self, _DBKey) -> None: ...
    comment_id: Any
    geom_type: Any
    path_curve: Any
    location: Any
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

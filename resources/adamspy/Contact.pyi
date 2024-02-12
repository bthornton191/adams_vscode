import Manager
import Object
from Geometry import Geometry, GeometrySolid
from DBAccess import MultiTypeObjectName as MultiTypeObjectName, MultiTypeObjectValue as MultiTypeObjectValue
from typing import Any, ItemsView, Iterable, List, ValuesView
from Marker import Marker


class ContactManager(Manager.AdamsManager):
    def createSolidToSolid(self,
                           name: str,
                           i_geometry: GeometrySolid,
                           j_geometry: GeometrySolid,
                           stiffness: float,
                           damping: float,
                           dmax: float,
                           exponent: float,
                           **kwargs) -> Contact: ...

    def createCurveToCurve(self, **kwargs): ...
    def createPointToCurve(self, **kwargs): ...
    def createPointToPlane(self, **kwargs): ...
    def createCurveToPlane(self, **kwargs): ...
    def createSphereToPlane(self, **kwargs): ...
    def createSphereToSphere(self, **kwargs): ...
    def createCylinderToCylinder(self, **kwargs): ...
    def createFlexToFlex(self, **kwargs): ...
    def createFlexEdgeToCurve(self, **kwargs): ...
    def createFlexEdgeToFlexEdge(self, **kwargs): ...
    def createFlexEdgeToPlane(self, **kwargs): ...
    def createFlexToSolid(self, **kwargs): ...
    def __getitem__(self, name) -> Contact: ...
    def __iter__(self, *args) -> Iterable[str]: ...
    def items(self) -> ItemsView[str, Contact]: ...
    def values(self) -> ValuesView[Contact]: ...


class Contact(Object.Object):
    solid_types: Any
    curve_types: Any
    flip_geom_types: Any
    contact_type: Any
    i_geometry: List[Geometry]
    i_geometry_name: List[str]
    j_geometry: List[Geometry]
    j_geometry_name: List[str]
    i_marker: List[Marker]
    i_marker_name: List[str]
    i_flex: Any
    i_flex_name: List[str]
    i_edge: Any
    i_edge_name: List[str]
    i_edge_index: Any
    j_flex: Any
    j_flex_name: List[str]
    j_edge: Any
    j_edge_name: List[str]
    j_edge_index: Any
    i_flip_normal: Any
    j_flip_normal: Any
    i_flip_geometry: Any
    i_flip_geometry_name: List[str]
    j_flip_geometry: Any
    j_flip_geometry_name: List[str]
    geometry_routines: Any
    stiffness: float
    damping: float
    dmax: float
    exponent: float
    penalty: Any
    restitution_coefficient: float
    normal_function: Any
    normal_routine: Any
    augmented_lagrangian_formulation: Any
    friction_function: Any
    friction_routine: Any
    coulomb_friction_dict: Any
    coulomb_friction: str
    mu_static: float
    mu_dynamic: float
    friction_transition_velocity: float
    stiction_transition_velocity: float
    no_friction: Any
    face_contact_top: Any
    face_contact_bottom: Any
    stiction: str
    max_stiction_deformation: float

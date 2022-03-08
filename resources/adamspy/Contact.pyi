import Manager
import Object
from DBAccess import MultiTypeObjectName as MultiTypeObjectName, MultiTypeObjectValue as MultiTypeObjectValue
from typing import Any

class ContactManager(Manager.AdamsManager):
    def createSolidToSolid(self, **kwargs): ...
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

class Contact(Object.Object):
    solid_types: Any
    curve_types: Any
    flip_geom_types: Any
    contact_type: Any
    i_geometry: Any
    i_geometry_name: Any
    j_geometry: Any
    j_geometry_name: Any
    i_marker: Any
    i_marker_name: Any
    i_flex: Any
    i_flex_name: Any
    i_edge: Any
    i_edge_name: Any
    i_edge_index: Any
    j_flex: Any
    j_flex_name: Any
    j_edge: Any
    j_edge_name: Any
    j_edge_index: Any
    i_flip_normal: Any
    j_flip_normal: Any
    i_flip_geometry: Any
    i_flip_geometry_name: Any
    j_flip_geometry: Any
    j_flip_geometry_name: Any
    geometry_routines: Any
    stiffness: Any
    damping: Any
    dmax: Any
    exponent: Any
    penalty: Any
    restitution_coefficient: Any
    normal_function: Any
    normal_routine: Any
    augmented_lagrangian_formulation: Any
    friction_function: Any
    friction_routine: Any
    coulomb_friction_dict: Any
    coulomb_friction: Any
    mu_static: Any
    mu_dynamic: Any
    friction_transition_velocity: Any
    stiction_transition_velocity: Any
    no_friction: Any
    face_contact_top: Any
    face_contact_bottom: Any

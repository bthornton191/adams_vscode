import Manager
import Object
from DBAccess import set_locori_expression as set_locori_expression
from Marker import MarkerManager, Marker
from DesignPoint import DesignPointManager
from Geometry import GeometryManager
from Expression import AdamsExpr as AdamsExpr
from typing import Any, ItemsView, Iterable, KeysView, List, Optional, ValuesView


class PartManager(Manager.SubclassManager):
    def createRigidBody(self, **kwargs) -> RigidBody: ...
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
                       index_in_database: Any = None,
                       damping_ratio: str = None,
                       damping_user_function: Any = None,
                       damping_routine: Any = None,
                       dynamic_limit: Any = None,
                       exact_x: float = None,
                       exact_y: float = None,
                       exact_z: float = None,
                       exact_psi: float = None,
                       exact_theta: float = None,
                       exact_phi: float = None,
                       invariants: Any = None,
                       characteristic_length: Any = None,
                       stability_factor: Any = None,
                       exact_coordinates: Any = None,
                       selected_modes: Any = None,
                       modal_exact_coordinates: Any = None,
                       initial_modal_displacements: Any = None,
                       initial_modal_velocities: Any = None,
                       node_count: Any = None,
                       mode_count: Any = None,
                       modal_neutral_file_name: Any = None,
                       bdf_file_name: Any = None,
                       generalized_damping: Any = None,
                       representation: Any = None,
                       **kwargs) -> FlexBody: ...
    def createPointMass(self, **kwargs) -> PointMass: ...
    def createExternalSystem(self, **kwargs) -> ExternalSystem: ...
    def createFEPart(self, **kwargs) -> FEPart: ...
    def __getitem__(self, name) -> Part: ...
    def __iter__(self, *args) -> Iterable[str]: ...
    def items(self) -> ItemsView[str, Part]: ...
    def values(self) -> ValuesView[Part]: ...
    def keys(self) -> KeysView[str]: ...


class Part(Object.Object):
    Markers: MarkerManager
    DesignPoints: DesignPointManager
    FloatingMarkers: MarkerManager
    Geometries: GeometryManager
    def __init__(self, _DBKey) -> None: ...
    ground_part: bool
    is_flexible: bool
    def destroy(self): ...
    relative_to: Any
    orientation: List[float]
    location: List[float]
    along_axis_orientation: Any
    in_plane_orientation: Any
    cm: Marker


class RigidBody(Part):
    mass: float
    cm: Marker
    cm_name: str
    im: Marker
    im_name: str
    vx: float
    vy: float
    vz: float
    ixx: float
    iyy: float
    izz: float
    ixy: float
    izx: float
    iyz: float
    wx: float
    wy: float
    wz: float
    wm: float
    wm_name: str
    vm: float
    vm_name: str
    exact_x: float
    exact_y: float
    exact_z: float
    exact_psi: float
    exact_theta: float
    exact_phi: float
    planar: bool
    density: float
    material_type: Any
    Geometries: GeometryManager
    def __init__(self, _DBKey) -> None: ...
    inertia_values: List[float]
    plane: Any


class FlexBody(Part):
    vx: float
    vy: float
    vz: float
    wx: float
    wy: float
    wz: float
    vm: float
    vm_name: str
    wm: float
    wm_name: str
    md_db_file_name: str
    index_in_database: Any
    damping_ratio: Optional[str]
    damping_user_function: Any
    damping_routine: Any
    dynamic_limit: Optional[float]
    exact_x: float
    exact_y: float
    exact_z: float
    exact_psi: float
    exact_theta: float
    exact_phi: float
    invariants: Any
    characteristic_length: Any
    stability_factor: Any
    exact_coordinates: Any
    selected_modes: Any
    modal_exact_coordinates: Any
    initial_modal_displacements: Any
    initial_modal_velocities: Any
    node_count: int
    mode_count: int
    modal_neutral_file_name: str
    bdf_file_name: Any
    generalized_damping: Any
    representation: Any
    def disable_modes_by_strain_energy(self, analysis: Any | None = ..., analysis_name: Any | None = ..., energy_tolerance: float = ...) -> None: ...


class PointMass(Part):
    vx: float
    vy: float
    vz: float
    cm: float
    cm_name: str
    mass: float
    vm: float
    vm_name: str
    exact_x: float
    exact_y: float
    exact_z: float
    material_type: Any
    density: float


class ExternalSystem(Part):
    Markers: MarkerManager
    def __init__(self, _DBKey) -> None: ...
    vx: float
    vy: float
    vz: float
    wx: float
    wy: float
    wz: float
    wm: float
    vm: float
    modal_neutral_file_name: str
    md_db_file_name: str
    index_in_database: Any
    interface_routines: Any
    type: Any
    input_file_name: Any


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
    i_location: Any
    j_location: Any
    material_type: Any
    ref_curve: Any
    cratiok: Any
    cratiom: Any
    faceting_tolerance: Any
    fepart_type: Any
    num_nodes: Any
    sorted_s: Any
    preload: Any
    vm: Any
    vm_name: Any
    wm: Any
    wm_name: Any
    coordinates: Any
    Geometries: Any
    def __init__(self, _DBKey) -> None: ...

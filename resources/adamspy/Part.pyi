import Manager
import Object
from DBAccess import set_locori_expression as set_locori_expression
from Expression import AdamsExpr as AdamsExpr
from typing import Any

class PartManager(Manager.SubclassManager):
    def createRigidBody(self, **kwargs): ...
    def createFlexBody(self, **kwargs): ...
    def createPointMass(self, **kwargs): ...
    def createExternalSystem(self, **kwargs): ...
    def createFEPart(self, **kwargs): ...

class Part(Object.Object):
    Markers: Any
    DesignPoints: Any
    FloatingMarkers: Any
    def __init__(self, _DBKey) -> None: ...
    ground_part: Any
    is_flexible: Any
    def destroy(self): ...
    relative_to: Any
    orientation: Any
    location: Any
    along_axis_orientation: Any
    in_plane_orientation: Any

class RigidBody(Part):
    mass: Any
    cm: Any
    cm_name: Any
    im: Any
    im_name: Any
    vx: Any
    vy: Any
    vz: Any
    ixx: Any
    iyy: Any
    izz: Any
    ixy: Any
    izx: Any
    iyz: Any
    wx: Any
    wy: Any
    wz: Any
    wm: Any
    wm_name: Any
    vm: Any
    vm_name: Any
    exact_x: Any
    exact_y: Any
    exact_z: Any
    exact_psi: Any
    exact_theta: Any
    exact_phi: Any
    planar: Any
    density: Any
    material_type: Any
    Geometries: Any
    def __init__(self, _DBKey) -> None: ...
    inertia_values: Any
    plane: Any

class FlexBody(Part):
    vx: Any
    vy: Any
    vz: Any
    wx: Any
    wy: Any
    wz: Any
    vm: Any
    vm_name: Any
    wm: Any
    wm_name: Any
    md_db_file_name: Any
    index_in_database: Any
    damping_ratio: Any
    damping_user_function: Any
    damping_routine: Any
    dynamic_limit: Any
    exact_x: Any
    exact_y: Any
    exact_z: Any
    exact_psi: Any
    exact_theta: Any
    exact_phi: Any
    invariants: Any
    characteristic_length: Any
    stability_factor: Any
    exact_coordinates: Any
    selected_modes: Any
    modal_exact_coordinates: Any
    initial_modal_displacements: Any
    initial_modal_velocities: Any
    node_count: Any
    mode_count: Any
    modal_neutral_file_name: Any
    bdf_file_name: Any
    generalized_damping: Any
    representation: Any
    def disable_modes_by_strain_energy(self, analysis: Any | None = ..., analysis_name: Any | None = ..., energy_tolerance: float = ...) -> None: ...

class PointMass(Part):
    vx: Any
    vy: Any
    vz: Any
    cm: Any
    cm_name: Any
    mass: Any
    vm: Any
    vm_name: Any
    exact_x: Any
    exact_y: Any
    exact_z: Any
    material_type: Any
    density: Any

class ExternalSystem(Part):
    Markers: Any
    def __init__(self, _DBKey) -> None: ...
    vx: Any
    vy: Any
    vz: Any
    wx: Any
    wy: Any
    wz: Any
    wm: Any
    vm: Any
    modal_neutral_file_name: Any
    md_db_file_name: Any
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

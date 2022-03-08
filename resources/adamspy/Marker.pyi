import Manager
import Object
from typing import Any

class MarkerManager(Manager.AdamsManager):
    @staticmethod
    def setDefault(key, type, o_rf) -> None: ...

class Marker(Object.Object):
    def __init__(self, _DBKey) -> None: ...
    node_id: Any
    curve_name: Any
    curve: Any
    velocity: Any
    vx: Any
    vy: Any
    vz: Any
    v1: Any
    v2: Any
    orientation: Any
    location: Any
    relative_to: Any
    reference_marker: Any
    reference_marker_name: Any
    along_axis_orientation: Any
    in_plane_orientation: Any
    location_global: Any

class FloatingMarker(Object.Object):
    node_id: Any
    adams_id: Any

class _i_j_parts_from_markers: ...

class _loc_ori_provider:
    location: Any
    orientation: Any
    relative_to: Any
    along_axis_orientation: Any
    in_plane_orientation: Any

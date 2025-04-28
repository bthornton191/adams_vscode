import Manager
import Object
from Part import Part
from typing import Any, ItemsView, Iterable, KeysView, List, Union, ValuesView


class Marker(Object.Object):
    def __init__(self, _DBKey) -> None: ...
    node_id: int
    curve_name: str
    curve: Any
    velocity: Any
    vx: float
    vy: float
    vz: float
    v1: float
    v2: float
    orientation: List[float]
    """Local when getting, global when setting"""
    location: List[float]
    """Local when getting, global when setting"""
    relative_to: Marker
    reference_marker: Marker
    reference_marker_name: str
    along_axis_orientation: List[float]
    in_plane_orientation: List[float]
    location_global: List[float]


class FloatingMarker(Object.Object):
    node_id: int
    adams_id: int


class _i_j_parts_from_markers:
    ...


class _loc_ori_provider:
    location: List[float]
    orientation: List[float]
    relative_to: Marker
    along_axis_orientation: List[float]
    in_plane_orientation: List[float]


class MarkerManager(Manager.AdamsManager):
    def __getitem__(self, name) -> Marker: ...
    def __iter__(self, *args) -> Iterable[str]: ...
    def items(self) -> ItemsView[str, Marker]: ...
    def values(self) -> ValuesView[Marker]: ...
    def keys(self) -> KeysView[str]: ...

    @staticmethod
    def setDefault(key, type, o_rf) -> None: ...

    def create(self,
               name=None,
               location=[0, 0, 0],
               orientation=[0, 0, 0],
               relative_to: Union[Marker, Part] = None,
               **kwargs) -> Marker:
        """Create a new marker object

        Parameters
        ----------
        name : str
            Name of the marker
        location : List[float]
            Global location of the marker (default is [0, 0, 0])
        orientation : List[float]
            Orientation of the marker. (default is [0, 0, 0])
        relative_to : Marker or Part
            Marker or part to which the new marker is relative to (default is ground)
        """
        ...

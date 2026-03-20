from __future__ import annotations
import DataElement
import Manager
import Object
from Part import Part
from typing import ItemsView, Iterable, KeysView, List, Union, ValuesView


class Marker(Object.Object):
    def __init__(self, _DBKey) -> None: ...
    node_id: List[int]
    """List of node identifiers associated with this marker (used for flex body markers)."""
    curve_name: str
    """Name of the curve along which this marker moves."""
    curve: DataElement.CurveData
    """Curve object along which this marker moves."""
    velocity: float
    """Initial velocity of a marker associated with a curve."""
    vx: float
    """Initial velocity in the x direction of the reference marker (for curve/surface markers)."""
    vy: float
    """Initial velocity in the y direction of the reference marker (for curve/surface markers)."""
    vz: float
    """Initial velocity in the z direction of the reference marker (for curve/surface markers)."""
    v1: float
    """Initial velocity in the first surface parameterization direction (for surface markers)."""
    v2: float
    """Initial velocity in the second surface parameterization direction (for surface markers)."""
    orientation: List[float]
    """Euler angles (ZBP) defining the marker's orientation in degrees. Returns local angles; accepts global angles on set."""
    location: List[float]
    """[x, y, z] location of the marker. Returns local coordinates; accepts global coordinates on set."""
    relative_to: Marker
    """Write-only. Marker relative to which this marker is located and oriented."""
    reference_marker: Marker
    """Reference marker object."""
    reference_marker_name: str
    """Full dot-path name of the reference marker."""
    along_axis_orientation: List[float]
    """Write-only. Orient by directing an axis: provide [x, y, z] of a point on the axis, or [x1, y1, z1, x2, y2, z2] for two points. Adams assigns an arbitrary rotation about the axis."""
    in_plane_orientation: List[float]
    """Write-only. Orient by axis + in-plane point: provide 6 values (axis point + in-plane point) or 9 values (origin + axis point + in-plane point)."""
    location_global: List[float]
    """Read-only. Global location of the marker [x, y, z]."""

    def setUseClosestNodeId(self, flex_body=None, flex_body_name: str = None, num_nodes: int = 1) -> None: ...


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

import Manager
import Object
from typing import Any, List, Literal


class FeatureManager(Manager.SubclassManager):
    def createThinShell(self,
                        name: str = None,
                        thickness: float = None,
                        subids: List[int] = None,
                        locations: List[float] = None,
                        **kwargs) -> FeatureThinShell:
        """Create a thin shell feature.

        Parameters
        ----------
        name : str, optional
            Name of the feature.
        thickness : float
            Shell thickness.
        subids : list of int, optional
            Sub-element IDs to apply the shell to.
        locations : list of float, optional
            Coordinates in multiples of 3 defining shell locations.
        """
        ...

    def createHole(self,
                   name: str = None,
                   radius: float = None,
                   subid: int = 0,
                   countersink: str = 'no',
                   center: List[float] = None,
                   depth: float = 0.0,
                   **kwargs) -> FeatureHole:
        """Create a hole feature.

        Parameters
        ----------
        name : str, optional
            Name of the feature.
        radius : float
            Hole radius.
        subid : int, optional
            Sub-element ID (default 0).
        countersink : str, optional
            Whether to countersink (default ``'no'``).
        center : list of float, optional
            [x, y, z] center coordinates of the hole.
        depth : float, optional
            Hole depth (default 0.0).
        """
        ...

    def createBlend(self,
                    name: str = None,
                    radius1: float = None,
                    subtype: Literal['edge', 'vertex'] = None,
                    subids: List[int] = None,
                    reference_marker: Object.Object = None,
                    reference_marker_name: str = None,
                    chamfer: str = 'no',
                    locations: List[float] = None,
                    radius2: float = None,
                    **kwargs) -> FeatureBlend:
        """Create a blend (fillet/chamfer) feature.

        Parameters
        ----------
        name : str, optional
            Name of the feature.
        radius1 : float
            Primary blend radius.
        subtype : str
            ``'edge'`` or ``'vertex'``.
        subids : list of int, optional
            Sub-element IDs.
        reference_marker : Marker, optional
            Reference marker for the blend.
        reference_marker_name : str, optional
            Full name of the reference marker.
        chamfer : str, optional
            Whether to chamfer (default ``'no'``).
        locations : list of float, optional
            Coordinates in multiples of 3.
        radius2 : float, optional
            Secondary radius (defaults to ``radius1``).
        """
        ...


class Feature(Object.Object):
    ...


class FeatureThinShell(Feature):
    subids: Any
    thickness: Any
    locations: Any


class FeatureHole(Feature):
    subid: Any
    center: Any
    countersink: Any
    radius: Any
    depth: Any


class FeatureBlend(Feature):
    subtype: Any
    subids: Any
    locations: Any
    chamfer: Any
    radius1: Any
    radius2: Any
    reference_marker: Any

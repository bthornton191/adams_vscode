import Manager
import Object
from DBAccess import ObjectName as ObjectName, ObjectValue as ObjectValue, RealArrayValue as RealArrayValue, RealValue as RealValue
from ctypes import byref as byref, c_double as c_double
from typing import ItemsView, Iterable, List, OrderedDict, Union, ValuesView

BUFFER_SIZE: int


class ResultComponent(Object.ObjectBase):
    values: List[float]
    unit: str


class Analysis(Object.ObjectBase):
    def __init__(self, _DBKey) -> None: ...
    title: str
    date_time: str
    """Read-only. Time and date for this analysis."""
    solver: str
    """Read-only. Solver for this analysis."""
    step_count: int
    """Read-only. Number of steps."""
    results_steps: int
    """Read-only. Number of result steps."""
    results_file: str
    results_version: int
    """Read-only. Results version."""
    graphics_steps: int
    """Read-only. Number of graphics steps."""
    request_steps: int
    """Read-only. Number of request steps."""
    step_type: int
    """Read-only. Step type."""
    results_from_xrf: bool
    """Read-only. Results from XRF."""
    terminal_status: str
    """Read-only. Terminal status."""
    simulation_status: List[int]
    """Read-only. Simulation status."""
    results: OrderedDict[str, Union[ResultComponent, OrderedDict[str, ResultComponent]]]
    """Read-only. Dictionary of results sets and components."""
    start_time: float
    """Read-only. Start time for the analysis."""
    end_time: float
    """Read-only. End time (terminal time) for the analysis."""


class AnalysisManager(Manager.AdamsManager):
    def createFromFile(self, *, file_name: str, name: str = None) -> Analysis:
        """Create an analysis from a .res, .req or .gra file 

        Parameters
        ----------
        file_name : str
            The name of the file to load
        name : str, optional
            The name to give the analysis, by default the base name of the file is used

        Returns
        -------
        Analysis
            The analysis object
        """

    def create(self, name: str = None, **kwargs) -> Analysis:
        """Create a new Analysis.

        Parameters
        ----------
        name : str, optional
            Name of the analysis.
        """
        ...

    def __getitem__(self, name: str) -> Analysis: ...
    def __iter__(self, *args) -> Iterable[str]: ...
    def items(self) -> ItemsView[str, Analysis]: ...
    def values(self) -> ValuesView[Analysis]: ...

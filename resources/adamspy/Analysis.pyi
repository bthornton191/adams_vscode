import Manager
import Object
from DBAccess import ObjectName as ObjectName, ObjectValue as ObjectValue, RealArrayValue as RealArrayValue, RealValue as RealValue
from ctypes import byref as byref, c_double as c_double
from typing import Any, ItemsView, Iterable, List, OrderedDict, Union, ValuesView

BUFFER_SIZE: int

class AnalysisManager(Manager.AdamsManager):
    def createFromFile(self, *, file_name: str, name:str =None)->Analysis: 
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
    def create(self, name=None, **kwargs) -> Analysis: ...
    def __getitem__(self, name: str) -> Analysis: ...
    def __iter__(self, *args) -> Iterable[str]: ...
    def items(self) -> ItemsView[str, Analysis]: ...
    def values(self) -> ValuesView[Analysis]: ...


class ResultComponent(Object.ObjectBase):
    values: List[float]

class Analysis(Object.ObjectBase):
    def __init__(self, _DBKey) -> None: ...
    title: Any
    date_time: Any
    solver: Any
    step_count: Any
    results_steps: Any
    results_file: Any
    results_version: Any
    graphics_steps: Any
    request_steps: Any
    step_type: Any
    results_from_xrf: Any
    terminal_status: Any
    simulation_status: Any
    results: OrderedDict[str, Union[ResultComponent, OrderedDict[str, ResultComponent]]]
    start_time: Any
    end_time: Any

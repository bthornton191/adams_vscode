import Manager
import Object
from DBAccess import ObjectName as ObjectName, ObjectValue as ObjectValue, RealArrayValue as RealArrayValue, RealValue as RealValue
from ctypes import byref as byref, c_double as c_double
from typing import Any, ItemsView, Iterable, List, OrderedDict, ValuesView

BUFFER_SIZE: int

class AnalysisManager(Manager.AdamsManager):
    def createFromFile(self, **kwargs): ...

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
    results: OrderedDict[str, ResultComponent]
    start_time: Any
    end_time: Any

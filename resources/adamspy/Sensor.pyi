import Object
from typing import Any, ItemsView, Iterable, KeysView, ValuesView
import Manager


class Sensor(Object.Object):
    compare: str
    """'eq', 'ge' or 'le'
    """
    codgen: bool
    halt: bool
    sensor_print: bool
    restart: bool
    sensor_return: bool
    """returns to the command level when the sensor is triggered"""
    yydump: bool
    bisection: float
    time_error: float
    dt: float
    value: float
    error: float
    angular: float
    angular_value: float
    angular_error: float
    stepsize: float
    function: str
    user_function: str
    routine: str
    evaluate: str
    user_evaluate: str
    evaluate_routine: str


class SensorManager(Manager.SubclassManager):
    def create(self,
               name: str = None,
               function: str = None,
               evaluate: str = None,
               time_error: float = None,
               compare: str = None,
               angular_value: float = None,
               codgen: bool = None,
               dt: float = None,
               halt: bool = None,
               restart: bool = None,
               sensor_return: bool = None,
               yydump: bool = None,
               angular_error: float = None,
               sensor_print: bool = None) -> Sensor: ...

    def items(self) -> ItemsView[str, Sensor]: ...
    def values(self) -> ValuesView[Sensor]: ...
    def keys(self) -> KeysView[str]: ...
    def __getitem__(self, name) -> Sensor: ...
    def __iter__(self, *args) -> Iterable[str]: ...

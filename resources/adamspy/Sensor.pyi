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
               compare: str = None,
               value: float = None,
               error: float = None,
               angular_value: float = None,
               angular_error: float = None,
               time_error: float = None,
               codgen: bool = None,
               dt: float = None,
               halt: bool = None,
               restart: bool = None,
               sensor_return: bool = None,
               yydump: bool = None,
               sensor_print: bool = None) -> Sensor:
        """_summary_

        Parameters
        ----------
        name : str
            Name of the sensor
        function : str
            Specifies a FUNCTION expression to define the sensor.
        evaluate : str, optional
            Run time function describing the return value
        compare : str
            Can be "GE", "EQ", or "LE". Specifies what kind of comparison is to be made to initiate 
            the action by the SENSOR.
        value : float, optional
            Specifies the non-angular VALUE you want to relate to the FUNCTION that Adams is 
            sensing.
        error : float, optional
            Specifies the absolute non-angular value of allowable error between VALUE and the value 
            of the FUNCTION that Adams is sensing.
        angular_value : float, optional
            Specifies the angular VALUE you want to relate to the FUNCTION that Adams is sensing.
        angular_error : float, optional
            Specifies the absolute angular value of allowable error between VALUE and the value of 
            the FUNCTION that Adams is sensing.
        time_error : float, optional
            Amount of time error allowed for the sensor to trigger
        codgen : bool, optional
            Specifies that Adams is to generate a new pivot sequence for matrix factorization when 
            the event Adams is sensing has the specified relationship to VALUE.
        dt : float, optional
            Specifies that the time between consecutive output steps should be redefined. This is 
            done when Adams first senses that the FUNCTION specified has the same relationship as
            specified to VALUE. Adams uses this value until it is changed.
        halt : bool, optional
            Specifies that execution should be terminated when the FUNCTION that Adams is sensing, 
            has the specified relationship to VALUE.
        restart : bool, optional
            Specifies that Adams should restart the integration when the FUNCTION that Adams is 
            sensing has the specified relationship to VALUE. Adams reinitializes the integration 
            step size to HINIT and reduces the integration order to one.
        sensor_return : bool, optional
            Specifies that Adams should stop the simulation and return to the command level, when 
            the FUNCTION that Adams is sensing has the specified relationship to VALUE.
        yydump : bool, optional
            Specifies that Adams should dump the state variable vector when the FUNCTION that Adams 
            is sensing has the specified relationship to VALUE.
        sensor_print : bool, optional
            Specifies that Adams should write data to the request, graphics, and output files when 
            the FUNCTION that Adams is sensing, has the specified relationship to VALUE.

        Returns
        -------
        Sensor

        """
        ...

    def items(self) -> ItemsView[str, Sensor]: ...
    def values(self) -> ValuesView[Sensor]: ...
    def keys(self) -> KeysView[str]: ...
    def __getitem__(self, name) -> Sensor: ...
    def __iter__(self, *args) -> Iterable[str]: ...

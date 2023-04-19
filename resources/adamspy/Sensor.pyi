import Object
from typing import Any

class Sensor(Object.Object):
    compare: str
    """'eq', 'ge' or 'le'
    """
    codgen: Any
    halt: Any
    sensor_print: Any
    restart: Any
    sensor_return: bool
    """returns to the command level when the sensor is triggered"""
    yydump: Any
    bisection: Any
    time_error: Any
    dt: Any
    value: Any
    error: Any
    angular: Any
    angular_value: Any
    angular_error: Any
    stepsize: Any
    function: Any
    user_function: Any
    routine: Any
    evaluate: str
    user_evaluate: Any
    evaluate_routine: Any

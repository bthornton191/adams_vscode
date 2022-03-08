import Manager
import Object
from ctypes import POINTER as POINTER, c_bool as c_bool, c_double as c_double, c_int as c_int, cast as cast
from typing import Any

BUFFER_SIZE: Any

class RuntimeFunctionManager(Manager.AdamsManager): ...

class RuntimeFunction(Object.ObjectBase):
    text_of_expression: Any
    argument_names: Any
    name: Any
    def modify(self, **kwargs) -> None: ...

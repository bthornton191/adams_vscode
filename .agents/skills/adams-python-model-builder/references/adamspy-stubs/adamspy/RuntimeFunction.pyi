import Manager
import Object
from ctypes import POINTER as POINTER, c_bool as c_bool, c_double as c_double, c_int as c_int, cast as cast
from typing import List, Optional

BUFFER_SIZE: int


class RuntimeFunctionManager(Manager.AdamsManager):
    ...


class RuntimeFunction(Object.ObjectBase):
    text_of_expression: str
    argument_names: Optional[List[str]]
    name: str
    def modify(self, **kwargs) -> None: ...

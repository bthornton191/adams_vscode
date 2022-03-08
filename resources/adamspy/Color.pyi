import Manager
import Object
from DBAccess import IntArrayValue as IntArrayValue, RealArrayValue as RealArrayValue
from typing import Any

class ColorManager(Manager.AdamsManager): ...

class Color(Object.ObjectBase):
    def __init__(self, _DBKey) -> None: ...
    rgb: Any

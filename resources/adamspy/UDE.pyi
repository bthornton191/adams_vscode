import Manager
import Object
from typing import Any

UdeModifyMacroDict: Any

class UDEDesignVariableProps:
    prop: Any
    def __init__(self, p) -> None: ...
    def __get__(self, instance, owner): ...
    def __set__(self, instance, val) -> None: ...
    def __delete__(self, instance) -> None: ...

class UserDefinedElementManager(Manager.AdamsManager): ...
class UserDefinedInstanceManager(Manager.AdamsManager): ...

class UserDefinedElement(Object.ObjectBase):
    definition_name: Any
    input_parameters: Any
    isa: Any
    objects: Any
    output_parameters: Any
    parameters: Any

class UserDefinedInstance(Object.ObjectBase):
    definition_name: Any
    definition: Any
    objects: Any
    input_parameters: Any
    output_parameters: Any
    parameters: Any
    inst_name: Any
    instance_name: Any
    location: Any
    orientation: Any
    params: Any
    def setProperties(self, **inDct) -> None: ...
    update: Any

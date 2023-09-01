import Manager
import Object
from DesignVariable import DesignVariable
from typing import Any, ItemsView, Iterable, KeysView, List, ValuesView

UdeModifyMacroDict: Any

class UDEDesignVariableProps:
    prop: Any
    def __init__(self, p) -> None: ...
    def __get__(self, instance, owner): ...
    def __set__(self, instance, val) -> None: ...
    def __delete__(self, instance) -> None: ...

class UserDefinedElementManager(Manager.AdamsManager):
    def items(self) -> ItemsView[str, UserDefinedElement]: ...
    def values(self) -> ValuesView[UserDefinedElement]: ...
    def keys(self) -> KeysView[str]: ...
    def __getitem__(self, name) -> UserDefinedElement: ...
    def __iter__(self, *args) -> Iterable[str]: ...

class UserDefinedInstanceManager(Manager.AdamsManager):
    def items(self) -> ItemsView[str, UserDefinedInstance]: ...
    def values(self) -> ValuesView[UserDefinedInstance]: ...
    def keys(self) -> KeysView[str]: ...
    def __getitem__(self, name) -> UserDefinedInstance: ...
    def __iter__(self, *args) -> Iterable[str]: ...

class UserDefinedElement(Object.ObjectBase):
    definition_name: str
    input_parameters: List[DesignVariable]
    isa: Any
    objects: List[Object.ObjectBase]
    output_parameters: List[DesignVariable]
    parameters: List[DesignVariable]

class UserDefinedInstance(Object.ObjectBase):
    definition_name: str
    definition: str
    objects: List[Object.ObjectBase]
    input_parameters: List[DesignVariable]
    output_parameters: List[DesignVariable]
    parameters: List[DesignVariable]
    inst_name: str
    instance_name: str
    location: List[float]
    orientation: List[float]
    params: Any
    def setProperties(self, **inDct) -> None: ...
    update: Any

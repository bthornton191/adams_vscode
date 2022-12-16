import Manager
import Object
from typing import Any, ItemsView, Iterable, Union, List, ValuesView

class DesignVariableManager(Manager.SubclassManager):
    iDv: str
    rDv: str
    sDv: str
    oDv: str
    def createInteger(self, **kwargs): ...
    def createReal(self, **kwargs): ...

    def createString(self, name: str = '', value: Union[str, List[str]] = '', **kwargs):
        """Creates a Design Variable of type `string`
        """
        ...
    def createObject(self, **kwargs): ...
    
    def __getitem__(self, name) -> Union[IntegerDesignVariable, RealDesignVariable, StringDesignVariable, ObjectDesignVariable]: ...
    def __iter__(self, *args) -> Iterable[str]: ...
    def items(self) -> ItemsView[str, Union[IntegerDesignVariable, RealDesignVariable, StringDesignVariable, ObjectDesignVariable]]: ...
    def values(self) -> ValuesView[Union[IntegerDesignVariable, RealDesignVariable, StringDesignVariable, ObjectDesignVariable]]: ...

class DesignVariable(Object.ObjectComment, Object.ObjectAdamsId):
    adams_id: Any
    def save(self) -> None: ...
    def restore(self) -> None: ...

obj_not_allowed_in_dv: Any
dv_objects: Any
__: Any

class IntegerDesignVariable(DesignVariable):
    value: List[int]
    range: Any
    allowed_values: Any
    delta_type: Any
    use_range: Any
    use_allowed_values: Any
    sensitivity: Any

class RealDesignVariable(DesignVariable):
    value: List[float]
    range: Any
    sensitivity: Any
    allowed_values: Any
    delta_type: Any
    use_range: Any
    use_allowed_values: Any
    units: Any

class StringDesignVariable(DesignVariable):
    value: List[str]

class ObjectDesignVariable(DesignVariable):
    value: List[Object.Object]

import Manager
import Object
from typing import Any

class DesignVariableManager(Manager.SubclassManager):
    iDv: str
    rDv: str
    sDv: str
    oDv: str
    def createInteger(self, **kwargs): ...
    def createReal(self, **kwargs): ...
    def createString(self, **kwargs): ...
    def createObject(self, **kwargs): ...

class DesignVariable(Object.ObjectComment, Object.ObjectAdamsId):
    adams_id: Any
    def save(self) -> None: ...
    def restore(self) -> None: ...

obj_not_allowed_in_dv: Any
dv_objects: Any
__: Any

class IntegerDesignVariable(DesignVariable):
    value: Any
    range: Any
    allowed_values: Any
    delta_type: Any
    use_range: Any
    use_allowed_values: Any
    sensitivity: Any

class RealDesignVariable(DesignVariable):
    value: Any
    range: Any
    sensitivity: Any
    allowed_values: Any
    delta_type: Any
    use_range: Any
    use_allowed_values: Any
    units: Any

class StringDesignVariable(DesignVariable):
    value: Any

class ObjectDesignVariable(DesignVariable):
    value: Any

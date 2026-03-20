import Manager
import Object
from typing import Any, ItemsView, Iterable, List, Literal, Optional, Union, ValuesView


class DesignVariable(Object.ObjectComment, Object.ObjectAdamsId):
    adams_id: Optional[int]
    def save(self) -> None: ...
    def restore(self) -> None: ...


obj_not_allowed_in_dv: List[str]
dv_objects: List[str]
__: Any


class IntegerDesignVariable(DesignVariable):
    value: List[int]
    """Integer number(s) stored in this Adams View variable."""
    range: List[float]
    """Range of values allowed for this variable [min, max]."""
    allowed_values: List[float]
    """Explicit list of allowed values for this variable."""
    delta_type: Literal['absolute', 'relative', 'percent_relative']
    """Perturbation delta type used in design studies. Default is 'absolute'."""
    use_range: bool
    """If True, the range specified by the range parameter is enforced."""
    use_allowed_values: bool
    """If True, the allowed_values list is enforced."""
    sensitivity: bool


class RealDesignVariable(DesignVariable):
    value: List[float]
    """Real number(s) stored in this Adams View variable."""
    range: List[float]
    """Range of values allowed for this variable [min, max]."""
    sensitivity: bool
    allowed_values: List[float]
    """Explicit list of allowed values for this variable."""
    delta_type: Literal['absolute', 'relative', 'percent_relative']
    """Perturbation delta type used in design studies. Default is 'absolute'."""
    use_range: bool
    """If True, the range specified by the range parameter is enforced."""
    use_allowed_values: bool
    """If True, the allowed_values list is enforced."""
    units: str
    """Units for this design variable."""


class StringDesignVariable(DesignVariable):
    value: List[str]
    """String(s) stored in this Adams View variable."""


class ObjectDesignVariable(DesignVariable):
    value: List[Object.Object]
    """Existing object(s) stored in this Adams View variable."""


class DesignVariableManager(Manager.SubclassManager):
    iDv: str
    rDv: str
    sDv: str
    oDv: str
    def createInteger(self, **kwargs) -> IntegerDesignVariable: ...
    def createReal(self, **kwargs) -> RealDesignVariable: ...

    def createString(self, name: str = '', value: Union[str, List[str]] = '', **kwargs) -> StringDesignVariable:
        """Creates a Design Variable of type `string`
        """
        ...

    def createObject(self, **kwargs) -> ObjectDesignVariable: ...

    def __getitem__(self, name) -> Union[IntegerDesignVariable, RealDesignVariable, StringDesignVariable, ObjectDesignVariable]: ...
    def __iter__(self, *args) -> Iterable[str]: ...
    def items(self) -> ItemsView[str, Union[IntegerDesignVariable, RealDesignVariable, StringDesignVariable, ObjectDesignVariable]]: ...
    def values(self) -> ValuesView[Union[IntegerDesignVariable, RealDesignVariable, StringDesignVariable, ObjectDesignVariable]]: ...

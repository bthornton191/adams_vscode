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

    def createInteger(self,
                      name: str = None,
                      value: Union[int, List[int]] = None,
                      range: List[int] = None,
                      allowed_values: List[int] = None,
                      use_range: bool = None,
                      use_allowed_values: bool = None,
                      **kwargs) -> IntegerDesignVariable:
        """Create an integer design variable.

        Parameters
        ----------
        name : str, optional
            Name of the design variable.
        value : int or list of int, optional
            Integer value(s).
        range : list of int, optional
            Allowed range [min, max].
        allowed_values : list of int, optional
            Discrete set of allowed values.
        use_range : bool, optional
            Whether to enforce the range constraint.
        use_allowed_values : bool, optional
            Whether to enforce the allowed values constraint.
        """
        ...

    def createReal(self,
                   name: str = None,
                   value: Union[float, List[float]] = None,
                   range: List[float] = None,
                   allowed_values: List[float] = None,
                   use_range: bool = None,
                   use_allowed_values: bool = None,
                   units: str = None,
                   **kwargs) -> RealDesignVariable:
        """Create a real design variable.

        Parameters
        ----------
        name : str, optional
            Name of the design variable.
        value : float or list of float, optional
            Real value(s).
        range : list of float, optional
            Allowed range [min, max].
        allowed_values : list of float, optional
            Discrete set of allowed values.
        use_range : bool, optional
            Whether to enforce the range constraint.
        use_allowed_values : bool, optional
            Whether to enforce the allowed values constraint.
        units : str, optional
            Unit string for the design variable.
        """
        ...

    def createString(self, name: str = '', value: Union[str, List[str]] = '', **kwargs) -> StringDesignVariable:
        """Create a string design variable.

        Parameters
        ----------
        name : str, optional
            Name of the design variable.
        value : str or list of str, optional
            String value(s).
        """
        ...

    def createObject(self,
                     name: str = None,
                     value: List[Object.Object] = None,
                     value_name: List[str] = None,
                     **kwargs) -> ObjectDesignVariable:
        """Create an object design variable.

        Parameters
        ----------
        name : str, optional
            Name of the design variable.
        value : list of Object, optional
            Object(s) stored in this variable.
        value_name : list of str, optional
            Full name(s) of the object(s).
        """
        ...

    def __getitem__(self, name) -> Union[IntegerDesignVariable, RealDesignVariable, StringDesignVariable, ObjectDesignVariable]: ...
    def __iter__(self, *args) -> Iterable[str]: ...
    def items(self) -> ItemsView[str, Union[IntegerDesignVariable, RealDesignVariable, StringDesignVariable, ObjectDesignVariable]]: ...
    def values(self) -> ValuesView[Union[IntegerDesignVariable, RealDesignVariable, StringDesignVariable, ObjectDesignVariable]]: ...

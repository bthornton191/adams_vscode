import Object
from typing import Any
from Model import Model


class AdamsDefaults(Object.ObjectBase):
    def __init__(self, _DBKey) -> None: ...
    units: DefaultUnits
    coordinate_system: Any
    def get(self, type): ...
    model: Model
    IconName_type: Any
    icon_naming: Any
    @property
    def info(self): ...


class DefaultUnits(Object.ObjectSubBase):
    def __init__(self) -> None: ...
    length: str
    mass: str
    time: str
    angle: str
    force: str
    frequency: str

    def setUnits(self,
                 length: str | None = ...,
                 mass: str | None = ...,
                 time: str | None = ...,
                 angle: str | None = ...,
                 force: str | None = ...,
                 frequency: str | None = ...) -> None:
        """Sets the model units

        Parameters
        ----------
        length : str, optional
            Can be one of the following:
            - 'mm'
            - 'cm'
            - 'meter'
            - 'km'
            - 'inch'
            - 'foot'
            - 'mile'
            - 'micrometer'
            - 'nanometer'
            - 'angstrom'
            - 'microinch'
            - 'mils'
            - 'yard'

        mass : str, optional
            Can be one of the following:
            - 'kg'
            - 'gram'
            - 'pound_mass'
            - 'kpound_mass'
            - 'slug'
            - 'slinch'
            - 'ounce_mass'
            - 'tonne'
            - 'milligram'
            - 'microgram'
            - 'nanogram'
            - 'us_ton'

        time : str, optional
            Can be one of the following:
            - 'second'
            - 'millisecond'
            - 'microsecond'
            - 'nanosecond'
            - 'minute'
            - 'hour'
            - 'day'

        angle : str, optional
            Can be one of the following:
            - 'degrees'
            - 'radians'
            - 'angular_minutes'
            - 'angular_seconds'
            - 'revolutions'
        force: str, optional
            Can be one of the following:
            - 'newton'
            - 'knewton'
            - 'dyne'
            - 'pound_force'
            - 'kpound_force'
            - 'kg_force'
            - 'ounce_force'
            - 'millinewton'
            - 'centinewton'
            - 'poundal'
            - 'micronewton'
            - 'nanonewton'
            - 'meganewton'  
        frequency: str, optional
            Can be one of the following:
            - 'hz'
            - 'radians_sec'
        """
        ...

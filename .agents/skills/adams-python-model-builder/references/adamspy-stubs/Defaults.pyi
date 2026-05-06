import Object
from typing import Any, Literal
from Model import Model


class DefaultUnits(Object.ObjectSubBase):
    def __init__(self) -> None: ...
    length: Literal['mm', 'cm', 'meter', 'km', 'inch', 'foot', 'mile', 'micrometer', 'nanometer', 'angstrom', 'microinch', 'mils', 'yard']
    mass: Literal['kg', 'gram', 'pound_mass', 'kpound_mass', 'slug', 'slinch', 'ounce_mass', 'tonne', 'milligram', 'microgram', 'nanogram', 'us_ton']
    time: Literal['second', 'millisecond', 'microsecond', 'nanosecond', 'minute', 'hour', 'day']
    angle: Literal['degrees', 'radians', 'angular_minutes', 'angular_seconds', 'revolutions']
    force: Literal['newton', 'knewton', 'dyne', 'pound_force', 'kpound_force', 'kg_force', 'ounce_force',
                   'millinewton', 'centinewton', 'poundal', 'micronewton', 'nanonewton', 'meganewton']
    frequency: Literal['hz', 'radians_sec']

    def setUnits(self,
                 length: Literal['mm', 'cm', 'meter', 'km', 'inch', 'foot', 'mile', 'micrometer',
                                 'nanometer', 'angstrom', 'microinch', 'mils', 'yard'] | None = ...,
                 mass: Literal['kg', 'gram', 'pound_mass', 'kpound_mass', 'slug', 'slinch',
                               'ounce_mass', 'tonne', 'milligram', 'microgram', 'nanogram', 'us_ton'] | None = ...,
                 time: Literal['second', 'millisecond', 'microsecond', 'nanosecond', 'minute', 'hour', 'day'] | None = ...,
                 angle: Literal['degrees', 'radians', 'angular_minutes', 'angular_seconds', 'revolutions'] | None = ...,
                 force: Literal['newton', 'knewton', 'dyne', 'pound_force', 'kpound_force', 'kg_force', 'ounce_force',
                                'millinewton', 'centinewton', 'poundal', 'micronewton', 'nanonewton', 'meganewton'] | None = ...,
                 frequency: Literal['hz', 'radians_sec'] | None = ...) -> None:
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

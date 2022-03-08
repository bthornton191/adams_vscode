import Object
from typing import Any

class AdamsDefaults(Object.ObjectBase):
    def __init__(self, _DBKey) -> None: ...
    units: Any
    coordinate_system: Any
    def get(self, type): ...
    model: Any
    IconName_type: Any
    icon_naming: Any
    @property
    def info(self): ...

class DefaultUnits(Object.ObjectSubBase):
    def __init__(self) -> None: ...
    length: Any
    mass: Any
    time: Any
    angle: Any
    force: Any
    frequency: Any
    def setUnits(self, length: Any | None = ..., mass: Any | None = ..., time: Any | None = ..., angle: Any | None = ..., force: Any | None = ..., frequency: Any | None = ...) -> None: ...

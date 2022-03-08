import Manager
import Object
from typing import Any

class SectionManager(Manager.SubclassManager):
    def createRectangular(self, **kwargs): ...
    def createCircular(self, **kwargs): ...
    def createIBeam(self, **kwargs): ...
    def createEllipse(self, **kwargs): ...
    def createFromProperties(self, **kwargs): ...

class Section(Object.Object):
    def __init__(self, _DBKey) -> None: ...
    autoCalculate: Any
    jxx: Any
    iyy: Any
    izz: Any
    iyz: Any
    area: Any

class Rectangular(Section):
    def __init__(self, _DBKey) -> None: ...
    rect_height: Any
    rect_base: Any
    rect_thickness: Any

class Circular(Section):
    def __init__(self, _DBKey) -> None: ...
    cyl_radius: Any
    cyl_thickness: Any

class IBeam(Section):
    def __init__(self, _DBKey) -> None: ...
    ib_height: Any
    ib_base: Any
    ib_flange: Any
    ib_web: Any

class Ellipse(Section):
    def __init__(self, _DBKey) -> None: ...
    major_radius: Any
    minor_radius: Any
    start_angle: Any
    end_angle: Any

import Manager
import Object


class SectionManager(Manager.SubclassManager):
    def createRectangular(self, **kwargs): ...
    def createCircular(self, **kwargs): ...
    def createIBeam(self, **kwargs): ...
    def createEllipse(self, **kwargs): ...
    def createFromProperties(self, **kwargs): ...


class Section(Object.Object):
    def __init__(self, _DBKey) -> None: ...
    autoCalculate: bool
    jxx: float
    iyy: float
    izz: float
    iyz: float
    area: float


class Rectangular(Section):
    def __init__(self, _DBKey) -> None: ...
    rect_height: float
    rect_base: float
    rect_thickness: float


class Circular(Section):
    def __init__(self, _DBKey) -> None: ...
    cyl_radius: float
    cyl_thickness: float


class IBeam(Section):
    def __init__(self, _DBKey) -> None: ...
    ib_height: float
    ib_base: float
    ib_flange: float
    ib_web: float


class Ellipse(Section):
    def __init__(self, _DBKey) -> None: ...
    major_radius: float
    minor_radius: float
    start_angle: float
    end_angle: float

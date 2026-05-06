import Manager
import Object


class SectionManager(Manager.SubclassManager):
    def createRectangular(self,
                          name: str = None,
                          rect_height: float = 10.0,
                          rect_base: float = 15.0,
                          rect_thickness: float = -1,
                          autoCalculate: bool = True,
                          **kwargs) -> Section:
        """Create a rectangular cross-section.

        Parameters
        ----------
        name : str, optional
            Name of the section.
        rect_height : float, optional
            Height of the rectangle (default 10.0).
        rect_base : float, optional
            Base width of the rectangle (default 15.0).
        rect_thickness : float, optional
            Wall thickness; -1 for solid (default -1).
        autoCalculate : bool, optional
            Auto-calculate section properties (default True).
        """
        ...

    def createCircular(self,
                       name: str = None,
                       cyl_radius: float = 10.0,
                       cyl_thickness: float = -1,
                       autoCalculate: bool = True,
                       **kwargs) -> Section:
        """Create a circular cross-section.

        Parameters
        ----------
        name : str, optional
            Name of the section.
        cyl_radius : float, optional
            Radius of the circle (default 10.0).
        cyl_thickness : float, optional
            Wall thickness; -1 for solid (default -1).
        autoCalculate : bool, optional
            Auto-calculate section properties (default True).
        """
        ...

    def createIBeam(self,
                    name: str = None,
                    ib_height: float = 50.0,
                    ib_base: float = 25.0,
                    ib_flange: float = 5.0,
                    ib_web: float = 5.0,
                    autoCalculate: bool = True,
                    **kwargs) -> Section:
        """Create an I-beam cross-section.

        Parameters
        ----------
        name : str, optional
            Name of the section.
        ib_height : float, optional
            Total height of the I-beam (default 50.0).
        ib_base : float, optional
            Flange width (default 25.0).
        ib_flange : float, optional
            Flange thickness (default 5.0).
        ib_web : float, optional
            Web thickness (default 5.0).
        autoCalculate : bool, optional
            Auto-calculate section properties (default True).
        """
        ...

    def createEllipse(self,
                      name: str = None,
                      major_radius: float = 100.0,
                      minor_radius: float = 50.0,
                      start_angle: float = 0.0,
                      end_angle: float = 360.0,
                      autoCalculate: bool = True,
                      **kwargs) -> Section:
        """Create an elliptical cross-section.

        Parameters
        ----------
        name : str, optional
            Name of the section.
        major_radius : float, optional
            Semi-major axis radius (default 100.0).
        minor_radius : float, optional
            Semi-minor axis radius (default 50.0).
        start_angle : float, optional
            Start angle in degrees (default 0.0).
        end_angle : float, optional
            End angle in degrees (default 360.0).
        autoCalculate : bool, optional
            Auto-calculate section properties (default True).
        """
        ...

    def createFromProperties(self,
                             name: str = None,
                             iyy: float = None,
                             izz: float = None,
                             iyz: float = None,
                             jxx: float = None,
                             area: float = None,
                             **kwargs) -> Section:
        """Create a cross-section from explicit properties.

        Parameters
        ----------
        name : str, optional
            Name of the section.
        iyy : float, optional
            Second moment of area about the y axis.
        izz : float, optional
            Second moment of area about the z axis.
        iyz : float, optional
            Product of inertia about the yz axes.
        jxx : float, optional
            Torsional constant.
        area : float, optional
            Cross-sectional area.
        """
        ...


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

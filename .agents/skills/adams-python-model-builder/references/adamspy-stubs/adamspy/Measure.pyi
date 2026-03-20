import Manager
from Marker import Marker
import Object
from typing import List, ItemsView, Iterable, ValuesView


class Measure(Object.ObjectComment):
    adams_id_id: int


class ObjectMeasure(Measure):
    comment_id: int
    legend: str
    """Text that appears at the top of the measure plot."""
    characteristic: str
    """Object characteristic to be measured."""
    component: str
    """Component of the characteristic in which you are interested."""
    coordinate_rframe: Marker
    """Marker defining the reference frame for coordinate measurements."""
    motion_rframe: Marker
    """Marker defining the reference frame for motion measurements."""
    object: Object.ObjectComment
    from_first: bool
    create_measure_display: bool


pt2pt_characteristics: List[str]


class Pt2ptMeasure(Measure):
    comment_id: int
    legend: str
    """Text that appears at the top of the measure plot."""
    characteristic: str
    """Kinematic characteristic to be measured."""
    component: str
    """Component of the characteristic in which you are interested."""
    coordinate_rframe: Marker
    """Marker defining the reference frame for coordinate measurements."""
    motion_rframe: Marker
    """Marker defining the reference frame for motion measurements."""
    from_point: Marker
    """Marker from which to measure."""
    to_point: Marker
    """Marker to which to measure."""
    create_measure_display: bool


class AngleMeasure(Measure):
    comment_id: int
    legend: str
    """Text that appears at the top of the measure plot."""
    first_point: Marker
    """First marker on an entity."""
    middle_point: Marker
    """Middle (vertex) marker on an entity."""
    last_point: Marker
    """Last marker on an entity."""
    create_measure_display: bool


class ComputedMeasure(Measure):
    comment_id: int
    legend: str
    """Text that appears at the top of the measure plot."""
    text_of_expression: str
    """Computation to be performed by the function."""
    units: str
    """Type of units to be used for this measure."""
    create_measure_display: bool


class OrientMeasure(Measure):
    comment_id: int
    legend: str
    """Text that appears at the top of the measure plot."""
    characteristic: str
    """Characteristic convention with which to associate the component."""
    component: str
    """Rotational component to measure."""
    to_frame: Object.ObjectComment
    """Coordinate system to which to measure."""
    from_frame: Object.ObjectComment
    """Coordinate system from which to measure."""
    create_measure_display: bool


class PointMeasure(Measure):
    comment_id: int
    legend: str
    """Text that appears at the top of the measure plot."""
    characteristic: str
    """Kinematic characteristic to be measured."""
    component: str
    """Component of the characteristic in which you are interested."""
    coordinate_rframe: Marker
    """Marker defining the reference frame for coordinate measurements."""
    motion_rframe: Marker
    """Marker defining the reference frame for motion measurements."""
    point: Marker
    """Marker or point to measure."""
    create_measure_display: bool


class RangeMeasure(Measure):
    comment_id: int
    legend: str
    """Text that appears at the top of the measure plot."""
    range_measure_type: str
    """Type of the range measure."""
    of_measure_name: str
    """Existing, predefined measure to analyze."""
    create_measure_display: bool


class FunctionMeasure(Measure):
    comment_id: int
    legend: str
    """Text that appears at the top of the measure plot."""
    function: str
    """Function expression to be evaluated during the simulation."""
    user_function: str
    """Up to 30 user-defined constants to be passed to the user-written subroutine."""
    routine: str
    """Library and subroutine name for the user-written function measure."""
    units: str
    """Units to be associated with the function measure result."""
    create_measure_display: bool


class MeasureManager(Manager.SubclassManager):
    def createObject(self,
                     name: str,
                     object: Object.ObjectComment,
                     characteristic: str,
                     component: str,
                     from_first: bool = False,
                     legend: str = None,
                     coordinate_rframe: Marker = None,
                     coordinate_rframe_name: str = None,
                     create_measure_display: bool = True,
                     **kwargs) -> ObjectMeasure:
        """Create a measure object.

        Parameters
        ----------
        name : str
            Name of the measure object.
        object : Object.ObjectComment
            Object on which the measure is to be created.
        characteristic : str
            Characteristic of the the object to be measured. Options are as follows:
            - angular_acceleration
            - angular_deformation
            - angular_deformation_velocity
            - angular_kinetic_energy
            - angular_momentum_about_cm
            - angular_velocity
            - ax_ay_az_projection_angles
            - cm_acceleration
            - cm_angular_acceleration
            - cm_angular_displacement
            - euler_angles
            - cm_angular_velocity
            - cm_position
            - cm_position_relative_to_body
            - cm_velocity
            - contact_point_location
            - element_force
            - element_torque
            - integrator_order
            - integrator_stepsize
            - integrator_time_step
            - iterator_steps
            - iteration_count
            - kinetic_energy
            - potential_energy_delta
            - power_consumption
            - pressure_angle
            - static_imbalance
            - strain_kinetic_energy
            - translational_acceleration
            - translational_deformation
            - translational_deformation_velocity
            - translational_displacement
            - translational_kinetic_energy
            - translational_momentum
            - translational_velocity

        component : str
            Component of the characteristic to be measured. Options are as follows:
            - x_component
            - y_component
            - z_component
            - mag_component
            - r_component
            - rho_component
            - theta_component
            - phi_component

        from_first : bool, optional
            If true, measure from i marker otherwise from j marker, by default False
        legend : str, optional
            Plot legend name, by default None
        coordinate_rframe : Marker, optional
            Marker in which the characteristic is to be measured, by default None
        coordinate_rframe_name : str, optional
            Name of marker in which the characteristic is to be measured, by default None
        create_measure_display : bool, optional
            If True, creates a display window in the gui, by default True

        Returns
        -------
        ObjectMeasure
            The newly created object measure .
        """
        ...

    def createPt2pt(self, **kwargs): ...
    def createAngle(self, **kwargs): ...
    def createComputed(self, **kwargs): ...
    def createOrient(self, **kwargs): ...
    def createPoint(self, **kwargs): ...
    def createRange(self, **kwargs): ...

    def createFunction(self,
                       name: str = None,
                       function: str = None,
                       user_function: str = None,
                       routine: str = None,
                       units: str = None,
                       legend: str = None,
                       create_measure_display: str = None,
                       comments: str = None,
                       **kwargs) -> FunctionMeasure: ...

    def __getitem__(self, name) -> Measure: ...
    def __iter__(self, *args) -> Iterable[str]: ...
    def items(self) -> ItemsView[str, Measure]: ...
    def values(self) -> ValuesView[Measure]: ...

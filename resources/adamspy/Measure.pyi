import Manager
from Marker import Marker
import Object
from typing import Any, ItemsView, Iterable, ValuesView

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
                       name:str=None,
                       function:str=None,
                       user_function:str=None,
                       routine:str=None,
                       units:str=None,
                       legend:str=None,
                       create_measure_display:str=None,
                       comments:str=None,
                       **kwargs)->FunctionMeasure: ...

    def __getitem__(self, name) -> Measure: ...
    def __iter__(self, *args) -> Iterable[str]: ...
    def items(self) -> ItemsView[str, Measure]: ...
    def values(self) -> ValuesView[Measure]: ...

class Measure(Object.ObjectComment):
    adams_id_id: int

class ObjectMeasure(Measure):
    comment_id: Any
    legend: Any
    characteristic: Any
    component: Any
    coordinate_rframe: Any
    motion_rframe: Any
    object: Any
    create_measure_display: Any

pt2pt_characteristics: Any

class Pt2ptMeasure(Measure):
    comment_id: Any
    legend: Any
    characteristic: Any
    component: Any
    coordinate_rframe: Any
    motion_rframe: Any
    from_point: Any
    to_point: Any
    create_measure_display: Any

class AngleMeasure(Measure):
    comment_id: Any
    legend: Any
    first_point: Any
    middle_point: Any
    last_point: Any
    create_measure_display: Any

class ComputedMeasure(Measure):
    comment_id: Any
    legend: Any
    text_of_expression: Any
    units: Any
    create_measure_display: Any

class OrientMeasure(Measure):
    comment_id: Any
    legend: Any
    characteristic: Any
    component: Any
    to_frame: Any
    from_frame: Any
    create_measure_display: Any

class PointMeasure(Measure):
    comment_id: Any
    legend: Any
    characteristic: Any
    component: Any
    coordinate_rframe: Any
    motion_rframe: Any
    point: Any
    create_measure_display: Any

class RangeMeasure(Measure):
    comment_id: Any
    legend: Any
    range_measure_type: Any
    of_measure_name: Any
    create_measure_display: Any

class FunctionMeasure(Measure):
    comment_id: int
    legend: str
    function: str
    user_function: str
    routine: str
    units: str
    create_measure_display: str

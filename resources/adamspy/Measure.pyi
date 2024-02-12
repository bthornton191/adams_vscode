import Manager
import Object
from typing import Any

class MeasureManager(Manager.SubclassManager):
    def createObject(self, **kwargs): ...
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

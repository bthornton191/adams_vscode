import Manager
import Object
from DBAccess import CustomProperty as CustomProperty
from EntityTypes import ent_femdata as ent_femdata
from typing import Any

class FemdataManager(Manager.AdamsManager): ...

class Femdata(Object.ObjectComment, Object.ObjectAdamsId):
    def __init__(self, _DBKey) -> None: ...
    fe_part: Any
    fe_part_name: Any
    output_type: Any
    markers: Any
    marker_names: Any
    hotspots: Any
    radius: Any
    criterion: Any
    file_name: Any
    start: Any
    end: Any
    skip: Any

import AppearanceSettings
import Manager
import Object
from typing import Any, ItemsView, Iterable, KeysView, ValuesView

from DesignVariable import DesignVariableManager
from SystemElement import SystemElementManager
from Constraint import ConstraintManager
from DataElement import DataElementManager
from Force import ForceManager
from Manager import AdamsManager
from Measure import MeasureManager
from Part import PartManager
from Material import MaterialManager
from Geometry import GeometryManager
from Marker import MarkerManager
from Contact import ContactManager
from Section import SectionManager
from Group import GroupManager
from Analysis import AnalysisManager
from RuntimeFunction import RuntimeFunctionManager
from Part import Part
from Simulation import SimulationManager
from UDE import UserDefinedInstanceManager

class ModelManager(Manager.AdamsManager):
    def create(self, **kwargs)->Model: ...
    @staticmethod
    def newFromAdm(model_name, file_name): ...
    def items(self) -> ItemsView[str, Model]: ...
    def values(self) -> ValuesView[Model]: ...
    def keys(self) -> KeysView[str]: ...
    def __getitem__(self, name) -> Model: ...
    def __iter__(self, *args) -> Iterable[str]: ...

class Model(Object.ObjectComment, AppearanceSettings.GeometryAppearanceSettings):
    active: Any
    render_mode: Any
    renderStyle: Any
    Constraints: ConstraintManager
    DataElements: DataElementManager
    SystemElements: SystemElementManager
    DesignVariables: DesignVariableManager
    Forces: ForceManager
    Measures: MeasureManager
    Parts: PartManager
    Materials: MaterialManager
    Geometries: GeometryManager
    Sensors: AdamsManager
    FloatingMarkers: MarkerManager
    Contacts: ContactManager
    Sections: SectionManager
    Models: ModelManager
    Groups: GroupManager
    Analyses: AnalysisManager
    RuntimeFunctions: RuntimeFunctionManager
    Simulations: SimulationManager
    settings: Any
    UserDefinedInstances: UserDefinedInstanceManager
    def __init__(self, _DBKey) -> None: ...
    ground_part: Part
    def exportAdmFile(self, file_name): ...
    def verify(self): ...
    num_parts: Any
    title: Any
    def mergeInto(self, into_model: int = ..., translation=..., orientation=..., add_to_group: int = ..., duplicate_parts: bool = ...) -> None: ...

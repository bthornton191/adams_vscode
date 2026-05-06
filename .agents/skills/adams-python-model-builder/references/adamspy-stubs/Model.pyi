from __future__ import annotations

import AppearanceSettings
import Manager
import Object
import Settings
from typing import ItemsView, Iterable, KeysView, Literal, ValuesView

from DesignVariable import DesignVariableManager
from SystemElement import SystemElementManager
from Constraint import ConstraintManager
from DataElement import DataElementManager
from Force import ForceManager
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
from Sensor import SensorManager


class Model(Object.ObjectComment, AppearanceSettings.GeometryAppearanceSettings):
    active: bool
    render_mode: Literal['inherit', 'wireframe', 'filled', 'shaded']
    renderStyle: Literal['inherit', 'wireframe', 'filled', 'shaded']
    Constraints: ConstraintManager
    DataElements: DataElementManager
    SystemElements: SystemElementManager
    DesignVariables: DesignVariableManager
    Forces: ForceManager
    Measures: MeasureManager
    Parts: PartManager
    Materials: MaterialManager
    Geometries: GeometryManager
    Sensors: SensorManager
    FloatingMarkers: MarkerManager
    Contacts: ContactManager
    Sections: SectionManager
    Models: ModelManager
    Groups: GroupManager
    Analyses: AnalysisManager
    RuntimeFunctions: RuntimeFunctionManager
    Simulations: SimulationManager
    settings: Settings.ModelSettings
    UserDefinedInstances: UserDefinedInstanceManager
    def __init__(self, _DBKey) -> None: ...
    ground_part: Part
    def exportAdmFile(self, file_name): ...
    def verify(self): ...
    num_parts: int
    title: str
    def mergeInto(self, into_model: int = ..., translation=..., orientation=..., add_to_group: int = ..., duplicate_parts: bool = ...) -> None: ...


class ModelManager(Manager.AdamsManager):
    def create(self, name: str = None, **kwargs) -> Model:
        """Create a new Model.

        Parameters
        ----------
        name : str, optional
            Name of the model.
        """
        ...

    @staticmethod
    def newFromAdm(model_name, file_name): ...
    def items(self) -> ItemsView[str, Model]: ...
    def values(self) -> ValuesView[Model]: ...
    def keys(self) -> KeysView[str]: ...
    def __getitem__(self, name) -> Model: ...
    def __iter__(self, *args) -> Iterable[str]: ...

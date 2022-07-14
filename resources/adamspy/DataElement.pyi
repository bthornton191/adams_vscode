import Manager
import Object
from typing import Any, ItemsView, List, ValuesView


class DataElement(Object.Object):
    ...


class CurveData(DataElement):
    closed: bool
    fit_type: Any
    tension: Any
    user_function: Any
    minimum_parameter: Any
    maximum_parameter: Any
    routine: Any
    matrix_name: str
    matrix: Any


class Spline(DataElement):
    x: List[float]
    y: List[float]
    z: List[float]
    linear_extrapolate: Any
    channel: Any
    file_type: Any
    block_name: str
    file_name: str
    routine: Any
    units: Any
    x_units: Any
    y_units: Any
    z_units: Any
    x_result_set_component: Any
    y_result_set_component: Any
    z_result_set_component: Any


class Array(DataElement):
    size: int


class ICArray(Array):
    numbers: List[float]


class GeneralArray(Array):
    numbers: List[float]


class XStateArray(Array):
    ...


class YOutputArray(Array):
    ...


class UInputArray(Array):
    variables: List[StateVariable]


class Matrix(DataElement):
    mtx_units_dict: dict
    units: Any


class MatrixFull(Matrix):
    row_count: Any
    column_count: Any
    values: Any
    input_order: Any


class MatrixSparse(Matrix):
    column_index: Any
    row_index: Any
    values: Any
    input_order: Any


class MatrixFile(Matrix):
    file: str
    name_of_matrix_in_file: str


class StateVariable(DataElement):
    initial_condition: float
    user_function: str
    routine: str
    function: str


class String(DataElement):
    string: str


class PInput(DataElement):
    variable_name: str
    variable: StateVariable


class POutput(DataElement):
    variable_name: str
    variable: StateVariable


class PState(DataElement):
    variable_name: str
    variable: StateVariable


class DataElementManager(Manager.SubclassManager):
    def __getitem__(self, name) -> DataElement: ...
    def values(self, *args) -> ValuesView[DataElement]: ...
    def items(self, *args) -> ItemsView[str, DataElement]: ...
    def createCurveData(self, **kwargs) -> CurveData: ...
    def createSpline(self, **kwargs) -> Spline: ...
    def createICArray(self, **kwargs) -> ICArray: ...
    def createGeneralArray(self, **kwargs) -> GeneralArray: ...
    def createXStateArray(self, **kwargs) -> XStateArray: ...
    def createYOutputArray(self, **kwargs) -> YOutputArray: ...
    def createUInputArray(self, **kwargs) -> UInputArray: ...
    def createMatrixFull(self, **kwargs) -> MatrixFull: ...
    def createMatrixSparse(self, **kwargs) -> MatrixSparse: ...
    def createMatrixFile(self, **kwargs) -> MatrixFile: ...
    def createStateVariable(self, **kwargs) -> StateVariable: ...
    def createString(self, **kwargs) -> String: ...
    def createPInput(self, **kwargs) -> PInput: ...
    def createPOutput(self, **kwargs) -> POutput: ...
    def createPState(self, **kwargs) -> PState: ...

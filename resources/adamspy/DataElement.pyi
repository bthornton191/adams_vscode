import Manager
import Object
from typing import Any, ItemsView, List, Optional, ValuesView


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
    linear_extrapolate: bool
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
    numbers: Optional[List[float]]


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
    variable: List[StateVariable]


class POutput(DataElement):
    variable_name: str
    variable: List[StateVariable]


class PState(DataElement):
    variable_name: str
    variable: List[StateVariable]


class DataElementManager(Manager.SubclassManager):
    def __getitem__(self, name) -> DataElement: ...
    def values(self, *args) -> ValuesView[DataElement]: ...
    def items(self, *args) -> ItemsView[str, DataElement]: ...
    def createCurveData(self, **kwargs) -> CurveData: ...

    def createSpline(self,
                     name: str = None,
                     x: List[float] = None,
                     y: List[float] = None,
                     z: List[float] = None,
                     linear_extrapolate: bool = None,
                     **kwargs) -> Spline: ...

    def createICArray(self, **kwargs) -> ICArray: ...

    def createGeneralArray(self,
                           name: str = None,
                           numbers: List = None,
                           **kwargs) -> GeneralArray: ...

    def createXStateArray(self, **kwargs) -> XStateArray: ...
    def createYOutputArray(self, **kwargs) -> YOutputArray: ...
    def createUInputArray(self, **kwargs) -> UInputArray: ...

    def createMatrixFull(self,
                         row_count: int,
                         column_count: int,
                         values: List[float],
                         input_order: str,
                         **kwargs) -> MatrixFull:
        """Create a full matrix data element.

        Parameters
        ----------
        row_count : int
            Specifies the number of rows (M) in the matrix.Used in the definition of a full matrix.
        column_count : int
            Specifies the number of columns (N) in the matrix used in the definition of a full matrix.
        values : List[float]
            Specifies the real number values that you enter to populate a FULL MATRIX.
        input_order : str
            'by_row' or 'by_column' to specify the order in which the values are entered.

        Returns
        -------
        MatrixFull
            _description_
        """
        ...

    def createMatrixSparse(self, **kwargs) -> MatrixSparse: ...
    def createMatrixFile(self, **kwargs) -> MatrixFile: ...

    def createStateVariable(self,
                            name: str = None,
                            function: str = '',
                            initial_condition: float = None,
                            routine: str = '',
                            user_function: str = '',
                            **kwargs) -> StateVariable: ...

    def createString(self, **kwargs) -> String: ...

    def createPInput(self,
                     name: str = None,
                     variable: List[StateVariable] = None,
                     variable_name: List[str] = None,
                     **kwargs) -> PInput: ...

    def createPOutput(self, **kwargs) -> POutput: ...
    def createPState(self, **kwargs) -> PState: ...

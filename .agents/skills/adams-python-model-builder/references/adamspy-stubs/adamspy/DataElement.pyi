from typing import ItemsView, List, Literal, Optional, ValuesView

import Manager
import Object


class DataElement(Object.Object):
    ...


class Spline(DataElement):
    x: List[float]
    y: List[float]
    z: List[float]
    linear_extrapolate: bool
    channel: int
    file_type: Literal['none', 'user', 'dac', 'rpc']
    block_name: str
    file_name: str
    routine: str
    units: str
    """Type of units to be used for this spline."""
    x_units: str
    """Type of units to be used for the x-axis of this spline."""
    y_units: str
    """Type of units to be used for the y-axis of this spline."""
    z_units: str
    """Type of units to be used for the z-axis of this spline."""
    x_result_set_component: List[float]
    """Result set component data for the x-axis."""
    y_result_set_component: List[float]
    """Result set component data for the y-axis."""
    z_result_set_component: List[float]
    """Result set component data for the z-axis."""


class Array(DataElement):
    size: int
    """Size of the array."""


class ICArray(Array):
    numbers: List[float]
    """One-dimensional array of real numbers for the initial conditions. The number of entries should match size."""


class GeneralArray(Array):
    numbers: Optional[List[float]]
    """One-dimensional array of real numbers. The number of entries should match size."""


class XStateArray(Array):
    ...


class YOutputArray(Array):
    ...


class StateVariable(DataElement):
    initial_condition: float
    """Initial value of the user-defined state variable."""
    user_function: List[float]
    """Up to 30 constant values for Adams to pass to the user-written subroutine."""
    routine: str
    function: str
    """Function expression definition used to compute the value of this variable."""


class UInputArray(Array):
    variables: List[StateVariable]
    """Array of state variable objects associated with this input array."""


class Matrix(DataElement):
    mtx_units_dict: dict
    units: str
    """Type of units to be used for this matrix."""


class MatrixFull(Matrix):
    row_count: int
    """Number of rows (M) in the full matrix."""
    column_count: int
    """Number of columns (N) in the full matrix."""
    values: List[float]
    """Real number values populating the full matrix."""
    input_order: Literal['by_row', 'by_column']


class MatrixSparse(Matrix):
    column_index: List[int]
    """Column position of each entry in the sparse matrix values list."""
    row_index: List[int]
    """Row position of each entry in the sparse matrix values list."""
    values: List[float]
    """Real number values populating the sparse matrix."""
    input_order: Literal['by_row', 'by_column']


class MatrixFile(Matrix):
    file: str
    """Name of the file containing the matrix values."""
    name_of_matrix_in_file: str
    """Name of the MATRIX to be read from the file."""


class CurveData(DataElement):
    closed: bool
    """Specifies if the curve is closed (meets at the ends)."""
    fit_type: Literal['curve_points', 'control_points']
    tension: float
    user_function: List[float | int]
    minimum_parameter: float
    """Minimum value of the curve parameter. Only used for user-written curves."""
    maximum_parameter: float
    """Maximum value of the curve parameter. Only used for user-written curves."""
    routine: str
    matrix_name: str
    """Name of an existing MATRIX data element containing the curve data."""
    matrix: Matrix
    """Existing MATRIX data element containing the curve data."""


class String(DataElement):
    string: str
    """The character string value, which may be referenced during Adams execution."""


class PInput(DataElement):
    variable_name: str
    """Name(s) of the existing state variable(s) associated with this plant input."""
    variable: List[StateVariable]
    """Existing state variable object(s) associated with this plant input."""


class POutput(DataElement):
    variable_name: str
    """Name(s) of the existing state variable(s) associated with this plant output."""
    variable: List[StateVariable]
    """Existing state variable object(s) associated with this plant output."""


class PState(DataElement):
    variable_name: str
    """Name(s) of the existing state variable(s) associated with this plant state."""
    variable: List[StateVariable]
    """Existing state variable object(s) associated with this plant state."""


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

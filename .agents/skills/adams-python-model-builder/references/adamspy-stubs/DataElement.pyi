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

    def createCurveData(self,
                        name: str = None,
                        closed: bool = None,
                        **kwargs) -> CurveData:
        """Create a curve data element.

        Parameters
        ----------
        name : str, optional
            Name of the curve data.
        closed : bool, optional
            Whether the curve is closed.
        """
        ...

    def createSpline(self,
                     name: str = None,
                     x: List[float] = None,
                     y: List[float] = None,
                     z: List[float] = None,
                     linear_extrapolate: bool = None,
                     **kwargs) -> Spline:
        """Create a 1D or 2D spline data element.

        Parameters
        ----------
        name : str, optional
            Name of the spline.
        x : list of float, optional
            Independent variable values (abscissa).
        y : list of float, optional
            Dependent variable values for a 1D spline, or multiple rows of
            dependent values for a 2D spline.
        z : list of float, optional
            Parameter values for a 2D spline (one per row of ``y``).
        linear_extrapolate : bool, optional
            If True, extrapolate linearly beyond the data range.
        """
        ...

    def createICArray(self,
                      name: str = None,
                      numbers: List = None,
                      **kwargs) -> ICArray:
        """Create an initial condition array.

        Parameters
        ----------
        name : str, optional
            Name of the IC array.
        numbers : list of float, optional
            Initial condition values. Length determines array size.
        """
        ...

    def createGeneralArray(self,
                           name: str = None,
                           numbers: List = None,
                           **kwargs) -> GeneralArray:
        """Create a general array data element.

        Parameters
        ----------
        name : str, optional
            Name of the array.
        numbers : list of float, optional
            Initial values. Length determines the array size.
        """
        ...

    def createXStateArray(self,
                          name: str = None,
                          **kwargs) -> XStateArray:
        """Create an X state array.

        Parameters
        ----------
        name : str, optional
            Name of the X state array.
        """
        ...

    def createYOutputArray(self,
                           name: str = None,
                           **kwargs) -> YOutputArray:
        """Create a Y output array.

        Parameters
        ----------
        name : str, optional
            Name of the Y output array.
        """
        ...

    def createUInputArray(self,
                          name: str = None,
                          variables: List = None,
                          **kwargs) -> UInputArray:
        """Create a U input array.

        Parameters
        ----------
        name : str, optional
            Name of the U input array.
        variables : list of StateVariable, optional
            State variables to include in the input array.
        """
        ...

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

    def createMatrixSparse(self,
                           name: str = None,
                           values: List[float] = None,
                           row_index: List[int] = None,
                           column_index: List[int] = None,
                           **kwargs) -> MatrixSparse:
        """Create a sparse matrix data element.

        Parameters
        ----------
        name : str, optional
            Name of the sparse matrix.
        values : list of float, optional
            Non-zero element values.
        row_index : list of int, optional
            Row indices for each value.
        column_index : list of int, optional
            Column indices for each value.
        """
        ...

    def createMatrixFile(self,
                         name: str = None,
                         file: str = None,
                         name_of_matrix_in_file: str = None,
                         **kwargs) -> MatrixFile:
        """Create a matrix loaded from a file.

        Parameters
        ----------
        name : str, optional
            Name of the matrix element.
        file : str, optional
            Path to the matrix file.
        name_of_matrix_in_file : str, optional
            Name of the matrix within the file.
        """
        ...

    def createStateVariable(self,
                            name: str = None,
                            function: str = '',
                            initial_condition: float = None,
                            routine: str = '',
                            user_function: str = '',
                            **kwargs) -> StateVariable:
        """Create a state variable (VARIABLE) data element.

        Parameters
        ----------
        name : str, optional
            Name of the state variable.
        function : str, optional
            Expression defining the variable value.
        initial_condition : float, optional
            Initial value of the state variable.
        routine : str, optional
            Name of the user subroutine (``VARSUB``).
        user_function : str, optional
            Values passed to the user subroutine.
        """
        ...

    def createString(self,
                     name: str = None,
                     string: str = None,
                     **kwargs) -> String:
        """Create a string data element.

        Parameters
        ----------
        name : str, optional
            Name of the string element.
        string : str, optional
            The string value.
        """
        ...

    def createPInput(self,
                     name: str = None,
                     variable: List[StateVariable] = None,
                     variable_name: List[str] = None,
                     **kwargs) -> PInput:
        """Create a plant input element.

        Parameters
        ----------
        name : str, optional
            Name of the plant input.
        variable : list of StateVariable, optional
            State variable objects for this plant input.
            Mutually exclusive with ``variable_name``.
        variable_name : list of str, optional
            Names of the state variables.
        """
        ...

    def createPOutput(self,
                      name: str = None,
                      variable: List = None,
                      variable_name: List[str] = None,
                      **kwargs) -> POutput:
        """Create a plant output element.

        Parameters
        ----------
        name : str, optional
            Name of the plant output.
        variable : list of StateVariable, optional
            State variable objects for this plant output.
        variable_name : list of str, optional
            Names of the state variables.
        """
        ...

    def createPState(self,
                     name: str = None,
                     variable: List = None,
                     variable_name: List[str] = None,
                     **kwargs) -> PState:
        """Create a plant state element.

        Parameters
        ----------
        name : str, optional
            Name of the plant state.
        variable : list of StateVariable, optional
            State variable objects for this plant state.
        variable_name : list of str, optional
            Names of the state variables.
        """
        ...

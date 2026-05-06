import DataElement
import Manager
import Object
from Libraries import amdlib as amdlib
from ctypes import create_string_buffer as create_string_buffer
from typing import List


class SystemElement(Object.Object):
    ...


class TransferFunction(SystemElement):
    x_state_array: DataElement.XStateArray
    """X state array object."""
    x_state_array_name: str
    """Name of the X state array."""
    u_input_array: DataElement.UInputArray
    """U input array object."""
    u_input_array_name: str
    """Name of the U input array."""
    y_output_array: DataElement.YOutputArray
    """Y output array object."""
    y_output_array_name: str
    """Name of the Y output array."""
    ic_array: DataElement.ICArray
    """IC (initial conditions) array object."""
    ic_array_name: str
    """Name of the IC array."""
    num_coeff: List[float]
    """Numerator polynomial coefficients."""
    den_coeff: List[float]
    """Denominator polynomial coefficients."""
    static_hold: bool
    """If True, initial conditions are held fixed during static analysis."""


class DifferentialEquation(SystemElement):
    initial_condition: List[float]
    """Initial value of the differential equation at the start of the simulation."""
    implicit: bool
    """If True, the function expression or subroutine defines the implicit form of the equation."""
    static_hold: bool
    """If True, equation states are not permitted to change during static and quasi-static simulations."""
    dynamic_hold: bool
    """If True, equation states are not permitted to change during dynamic simulations."""
    function: str
    routine: str
    user_function: List[float | int]


class LinearStateEquation(SystemElement):
    x_state_array: DataElement.XStateArray
    """X state array object."""
    x_state_array_name: str
    """Name of the X state array."""
    u_input_array: DataElement.UInputArray
    """U input array object."""
    u_input_array_name: str
    """Name of the U input array."""
    y_output_array: DataElement.YOutputArray
    """Y output array object."""
    y_output_array_name: str
    """Name of the Y output array."""
    ic_array: DataElement.ICArray
    """IC array object."""
    ic_array_name: str
    """Name of the IC array."""
    a_state_matrix: DataElement.MatrixFull
    """A state matrix object."""
    a_state_matrix_name: str
    """Name of the A state matrix."""
    b_input_matrix: DataElement.MatrixFull
    """B input matrix object."""
    b_input_matrix_name: str
    """Name of the B input matrix."""
    c_output_matrix: DataElement.MatrixFull
    """C output matrix object."""
    c_output_matrix_name: str
    """Name of the C output matrix."""
    d_feedforward_matrix: DataElement.MatrixFull
    """D feedforward matrix object."""
    d_feedforward_matrix_name: str
    """Name of the D feedforward matrix."""
    static_hold: bool
    """If True, initial conditions are held fixed during static analysis."""


class GeneralStateEquation(SystemElement):
    x_state_array: DataElement.XStateArray
    """X state array object."""
    x_state_array_name: str
    """Name of the X state array."""
    discrete_x_state_array: DataElement.XStateArray
    """Discrete X state array object."""
    discrete_x_state_array_name: str
    """Name of the discrete X state array."""
    u_input_array: DataElement.UInputArray
    """U input array object."""
    u_input_array_name: str
    """Name of the U input array."""
    y_output_array: DataElement.YOutputArray
    """Y output array object."""
    y_output_array_name: str
    """Name of the Y output array."""
    ic_array: DataElement.ICArray
    """IC array object."""
    ic_array_name: str
    """Name of the IC array."""
    discrete_ic_array: DataElement.ICArray
    """Discrete IC array object."""
    discrete_ic_array_name: str
    """Name of the discrete IC array."""
    output_equation_count: int
    """Number of output equations."""
    state_equation_count: int
    """Number of continuous state equations."""
    discrete_state_equation_count: int
    """Number of discrete state equations."""
    user_function: List[float | int]
    """Constants to be passed to GSE subroutines."""
    static_hold: bool
    """If True, initial conditions are held fixed during static analysis."""
    implicit: bool
    statics_only: bool
    """If True, the GSE is activated only during static analysis."""
    discrete: bool
    """If True, specifies a discrete GSE."""
    sample_offset: float
    """Sample offset for the analysis."""
    user_sample_period: float
    """User-defined sample period for the analysis."""
    sample_period: str
    """Sampling time expression."""
    sample_routine: str
    """Sample routine for the analysis."""
    interface_routine: str
    """Interface routine for the analysis."""
    routine: str
    """Routine name for the GSE subroutine."""
    discrete_state_arrays: DataElement.XStateArray
    discrete_state_arrays_name: str
    set_equation_count: int


class SystemElementManager(Manager.SubclassManager):
    def createDifferentialEquation(self, name: str,
                                   function: str = '',
                                   initial_condition: float = 0.0,
                                   implicit: bool = False,
                                   static_hold: bool = False,
                                   **kwargs) -> DifferentialEquation:
        """Create a differential equation (DIFF).

        Parameters
        ----------
        name : str
            Name of the differential equation.
        function : str, optional
            Expression defining the differential equation.
        initial_condition : float, optional
            Initial condition value (default 0.0).
        implicit : bool, optional
            If True, use implicit formulation (default False).
        static_hold : bool, optional
            If True, hold state during static analysis (default False).
        """
        ...

    def createGeneralStateEquation(self,
                                   name: str = None,
                                   output_equation_count: int = None,
                                   user_function: List[float] = None,
                                   **kwargs):
        """Create a general state equation (GSE).

        Parameters
        ----------
        name : str, optional
            Name of the GSE.
        output_equation_count : int
            Number of output equations.
        user_function : list of float
            Values passed to the user subroutine.
        """
        ...

    def createLinearStateEquation(self,
                                  name: str = None,
                                  x_state_array=None,
                                  x_state_array_name: str = None,
                                  a_state_matrix=None,
                                  a_state_matrix_name: str = None,
                                  b_input_matrix=None,
                                  c_output_matrix=None,
                                  d_feedforward_matrix=None,
                                  u_input_array=None,
                                  y_output_array=None,
                                  ic_array=None,
                                  **kwargs):
        """Create a linear state equation (LSE).

        Parameters
        ----------
        name : str, optional
            Name of the LSE.
        x_state_array : XStateArray, optional
            X state array object. Mutually exclusive with ``x_state_array_name``.
        x_state_array_name : str, optional
            Full name of the X state array.
        a_state_matrix : MatrixFull, optional
            A state matrix. Mutually exclusive with ``a_state_matrix_name``.
        a_state_matrix_name : str, optional
            Full name of the A state matrix.
        b_input_matrix : MatrixFull
            B input matrix.
        c_output_matrix : MatrixFull
            C output matrix.
        d_feedforward_matrix : MatrixFull
            D feedforward matrix.
        u_input_array : UInputArray
            U input array.
        y_output_array : YOutputArray
            Y output array.
        ic_array : ICArray
            Initial condition array.
        """
        ...

    def createTransferFunction(self,
                               name: str = None,
                               x_state_array=None,
                               x_state_array_name: str = None,
                               y_output_array=None,
                               y_output_array_name: str = None,
                               u_input_array=None,
                               u_input_array_name: str = None,
                               num_coeff: List[float] = None,
                               den_coeff: List[float] = None,
                               **kwargs):
        """Create a transfer function (TFSISO).

        Parameters
        ----------
        name : str, optional
            Name of the transfer function.
        x_state_array : XStateArray, optional
            X state array. Mutually exclusive with ``x_state_array_name``.
        x_state_array_name : str, optional
            Full name of the X state array.
        y_output_array : YOutputArray, optional
            Y output array. Mutually exclusive with ``y_output_array_name``.
        y_output_array_name : str, optional
            Full name of the Y output array.
        u_input_array : UInputArray, optional
            U input array. Mutually exclusive with ``u_input_array_name``.
        u_input_array_name : str, optional
            Full name of the U input array.
        num_coeff : list of float
            Numerator polynomial coefficients (max 30).
        den_coeff : list of float
            Denominator polynomial coefficients (min 2, max 30).
        """
        ...

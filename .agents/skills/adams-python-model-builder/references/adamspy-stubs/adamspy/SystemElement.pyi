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
                                   **kwargs) -> DifferentialEquation: ...

    def createGeneralStateEquation(self, **kwargs): ...
    def createLinearStateEquation(self, **kwargs): ...
    def createTransferFunction(self, **kwargs): ...

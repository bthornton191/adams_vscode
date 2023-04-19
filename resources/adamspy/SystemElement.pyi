import Manager
import Object
from Libraries import amdlib as amdlib
from ctypes import create_string_buffer as create_string_buffer
from typing import Any

class SystemElementManager(Manager.SubclassManager):
    def createDifferentialEquation(self, name: str, function: str, **kwargs): ...
    def createGeneralStateEquation(self, **kwargs): ...
    def createLinearStateEquation(self, **kwargs): ...
    def createTransferFunction(self, **kwargs): ...

class SystemElement(Object.Object): ...

class TransferFunction(SystemElement):
    x_state_array: Any
    x_state_array_name: Any
    u_input_array: Any
    u_input_array_name: Any
    y_output_array: Any
    y_output_array_name: Any
    ic_array: Any
    ic_array_name: Any
    num_coeff: Any
    den_coeff: Any
    static_hold: Any

class DifferentialEquation(SystemElement):
    initial_condition: Any
    implicit: Any
    static_hold: Any
    dynamic_hold: Any
    function: Any
    routine: Any
    user_function: Any

class LinearStateEquation(SystemElement):
    x_state_array: Any
    x_state_array_name: Any
    u_input_array: Any
    u_input_array_name: Any
    y_output_array: Any
    y_output_array_name: Any
    ic_array: Any
    ic_array_name: Any
    a_state_matrix: Any
    a_state_matrix_name: Any
    b_input_matrix: Any
    b_input_matrix_name: Any
    c_output_matrix: Any
    c_output_matrix_name: Any
    d_feedforward_matrix: Any
    d_feedforward_matrix_name: Any
    static_hold: Any

class GeneralStateEquation(SystemElement):
    x_state_array: Any
    x_state_array_name: Any
    discrete_x_state_array: Any
    discrete_x_state_array_name: Any
    u_input_array: Any
    u_input_array_name: Any
    y_output_array: Any
    y_output_array_name: Any
    ic_array: Any
    ic_array_name: Any
    discrete_ic_array: Any
    discrete_ic_array_name: Any
    output_equation_count: Any
    state_equation_count: Any
    discrete_state_equation_count: Any
    user_function: Any
    static_hold: Any
    implicit: Any
    statics_only: Any
    discrete: Any
    sample_offset: Any
    user_sample_period: Any
    sample_period: Any
    sample_routine: Any
    interface_routine: Any
    routine: Any
    discrete_state_arrays: Any
    discrete_state_arrays_name: Any
    set_equation_count: Any

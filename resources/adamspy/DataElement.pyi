import Manager
import Object
from typing import Any

class DataElementManager(Manager.SubclassManager):
    def createCurveData(self, **kwargs): ...
    def createSpline(self, **kwargs): ...
    def createICArray(self, **kwargs): ...
    def createGeneralArray(self, **kwargs): ...
    def createXStateArray(self, **kwargs): ...
    def createYOutputArray(self, **kwargs): ...
    def createUInputArray(self, **kwargs): ...
    def createMatrixFull(self, **kwargs): ...
    def createMatrixSparse(self, **kwargs): ...
    def createMatrixFile(self, **kwargs): ...
    def createStateVariable(self, **kwargs): ...
    def createString(self, **kwargs): ...
    def createPInput(self, **kwargs): ...
    def createPOutput(self, **kwargs): ...
    def createPState(self, **kwargs): ...

class DataElement(Object.Object): ...

class CurveData(DataElement):
    closed: Any
    fit_type: Any
    tension: Any
    user_function: Any
    minimum_parameter: Any
    maximum_parameter: Any
    routine: Any
    matrix_name: Any
    matrix: Any

class Spline(DataElement):
    x: Any
    y: Any
    z: Any
    linear_extrapolate: Any
    channel: Any
    file_type: Any
    block_name: Any
    file_name: Any
    routine: Any
    units: Any
    x_units: Any
    y_units: Any
    z_units: Any
    x_result_set_component: Any
    y_result_set_component: Any
    z_result_set_component: Any

class Array(DataElement):
    size: Any

class ICArray(Array):
    numbers: Any

class GeneralArray(Array):
    numbers: Any

class XStateArray(Array): ...
class YOutputArray(Array): ...

class UInputArray(Array):
    variables: Any

class Matrix(DataElement):
    mtx_units_dict: Any
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
    file: Any
    name_of_matrix_in_file: Any

class StateVariable(DataElement):
    initial_condition: Any
    user_function: Any
    routine: Any
    function: Any

class String(DataElement):
    string: Any

class PInput(DataElement):
    variable_name: Any
    variable: Any

class POutput(DataElement):
    variable_name: Any
    variable: Any

class PState(DataElement):
    variable_name: Any
    variable: Any

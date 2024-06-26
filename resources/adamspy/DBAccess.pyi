from typing import Any

BUFFER_SIZE: int

class ArraySizeError(TypeError): ...
class DatabaseError(Exception): ...
class SetValueFailed(DatabaseError): ...
class ReadOnlyError(AttributeError): ...
class WriteOnlyError(AttributeError): ...

def isPropIdSet(obj) -> None: ...
def validateLength(val) -> None: ...
def validateMass(val) -> None: ...
def validateNonnegative(val) -> None: ...
def validatePositive(val) -> None: ...
def getExpressionString(obj, prop_obj): ...
def stub(val) -> None: ...
def set_string(_DBKey, id, val, offset: int = ...): ...
def get_string(_DBKey, id, offset, val, sdk: bool = ...): ...
def lookup_by_name(DBRoot, ent_type, name, sdk: bool = ...): ...
def find_by_full_name(val): ...
def set_locori_expression(_DBKey, offset, expr_str) -> None: ...

unit_validators: Any

class PropertyValue:
    dataType: Any
    exprType: int
    id: Any
    units: Any
    offset: Any
    readonly: Any
    writeonly: Any
    unitValidator: Any
    dbt: Any
    default: Any
    __doc__: Any
    min: Any
    max: Any
    gtmin: Any
    ltmax: Any
    useAprKey: Any
    unsetValue: Any
    def __init__(self, id: int = ..., units=..., offset: int = ..., readonly: bool = ..., writeonly: bool = ..., dbt: bool = ..., default: Any | None = ..., fpreset: Any | None = ..., fpostset: Any | None = ..., doc: Any | None = ..., min: Any | None = ..., gtmin: bool = ..., max: Any | None = ..., ltmax: bool = ..., useAprKey: bool = ...) -> None: ...
    def __get__(self, instance, owner): ...
    def __set__(self, instance, val): ...
    def __checkValueRange__(self, val) -> None: ...
    def restoreDefault(self, instance) -> None: ...
    def getValue(self, instance, owner, dbt) -> None: ...
    def setValue(self, instance, val, dbt) -> None: ...

class CustomProperty(PropertyValue):
    def __init__(self, fget: Any | None = ..., fset: Any | None = ..., datatype: Any | None = ..., isLocOri: bool = ..., **kwargs) -> None: ...
    def __get__(self, instance, owner): ...
    def __set__(self, instance, val): ...
    def getValue(self, instance, owner, dbt): ...
    def setValue(self, instance, val, dbt): ...
    def getDataType(self): ...

class ArrayProperty(PropertyValue):
    num: Any
    buffer_size: Any
    def __init__(self, num: Any | None = ..., **kwargs) -> None: ...
    def __set__(self, instance, val): ...

class BoolValue(PropertyValue):
    bool_str = {
        'true': True,
        'yes': True,
        'on': True,
        'false': False,
        'no': False,
        'off': False,
        1: True,
        0: False
    }
    """Use this dictionary to convert strings to boolean values."""
    def getValue(self, instance, owner, dbt): ...
    def setValue(self, instance, val, dbt): ...

class RealValue(PropertyValue):
    dataType: Any
    exprType: int
    val: Any
    def __init__(self, **kwargs) -> None: ...
    def getValue(self, instance, owner, dbt): ...
    def setValue(self, instance, value, dbt): ...

class RealArrayValue(ArrayProperty):
    dataType: Any
    exprType: int
    def __set__(self, instance, val): ...
    def getValue(self, instance, owner, dbt): ...
    def setValue(self, instance, val, dbt): ...

class BoolArrayValue(ArrayProperty):
    def __init__(self, **kwargs) -> None: ...
    def getValue(self, instance, owner, dbt): ...
    def setValue(self, instance, vals, dbt): ...

class IntValue(PropertyValue):
    dataType: Any
    exprType: int
    def __init__(self, **kwargs) -> None: ...
    def getValue(self, instance, owner, dbt): ...
    def setValue(self, instance, val, dbt): ...

StrToIntValue: Any

class IntArrayValue(ArrayProperty):
    dataType: Any
    def getValue(self, instance, owner, dbt): ...
    def setValue(self, instance, val, dbt): ...

class StringValue(PropertyValue):
    dataType: Any
    exprType: int
    def getValue(self, instance, owner, dbt): ...
    def setValue(self, instance, val, dbt): ...

class StringArrayValue(ArrayProperty):
    dataType: Any
    exprType: int
    def getValue(self, instance, owner, dbt): ...
    def setValue(self, instance, val, dbt): ...

class ExpressionValue(PropertyValue):
    dataType: Any
    exprType: int
    def getValue(self, instance, owner, dbt): ...
    def setValue(self, instance, val, dbt): ...

class ObjectValue(PropertyValue):
    exprType: int
    obj_type: Any
    def __init__(self, obj_type: Any | None = ..., **kwargs) -> None: ...
    def getValue(self, instance, owner, dbt): ...
    def setValue(self, instance, val, dbt): ...

class ObjectName(ObjectValue):
    def getValue(self, instance, owner, dbt): ...

class MultiTypeObjectValue(ObjectValue):
    obj_types: Any
    def __init__(self, obj_types, **kwargs) -> None: ...

class MultiTypeObjectName(ObjectName):
    obj_types: Any
    def __init__(self, obj_types, **kwargs) -> None: ...

class ObjectArray(ArrayProperty):
    obj_type: Any
    excluded_type: Any
    def __init__(self, obj_type: Any | None = ..., excluded_type: Any | None = ..., offset: int = ..., num: Any | None = ..., readonly: bool = ..., **kargs) -> None: ...
    def getValue(self, instance, owner, dbt): ...
    def setValue(self, instance, vlist, dbt): ...

class ObjectArrayValue(ObjectArray):
    def setValue(self, instance, val, dbt): ...

class ObjectArrayName(ObjectArray):
    def setValue(self, instance, val, dbt): ...
    def getValue(self, instance, owner, dbt): ...

class EnumValue(PropertyValue):
    enum: Any
    accepted_values: Any
    def __init__(self, decoder, decoder_count: Any | None = ..., subset: Any | None = ..., exclude: Any | None = ..., **kwargs) -> None: ...
    def getValue(self, instance, owner, dbt): ...
    def setValue(self, instance, val, dbt): ...

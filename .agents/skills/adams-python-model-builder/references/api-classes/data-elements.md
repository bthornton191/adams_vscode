# Data Elements — Python API Reference

> **Authoritative stubs**: `references/adamspy-stubs/DataElement.pyi`, `DesignVariable.pyi`, `Material.pyi`

---

## Spline (1D and 2D Lookup Tables)

```python
# 1D spline (y vs x)
spl = m.DataElements.createSpline(
    name='ROAD_PROFILE',
    x=[0.0, 10.0, 20.0, 30.0],
    y=[0.0,  5.0,  3.0,  8.0],
    linear_extrapolate=True   # extrapolate linearly beyond data range (default False)
)

# 2D spline (multiple y curves at different z values)
spl2d = m.DataElements.createSpline(
    name='TIRE_FORCE_MAP',
    x=[0.0, 1.0, 2.0, 3.0],
    y=[[0, 100, 150, 180],   # y-values at z=0
       [0, 120, 170, 200]],  # y-values at z=1
    z=[0.0, 1.0]
)
```

Use in FUNCTION= expressions with `AKISPL()` or `CUBSPL()`:
```python
sforce.function = f'AKISPL(DX(.model.body.cm, .model.ground.ref), 0, {spl.full_name}, 0)'
```

**Spline properties**:

| Property | Type | Description |
|----------|------|-------------|
| `x` | `List[float]` | Independent variable values |
| `y` | `List[float]` | Dependent variable values (reassign fully) |
| `z` | `List[float]` | Second independent variable (2D spline) |
| `linear_extrapolate` | `bool` | Linear extrapolation beyond data bounds |
| `file_name` | `str` | Load data from file |
| `file_type` | `str` | File type for file-based spline |
| `channel` | `Any` | Channel identifier for multi-channel files |

---

## Design Variables

Design variables parameterize model properties. Assign them to properties via `Adams.expression()`.

```python
from Adams import expression

# Real (float) design variable
dv_k = m.DesignVariables.createReal(name='SPRING_K', value=5000.0)
spring.stiffness = expression(dv_k.full_name)

# Integer design variable
dv_n = m.DesignVariables.createInteger(name='NUM_LINKS', value=5)

# String design variable
dv_s = m.DesignVariables.createString(name='PART_COLOR', value='Red')

# Object design variable (references another Adams object)
dv_o = m.DesignVariables.createObject(name='REF_PART', value=link_part)
```

**Accessing value**:
```python
val = Adams.evaluate_exp(dv_k.full_name)   # evaluates and returns float
```

**Design variable properties**:

| Property | Type | Description |
|----------|------|-------------|
| `value` | varies | Current value (`List[float]` for Real, `List[int]` for Integer) |
| `range` | `Any` | Allowed range for optimization |
| `sensitivity` | `Any` | Sensitivity info |
| `full_name` | `str` | `.MODEL.DV_NAME` — use in expression() calls |

---

## State Variable

State variables compute a scalar result from a FUNCTION= expression during simulation.

```python
sv = m.DataElements.createStateVariable(
    name='CONTACT_FORCE',
    function='FZ(.model.WHEEL.cm, .model.ground.ref, .model.ground.ref)',
    initial_condition=0.0
)
```

State variables can be read back with `VARVAL(.model.CONTACT_FORCE)` in other expressions.

---

## Array

### General Array (constant vector)
```python
arr = m.DataElements.createGeneralArray(
    name='IC_VEC',
    numbers=[0.0, 0.0, 0.0, 1.0, 0.0, 0.0]
)
```

### Initial Conditions Array
```python
ic = m.DataElements.createICArray(numbers=[0.0, 0.0, 10.0])
```

### Control Arrays (for system elements)
```python
u_in  = m.DataElements.createUInputArray(variable=[sv1, sv2])   # input variables
x_st  = m.DataElements.createXStateArray()
y_out = m.DataElements.createYOutputArray()
```

---

## Matrix

```python
# Full matrix
mtx = m.DataElements.createMatrixFull(
    row_count=3,
    column_count=3,
    values=[1, 0, 0,
            0, 1, 0,
            0, 0, 1],
    input_order='by_row'   # 'by_row' or 'by_column'
)

# Sparse matrix
mtx_s = m.DataElements.createMatrixSparse(row_index=[1,2], column_index=[1,2], values=[1.0, 1.0])

# Matrix from file
mtx_f = m.DataElements.createMatrixFile(file='stiffness.mtx', name_of_matrix_in_file='K')
```

---

## Material

```python
mat = m.Materials.create(
    name='steel',
    youngs_modulus=2.07e5,    # MPa (for mm-tonne-s) or N/mm² (for mm-kg-s: 2.07e5)
    poissons_ratio=0.29,
    density=7.8e-6            # tonne/mm³ (mm-tonne-s) or 7.8e-3 kg/mm³
)
part.material_type = mat
```

Common densities by unit system:
- mm-kg-s: `density = 7.8e-3` kg/mm³ (steel)
- mm-tonne-s: `density = 7.8e-6` tonne/mm³ (steel)
- m-kg-s: `density = 7800` kg/m³ (steel)

---

## PInput / POutput / PState (Control System I/O)

```python
inp  = m.DataElements.createPInput(name='U', variable=[sv_control])
outp = m.DataElements.createPOutput(name='Y', variable=[sv_output])
pst  = m.DataElements.createPState(name='X', variable=[sv_state])
```

---

## String Data Element

```python
s = m.DataElements.createString(name='MODEL_ID', string='rev2')
```

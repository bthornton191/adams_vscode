# System Elements — Python API Reference

> **Authoritative stub**: `references/adamspy-stubs/SystemElement.pyi`

System elements model control systems and ODEs coupled to the multibody simulation. They are created via `model.SystemElements.createX(**kwargs)`.

---

## Differential Equation (DIFF)

Defines a first-order ODE: `ẋ = f(x, u, t)`

```python
diff = m.SystemElements.createDifferentialEquation(
    name='DIFF_1',
    function='(-1/TAU) * (x - INPUT_SIGNAL)',   # FUNCTION= expression for ẋ
    initial_condition=0.0,
    implicit=False,      # True for implicit integration
    static_hold=True     # holds x constant during static analysis
)
```

Reference the state with `VARVAL(diff.full_name)` in other FUNCTION= expressions.

---

## Transfer Function

Linear transfer function `H(s) = Y(s)/U(s)`:

```python
tf = m.SystemElements.createTransferFunction(
    name='LOW_PASS',
    num_coeff=[1.0],            # numerator polynomial coefficients (constant first)
    den_coeff=[1.0, 0.1],       # denominator polynomial [a0 + a1*s + a2*s² + ...]
    u_input_array=u_in_array,   # UInputArray data element
    y_output_array=y_out_array, # YOutputArray data element
    x_state_array=x_st_array,   # XStateArray data element
    ic_array=ic_arr,            # ICArray for initial conditions
    static_hold=True
)
```

---

## Linear State Equation (LSE)

State-space model `ẋ = Ax + Bu`, `y = Cx + Du`:

```python
lse = m.SystemElements.createLinearStateEquation(
    name='LSE_1',
    a_state_matrix=A_matrix,      # MatrixFull object
    b_input_matrix=B_matrix,
    c_output_matrix=C_matrix,
    d_feedforward_matrix=D_matrix,
    u_input_array=u_in,
    y_output_array=y_out,
    x_state_array=x_st,
    ic_array=ic_arr,
    static_hold=True
)
```

---

## General State Equation (GSE)

Nonlinear state equations via FUNCTION= expressions:

```python
gse = m.SystemElements.createGeneralStateEquation(
    name='GSE_1',
    state_equation_count=2,
    output_equation_count=1,
    u_input_array=u_in,
    y_output_array=y_out,
    x_state_array=x_st,
    ic_array=ic_arr,
    routine='myDll:myGSE',   # user subroutine
    static_hold=True
)
```

---

## Connecting System Elements to the Model

System elements receive inputs from `StateVariable` or other elements via `UInputArray`, and feed outputs back via `YOutputArray`. Typical loop:

```python
# 1. Create state variables to serve as inputs
sv_input = m.DataElements.createStateVariable(name='FORCE_IN',
               function='FZ(.model.wheel.cm, .model.ground.ref)')

# 2. Create control arrays
u_arr = m.DataElements.createUInputArray(name='U_ARR', variable=[sv_input])
y_arr = m.DataElements.createYOutputArray(name='Y_ARR')
x_arr = m.DataElements.createXStateArray(name='X_ARR')

# 3. Create transfer function
tf = m.SystemElements.createTransferFunction(
    name='DAMPER_TF',
    num_coeff=[1.0],
    den_coeff=[1.0, 0.01],
    u_input_array=u_arr,
    y_output_array=y_arr,
    x_state_array=x_arr,
    static_hold=True
)

# 4. Feed output back into a force
sforce.function = f'VARVAL({y_arr.full_name}, 1)'
```

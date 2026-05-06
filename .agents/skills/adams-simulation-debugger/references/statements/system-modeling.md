# Statements: System Modeling (DIFF, GSE, LSE, TFSISO, VARIABLE)

## DIFF
User-defined differential equation (one scalar state variable).
```
DIFF/id, [IC=r],                                                              &
    FUNCTION=expr|USER(r1,...)                                                &
    [, IMPLICIT] [, STATIC_HOLD]                                              &
    [, ROUTINE=libname::subname]                                              &
    [, LABEL=c]
```
- Defines: `dq/dt = FUNCTION(q, t, ...)` where `q` is the state accessed via `DIF(id)`
- IMPLICIT: redefines as `0 = FUNCTION(...)` — solver treats as algebraic (index-1) constraint
- STATIC_HOLD: holds the differential state constant during static equilibrium (IC value held)
- IC: initial value of the state variable; required for consistent initial conditions
- Nested DIFF expressions (DIFF calling DIF of another DIFF) can cause index issues; prefer GSE

## GSE
General State Equation — arbitrary MIMO dynamic system in state-space form.
```
GSE/id,                                                                      &
    X_ARRAY=array_id, U_ARRAY=array_id, Y_ARRAY=array_id,                   &
    IC_ARRAY=array_id,                                                        &
    ROUTINE=libname::subname                                                  &
    [, STATIC_HOLD] [, IMPLICIT]                                             &
    [, LABEL=c]
```
- GSESUB user subroutine evaluates state derivatives and outputs
- X_ARRAY: state vector; U_ARRAY: input vector; Y_ARRAY: output vector; IC_ARRAY: initial states
- STATIC_HOLD: fixes all states during static analysis (prevents integrator failure from dynamic-only states)
- IMPLICIT flag switches to algebraic form (DAE index 1)

## LSE
Linear State Equation — state-space MIMO system with constant matrices.
```
LSE/id,                                                                      &
    A_MATRIX=matrix_id, B_MATRIX=matrix_id,                                  &
    C_MATRIX=matrix_id, D_MATRIX=matrix_id,                                  &
    X_ARRAY=array_id, U_ARRAY=array_id, Y_ARRAY=array_id,                   &
    IC_ARRAY=array_id                                                         &
    [, STATIC_HOLD] [, LABEL=c]
```
- Implements: `ẋ = Ax + Bu`, `y = Cx + Du`
- STATIC_HOLD recommended unless the linear system has a meaningful static equilibrium
- All matrices must be pre-defined MATRIX statements; dimensions must be consistent

## TFSISO
Transfer function (single-input, single-output) in s-domain.
```
TFSISO/id, INPUT_VARIABLE=variable_id, OUTPUT_ARRAY=array_id,               &
    NUM_COEFF=a0[,a1,...], DEN_COEFF=b0[,b1,...]                            &
    [, IC_ARRAY=array_id] [, STATIC_HOLD] [, LABEL=c]
```
- NUM/DEN coefficients in ascending order: `H(s) = (a0 + a1·s + ...) / (b0 + b1·s + ...)`
- Automatically converts to state-space internally; order = max(degree_num, degree_den)
- STATIC_HOLD freezes states during static equilibrium
- For stable transfer functions, STATIC_HOLD usually not needed (DC value provides equilibrium)

## VARIABLE
Defines an algebraic (non-state) result variable from an expression.
```
VARIABLE/id, FUNCTION=expr|USER(r1,...)                                      &
    [, ROUTINE=libname::subname]                                              &
    [, LABEL=c]
```
- Evaluated algebraically at every step; no integration
- Access in other expressions via VARVAL(id)
- Use for intermediate calculations (forces, positions, sensor signals) referenced by multiple elements
- Heavy use of deeply nested VARIABLEs can slow Jacobian construction; group terms in GSE/DIFF where possible

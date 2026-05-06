# Commands: System Elements (VARIABLE, ARRAY, SPLINE)

> Elements without a command form (DIFF, GSE, LSE, TFSISO, CONTACT, COUPLER, GEAR) can only be
> modified by rewriting the `.adm` dataset or by using ACTIVATE/DEACTIVATE commands.

## VARIABLE
Redefine the function expression or initial condition of an existing algebraic variable.
```
VARIABLE/id [, FUNCTION=e | USER(r1[,...,r30])]
            [, IC=r]
            [, ROUTINE=libname::subname]
            [, LIST]
```
- `FUNCTION=e`: Redefine the scalar algebraic expression. Must be last argument or followed by `\`. Must be smooth, convergent, and non-self-referential.
- `FUNCTION=USER(r1[,...,r30])`: Pass up to 30 constants to VARSUB user subroutine.
- `IC=r`: Respecify approximate initial value (Adams may adjust during IC analysis). Can only be changed **before** a simulation has run — rejected afterwards.
- `ROUTINE=libname::subname`: Alternate VARSUB library/subroutine name.
- `LIST`: Print current VARIABLE data.

---

## ARRAY
Redefine numeric values of an IC-type ARRAY.
```
ARRAY/id [, NUMBERS=r1[,r2,...]]
         [, LIST]
```
- `NUMBERS=r1[,r2,...]`: Respecify up to 1,200 real numbers stored in the IC array.
- `LIST`: Print current array values.

> Only works on `IC`-type arrays. Issuing on X-, U-, or Y-type arrays produces an error.

---

## SPLINE
Modify data values or file reference of an existing SPLINE element.
```
SPLINE/id, X=x1,...,xn, Y=y1,...,yn
  or
SPLINE/id, X=x1,...,xn, Y=z1,y11,...,y1n [, Y=z2,y21,...,y2n] ...
  or
SPLINE/id, FILE=filename [, CHANNEL=id] [, LINEAR_EXTRAPOLATE]
         [, LIST]
```
- `X=x1,...,xn`: Respecify x-values. Minimum 4. Must be strictly increasing. Constants only — no expressions.
- `Y=y1,...,yn`: Respecify y-values for a 2D curve (one value per x-value).
- `Y=z, y1,...,yn`: Respecify one family curve at z-value `z` (repeated for each z-level). z-values must be strictly increasing.
- `FILE=filename`: Respecify Adams Durability source file (DAC or RPC III format). Only allowed if originally defined via Adams Durability type.
- `CHANNEL=id`: RPC III channel ID. Required for RPC III files; ignored for DAC.
- `LINEAR_EXTRAPOLATE`: Use linear tangent extrapolation outside data range. Default: cubic.
- `LIST`: Print current SPLINE data.

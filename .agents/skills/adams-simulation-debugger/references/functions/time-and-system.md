# Functions: Time, System State, and Constants

> All angles are in **radians** unless the `D` suffix is used (e.g. `90D`).
> All functions are evaluated at the current simulation time unless stated otherwise.

## TIME
Current simulation time.
- **Returns:** real, time units
- **Example:** `10*SIN(2*PI*TIME)`

## PI
Mathematical constant π = 3.14159265…
- **Returns:** real (dimensionless)

## RTOD
Radians-to-degrees conversion factor (180/π ≈ 57.296).
- **Returns:** real (dimensionless)
- **Example:** `AZ(23,14)*RTOD` → angle in degrees

## DTOR
Degrees-to-radians conversion factor (π/180 ≈ 0.01745).
- **Returns:** real (dimensionless)
- **Example:** `30*DTOR` → 30 degrees in radians

## MODE
Current analysis mode integer.
- **Returns:** 1=Kinematics, 3=IC, 4=Dynamics, 5=Statics, 6=Quasi-statics, 7=Linear
- **Notes:** Use `IF(MODE-4:0,0,expr)` to apply force only during dynamic analysis.

## VARVAL(id)
Current value of algebraic VARIABLE/id.
- **id:** integer VARIABLE element ID
- **Returns:** real, units match variable definition

## ARYVAL(id, comp)
Component `comp` (1-based) of ARRAY/id.
- **id:** ARRAY element ID; **comp:** integer index ≥ 1
- **Returns:** real
- **Example:** `ARYVAL(5, 3)` → third element of ARRAY/5

## PINVAL(id, comp)
Component `comp` of PINPUT/id (plant input channel).
- **Returns:** real

## POUVAL(id, comp)
Component `comp` of POUTPUT/id (plant output channel).
- **Returns:** real

## SENVAL(id)
Last value scored by the EVALUATE expression of SENSOR/id. Returns 0 if no EVALUATE argument.
- **Returns:** real

## DIF(id)
Current state value of DIFF/id (accumulated integral of the DIFF function).
- **id:** DIFF element ID
- **Returns:** real; the state variable q

## DIF1(id)
Time derivative of the state variable of DIFF/id.
- **Returns:** real; uses numerical differencing for implicit (algebraic) DIFF elements

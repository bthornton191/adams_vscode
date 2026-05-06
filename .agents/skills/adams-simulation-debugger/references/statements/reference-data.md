# Statements: Reference Data (ARRAY, SPLINE, CURVE, SURFACE, MATRIX, STRING, PINPUT, POUTPUT)

## ARRAY
Defines input (U), state (X), output (Y), or initial-condition (IC) vectors for system elements.
```
ARRAY/id, {U, VARIABLES=id1[,id2,...] |                                      &
           X [, SIZE=i]               |                                      &
           Y [, SIZE=i]               |                                      &
           IC, NUMBERS=r1[,r2,...] [, SIZE=i]}                               &
    [, LABEL=c]
```
- U array: ordered list of VARIABLE ids; array value accessed by ARYVAL(id, n) (1-based index)
- X and Y arrays may only be owned by one LSE/GSE/TFSISO element each
- IC array: initial conditions matched by position to the X array of the same system element
- Size defaults to number of listed items; explicit SIZE pads with zeros or truncates

## SPLINE
Discrete data table used for interpolation by AKISPL() or CUBSPL() function.
```
SPLINE/id, X=x1,...,xn, Y=y1,...,yn                                         &
    [, FILE=filename] [, LINEAR_EXTRAPOLATE]                                 &
    [, LABEL=c]
```
- For 2D family (surface lookup): Y contains alternating z-breakpoints then row values:
  `Y=z1, y(x,z1)_vals..., z2, y(x,z2)_vals...`
- AKISPL: local Akima cubic (stable, no oscillation between points)
- CUBSPL: global cubic spline (smoother but can overshoot at ends)
- LINEAR_EXTRAPOLATE extends outside data range with linear segments; default is cubic extrapolation
- Extend data ±10% beyond simulation range to avoid extrapolation artifacts

## CURVE
Parametric 3D curve for PTCV/CVCV constraints and GRAPHICS.
```
CURVE/id, {OPEN|CLOSED},                                                     &
    {CURVE_POINTS, MATRIX=matrix_id [, ORDER=i] |                            &
     FUNCTION=USER(r1,...) [, MINPAR=r] [, MAXPAR=r]                        &
     [, ROUTINE=libname::subname]}                                           &
    [, LABEL=c]
```
- CURVE_POINTS: Adams fits a B-spline of ORDER (default 4 = cubic) through matrix data points
- CLOSED: endpoint continuity enforced; PTCV/CVCV can traverse the closure
- FUNCTION/ROUTINE: CURSUB user subroutine evaluates curve at parameter u ∈ [MINPAR, MAXPAR]
- Discontinuous curves → PTCV/CVCV convergence failure; ensure smooth C1 continuity

## SURFACE
Parametric 3D surface for surface-contact marker constraints.
```
SURFACE/id,                                                                  &
    {FILE=file.xmt_txt |                                                     &
     FUNCTION=USER(r1,...) [, MINPAR=r1,r2] [, MAXPAR=r1,r2]               &
     [, UCLOSED] [, VCLOSED] [, ROUTINE=libname::subname]}                  &
    [, LABEL=c]
```
- FILE: single-face Parasolid sheet body (.xmt_txt)
- FUNCTION: SURSUB user subroutine for analytic surface
- UCLOSED/VCLOSED: surface wraps in u or v parametric direction
- Penalty stiffness K=1e8 keeps surface marker on surface; SURSUB must extrapolate outside domain

## MATRIX
General M×N numerical matrix for system equations, NFORCE, FLEX_BODY, etc.
```
MATRIX/id,                                                                   &
    {FULL={RORDER|CORDER}, ROWS=i, COLUMNS=i, VALUES=r1,...  |              &
     SPARSE, ROWS=i, COLUMNS=i, I=..., J=..., VALUES=...    |              &
     FILE=filename, NAME=matname}                                             &
    [, LABEL=c]
```
- FULL RORDER: row-major input; CORDER: column-major input
- SPARSE: lists non-zero positions (I, J) and their values; efficient for large matrices
- FILE supports ADAMSMAT and MATRIXx formats; NAME selects a named matrix within the file
- Maximum inline VALUES list: approx 48×48 before file-based input is preferred

## STRING
Stores a character string for retrieval in user subroutines via GTSTRG().
```
STRING/id, STRING=c                                                          &
    [, LABEL=c]
```
- Maximum 1024 characters
- Comma, semicolon, `&`, and `!` not permitted within the string value
- Access in user subroutines: `CALL GTSTRG(id, string_var, nchar, errflg)`

## PINPUT
Defines the ordered list of VARIABLE ids that form system input channels for linearization.
```
PINPUT/id, VARIABLES=id1[,id2,...]                                           &
    [, LABEL=c]
```
- Access in expressions: PINVAL(pinput_id, seq_num) (1-based index)
- Referenced in SIMULATE/LINEAR or STATEMAT commands
- Combined with POUTPUT to compute A, B, C, D state matrices

## POUTPUT
Defines the ordered list of VARIABLE ids that form system output channels for linearization.
```
POUTPUT/id, VARIABLES=id1[,id2,...]                                          &
    [, LABEL=c]
```
- Access in expressions: POUVAL(poutput_id, seq_num)
- Must be defined alongside a matching PINPUT for linearization to proceed

# Statements: Output (OUTPUT, REQUEST, RESULTS, SENSOR)

## OUTPUT
Controls which output files are written during simulation.
```
OUTPUT [, GRSAVE] [, REQSAVE] [, RPCSAVE] [, DACSAVE]                       &
    [, LOADS={ABAQUS|ANSYS|NASTRAN|GENERIC|DAC|RPC}]                        &
    [, NOSEPARATOR] [, YPR]                                                  &
    [, LABEL=c]
```
- GRSAVE: enables `.gra` graphics file; REQSAVE: enables `.req` request file
- RPCSAVE / DACSAVE: save all requests in RPC III or DAC format respectively
- NOSEPARATOR: suppresses file-break headers when topology changes mid-simulation
- YPR: outputs yaw-pitch-roll angles instead of default Euler psi-theta-phi
- REQUEST statements have no effect unless OUTPUT/REQSAVE is set

## REQUEST
Defines output channels (displacement, velocity, acceleration, force, or user-defined).
```
REQUEST/id,                                                                   &
    {DISPLACEMENT|VELOCITY|ACCELERATION|FORCE}, I=marker_id [, J=marker_id] &
    [, RM=marker_id] [, MOTION_RFRAME=marker_id]                             &
    | F2=expr\ F3=expr\ F4=expr\ F6=expr\ F7=expr\ F8=expr                  &
    [, TITLE=c] [, COMMENT=c]                                                &
    [, RESULTS_NAME=name] [, CNAMES=n1,...] [, CUNITS=u1,...]               &
    [, LABEL=c]
```
- F2–F8: arbitrary expression outputs (F1 = time, F5 = magnitude auto-computed)
- RM: resolves vector components into RM marker frame
- MOTION_RFRAME: changes reference frame for velocity/acceleration derivatives
- RESULTS_NAME: groups multiple requests into one XML result set
- CNAMES: renames output columns; fewer names than 8 → remaining columns dropped

## RESULTS
Creates a comprehensive output file containing all simulation results.
```
RESULTS [, FORMATTED | XRF]                                                  &
    [, NOACCELERATIONS] [, NOVELOCITIES] [, NODISPLACEMENTS]                 &
    [, NOREACTIONFORCES] [, NOAPPLIEDFORCES] [, NODATASTRUCTURES]            &
    [, NOSYSTEMELEMENTS] [, NOFLOATINGMARKERS] [, NOCONTACTS]                &
    [, DECIMALPLACES=i] [, ROUNDOFF] [, SIGNIFICANTFIGURES=i]               &
    [, LABEL=c]
```
- Default output: binary `.res` file; FORMATTED = ASCII text; XRF = XML
- NO... flags suppress categories to reduce file size and speed post-processing
- DECIMALPLACES/ROUNDOFF/SIGNIFICANTFIGURES/ZEROTHRESHOLD: XRF-only precision controls

## SENSOR
Monitors a function expression and takes an action when a threshold is crossed.
```
SENSOR/id, FUNCTION=expr|USER(r1,...),                                       &
    VALUE=r [, ERROR=r] [, {EQ|GE|LE}]                                      &
    [, {HALT|RETURN|PRINT|RESTART|CODGEN}]                                   &
    [, DT=r] [, STEPSIZE=r]                                                  &
    [, EVALUATE=expr|USER(...)]                                               &
    [, BISECTION] [, TERROR=r]                                               &
    [, ROUTINE=libname::subname]                                              &
    [, LABEL=c]
```
- EQ (default): triggers when |f − VALUE| ≤ ERROR; GE: f ≥ VALUE−ERROR; LE: f ≤ VALUE+ERROR
- HALT: terminates simulation; RETURN: stops and returns to script; RESTART: resets integrator
- BISECTION: root-finding for discontinuous signals (default: secant algorithm)
- DT: minimum time between successive triggers; STEPSIZE: forces step size at trigger time
- SENVAL(id): retrieves the value computed by EVALUATE at trigger time
- Use to end simulation at system failure, touchdown, or other discrete events

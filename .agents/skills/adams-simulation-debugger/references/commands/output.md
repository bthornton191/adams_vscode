# Commands: Output (OUTPUT, REQUEST, SENSOR)

## OUTPUT
Control which output files are written to disk.
```
OUTPUT [, {GRSAVE | NOGRSAVE}]
       [, {REQSAVE | NOREQSAVE}]
       [, {SEPARATOR | NOSEPARATOR}]
       [, LIST]
```
- `GRSAVE`: Resume writing graphics (`.gra`) file.
- `NOGRSAVE`: Stop writing graphics output.
- `REQSAVE`: Resume writing request (`.req`) file.
- `NOREQSAVE`: Stop writing request output.
- `SEPARATOR` (default): Write separator + new header when model topology changes mid-simulation. Produces two non-continuous output blocks — correct but discontinuous in plots.
- `NOSEPARATOR`: Suppress separators. Produces one continuous file; animation/plots uninterrupted, but may be misleading if topology actually changed.
- `LIST`: Print current OUTPUT settings.

---

## REQUEST
Redefine function expressions for an existing REQUEST element.
```
REQUEST/id [, F2=e] [, F3=e] [, F4=e]
           [, F6=e] [, F7=e] [, F8=e]
           [, FUNCTION=USER(r1[,...,r30])]
           [, ROUTINE=libname::subname]
           [, LIST]
```
- `F2=e`, `F3=e`, `F4=e`: Redefine output channels 2, 3, 4. Must be last argument or followed by `\`.
- `F6=e`, `F7=e`, `F8=e`: Redefine output channels 6, 7, 8.
  - Channel 1 = TIME (fixed); Channel 5 = magnitude of F2–F4 (auto-computed).
- `FUNCTION=USER(r1[,...,r30])`: Redefine via REQSUB subroutine (defines channels 2–4 and 6–8 only).
- `ROUTINE=libname::subname`: Alternate REQSUB library/subroutine.
- `LIST`: Print current REQUEST data.

---

## SENSOR
Redefine the trigger function of an existing SENSOR element.
```
SENSOR/id [, FUNCTION=e | USER(r1[,...,r30])]
          [, ROUTINE=libname::subname]
          [, EVALUATE_ROUTINE=libname::subname]
          [, LIST]
```
- `FUNCTION=e`: Redefine the sensor expression. Must be last argument or followed by `\`.
- `FUNCTION=USER(r1[,...,r30])`: Redefine via SENSUB subroutine with up to 30 constants.
- `ROUTINE=libname::subname`: Alternate SENSUB library/subroutine.
- `EVALUATE_ROUTINE=libname::subname`: Alternate SEVSUB evaluation routine (computes SENVAL(id) at trigger).
- `LIST`: Print current SENSOR data.

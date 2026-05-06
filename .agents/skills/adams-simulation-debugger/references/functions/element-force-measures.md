# Functions: Element-Specific Force/Torque Access

> All element functions share the same `comp` index:
> | comp | Meaning |
> |------|---------|
> | 1 | Force magnitude \|F\| |
> | 2 | Fx |
> | 3 | Fy |
> | 4 | Fz |
> | 5 | Torque magnitude \|T\| |
> | 6 | Tx |
> | 7 | Ty |
> | 8 | Tz |
>
> `jflag`: 0 = I marker side, 1 = J marker side. `rm`: result coordinate marker (0 = global).

## BEAM(id, jflag, comp, rm)
Force/torque component of BEAM/id.
- **Returns:** real, force or torque units

## BUSH(id, jflag, comp, rm)
Force/torque component of BUSHING/id.
- **Returns:** real, force or torque units

## CONTACT(id, jflag, comp, rm)
Force/torque component due to CONTACT/id (summed over all contact incidents).
- **Returns:** real, force or torque units

## FIELD(id, jflag, comp, rm)
Force/torque component of FIELD/id.
- **Returns:** real, force or torque units

## GFORCE(id, jflag, comp, rm)
Force/torque component of GFORCE/id.
- **Returns:** real, force or torque units

## JOINT(id, jflag, comp, rm)
Constraint force/torque component of JOINT/id.
- **Returns:** real, force or torque units
- **Example (friction input):** `JOINT(1,0,1,23)` = constraint force magnitude in J-frame 23.
  Radial load from revolute: `JOINT(1,0,1,23) - ABS(JOINT(1,0,4,23))`

## JPRIM(id, jflag, comp, rm)
Force/torque component of JPRIM/id primitive joint.
- **Returns:** real, force or torque units

## MOTION(id, jflag, comp, rm)
Reaction force/torque of MOTION/id at the constrained DOF.
- **Returns:** real, force or torque units

## NFORCE(id, at_marker, comp, rm)
Force/torque component of NFORCE/id at a specific connector marker.
- **at_marker:** must be one of the NFORCE connector markers
- **Returns:** real, force or torque units

## SFORCE(id, jflag, comp, rm)
Force/torque component of SFORCE/id.
- **Returns:** real, force or torque units

## SPDP(id, jflag, comp, rm)
Force/torque component of SPRINGDAMPER/id.
- **Returns:** real, force or torque units
- **Note:** Function name is `SPDP`, not `SPRINGDAMPER`.

## VFORCE(id, jflag, comp, rm)
Force/torque component of VFORCE/id.
- **Returns:** real, force or torque units

## VTORQ(id, jflag, comp, rm)
Torque component of VTORQUE/id. Force components (1–4) always return 0.
- **Returns:** real, torque units (comp 5–8); 0 for comp 1–4
- **Note:** Function name is `VTORQ`, not `VTORQUE`.

## CVCV(id, jflag, comp, rm)
Force/torque component of curve-curve constraint CVCV/id.
- **jflag:** 0 = IFLOAT marker, 1 = JFLOAT marker
- **Returns:** real, force or torque units

## PTCV(id, jflag, comp, rm)
Force component of point-to-curve constraint PTCV/id.
- **Returns:** real, force or torque units

## FRICTION(id, index)
Friction force/torque data from FRICTION/id. Available from REQUEST and SENSOR expressions only.
| index | Description |
|-------|-------------|
| 1–3 | Friction force components FFX, FFY, FFZ in J-frame |
| 4–6 | Friction torque components FTX, FTY, FTZ in J-frame |
| 7–9 | Friction coefficients μx, μy, μz |
| 10–12 | Rotational friction coefficients |
| 13 | Effective static friction coefficient (0 if sliding) |
| 14–16 | Joint sliding velocity Vx, Vy, Vz |
| 17–19 | Joint angular velocity Wx, Wy, Wz |
| 26 | BETA: stiction transition factor |

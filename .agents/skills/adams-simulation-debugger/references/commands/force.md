# Commands: Forces

> Commands modify existing force elements. None can change I/J marker assignments or element type.

## SFORCE
Redefine the function or application of a single-component force/torque.
```
SFORCE/id [, FUNCTION=e | USER(r1[,...,r30])]
          [, I=id, J=id]
          [, {ACTIONONLY | REACTION}]
          [, ROUTINE=libname::subname]
          [, LIST]
```
- `FUNCTION=e`: Redefine scalar force/torque expression. Must be last argument or followed by `\`.
- `FUNCTION=USER(r1[,...,r30])`: Pass up to 30 constants to SFOSUB user subroutine.
- `I=id, J=id`: Respecify application markers.
- `ACTIONONLY`: Apply force at I only; no reaction at J.
- `REACTION`: Action at I, equal/opposite reaction at J. **Default.**
- `LIST`: Print current SFORCE data.

---

## VFORCE
Redefine components of a 3-component translational force vector.
```
VFORCE/id [, FX=e] [, FY=e] [, FZ=e] [, FXYZ=e3d]
          [, I=id] [, JFLOAT=id] [, RM=id]
          [, FUNCTION=USER(r1[,...,r30])]
          [, ROUTINE=libname::subname]
          [, LIST]
```
- `FX=e`, `FY=e`, `FZ=e`: Redefine individual force components along RM marker axes.
- `FXYZ=e3d`: Redefine all three components as a single 3D vector expression.
- `I=id`: Respecify action marker (fixed; different part from JFLOAT).
- `JFLOAT=id`: Respecify floating reaction marker (kept coincident with I).
- `RM=id`: Respecify reference frame marker for component orientation.
- `LIST`: Print current VFORCE data.

---

## VTORQUE
Redefine components of a 3-component torque vector.
```
VTORQUE/id [, TX=e] [, TY=e] [, TZ=e] [, TXYZ=e3d]
           [, I=id] [, JFLOAT=id] [, RM=id]
           [, FUNCTION=USER(r1[,...,r30])]
           [, ROUTINE=libname::subname]
           [, LIST]
```
- `TX=e`, `TY=e`, `TZ=e`: Redefine torque components about RM marker axes (right-hand rule; CCW positive).
- `TXYZ=e3d`: Redefine all three torque components as a 3D vector expression.
- `I=id`, `JFLOAT=id`, `RM=id`: Respecify markers (same rules as VFORCE).
- `LIST`: Print current VTORQUE data.

---

## GFORCE
Redefine components of a 6-component generalised force (3 force + 3 torque).
```
GFORCE/id [, FX=e] [, FY=e] [, FZ=e] [, FXYZ=e3d]
          [, TX=e] [, TY=e] [, TZ=e] [, TXYZ=e3d]
          [, I=id] [, JFLOAT=id] [, RM=id]
          [, FUNCTION=USER(r1[,...,r30])]
          [, ROUTINE=libname::subname]
          [, LIST]
```
- `FX/FY/FZ/FXYZ`: Redefine translational force components along RM marker axes.
- `TX/TY/TZ/TXYZ`: Redefine rotational torque components.
- `FUNCTION=USER(...)`: Pass up to 30 constants to GFOSUB.
- `LIST`: Print current GFORCE data.

---

## SPRINGDAMPER
Redefine spring/damper stiffness, damping, and reference values.
```
SPRINGDAMPER/id [, K=r]     [, C=r]
               [, LENGTH=r] [, FORCE=r]
               [, KT=r]     [, CT=r]
               [, ANGLE=r]  [, TORQUE=r]
               [, LIST]
```
- `K=r`: Translational spring stiffness. Range: `> 0`
- `C=r`: Translational viscous damping. Range: `≥ 0`
- `LENGTH=r`: Reference length (free length when preload=0). Range: `> 0`
- `FORCE=r`: Translational preload at LENGTH.
- `KT=r`: Torsional spring stiffness. Range: `> 0`
- `CT=r`: Torsional viscous damping. Range: `> 0`
- `ANGLE=r`: Reference angle (radians; append `D` for degrees).
- `TORQUE=r`: Torsional preload at ANGLE.
- `LIST`: Print current SPRINGDAMPER data.

---

## BUSHING
Redefine stiffness, damping, and preload of an existing bushing.
```
BUSHING/id [, K=r1,r2,r3]    [, C=r1,r2,r3]
           [, KT=r1,r2,r3]   [, CT=r1,r2,r3]
           [, FORCE=r1,r2,r3] [, TORQUE=r1,r2,r3]
           [, LIST]
```
- `K=r1,r2,r3`: Translational stiffness (x, y, z of J marker).
- `C=r1,r2,r3`: Translational viscous damping.
- `KT=r1,r2,r3`: Torsional stiffness (rotational about x, y, z).
- `CT=r1,r2,r3`: Torsional viscous damping.
- `FORCE=r1,r2,r3`: Translational preload.
- `TORQUE=r1,r2,r3`: Rotational preload.
- `LIST`: Print current BUSHING data.

> Rotational constitutive equations only valid when rotation angles about x and y remain < 10°. Rotation about z can exceed 90°.

---

## BEAM
Redefine cross-section properties and material of an existing beam element.
```
BEAM/id [, AREA=r]   [, EMODULUS=r]  [, GMODULUS=r]
        [, IXX=r]    [, IYY=r, IZZ=r]
        [, ASY=r]    [, ASZ=r]
        [, CRATIO=r] [, CMATRIX=r1,...,r21]
        [, LENGTH=r]
        [, LIST]
```
- `AREA=r`: Cross-sectional area.
- `EMODULUS=r`: Young's modulus of elasticity.
- `GMODULUS=r`: Shear modulus.
- `IXX=r`: Torsional shape factor (polar moment for solid circle: `πr⁴/2`).
- `IYY=r, IZZ=r`: Second moments of area (solid circle: `πr⁴/4` each).
- `ASY=r, ASZ=r`: Timoshenko shear correction factors.
- `CRATIO=r`: Structural damping ratio: `CMATRIX = CRATIO × KMATRIX`.
- `CMATRIX=r1,...,r21`: Explicit 6×6 symmetric damping matrix (21 upper-triangle values, column-major).
- `LENGTH=r`: Undeformed beam length.
- `LIST`: Print current BEAM data.

---

## FIELD
Redefine stiffness, damping, preload, and reference values of a 6-DOF field force.
```
FIELD/id [, KMATRIX=r1,...,r36]  [, CMATRIX=r1,...,r36]
         [, CRATIO=r]             [, FORCE=r1,...,r6]
         [, LENGTH=r1,...,r6]
         [, FUNCTION=USER(r1[,...,r30])]
         [, ROUTINE=libname::subname]
         [, LIST]
```
- `KMATRIX=r1,...,r36`: 6×6 stiffness matrix (column-major, 36 values). Must be positive semi-definite.
- `CMATRIX=r1,...,r36`: 6×6 damping matrix (column-major). Must be positive semi-definite.
- `CRATIO=r`: `CMATRIX = CRATIO × KMATRIX`.
- `FORCE=r1,...,r6`: Six preload components (3 forces + 3 torques) at LENGTH reference.
- `LENGTH=r1,...,r6`: Reference position/orientation (3 translational + 3 projected angles in J-frame; not Euler angles).
- `FUNCTION=USER(r1[,...,r30])`: Nonlinear field via FIESUB.
- `LIST`: Print current FIELD data.

---

## FRICTION
Modify friction parameters on an existing joint friction element.
```
FRICTION/id [, MU_DYNAMIC=r]    [, MU_STATIC=r]
            [, STICTION_TRANSITION_VELOCITY=r]
            [, MAX_STICTION_DEFORMATION=r]
            [, PIN_RADIUS=r]    [, BALL_RADIUS=r]
            [, FRICTION_ARM=r]  [, REACTION_ARM=r]
            [, EFFECT={ALL | STICTION | SLIDING}]
            [, INPUTS=(listing)]
            [, INACTIVE=STATIC]
            [, JOINT=id]
            [, LIST]
```
- `MU_DYNAMIC=r`: Dynamic friction coefficient.
- `MU_STATIC=r`: Static friction coefficient.
- `STICTION_TRANSITION_VELOCITY=r`: Velocity threshold for stiction activation. Range: `> 0`
- `EFFECT={ALL|STICTION|SLIDING}`: Include stiction (`STICTION`), sliding (`SLIDING`), or both (`ALL`, default). Disabling `STICTION` greatly improves speed but removes stick-slip behaviour.
- `INPUTS=(...)`: Which reaction loads feed the friction model: `ALL`, `NONE`, `PRELOAD`, `REACTION_FORCE`, `BENDING_MOMENT`, `TORSIONAL_MOMENT`.
- `INACTIVE=STATIC`: Suppress friction during static/quasi-static analyses (avoids stiction convergence problems).
- `JOINT=id`: Reassign friction to a different joint.
- `LIST`: Print current FRICTION data.

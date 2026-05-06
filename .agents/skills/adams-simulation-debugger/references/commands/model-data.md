# Commands: Model Data (PART, MARKER, JOINT, MOTION)

> These commands modify existing dataset elements. They cannot create new elements.
> After modification, Adams re-processes ICs at the next SIMULATE call.

## PART
Redefine mass and inertia properties of an existing part.
```
PART/id [, MASS=r]
        [, IP=xx,yy,zz [,xy,xz,yz]]
        [, LIST]
```
- `MASS=r`: Respecify part mass.
- `IP=xx,yy,zz[,xy,xz,iyz]`: Respecify inertia tensor about IM (or CM) marker origin, in IM marker axes. Diagonal moments: xx, yy, zz. Cross products: xy, xz, yz (positive integral sign convention). Omit cross terms to zero them.
- `LIST`: Print current PART data.

> After PART modification, the solver performs IC analysis and integrator restart at the next SIMULATE command.

---

## MARKER
Reposition or reorient an existing fixed marker relative to its parent part.
```
MARKER/id [, QP=x,y,z]
          [, REULER=a,b,c]
          [, ZP=x,y,z] [, XP=x,y,z]
          [, RM=id] [, USEXP]
          [, LIST]
```
- `QP=x,y,z`: Marker origin in parent-part BCS coordinates (append `D` for degrees on angles).
- `REULER=a,b,c`: Orientation via body-fixed 3-1-3 Euler angles (Z by a, X' by b, Z'' by c), in radians. Completely replaces previous orientation.
- `ZP=x,y,z`: Point on positive z-axis of marker (BCS coords). With `USEXP`: point in positive xz-plane.
- `XP=x,y,z`: Point in positive xz-plane (not on x-axis). With `USEXP`: point on positive x-axis.
- `RM=id`: Reference marker for interpreting QP/XP/ZP/REULER.
- `USEXP`: Swap XP/ZP semantic roles — XP → x-axis direction; ZP → xz-plane.
- `LIST`: Print current marker data in BCS coordinates.

> Floating markers can be listed but not repositioned via command.

---

## JOINT
List data for an existing joint. (Joint parameters cannot be modified via command.)
```
JOINT/id [, LIST]
```
- `LIST`: Print current JOINT connectivity and type.

---

## MOTION
Redefine the function expression or characteristics of an existing motion constraint.
```
MOTION/id [, FUNCTION=e | USER(r1[,...,r30])]
          [, {DISPLACEMENT | VELOCITY | ACCELERATION}]
          [, JOINT=id] [, I=id, J=id]
          [, {ROTATION | TRANSLATION}]
          [, {X | Y | Z | B1 | B2 | B3}]
          [, ICDISP=r] [, ICVEL=r]
          [, ROUTINE=libname::subname]
          [, LIST]
```
- `FUNCTION=e`: Redefine motion as a scalar expression (time-only function; **not** state-dependent).
- `FUNCTION=USER(r1[,...,r30])`: Redefine using MOTSUB subroutine with up to 30 real constants.
- `DISPLACEMENT`: Motion defines displacement. **Default.**
- `VELOCITY`: Motion defines velocity.
- `ACCELERATION`: Motion defines acceleration.
- `JOINT=id`: Reassign motion to a different joint.
- `ROTATION`: Apply as rotational motion (cylindrical joints).
- `TRANSLATION`: Apply as translational motion (cylindrical joints).
- `X|Y|Z`: Redefine as DX(I,J,J), DY(I,J,J), or DZ(I,J,J) respectively.
- `B1|B2|B3`: Redefine as first/second/third Body 1-2-3 Euler angle.
- `ICDISP=r`: Initial displacement (for velocity- or acceleration-defined motions).
- `ICVEL=r`: Initial velocity (for acceleration-defined motions).
- `LIST`: Print current MOTION data.

# Statements: Constraints

## JOINT
Defines a kinematic joint between two markers, removing DOFs.
```
JOINT/id, {REVOLUTE|TRANSLATIONAL|CYLINDRICAL|SPHERICAL|PLANAR|FIXED|         &
           CONVEL|HOOKE|SCREW|UNIVERSAL|ATPOINT|INLINE|INPLANE|ORIENTATION|   &
           PARALLEL_AXES|PERPENDICULAR},                                       &
    I=marker_id, J=marker_id                                                   &
    [, PITCH=r]   ! SCREW only                                                 &
    [, LABEL=c]
```
- I marker on moving part; J marker on reference part (often ground)
- Z-axes must be aligned for REVOLUTE, TRANSLATIONAL, CYLINDRICAL (coincident I/J Z-axes)
- SCREW PITCH= meters per radian of rotation
- ATPOINT / INLINE / INPLANE are primitive joints; useful for building compound connections

## JPRIM
Joint primitive — removes one or more DOFs without prescribing a complete joint.
```
JPRIM/id, {ATPOINT|INLINE|INPLANE|ORIENTATION|PARALLEL_AXES|PERPENDICULAR},  &
    I=marker_id, J=marker_id                                                   &
    [, LABEL=c]
```
- ATPOINT: coincident origins (3 translational DOF removed)
- INLINE: I origin on J Z-axis (2 translational)
- INPLANE: I origin on J XY-plane (1 translational)
- Combine JPRIMs to build compound constraints (e.g., INLINE + ORIENTATION = TRANSLATIONAL JOINT)

## MOTION
Prescribes displacement, velocity, or acceleration along a joint DOF.
```
MOTION/id, JOINT=joint_id, [JPRIMIT=joint_prim_id],                          &
    {ROTATION|TRANSLATION},                                                    &
    {DISPLACEMENT|VELOCITY|ACCELERATION},                                      &
    FUNCTION=expr|USER(r1,...)                                                 &
    [, ROUTINE=libname::subname]                                               &
    [, LABEL=c]
```
- FUNCTION evaluated at every timestep — must return the prescribed value in radians or model length units
- DISPLACEMENT motions differentiated numerically for velocity/acceleration; VELOCITY motions integrated for displacement
- A joint must exist before the MOTION can reference it

## COUPLER
Links motion of two or more joints by a gear or differential relationship.
```
COUPLER/id, JOINTS=jid1,jid2[,jid3],                                         &
    TYPE={ROT,ROT | ROT,TRANS | TRANS,TRANS | ...},                           &
    SCALES=r1,r2[,r3]                                                          &
    [, LABEL=c]
```
- SCALES: ratio coefficients; relationship: scale1·q1 + scale2·q2 [+ scale3·q3] = 0
- TYPE pair specifies which DOF of each joint (ROT = rotation, TRANS = translation)

## GEAR
Defines a simple gear pair using pitch circle markers on two joints.
```
GEAR/id, JOINTS=joint_id1,joint_id2, CV=marker_id                             &
    [, LABEL=c]
```
- CV (common velocity marker) defines the pitch contact point — must be on the carrier body
- Ratio determined automatically from marker geometry
- Preferred alternative to COUPLER when explicit pitch circles are defined

## GCON
General constraint — imposes an arbitrary algebraic or scalar constraint via a user expression.
```
GCON/id, I=marker_id, J=marker_id,                                            &
    FUNCTION=expr|USER(r1,...)                                                 &
    [, ROUTINE=libname::subname]                                               &
    [, LABEL=c]
```
- Expression must evaluate to a scalar residual (= 0 when satisfied)
- Jacobian estimated numerically unless the ROUTINE provides analytic derivatives
- Numerical Jacobian errors → convergence problems; provide analytic derivatives in user routine

## CVCV
Curve-to-curve contact constraint (velocity-level, smooth sliding).
```
CVCV/id, I_CURVE=curve_id, I_RM=marker_id,                                   &
    J_CURVE=curve_id, J_RM=marker_id                                           &
    [, LABEL=c]
```
- I_RM / J_RM: reference markers for the respective curves
- Forces two curves to remain tangent; floating markers identify contact point
- Used for cam/follower, rack/pinion geometric contact (no penetration model)

## PTCV
Point-to-curve constraint (point on I slides along curve on J).
```
PTCV/id, I=marker_id, CURVE=curve_id, RM=marker_id                           &
    [, LABEL=c]
```
- I marker origin is constrained to lie on CURVE; RM is the curve's reference marker
- Removes 2 translational DOFs (point stays on 3D curve)
- Floating marker at contact point auto-repositioned each step

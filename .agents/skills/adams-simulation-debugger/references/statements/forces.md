# Statements: Forces

## ACCGRAV
Defines gravitational acceleration applied to all parts.
```
ACCGRAV [, IGRAV=r] [, JGRAV=r] [, KGRAV=r]
```
- IGRAV/JGRAV/KGRAV: components in the global X, Y, Z directions
- Default MKS: `-9.80665` in JGRAV (global Y down); IPS: `-386.09` in JGRAV
- Omitting ACCGRAV disables gravity entirely

## SFORCE
Single-component force or torque along/about a specified axis.
```
SFORCE/id, I=marker_id, J=marker_id,                                         &
    {TRANSLATIONAL|ROTATIONAL},                                               &
    FUNCTION=expr|USER(r1,...)                                                &
    [, ACTIONONLY] [, ROUTINE=libname::subname]                               &
    [, LABEL=c]
```
- Positive value: force along I marker Z-axis (TRANSLATIONAL) or torque about Z-axis (ROTATIONAL)
- Reaction applied to J unless ACTIONONLY
- DM(I,J) and VR(I,J) commonly used in FUNCTION for spring/damper expressions

## VFORCE
Three-component force vector applied at a marker.
```
VFORCE/id, I=marker_id, JFLOAT=marker_id, RM=marker_id,                     &
    FX=expr|USER(...), FY=expr|USER(...), FZ=expr|USER(...)                  &
    [, ACTIONONLY] [, ROUTINE=libname::subname]                               &
    [, LABEL=c]
```
- FX/FY/FZ expressed in the RM reference marker frame
- JFLOAT marker repositioned by solver to coincide with I each step (floating marker)

## VTORQUE
Three-component torque vector applied at a marker.
```
VTORQUE/id, I=marker_id, JFLOAT=marker_id, RM=marker_id,                    &
    TX=expr|USER(...), TY=expr|USER(...), TZ=expr|USER(...)                  &
    [, ACTIONONLY] [, ROUTINE=libname::subname]                               &
    [, LABEL=c]
```
- TX/TY/TZ expressed in RM frame; JFLOAT is floating reference point

## GFORCE
Six-component generalised force (3 force + 3 torque) defined in one statement.
```
GFORCE/id, I=marker_id, JFLOAT=marker_id, RM=marker_id,                     &
    FX=expr, FY=expr, FZ=expr, TX=expr, TY=expr, TZ=expr                    &
    |USER(r1,...)                                                             &
    [, ACTIONONLY] [, ROUTINE=libname::subname]                               &
    [, LABEL=c]
```
- Preferred over separate VFORCE + VTORQUE for coupled force/torque expressions
- USER mode: GFOSUB user subroutine returns all 6 components

## SPRINGDAMPER
Translational or rotational spring/damper element.
```
SPRINGDAMPER/id, I=marker_id, J=marker_id,                                  &
    {TRANSLATIONAL|ROTATIONAL},                                              &
    [K=r|KSPLINE=spline_id], [C=r|CSPLINE=spline_id],                       &
    [LENGTH=r|ANGLE=r],                                                      &
    [PRELOAD=r]                                                               &
    [, LABEL=c]
```
- K and C can be constants or spline-interpolated (nonlinear) functions of deformation/rate
- LENGTH (or ANGLE for ROTATIONAL): free length/angle at zero force
- PRELOAD adds a constant offset force/torque independent of deformation

## BUSHING
Six-DOF linear spring/damper (generalized flexible connection).
```
BUSHING/id, I=marker_id, J=marker_id,                                        &
    K=kx,ky,kz,ktx,kty,ktz,                                                  &
    C=cx,cy,cz,ctx,cty,ctz,                                                   &
    [PRELOAD=fx,fy,fz,tx,ty,tz]                                               &
    [, LABEL=c]
```
- K: translational (kx, ky, kz) and rotational (ktx, kty, ktz) stiffness
- C: translational and rotational damping
- Force resolved in J marker frame; small-angle linearisation of rotation

## BEAM
Euler-Bernoulli beam element with full axial, bending, shear, and torsion.
```
BEAM/id, I=marker_id, J=marker_id,                                           &
    LENGTH=r, ASY=r, ASZ=r,                                                  &
    IYY=r, IZZ=r, IXX=r,                                                     &
    EMODULUS=r [, GMODULUS=r] [, CRATIO=r]                                   &
    [, LABEL=c]
```
- LENGTH: undeformed beam length; ASY/ASZ: shear areas in Y, Z
- IYY/IZZ: area moments about Y and Z (bending); IXX: polar moment (torsion)
- CRATIO: structural damping coefficient (fraction of critical damping)
- Beam assumes small deflection theory; use flexible bodies for large deformation

## CONTACT
Geometric contact with normal and friction force models.
```
CONTACT/id,                                                                   &
    I_GEOMETRY=geometry_id, J_GEOMETRY=geometry_id,                          &
    [STIFFNESS=r] [, EXPONENT=r] [, DAMPING=r] [, DMAX=r]                   &
    [, STATIC_MU=r] [, DYNAMIC_MU=r] [, STICTION_TRANSITION_VEL=r]          &
    [, FRICTION_TRANSITION_VEL=r]                                             &
    [, COULOMB_FRICTION={ON|OFF}]                                             &
    [, GEOMETRY_LIBRARY={Default_library|Parasolid}]                          &
    [, LABEL=c]
```
- Normal force: `F = k·δ^e − damp·δ̇` (IMPACT model); DMAX = penetration depth for full damping
- EXPONENT=1.5 for Hertz contact; EXPONENT=1 for soft/compliant contact
- STIFFNESS values: metals ~1e5–1e8 N/mm; rubber ~100–1000 N/mm
- Contact is computationally expensive; large DMAX and high EXPONENT can cause divergence

## NFORCE
N-body force field connecting multiple markers via a matrix of stiffness/damping.
```
NFORCE/id, MARKERS=id1,id2,...,                                              &
    KMATRIX=matrix_id, CMATRIX=matrix_id,                                    &
    REFERENCE_MARKERS=id1,id2,...                                             &
    [, LABEL=c]
```
- Implements non-diagonal cross-coupling stiffness (e.g., for flexible chassis or fluid coupling)
- KMATRIX: 6n×6n stiffness matrix; CMATRIX: 6n×6n damping matrix

## MFORCE
Marker-based multi-point force defined entirely by a user subroutine.
```
MFORCE/id, MARKERS=id1,id2,...,                                              &
    USER(r1,...)                                                              &
    [, ROUTINE=libname::subname]                                              &
    [, LABEL=c]
```
- MFOSUB user subroutine receives all marker states and returns force/torque vectors
- Use when analytic expression is insufficient for complex multi-body interaction

## FIELD
Coupled spring-damper matrix connecting 6 DOFs of two markers.
```
FIELD/id, I=marker_id, J=marker_id,                                          &
    TRANSLATIONAL_STIFFNESS=kx,ky,kz,                                        &
    ROTATIONAL_STIFFNESS=ktx,kty,ktz,                                        &
    [TRANSLATIONAL_DAMPING=...] [, ROTATIONAL_DAMPING=...]                   &
    [, CRATIO=r]                                                              &
    [, LABEL=c]
```
- Similar to BUSHING but allows nonlinear stiffness via FUNCTION or USER subroutine mode
- CRATIO mode applies proportional damping across all components

## FRICTION
Adds Coulomb friction model to a joint.
```
FRICTION/id, JOINT=joint_id,                                                 &
    MU_STATIC=r, MU_DYNAMIC=r,                                               &
    [STICTION_TRANSITION_VEL=r] [, FRICTION_TRANSITION_VEL=r]               &
    [, BENDING_REACTION_ARM=r] [, PIN_RADIUS=r]                              &
    [, PRELOAD_F=r] [, PRELOAD_M=r]                                          &
    [, REACTION_ARM=r]                                                        &
    [, LABEL=c]
```
- Friction forces are reaction-load dependent; highly nonlinear → can cause convergence issues
- STICTION_TRANSITION_VEL: velocity below which static friction applies (typically 0.1 mm/s)
- Reduce MU values or increase transition velocities if friction causes stiction oscillations

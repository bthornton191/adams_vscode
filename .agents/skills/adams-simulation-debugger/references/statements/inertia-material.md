# Statements: Inertia & Material (PART, POINT_MASS, FLEX_BODY)

## PART
Defines a rigid body with mass properties and initial placement.
```
PART/id, MASS=r, CM=marker_id, IM=marker_id,                   &
    [IP=ixx,iyy,izz[,ixy,ixz,iyz]],                            &
    [QG=x,y,z], [REULER=psi,theta,phi],                        &
    [VX=r,VY=r,VZ=r], [WX=r,WY=r,WZ=r],                       &
    [GROUND] [, LABEL=c]
```
- CM marker defines centre-of-mass location and inertia axes; IM marker orients principal inertia axes if different from CM
- IP: six inertia components (Ixx, Iyy, Izz, Ixy, Ixz, Iyz) in CM marker axes
- QG/REULER: initial position (global origin) and Euler orientation `(ψ θ φ)` of the body reference frame
- GROUND flag makes this part the fixed reference frame (only one GROUND part allowed)
- No GROUND marker has id=0; always reference as PART/id=0 or name `GROUND`

## POINT_MASS
Defines a particle (3 translational DOF only, no rotational DOF).
```
POINT_MASS/id, MASS=r, QG=x,y,z,                              &
    [VX=r,VY=r,VZ=r],                                          &
    [LABEL=c]
```
- No inertia tensor — point masses cannot carry rotational loads
- Only spherical, atpoint, inline, and inplane joints/primitives may be applied to a point mass
- Initial velocity components must be given in global frame

## FLEX_BODY
Imports a Mode Neutral File (.mnf) to define a flexible body.
```
FLEX_BODY/id, MNF_FILE=filename,                               &
    [QG=x,y,z], [REULER=psi,theta,phi],                        &
    [VX=r,VY=r,VZ=r], [WX=r,WY=r,WZ=r],                       &
    [DAMPING={OFF|MODAL|STIFFNESS|COMBINED}], [ALPHA=r,BETA=r],&
    [MODES=id1,id2,...], [NODE_INCIDENTS]                       &
    [, LABEL=c]
```
- MNF_FILE path may be relative (to dataset directory) or absolute
- MODAL damping: specify critical damping ratios per mode in FLEX_BODY/DAMPING_RATIOS
- MODES restricts active mode set; smaller set speeds simulation and may help convergence
- Interface nodes connect to joints/forces via floating MARKER statements within the FLEX_BODY

## END
Terminates the Adams dataset file.
```
END
```
- Must be the last statement in the `.adm` file; any statements after END are ignored

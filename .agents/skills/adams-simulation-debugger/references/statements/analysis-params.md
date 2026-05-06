# Statements: Analysis Parameters (DEBUG, INTEGRATOR, EQUILIBRIUM, IC, KINEMATICS, LSOLVER, PREFERENCES, UNITS)

## DEBUG
Enables diagnostic output during simulation.
```
DEBUG [, EPRINT] [, JMDUMP] [, RHSDUMP] [, MATLAB]
```
- **EPRINT**: prints per-step/iteration diagnostics to message file:
  - Step number, order, integration error, largest state correction (variable and part), Jacobian evaluation flag
  - Format: `T=<time> H=<step> O=<order> E=<error> DOBJ=<correction>` plus element/variable IDs
- **JMDUMP**: writes full Jacobian matrix to `.jac` file at every corrector iteration
- **RHSDUMP**: writes right-hand-side residual vector to `.rhs` file at every corrector iteration
- **MATLAB**: formats JMDUMP/RHSDUMP output for direct import (`load filename.jac` in MATLAB)
- Limit JMDUMP/RHSDUMP to short runs — files grow proportional to iterations × model size

## INTEGRATOR
Controls the numerical integrator for dynamic analysis.
```
INTEGRATOR [, {GSTIFF|WSTIFF|HHT|NEWMARK|HASTIFF}]                         &
    [, {I3|SI2|SI1}]                                                         &
    [, ERROR=r] [, HMAX=r] [, HMIN=r] [, HINIT=r]                          &
    [, MAXIT=i] [, KMAX=i]                                                   &
    [, PATTERN=c1:c2:...:c10]                                                &
    [, CORRECTOR={ORIGINAL|MODIFIED|ORIG_CONSTANT}]                          &
    [, INTERPOLATE={ON|OFF}]                                                  &
    [, ALPHA=r] [, FIXIT=i]                                                  &
    [, ADAPTIVITY=r] [, HRATIO=i] [, MAXERR=r]
```
- **Default**: GSTIFF/I3, ERROR=1e-3
- SI2 (for GSTIFF/WSTIFF) or SI1 (for HASTIFF): index-reduction formulations for better velocity accuracy
- **CORRECTOR=MODIFIED**: recommended for models with contact; re-evaluates Jacobian every iteration
- PATTERN=F: adaptive Jacobian — mark evaluation positions; `T` = always evaluate; `F` = reuse previous
- FIXIT=i: forces fixed step count per output interval for real-time applications
- HHT/NEWMARK defaults: ERROR=1e-5; add ALPHA=-0.05 for HHT numerical dissipation

## EQUILIBRIUM
Sets tolerances for static and quasi-static analyses.
```
EQUILIBRIUM [, ERROR=r] [, IMBALANCE=r] [, MAXIT=i]                        &
    [, ALIMIT=r] [, TLIMIT=r] [, STABILITY=r]                               &
    [, PATTERN=c1:...:c10]                                                   &
    [, METHOD={ORIGINAL|ADVANCED|AGGRESSIVE|ALL}]
```
- Default: ERROR=1e-4, IMBALANCE=1e-4, MAXIT=25, STABILITY=1e-5
- **STABILITY**: multiplier for augmentation `α·(M+C)` added to stiffness to handle neutral modes
- **METHOD=ADVANCED**: tries ORIGINAL, then Trust-Region, then Tensor-Krylov automatically
- **METHOD=ALL**: additionally tries Broyden-Armijo and Hooke-Jeeves pattern search
- ALIMIT (rad): max angular correction per Newton iteration; default 30° (π/6)
- TLIMIT (model units): max translational correction per iteration; default 100

## IC
Sets tolerances for initial condition assembly.
```
IC [, ERROR=r] [, MAXIT=i] [, PATTERN=c1:...:c10]                          &
    [, TLIMIT=r] [, ALIMIT=r]                                                &
    [, AERROR=r] [, AMAXIT=i] [, APATTERN=c1:...:c10]                      &
    [, VERROR=r]
```
- ERROR: position/displacement assembly tolerance; default 1e-10
- AERROR: acceleration assembly tolerance; default 1e-4
- VERROR: velocity assembly tolerance; default 1e-4
- Called automatically before every dynamic or static analysis
- WSTIFF with INTERPOLATE=ON re-runs IC assembly at each output step

## KINEMATICS
Sets tolerances for zero-DOF kinematic analyses.
```
KINEMATICS [, ERROR=r] [, MAXIT=i] [, PATTERN=c1:...:c10]                  &
    [, TLIMIT=r] [, ALIMIT=r]                                                &
    [, AERROR=r] [, AMAXIT=i] [, APATTERN=c1:...:c10] [, HMAX=r]
```
- Default ERROR=1e-4; ALIMIT=30°; MAXIT=25
- Kinematic analysis requires exactly 0 DOFs; uses Newton-Raphson per output step
- TLIMIT/ALIMIT prevent large steps that assemble to the wrong configuration
- HMAX: maximum step size for kinematic analyses (defaults to output step size)

## LSOLVER
Selects the linear algebra solver for Jacobian factorization.
```
LSOLVER [, {AUTO|CALAHAN|UMF}] [, STABILITY=r]
```
- AUTO (default): switches to UMF when model size exceeds threshold (~1M equations)
- CALAHAN: fast sparse direct solver; optimal for small-to-medium models
- UMF: Unsymmetric Multi-Frontal; better for large or dense systems; SMP-capable via NTHREADS
- STABILITY (0–1): Markowitz pivot quality criterion; increase toward 1.0 if factorization fails

## PREFERENCES
Controls global solver options: threading, contact, flex body, plugin paths.
```
PREFERENCES [, CONTACT_GEOMETRY_LIBRARY={Default_library|Parasolid}]        &
    [, CONTACT_FACETING_TOLERANCE=r]                                         &
    [, NTHREADS=n]                                                           &
    [, LIBPATH=dir1:dir2:...]                                                &
    [, FLEX_BODY_FORMULATION={ORIGINAL|OPTIMIZED|MAX_OPTIMIZATION}]          &
    [, FLEX_LIMIT_CHECK={skin|SELNOD}]                                       &
    [, FLEX_LIMIT_CHECK_ACTION={HALT|RETURN|MESSAGE_ONLY}]                   &
    [, STATUS_MESSAGE={ON|OFF}]
```
- Default geometry library: RAPID (polygon-based); Parasolid is more accurate but slower
- NTHREADS: enables SMP parallelism (optimal = physical core count to 2× with HyperThreading)
- LIBPATH: prepends directories searched for user subroutine DLL/shared library plug-ins

## UNITS
Defines the unit system for the solver.
```
UNITS [, SYSTEM={CGS|FPS|IPS|MKS|NONE}]                                     &
    | [FORCE={...}, MASS={...}, LENGTH={...}, TIME={...}]                    &
    [, UCF=r]
```
- SYSTEM=MKS: m, kg, s, N; IPS: in, lbm, s, lbf/386.09
- UCF (Units Consistency Factor): required when unit system is non-dynamical
- Adams always uses radians internally regardless of UNITS setting
- ACCGRAV values must match the chosen length and time units

# Commands: Analysis Parameters
> Commands modify existing elements already defined in the `.adm` dataset. They never create new elements.
> Statement form uses `/id` and creates; command form uses `/id` and modifies or queries.

## DEBUG
Controls diagnostic output verbosity and matrix dumps.
```
DEBUG [, EPRINT | NOEPRINT]
      [, JMDUMP | NOJMDUMP]
      [, RHSDUMP | NORHSDUMP]
      [, VERBOSE | NOVERBOSE]
      [, REQDUM | NOREQDUMP]
      [, MATLAB]
      [, DUMP]
      [, LIST]
```
- `EPRINT`: Print per-step/iteration table (step#, order, time, step size, residual, Jacobian flag). Default: `NOEPRINT`
- `NOEPRINT`: Suppress iteration table. Default.
- `JMDUMP`: Dump Jacobian matrix to `.jac` file each iteration. Default: `NOJMDUMP`
- `RHSDUMP`: Dump YY, RHS, and DELTA vectors to `.rhs` file each iteration. Default: `NORHSDUMP`
- `VERBOSE`: Output subroutine names, explanations, and remedies in screen diagnostics. Default: `NOVERBOSE`
- `MATLAB`: Format JMDUMP/RHSDUMP output as MATLAB-importable code. Use with JMDUMP or RHSDUMP.
- `DUMP`: Write current dataset representation with numeric values for functions/orientations to message file.
- `LIST`: Print current DEBUG settings.

## INTEGRATOR
Redefine integration algorithm and step-control parameters for dynamic analysis.
```
INTEGRATOR [/ {GSTIFF | WSTIFF | HASTIFF | HHT | NEWMARK}]
           [, {I3 | SI2 | SI1}]
           [, CORRECTOR={original | modified | orig_constant}]
           [, ERROR=r]   [, HINIT=r]   [, HMAX=r]  [, HMIN=r]
           [, KMAX=i]    [, MAXIT=i]   [, PATTERN=c1[:...:c10]]
           [, INTERPOLATE={ON | OFF}]
           [, FIXIT=i]   [, HRATIO=i]  [, MAXERR=r]
           [, ALPHA=r]   [, BETA=r]    [, GAMMA=r]
           [, DEFAULT]   [, LIST]
```
- `GSTIFF`: Gear Stiff BDF integrator. **Default.**
- `WSTIFF`: Wielenga Stiff BDF — step-size-aware coefficients.
- `HASTIFF`: Hiller-Anantharaman Stiff BDF; default formulation: SI1.
- `HHT`: Hilber-Hughes-Taylor; preferred for structural/flexible body problems.
- `NEWMARK`: Newmark-β integrator.
- `I3`: Index-3 formulation. Default for GSTIFF/WSTIFF/HHT.
- `SI2`: Stabilised Index-2; monitors velocity error. Available with GSTIFF/WSTIFF/HASTIFF.
- `SI1`: Stabilised Index-1. Available (and default) with HASTIFF only.
- `CORRECTOR`: `original` (default) — tolerance on all variables; `modified` — tolerance on integrated variables only (robust for contact/discontinuous models); `orig_constant` — evaluate Jacobian once at start.
- `ERROR=r`: Integration error tolerance. Default: `1e-3`. HHT/Newmark default: `1e-5`. Range: `> 0`
- `HINIT=r`: Initial step size. Range: `HMIN < HINIT < HMAX`
- `HMAX=r`: Maximum step size. Default: output step size. Range: `> HMIN`
- `HMIN=r`: Minimum step size. Default: `1e-6 * HMAX`. Range: `> 0`
- `KMAX=i`: Maximum integration order (1–6). Default: `6`
- `MAXIT=i`: Maximum corrector iterations per step. Default: `10`
- `PATTERN=c1[:...:c10]`: Jacobian re-evaluation pattern; `T` = evaluate, `F` = reuse. Default: `T:F:F:F:T:F:F:F:T:F`
- `INTERPOLATE=ON|OFF`: Allow overshoot and interpolate back to output points. Default: `OFF`
- `FIXIT=i`: Fixed-step corrector iterations (enables fixed-step mode for real-time). Range: `1–10`
- `ALPHA=r`: HHT numerical damping coefficient. Default: `-0.3`. Range: `[-1/3, 0]`
- `DEFAULT`: Reset all parameters to built-in defaults.
- `LIST`: Print current integrator settings.

## EQUILIBRIUM
Redefine parameters for static/quasi-static equilibrium analysis.
```
EQUILIBRIUM [, ALIMIT=r]   [, ERROR=r]    [, IMBALANCE=r]
            [, MAXIT=i]    [, PATTERN=c1[:...:c10]]
            [, STABILITY=r] [, TLIMIT=r]
            [, METHOD={ORIGINAL | ADVANCED | AGGRESSIVE | ALL}]
            [, ATOL=r]     [, RTOL=r]     [, MAXITL=i]
            [, DEFAULT]    [, LIST]
```
- `ALIMIT=r`: Max angular correction per Newton iteration (radians; append `D` for degrees). Default: `10D`
- `ERROR=r`: Correction convergence threshold. Default: `1e-4`. Range: `> 0`
- `IMBALANCE=r`: Residual convergence threshold. Default: `1e-4`. Range: `> 0`
- `MAXIT=i`: Max Newton iterations. Default: `25`
- `STABILITY=r`: Fraction of `(M+C)` added to stiffness for neutral-mode stabilisation. Default: `1e-5`. Range: `> 0`
- `TLIMIT=r`: Max translational correction per iteration. Default: `20`. Range: `> 0`
- `METHOD`: `ORIGINAL` = classic Newton (default); `ADVANCED` = Newton + Trust-Region + Tensor-Krylov; `AGGRESSIVE` = adds Broyden-Armijo; `ALL` = adds Hooke-Jeeves
- `ATOL=r`: Absolute tolerance for advanced solvers. Default: `1e-6`
- `RTOL=r`: Relative tolerance for advanced solvers. Default: `0.0`
- `DEFAULT`: Reset to: `ALIMIT=10D, ERROR=1e-4, IMBALANCE=1e-4, MAXIT=25, STABILITY=1e-5, TLIMIT=20`
- `LIST`: Print current equilibrium settings.

## IC
Redefine tolerances for initial condition assembly.
```
IC [, AERROR=r]  [, ALIMIT=r]  [, AMAXIT=i]  [, APATTERN=c1[:...:c10]]
   [, ERROR=r]   [, MAXIT=i]   [, PATTERN=c1[:...:c10]]
   [, TLIMIT=r]  [, VERROR=r]
   [, DEFAULT]   [, LIST]
```
- `ERROR=r`: Displacement assembly tolerance. Default: `1e-10`
- `AERROR=r`: Acceleration assembly tolerance. Default: `1e-4`
- `VERROR=r`: Velocity assembly tolerance. Default: `1e-4`
- `ALIMIT=r`: Max angular increment per iteration. Default: `30D`
- `MAXIT=i`: Max displacement iterations. Default: `25`
- `AMAXIT=i`: Max acceleration iterations. Default: `25`
- `TLIMIT=r`: Max translational increment per iteration. Default: `1e10` (no limit)
- `DEFAULT`: Reset all IC parameters to defaults.
- `LIST`: Print current IC settings.

## KINEMATICS
Redefine solution parameters for zero-DOF kinematic analysis.
```
KINEMATICS [, AERROR=r]  [, ALIMIT=r]  [, AMAXIT=i]
           [, ERROR=r]   [, MAXIT=i]   [, PATTERN=c1[:...:c10]]
           [, TLIMIT=r]  [, HMAX=r]
           [, DEFAULT]   [, LIST]
```
- `ERROR=r`: Displacement error per step. Default: `1e-4`
- `AERROR=r`: Acceleration error per step. Default: `1e-4`
- `ALIMIT=r`: Max angular increment. Default: `30D`
- `MAXIT=i`: Max iterations per step. Default: `25`
- `HMAX=r`: Max time step (useful for fast-rotating mechanisms)
- `DEFAULT`: Reset all parameters to defaults.
- `LIST`: Print current settings.

## LSOLVER
Select the sparse linear algebra solver for Jacobian factorization.
```
LSOLVER [, {AUTO | CALAHAN | UMF}]
        [, STABILITY=r]
        [, LIST]
```
- `AUTO`: Automatic selection (CALAHAN below size threshold, UMF above). **Default.**
- `CALAHAN`: Fast sparse direct solver; optimal for small/medium models.
- `UMF`: Unstructured Multi-Frontal solver; better for large/dense systems; SMP-capable.
- `STABILITY=r`: Pivoting quality criterion for LU factorization. Default: `0.01`. Range: `(0, 1]`; increase toward 1.0 for stiff/badly-scaled systems.
- `LIST`: Print current solver name and stability value.

## PREFERENCES
Control solver global options: geometry library, failure behaviour, output messages.
```
PREFERENCES [, CONTACT_GEOMETRY_LIBRARY={Parasolid | Default_library}]
            [, CONTACT_FACETING_TOLERANCE=r]
            [, SIMFAIL={STOPCF | NOSTOPCF}]
            [, STATUS_MESSAGE={ON | OFF}]
            [, LIST]
```
- `CONTACT_GEOMETRY_LIBRARY`: `Parasolid` — precise but slower; `Default_library` — built-in (faster). **Must be set before simulation starts.**
- `CONTACT_FACETING_TOLERANCE=r`: Mesh resolution: `(1/r) * min_bbox_dimension`. Default: `300`. **Must be set before simulation starts.**
- `SIMFAIL`: `STOPCF` = halt ACF execution on failure; `NOSTOPCF` = continue ACF (default).
- `STATUS_MESSAGE={ON|OFF}`: Write `"Simulate status = i"` messages to `.msg` file. Default: `OFF`
- `LIST`: Print current PREFERENCES settings.

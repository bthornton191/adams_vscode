# Commands: Simulation

## SIMULATE
Specify the type, duration, and output resolution of the next analysis run.
```
SIMULATE [/ {DYNAMICS | KINEMATICS | STATICS | TRANSIENT | SETTLE}]
         [, {END=r | DURATION=r}]
         [, {STEPS=i | DTOUT=r}]
         [, INITIAL_CONDITIONS [{DISPLACEMENT | VELOCITY | ACCELERATION}]]
```
- `DYNAMICS`: Integrate equations of motion. Zero-DOF system triggers warning and uses kinematics.
- `KINEMATICS`: Kinematic analysis (zero-DOF required). Non-zero DOF → dynamic with warning.
- `STATICS`: Static equilibrium at current time (no END/STEPS) or quasi-static sweep (with END/STEPS).
- `TRANSIENT`: Kinematic if 0 DOF; dynamic if ≥1 DOF.
- `SETTLE`: Drive DIFF/GSE/LSE/TFSISO states to steady-state (all ẋ=0); time does not advance.
- `END=r`: Absolute end time. `END > current_time`. Mutually exclusive with `DURATION`.
- `DURATION=r`: Analysis duration relative to current time. `> 0`. Mutually exclusive with `END`.
- `STEPS=i`: Number of equally-spaced output steps. `≥ 1`. Mutually exclusive with `DTOUT`.
- `DTOUT=r`: Output step size in time units. `> 0`. Mutually exclusive with `STEPS`.
- `INITIAL_CONDITIONS`: Run IC analysis before simulation. Without qualifier: all three (displacement + velocity + acceleration). `DISPLACEMENT` — displacement IC only. `VELOCITY` — dispatch + velocity. `ACCELERATION` — all three.

> `END=1` at t=0 ends at t=1; `DURATION=1` at t=0.5 ends at t=1.5.

---

## LINEAR
Linearize the model to compute eigendata, state-space matrices, or export a Nastran deck.
```
LINEAR [/ {EIGENSOL | STATEMAT | MKB | EXPORT}]
       [, NODAMPIN] [, NOVECTOR]
       [, RM=id] [, PSTATE=id] [, PINPUT=id] [, POUTPUT=id]
       [, FILE=c] [, FORMAT={MATRIXX | MATLAB}]
       [, COORDS=i1[,i2]]   [, KINETIC=i1[,i2]]
       [, DISSIPAT=i1[,i2]] [, STRAIN=i1[,i2]]
       [, FCOORDS=r1,r2]    [, FKINETIC=r1,r2]
       [, MLIST=id1[,...]]  [, MRANGE=i1[,i2]]
       [, ENERGY_PER_MODE={ALL | m,n}]
       [, MASS_PER_MODE={ALL | m,n} [, MODAL_RM=id]]
       [, NAMES] [, TABLE_PRECISION=i]
       [, TYPE={CLOSEDBOX | OPENBOX}] [, CONFIG=c]
       [, ORIGINAL]
```
- `EIGENSOL`: Compute eigenvalues and mode shapes. Results to `.res` file. Requires `RESULTS/XRF` in dataset for Adams View post-processing.
- `STATEMAT`: Compute A, B, C, D matrices (`ẋ=Ax+Bu, y=Cx+Du`). `FILE` required. Default format: `MATRIXX`.
- `MKB`: Compute M, K, B (mass, stiffness, damping) matrices in Nastran-compatible form. `FILE` required.
- `EXPORT`: Export as Nastran bulk data deck. `FILE` and `TYPE` required.
- `NODAMPIN`: Suppress velocity-dependent terms from A matrix (eigenanalysis only).
- `NOVECTOR`: Eigenvalues only; skip mode shapes. Incompatible with `COORDS`/`KINETIC`/etc.
- `RM=id`: Reference marker for linearization state coordinates.
- `PINPUT=id`: PINPUT statement ID for B and D matrix computation.
- `POUTPUT=id`: POUTPUT statement ID for C and D matrix computation.
- `FILE=c`: Output filename (required for STATEMAT/MKB/EXPORT). Max 76 chars.
- `FORMAT`: `MATRIXX` = single FSAVE file (default); `MATLAB` = separate ASCII files.
- `COORDS=i1[,i2]`: Output coordinate table for modes i1 to i2.
- `KINETIC=i1[,i2]`: Kinetic energy distribution table for modes i1 to i2.
- `DISSIPAT=i1[,i2]`: Dissipative power table.
- `STRAIN=i1[,i2]`: Strain energy distribution table.
- `MASS_PER_MODE={ALL|m,n}`: Effective mass and modal participation factors per mode.
- `TYPE={CLOSEDBOX|OPENBOX}`: For EXPORT — `CLOSEDBOX` = DMIG cards; `OPENBOX` = element-by-element.
- `TABLE_PRECISION=i`: Significant digits in modal tables. Default: `2` (old format); `> 2` uses exponential.
- `ORIGINAL`: Use FORTRAN-compatible linearization (global Euler angles, no pre-reconcile).

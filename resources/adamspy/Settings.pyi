import Manager
import Object
from DatabaseIds import PreferenceIds as PreferenceIds
from collections.abc import Generator
from typing import Any

BUFFER_SIZE: Any
__asita__: str

class SessionPreferences(Object.ObjectSubBase):
    def __init__(self, _DBKey) -> None: ...
    general: GeneralPreferences
    single_run: SinglerunPreferences
    single_run_debugger: SinglerunDebuggerPreferences
    multi_run: MultirunPreferences
    optimization: OptimizationPreferences

class ModelSettings(Object.ObjectSubBase):
    advanced: Any
    def __init__(self, mod) -> None: ...
    integrator: Any
    linear_solver: Any
    kinematics: Any
    equilibrium: Any
    initial_conditions: Any
    contact: Any
    flex_body: Any
    debug: Any
    solver: Any
    output: Any

class AdvancedSettingManager(Manager.AdamsManager):
    def iterDBKeys(self) -> Generator[Any, None, None]: ...

class SinglerunPreferences(Object.ObjectSubBase):
    icon_visibility: Any
    time_delay: Any
    update_graphics: Any
    monitor: Any
    alert: Any
    save_analyses: Any
    analysis_prefix: Any

class GeneralPreferences(Object.ObjectSubBase):
    file_prefix: Any
    save_files: Any
    load_analysis: Any
    model_update: Any
    solver_preference: Any
    verify_first: Any
    hold_solver_license: Any
    user_solver_executable: Any
    show_all_messages: Any
    choice_for_solver: Any
    remote_compute: Any
    node_name: Any
    mdi_directory_remote: Any
    remote_directory: Any

class SinglerunDebuggerPreferences(Object.ObjectSubBase):
    iterations_per_step_measure: Any
    integrator_order_measure: Any
    static_imbalance_measure: Any
    step_size_measure: Any
    enable_debugger: Any
    track_maximum: Any
    show_table: Any
    highlight_objects: Any

class MultirunPreferences(Object.ObjectSubBase):
    save_analyses: Any
    load_analyses: Any
    analysis_prefix: Any
    save_curves: Any
    chart_design_objectives: Any
    chart_design_objective_variables: Any
    stop_on_error: Any
    show_summary: Any
    write_single_parasolid_file: Any

class OptimizationPreferences(Object.ObjectSubBase):
    algorithm: Any
    maximum_iterations: Any
    convergence_tolerance: Any
    differencing_technique: Any
    scaled_perturbation: Any
    user_parameters: Any
    rescale_iterations: Any
    slp_convergence_iter: Any
    debug: Any

class SolverSettings(Object.ObjectSubBase):
    threads: Any
    library_path: Any
    status_message: Any

class LinearSolverSettings(Object.ObjectSubBase):
    solver: Any
    stability: Any

class IntegratorSettings(Object.ObjectSubBase):
    def __init__(self, _DBKey) -> None: ...
    type: Any
    pattern: Any
    formulation: Any
    corrector: Any
    error: Any
    hinit: Any
    hmax: Any
    hmin: Any
    interpolate: Any
    maxit: Any
    kmax: Any
    alpha: Any
    beta: Any
    gamma: Any
    fixit: Any
    hratio: Any
    maxerror: Any

class KinematicsSettings(Object.ObjectSubBase):
    def __init__(self, _DBKey) -> None: ...
    apattern: Any
    pattern: Any
    aerror: Any
    error: Any
    alimit: Any
    tlimit: Any
    hmax: Any
    amaxit: Any
    maxit: Any

class InitialConditionsSettings(Object.ObjectSubBase):
    def __init__(self, _DBKey) -> None: ...
    aerror: Any
    error: Any
    alimit: Any
    tlimit: Any
    verror: Any
    amaxit: Any
    maxit: Any
    apattern: Any
    pattern: Any

class EquilibriumSettings(Object.ObjectSubBase):
    def __init__(self, _DBKey) -> None: ...
    alimit: Any
    error: Any
    imbalance: Any
    tlimit: Any
    stability: Any
    maxit: Any
    solver_method: Any
    atol: Any
    rtol: Any
    maxitl: Any
    etamax: Any
    eta: Any
    pattern: Any

class ContactSettings(Object.ObjectSubBase):
    def __init__(self, _DBKey) -> None: ...
    faceting_tolerance: Any
    geometry_library: Any

class FlexBodySettings(Object.ObjectSubBase):
    def __init__(self, _DBKey) -> None: ...
    limit_check: Any
    limit_action: Any
    formulation: Any

class DebugSettings(Object.ObjectSubBase):
    def __init__(self, _DBKey) -> None: ...
    debug: Any
    dump: Any
    eprint: Any
    verbose: Any
    reqdump: Any
    jmdump: Any
    rhsdump: Any
    dof: Any
    topology: Any

class AdvancedSetting(Object.ObjectSubBase):
    setting: Any
    value: Any
    deactivate: Any
    def destroy(self): ...

class OutputSettings(Object.ObjectSubBase):
    Femdatas: Any
    def __init__(self, _DBKey) -> None: ...
    stress: Any
    strain: Any

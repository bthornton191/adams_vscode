class AnalysisIds:
    gra_step_types: int
    res_step_types: int
    term_status: int

class AngleMeasureIds:
    comments: int
    create_measure_display: int
    first_point: int
    last_point: int
    legend: int
    middle_point: int

class AppearanceSettingsIds:
    active: int
    color: int
    icon_size: int
    name_visibility: int
    visibility: int

class CircularIds:
    cyl_radius: int
    cyl_thickness: int
    type: int

class ColorIds:
    components: int
    rgb: int

class ComputedMeasureIds:
    comments: int
    create_measure_display: int
    legend: int
    units: int

class ContactIds:
    coulomb_friction: int
    face_contact_bottom: int
    face_contact_top: int
    i_markers: int
    iedge_index: int
    iflip_geoms: int
    iflip_normals: int
    impact: int
    jedge_index: int
    jflip_geoms: int
    jflip_normals: int
    no_friction: int
    type: int

class CouplerConstraintIds:
    type_of_freedom: int

class DefaultIds:
    naming_references: int

class DesignVariableIds:
    delta_type: int
    object_value: int
    real_value: int
    sensitivity: int
    units: int
    use_allowed_values: int
    use_range: int

class DifferentialEquationIds:
    function: int

class EllipseIds:
    end_angle: int
    major_radius: int
    minor_radius: int
    start_angle: int

class ExternalIds:
    element: int
    faceting_tolerance: int
    file: int
    ref_marker_name: int
    rm: int
    solid_id: int

class FENodeIds:
    label: int

class FEPartIds:
    by_coordinates: int
    cratioM: int
    cratiok: int
    faceting_tolerance: int
    i_marker: int
    j_marker: int
    ref_curve: int
    type: int
    vm: int
    wm: int

class FeatureBlendIds:
    chamfer: int
    locations: int
    radius1: int
    radius2: int
    reference_marker: int

class FeatureHoleIds:
    countersink: int
    depth: int
    radius: int

class FeatureThinShellIds:
    locations: int
    thickness: int

class FemdataIds:
    criterion: int
    end: int
    fe_part: int
    file_name: int
    hotspots: int
    markers: int
    output_type: int
    radius: int
    skip: int
    start: int

class FlexBodyIds:
    generalized_damping: int
    mode_count: int
    node_count: int
    representation: int

class ForceVectorIds:
    x_force_function: int
    xyz_force_function: int
    y_force_function: int
    z_force_function: int

class FunctionMeasureIds:
    comments: int
    create_measure_display: int
    function: int
    legend: int
    routine: int
    units: int
    user_function: int

class GeneralConstraintIds:
    function: int

class GeneralForceIds:
    x_force_function: int
    x_torque_function: int
    xyz_force_function: int
    xyz_torque_function: int
    y_force_function: int
    y_torque_function: int
    z_force_function: int
    z_torque_function: int

class GeometryAppearanceSettingsIds:
    render: int
    transparency: int

class GeometryArcIds:
    close: int

class GeometryChainIds:
    adams_id: int
    comments: int
    object_in_chain: int

class GeometryCsgIds:
    adams_id: int
    comments: int
    solid1: int
    solid2: int
    type: int

class GeometryEllipseIds:
    adams_id: int
    cm: int
    comments: int
    end_angle: int
    major_radius: int
    minor_radius: int
    start_angle: int

class GeometryExtrusionIds:
    path: int
    profile: int

class GeometryGContactIds:
    adams_id: int
    comments: int
    contact_element_name: int
    force_display: int

class GeometryLinkIds:
    adams_id: int
    comments: int
    depth: int
    i_marker: int
    j_marker: int
    width: int

class GeometryNurbCurveIds:
    comments: int
    control_points: int
    degree: int
    knots: int
    periodic: int
    rational: int
    weights: int

class GeometryPlateIds:
    comments: int
    markers: int
    radius: int
    width: int

class GeometryPolylineIds:
    adams_id: int
    close: int
    comments: int
    points: int

class GeometryRevolutionIds:
    number_of_sides: int

class GeometrySheetIds:
    sheet_id: int

class GeometryShellIds:
    comments: int
    connections: int
    file: int
    points: int
    reference_marker: int
    scale_factor: int
    wireframe_only: int

class GeometrySolidIds:
    solid_id: int

class GroupIds:
    comments: int

class IBeamIds:
    ib_base: int
    ib_flange: int
    ib_height: int
    ib_web: int

class JointIds:
    type: int

class JointMotionIds:
    function: int
    type_of_freedom: int

class JprimIds:
    type: int

class MarkerIds:
    external_id: int
    external_id_loc: int
    external_id_ori: int

class MatrixIds:
    units: int

class MeasureIds:
    adams_id: int

class ModalForceIds:
    scale: int

class ObjectMeasureIds:
    characteristic: int
    comments: int
    component: int
    coordinate_rframe: int
    create_measure_display: int
    legend: int
    motion_rframe: int
    obj: int

class OrientMeasureIds:
    characteristic: int
    comments: int
    component: int
    create_measure_display: int
    from_frame: int
    legend: int
    to_frame: int

class OutputSettingsIds:
    output_strain: int
    output_stress: int

class PointMassIds:
    density: int

class PointMeasureIds:
    characteristic: int
    comments: int
    component: int
    coordinate_rframe: int
    create_measure_display: int
    legend: int
    motion_rframe: int
    point: int

class PointMotionIds:
    function: int
    type: int

class PreferenceIds:
    ic_aerror: int

class Pt2ptMeasureIds:
    characteristic: int
    comments: int
    component: int
    coordinate_rframe: int
    create_measure_display: int
    from_point: int
    legend: int
    motion_rframe: int
    to_point: int

class RangeMeasureIds:
    comments: int
    create_measure_display: int
    legend: int
    of_measure_name: int
    type: int

class RectangularIds:
    rect_base: int
    rect_height: int
    rect_thickness: int
    type: int

class RigidBodyIds:
    density: int
    planar_axes: int

class SectionIds:
    area: int
    autoCalculate: int
    iyy: int
    iyz: int
    izz: int
    jxx: int
    moments: int

class SensorIds:
    angular: int
    angular_error: int
    angular_value: int
    codgen: int
    dt: int
    flags: int
    func: int
    halt: int
    id: int
    restart: int
    stepsize: int
    yydump: int

class SimulationIds:
    commands: int
    comments: int
    duration: int
    end_time: int
    initial_static: int
    number_of_steps: int
    script_type: int
    sim_script_name: int
    solver_commands: int
    step_size: int
    type: int

class SimulationPreferenceIds:
    alert: int
    assoc: int
    chart_objectives: int
    chart_variables: int
    directory_remote: int
    enable_debugger: int
    file_prefix: int
    highlight_objects: int
    hold_solver_license: int
    icon_visibility: int
    integrator_order_measure: int
    iterations_per_step_measure: int
    load_analysis: int
    m_analysis_prefix: int
    m_load_analyses: int
    m_save_analyses: int
    mdi_directory_remote: int
    model_update: int
    monitor: int
    name: int
    node_name: int
    opt_algorithm: int
    opt_convergence_tolerance: int
    opt_debug: int
    opt_differencing_technique: int
    opt_maximum_iterations: int
    opt_rescale_iterations: int
    opt_scaled_perturbation: int
    opt_slp_convergence_iter: int
    opt_user_parameters: int
    parent: int
    remote_compute: int
    s_analysis_prefix: int
    s_save_analyses: int
    save_curves: int
    save_files: int
    show_all_messages: int
    show_summary: int
    show_table: int
    sim_pref_name: int
    solver_preference: int
    static_imbalance_measure: int
    step_size_measure: int
    stop_on_error: int
    time_delay: int
    track_model_element: int
    update: int
    user_solver_executable: int
    verify_first: int
    write_single_parasolid_file: int

class SingleComponentForceIds:
    function: int
    translation: int
    translational: int

class SplineIds:
    units: int
    x_units: int
    xs: int
    y_units: int
    ys: int
    z_units: int
    zs: int

class StateVariableIds:
    function: int

class TorqueVectorIds:
    x_torque_function: int
    xyz_torque_function: int
    y_torque_function: int
    z_torque_function: int

class UserDefinedElementIds:
    assoc: int
    definition_name: int
    input_parameters: int
    isa: int
    objects: int
    output_parameters: int
    parameters: int
    udedef_name: int

class UserDefinedInstanceIds:
    input_parameters: int
    instance_name: int
    location: int
    objects: int
    orientation: int
    output_parameters: int
    parameters: int
    relative_to: int
    udedef: int
    udeinst_name: int

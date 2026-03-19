# measure create object

Creates an object measure.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `measure_name` | New point measure | Specifies the name of the new point measure. You can use this name later to refer to this measure. |
| `component` | X_COMPONENT, Y_COMPONENT, Z_COMPONENT, MAG_COMPONENT, R_COMPONENT, RHO_COMPONENT, THETA_COMPONENT, PHI_COMPONENT | Specifies the component in which you are interested. The components available depend on the coordinate system. |
| `motion_rframe` | Existing marker | Specifies existing marker |
| `coordinate_rframe` | Existing marker | Specifies existing marker |
| `characteristic` | ANGULAR_ACCELERATION, ANGULAR_DEFORMATION, ANGULAR_DEFORMATION_VELOCITY, ANGULAR_KINETIC_ENERGY, ANGULAR_MOMENTUM_ABOUT_CM, ANGULAR_VELOCITY, AX_AY_AZ_PROJECTION_ANGLES, CM_ACCELERATION, CM_ANGULAR_ACCELERATION, CM_ANGULAR_DISPLACEMENT, EULER_ANGLES, CM_ANGULAR_VELOCITY, CM_POSITION, CM_POSITION_RELATIVE_TO_BODY, CM_VELOCITY, CONTACT_POINT_LOCATION, ELEMENT_FORCE, ELEMENT_TORQUE, INTEGRATOR_ORDER, INTEGRATOR_STEPSIZE, INTEGRATOR_TIME_STEP, ITERATOR_STEPS, ITERATION_COUNT, KINETIC_ENERGY, POTENTIAL_ENERGY_DELTA, POWER_CONSUMPTION, PRESSURE_ANGLE, STATIC_IMBALANCE, STRAIN_KINETIC_ENERGY, TRANSLATIONAL_ACCELERATION, TRANSLATIONAL_DEFORMATION, TRANSLATIONAL_DEFORMATION_VELOCITY, TRANSLATIONAL_DISPLACEMENT, TRANSLATIONAL_KINETIC_ENERGY, TRANSLATIONAL_MOMENTUM, TRANSLATIONAL_VELOCITY | Specifies the object characteristic to be measured. |
| `object` | Existing object in Adams | Enter the object to measure. |
| `legend` | String | Specifies the text that will appear in the top of the measure window. |
| `comments` | String | Specifies any comments on this measure. |
| `create_measure_display` | Yes/No | Specifies yes if you want to display a strip chart of the measure. |

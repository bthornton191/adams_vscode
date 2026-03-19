# highlight

The HIGHLIGHT command changes the appearance of an object, so that you can see its position in the model. Optionally, you can also see the other entities it depends upon or which depend on it.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `marker_name` | Existing Marker | Specifies the name of the marker to be highlighted |
| `geometry_name` | Existing Geometric Entity | Specifies the name of the geometric object to be highlighted. The geometric element may be one of OUTLINE, ARC, CIRCLE, BSPLINE, BLOCK, CYLINDER, FRUSTUM, SPRING_DAMPER, or FORCE. |
| `part_name` | Existing Body | Specifies the name of the part to be highlighted. |
| `constraint_name` | Existing Constraint | Specifies the name of the constraint object to be highlighted. The constraint element may be one of JOINT, JOINT_PRIMITIVE, HIGHER_PAIR_CONTACT, MOTION_GENERATOR, or USER_DEFINED. |
| `force_name` | Existing Force | Specifies the name of the force object to be highlighted. The force element may be one of BEAM, BUSHING, FIELD, TRANSLATIONAL_SPRING_DAMPER, ROTATIONAL_SPRING_DAMPER, TIRE, SINGLE_COMPONENT_FORCE, FORCE_VECTOR, TORQUE_VECTOR, GENERAL_FORCE, or MULTI_POINT_FORCE. |
| `color` | Existing Color | Specifies what COLOR an object should be changed to, when it is highlighted. |
| `line_type` | Solid, Dash, Dotdash, Dot, None | Specifies the selection for the LINE_TYPE for the object or objects being highlighted. |
| `time_delay` | Real | The TIME_DELAY parameter is used to specify the number of seconds to temporarily halt command processing. Command processing will resume after the specified number of seconds has elapsed or when the user types any character on the keyboard or makes a pick with the mouse in the Adams View window. |
| `entity` | Self, Dependents, Referents, Parts, All | Specifies which entities related to the selected object are to be highlighted. |

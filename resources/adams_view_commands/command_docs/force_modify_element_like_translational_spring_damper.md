# force modify element_like translational_spring_damper

Allows modification of the translational spring damper object.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `spring_damper_name` | An Existing Spring-damper Force | Specifies the spring-damper force to modify. You use this parameter to identify the existing spring-damper to affect with this command. |
| `new_spring_damper_name` | A New Spring-damper Force | Specifies the name of the new spring-damper force. You may use this name later to refer to this spring-damper.Adams View will not allow you to have two spring-dampers with the same full name, so you must provide a unique name. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `damping` | Damping | Specifies the viscous damping coefficient for the spring damper. |
| `stiffness` | Stiffness | Specifies the spring stiffness coefficient for the spring damper. |
| `preload` | Force | Specifies the reference force or torque for the spring. This is the force the spring exerts when the displacement between the I and J markers is equal toDISPLACEMENT_AT_PRELOAD (the reference length of the spring). |
| `displacement_at_preload` | Length | Specifies the reference length for the spring. If PRELOAD (the reference force of the spring) is zero, DISPLACEMENT_AT_PRELOAD equals the free length |
| `i_marker_name` | An Existing Marker | Specifies a marker on the first of two parts connected by this force element. Adams View connects this element to one part at the I marker and to the other at the J marker. |
| `j_marker_name` | An Existing Marker | Specifies a marker on the second of two parts connected by this force element. Adams View connects this element to one part at the I marker and to the other at the J marker. |

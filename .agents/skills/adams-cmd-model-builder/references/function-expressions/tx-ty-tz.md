# TX / TY / TZ — Applied Torque Components

Return a single Cartesian component (x, y, or z) of the net torque applied between two markers.

> **3rd argument is "About Marker"** — distinguishes these from FX/FY/FZ whose 3rd argument is "Along Marker". Torques act *about* an axis; forces act *along* an axis.

## Formats

```
TX(Applied To Marker, Applied From Marker, About Marker)
TY(Applied To Marker, Applied From Marker, About Marker)
TZ(Applied To Marker, Applied From Marker, About Marker)
```

## Arguments

| Argument | Req | Description |
|----------|-----|-------------|
| `Applied To Marker` | Required | Marker at which the torque is applied (I marker) |
| `Applied From Marker` | Optional | J marker (reaction point); if omitted, returns action-only torques at Applied To |
| `About Marker` | Optional | Marker whose x/y/z axis defines the torque component; defaults to global x/y/z |

## Examples

```adams_fn
! Torque about the Z-axis of a revolute joint
TZ(.MODEL.ARM.pin_mkr, .MODEL.ground.pivot_mkr, .MODEL.ground.pivot_mkr)

! Torque about a part's own local y-axis
TY(.MODEL.BODY.i_mkr, .MODEL.BASE.j_mkr, .MODEL.BODY.i_mkr)

! Torque feedback in a control variable
data_element create variable &
    variable_name = .MODEL.VAR_TORQUE &
    function = "TZ(.MODEL.ARM.pin_mkr)"
```

## Key argument naming difference

| Function family | 3rd argument | Intuition |
|-----------------|-------------|-----------|
| FX/FY/FZ | `Along Marker` | Force is applied *along* a line/axis |
| TX/TY/TZ | `About Marker` | Torque is applied *about* an axis |

## Notes

- TX/TY/TZ are **output functions** that read back torques already applied by force/torque elements.
- Returns a signed value; positive follows the right-hand rule about the specified axis.

## See also

- [FX / FY / FZ](fx-fy-fz.md) — force components (3rd arg = "**Along** Marker")
- [WX / WY / WZ](wx-wy-wz.md) — angular velocity (3rd arg also "**About** Marker")

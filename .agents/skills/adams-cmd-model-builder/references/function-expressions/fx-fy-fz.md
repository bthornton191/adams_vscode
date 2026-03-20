# FX / FY / FZ — Applied Force Components

Return a single Cartesian component (x, y, or z) of the net translational force applied between two markers.

> **3rd argument is "Along Marker"** — distinguishes these from TX/TY/TZ whose 3rd argument is "About Marker".

## Formats

```
FX(Applied To Marker, Applied From Marker, Along Marker)
FY(Applied To Marker, Applied From Marker, Along Marker)
FZ(Applied To Marker, Applied From Marker, Along Marker)
```

## Arguments

| Argument | Req | Description |
|----------|-----|-------------|
| `Applied To Marker` | Required | Marker at which the force is applied (I marker) |
| `Applied From Marker` | Optional | J marker (reaction point); if omitted, returns action-only forces at Applied To |
| `Along Marker` | Optional | Marker whose x/y/z axis defines the component direction; defaults to global x/y/z |

## Examples

```adams_fn
! Z-component of the force at JOINT_1's I marker, in global frame
FZ(.MODEL.LINK.pin_mkr, .MODEL.ground.base_mkr)

! Force component along the local axis of BODY
FX(.MODEL.BODY.i_mkr, .MODEL.BASE.j_mkr, .MODEL.BODY.i_mkr)

! Use measured force in a dependent variable
data_element create variable &
    variable_name = .MODEL.VAR_FZ &
    function = "FZ(.MODEL.BODY.CM, .MODEL.ground.ORIGIN)"
```

## Notes

- FX/FY/FZ are **output functions** — they read back forces already applied by force elements. They cannot be used to *apply* a force without also referencing the element.
- Used in `FUNCTION=` parameters of variable elements, force outputs, and Sensor triggers.
- Returns signed value; direction follows the axis of the Along Marker.

## See also

- [TX / TY / TZ](tx-ty-tz.md) — torque components (3rd arg = "**About** Marker")
- [VM](vm.md) — velocity magnitude

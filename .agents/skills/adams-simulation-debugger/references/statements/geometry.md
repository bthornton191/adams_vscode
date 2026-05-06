# Statements: Geometry (MARKER, GRAPHICS)

## MARKER
Defines a coordinate frame fixed to a part; the primary geometric primitive for all connections.
```
MARKER/id, PART=part_id,                                       &
    [QP=x,y,z], [REULER=psi,theta,phi],                        &
    [FLOATING] [, ZP=x,y,z] [, XP=x,y,z]                      &
    [, LABEL=c]
```
- QP: position in parent-part reference frame (or global frame for GROUND-based markers)
- REULER: Euler angles (Z-X-Z body-fixed, `ψ θ φ`) defining marker orientation
- ZP / XP: alternative orientation — specify a point on the Z-axis and a point in the XZ-plane
- FLOATING: marker is not fixed to a part body; solver repositions it to satisfy a geometric constraint (used by PTCV, CVCV, SURFACE contacts)
- Marker 0 is the global origin / GROUND frame and cannot be redefined

## GRAPHICS
Defines visual geometry attached to a part (does not affect dynamics).
```
GRAPHICS/id, PART=part_id,                                     &
    {BOX, CORNER=marker_id, X=r, Y=r, Z=r |                    &
     CYLINDER, CM=marker_id, LENGTH=r, RADIUS=r [, SIDES=i] |  &
     SPHERE, CENTER=marker_id, RADIUS=r [, SEG=i] |            &
     ELLIPSOID, CM=marker_id, XSCALE=r, YSCALE=r, ZSCALE=r |   &
     LINK, I=marker_id, J=marker_id, WIDTH=r, DEPTH=r |        &
     PLATE, CORNER=marker_id, WIDTH=r, DEPTH=r, THICKNESS=r |  &
     FRUSTUM, CM=marker_id, TOP=r, BOTTOM=r, LENGTH=r |        &
     TORUS, CM=marker_id, MINOR_RADIUS=r, MAJOR_RADIUS=r |     &
     CURVE, CURVE=curve_id, SEG=i |                             &
     OUTLINE, POINTS=marker_id1,...}                            &
    [, LABEL=c]
```
- CORNER marker defines origin corner for BOX; CM marker used as reference origin for other shapes
- LINK: creates a rounded-box shape connecting markers I and J — useful for visualizing rigid links
- OUTLINE: draws a polyline through the listed markers (wire-frame shapes, no fill)
- Graphics only affect visualisation; errors in this statement do not usually prevent simulation

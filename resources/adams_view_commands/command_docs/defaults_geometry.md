# defaults geometry

The DEFAULTS GEOMETRY command assigns a value to following DEFAULTS GEOMETRY_PARAMETERS.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `curvechordtolerancescale` | Real value | Curve chord tolerance scale is the multiplying factor for the curve chord tolerance. Curve chord tolerance is the maximum chordal distance between a facet edge and its original edge entity.The default value is 0.3If the curve chord tolerance scale is less than 0.3, the tessellation will be finer. A value greater than 0.3 will result in a coarser tessellation. |
| `curvechordangle` | Real value | Curve chord angle is the maximum angle (always in radians, irrespective of model units) which is permitted between a facet chord and its original edge entity.The default is 0.26 (that is 15 deg) which means a value will be automatically set by Adams if it is not explicitly set by the user. Lesser curve chord angle will result in a finer tessellation. Greater angle will result in a coarser tessellation. |
| `surfaceplanetolerancescale` | Real value | Surface plane tolerance scale is the multiplying factor for the surface plane tolerance. Surface plane tolerance is the maximum distance between the mid-plane of a facet and its original face entity.The default value is 0.3. If the surface plane tolerance scale is less than 0.3, the tessellation will be finer. A value greater than 0.3 will result in a coarser tessellation. |
| `surfaceplaneangle` | Real value | Surface plane angle is the maximum angle (always in radians, irrespective of model units) which is permitted between the surface normal at any two positions on the surface which lie within the facet boundary. The default is 0.26 (that is 15 deg) which means a value will be automatically set by Adams if it is not explicitly set by the user.Lesser surface plane angle will result in a finer tessellation. Greater angle will result in a coarser tessellation. |

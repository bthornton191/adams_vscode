# geometry modify curve bspline

Allows you to modify an existing bspline.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `bspline_name` | An Existing Gcurve | Specifies the name of an existing BSPLINE to modify |
| `new_bspline_name` | A New Gcurve | Specifies the name of the new BSPLINE. |
| `adams_id` | Adams_id | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `ref_curve_name` | An Existing Acurve | Specifies an existing CURVE that will be used to create and display the BSPLINE geometric element. |
| `ref_marker_name` | An Existing Marker | Specifies an existing MARKER that will be used to locate and orient the BSPLINE geometric element. |
| `ref_profile_name` | An Existing Wire Geometry | Specifies an existing GWire geometry, from which to create and display the BSPLINE geometric element. |
| `spread_points` | Boolean | Specifies whether the bspline be created in a way that the points (as defined by a reference profile) are equally spaced or otherwise. The parameter will be ignored if a ref_curve_name is specified. |
| `closed` | Boolean | Specifies whether that the generated bspline is a closed one or otherwise. |
| `num_new_pts` | Integer | Specifies the number of points on the created bspline. The parameter is valid only if the spread_points parameter is set to 'yes' (and as such can be valid only when a reference profile is specified). |
| `segment_count` | Integer | Specifies the number of polynomial segments Adams View uses for fitting the CURVE_POINTS when FIT_TYPE is set to CURVE_POINTS. |

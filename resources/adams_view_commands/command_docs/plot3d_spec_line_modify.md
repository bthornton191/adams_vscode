# plot3d spec_line modify

Allows you to modify a spec line.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `spec_line_name` | A New Spec_line | Specifies a name for the spec line. A string of characters that identifies a spec line. Spec line names are assigned when spec lines are created. After a spec line has been created, you can reference it by its name until it is deleted. A spec line on the same plot cannot have the same name as another spec line. |
| `line_type` | Line_style | This parameter allows the selection of the line type for a spec line. The line type describes how the line will look when displayed on a plot. |
| `color` | An Existing Color | Specifies the color of the spec line. |
| `thickness` | Real | This parameter allows the specification of the thickness of the curve. |
| `start_point` | Location | x,y,z location of spec line start point. |
| `end_point` | Location | x,y,z location of spec line end point. |

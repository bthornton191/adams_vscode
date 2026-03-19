# geometry modify curve outline

Allows for modification of an existing outline object.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `outline_name` | An Existing Outline | Specifies the name of an existing outline |
| `new_outline_name` | A New Outline | Specifies the name of a new outline |
| `adams_id` | Adams_id | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `marker_name` | An Existing Marker | Specifies the marker associated with this entity. |
| `visibility_between_markers` | On_off | Specifies whether the outline is visible between two markers. |
| `image_file_name` | String | Specifies the name of an image file on disk. File types supported include .bmp, .jpg, .gif, and .png. |
| `horizontal` | Clamp_repeat | Controls how the desired polygon is horizontally filled with the image |
| `vertical` | Clamp_repeat | Controls how the desired polygon is vertically filled with the image |
| `close` | Boolean | Specifies the whether or not Adams View should close the outline when it is created. |

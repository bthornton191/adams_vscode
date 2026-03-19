# notes modify

Allows you to modify an existing note.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `note_name` | Existing Note | Specifies the name of an existing note. |
| `new_note_name` | New Note | Specifies the new name of the note |
| `text` | String | Specifies the text string(s) that will comprise the note text. |
| `location` | Location | Specifies the location to be used to define the note. |
| `pick` | Pick Location | Specifies a position in a view by picking with the mouse or pen. |
| `screen_coords` | Real | Specifies an x,y location in a view on the Adams View screen. SCREEN_COORDS refers to a coordinate reference tied to the terminal screen. |
| `size` | Integer | Specifies the size, in modeling units, that the note height will appear in. The width of each character in the note is approximately 60% of the height. |
| `unitless_size` | Real | Specifies a real number |
| `point_size` | Integer | Specifies an integer to define the point size |
| `bitmapped_text` | On, Off | Specifies whether or not a note is to be drawn using bitmapped text. |
| `leader_line` | Location | Specifies the screen locations which define a leader line for a note. |
| `arrow_visibility` | On, Off | Specifies whether there should be an arrow head at the last point on the leader line of the note. |
| `arrow_size` | Real | Specifies the size, in modeling units, that the arrow head of the leader line on the note will appear. If arrow_size has not been set, or it is set to zero the arrowhead will be roughly the size of the text in the note. |
| `user_text` | On, Off | Specifies on or off. |
| `user_location` | On, Off | Specifies on or off. |
| `rotation` | Real | This parameter specifies the rotations (about to the global origin) that are applied to the parts, polylines, and notes beneath the source model before it is merged with the destination model. The source model will not be changed after the merge operation. |
| `alignment` | Left, Center, Right | Specifies the alignment of the text in the note. |

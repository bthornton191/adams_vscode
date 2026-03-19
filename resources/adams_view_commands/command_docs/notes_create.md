# notes create

Allows you to create a note, with an optional leader line.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `note_name` | New Note | Specifies the name of the new note.You may use this name later to refer to this note. |
| `text` | String | Specifies the text string(s) that will comprise the note text. |
| `location` | Location | Specifies the location to be used to define the note. The location coordinates for plot notes in Adams PostProcessor do not relate to the plot coordinates themselves. They are unfortunately difficult to predict since they depend strongly upon a number of factors including plot aspect ratio, visibility of the title, sub-title and axis labels, Viewport orientation and so on. This is why the direct interactive placement is preferred. Users who really want to script the creation of plot notes are advised to, from the command navigator dialog, use the interactive pick option to fill the location fields. This allows one to see the location coordinates used behind the scenes. |
| `pick` | Pick Location | Specifies a position in a view by picking with the mouse or pen. |
| `screen_coords` | Real | Specifies an x,y location in a view on the Adams View screen. SCREEN_COORDS refers to a coordinate reference tied to the terminal screen. |
| `size` | Integer | Specifies the size, in modeling units, that the note height will appear in. The width of each character in the note is approximately 60%of the height. |
| `unitless_size` | Real | Specifies a real number |
| `point_size` | Integer | Specifies an integer to define the point size |
| `bitmapped_text` | On, Off | Specifies whether or not a note is to be drawn using bitmapped text. |
| `leader_line` | Location | Specifies the screen locations which define a leader line for a note. |
| `arrow_visibility` | On, Off | Specifies whether there should be an arrow head at the last point on the leader line of the note. |
| `arrow_size` | Real | Specifies the size, in modeling units, that the arrow head of the leader line on the note will appear. If arrow_size has not been set, or it is set to zero, the arrowhead will be roughly the size of the text in the note. |
| `user_text` | On, Off | Specifies on or off. |

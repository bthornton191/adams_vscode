# file html write

Allows you to export the Adams PostProcessor data in the current session of Adams PostProcessor as an HTML report for viewing by others in your organization.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `file_name` | File name | Specifies the name of the top-level file that is to be written. |
| `output_directory` | String | Specifies where you want the resulting HTML files and folders to be stored. This directory may not exist yet. |
| `title` | String | Specifies a title for the published data. It will be used as the title in the top HTML file, and appear on the title page. |
| `author` | String | Specifies the author of the data. It will appear on the title page. |
| `date` | Date | Specifies the date the data was published. It will appear on the title page. |
| `comment` | String | Specifies any comments about the data. It will appear on the title page. |
| `model_names` | Existing model | Specifies the models for which you want to export information. |
| `page_name` | Existing page | Specifies the pages of plots and animations you want exported. |
| `title_image_file_name` | File | Specifies the path and file of an image to appear in the upper right corner. |
| `image_width` | Integer | Enter the pixel size width of the exported pages. |
| `image_height` | Integer | Enter the pixel size height of the exported pages. |
| `image_format` | Png/jpg | For the pages of plots, enter the image format in which to store the pages of plots. |
| `movie_format` | Png/ jpg/ avi/mpg. | Specifies the type of movie to export the animation as. (AVI format is only available on Windows.) |
| `export_animations` | Yes/No | Values are: |
| `avi_frames_per_second` | Integer | If you select compressed AVI format, set the frame rate. The default is a frame rate of 10 seconds per frame. |
| `avi_compression` | Yes/no | Specifies whether or not to compress an AVI file. Values are: yes and no. The default is yes. |
| `avi_quality` | Integer | Specifies quality as a percent_integer from 1 to 100. Larger the number, better the quality and larger the AVI file. The default is 75% compression. |
| `avi_keyframe_every` | Integer | Indicates how often a complete frame (keyframe) is written to the AVI file; the smaller the number, the larger the file. The default is each key frame 500 frames apart. |
| `mpeg_ngop` | Integer | Indicates how often a complete frame (keyframe) is written to the MPEG file |
| `mpeg_round_size` | Yes/no | Some playback programs require the pixel height and width to be multiplies of 16. Set this option to yes to ensure that your movie plays in many playback programs. |
| `include_points` | Yes/No | Specifies whether Points information needs to be included in the HTML report |
| `include_markers` | Yes/No | Specifies whether Marker information needs to be included in the HTML report |

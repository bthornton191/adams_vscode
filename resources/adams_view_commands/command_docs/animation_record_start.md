# animation record start

Allows you to record the animation. The video file is saved in the current working directory.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `image_prefix` | String | Set the prefix used to name the set of files. |
| `image_type` | String | Select the format: .avi, .tif, .jpg, .bmp, .mpg, .png, and .xpm |
| `avi_frames_per_sec` | Integer | Enter the number of frames per second used in the recording. |
| `avi_compression` | Boolean | Enters yes or no depending on whether or not the avi needs to be compressed. |
| `avi_quality` | Integer | Enters a value or use the slider to set the image quality. |
| `avi_keyframe_every` | Integer | Sets the interval between key frames. The default is a key frame every 5000 frames. |
| `mpeg_ngop` | Integer | "1" is the same as not using "Compress using P Frames", and setting it to "12" means using "Compress using P Frames". Turn off the compression using P frames to ensure your movie plays in many playback programs, including xanim. It results, however, in a much larger file (up to 4 times as large). |
| `mpeg_round_size` | Boolean | Specifies yes or no if size is to be rounded to multiples of 16. |
| `window_size` | Integer | Enters an integer number to specify window size. |

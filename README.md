# ASL - AnimeSceneLabel
Generate tags for the content of scenes in anime videos.
It generates a thumbnail from each scene of the video, uses DeepDanbooru to generate tags for the contents of each thumbnail, and outputs to a .csv file.

## Requirements
`pip install -r requirements.txt`

## Usage
`python animescenelabel.py input -o output_folder -k`

```
positional arguments:
  input              a video file or a folder containing video files

options:
  -h, --help         show this help message and exit
  -o, --output       specify a directory to save outputs to
  -k, --keep-thumbs  keep generated thumbnails in a folder named after each video file
  ```
Thumbnails are saved at a fixed resolution of 512x512, because this is the input size needed by DeepDanbooru.
If an output directory is not specified, files will be saved in the same location as the input video.
If you provide a folder as the input, it will process all videos in the folder.

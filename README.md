# ASL - AnimeSceneLabel
Generate tags for the content of scenes in anime videos.
<br>It generates a thumbnail from each scene of the video, uses DeepDanbooru to generate tags for the contents of each thumbnail, and outputs to a .csv file.

## Requirements
`Python` (version 3.7 is probably the minimum version supported)

Install requirements by downloading the requirements.txt file and running this command:
<br>`pip install -r requirements.txt`

## Usage
Download the animescenelabel.py file and run it as follows:
<br>`python animescenelabel.py input -o output_folder -k`

```
positional arguments:
  input              a video file or a folder containing video files

options:
  -o, --output       specify a directory to save outputs to
  -k, --keep-thumbs  keep generated thumbnails in a folder named after each video file
  ```
Thumbnails are saved at a fixed resolution of 512x512, because this is the input size needed by DeepDanbooru.
<br>If an output directory is not specified, files will be saved in the same location as the input video.
<br>If you provide a folder as the input, it will process all videos in the folder.

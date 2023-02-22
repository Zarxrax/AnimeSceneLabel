# SceneLabel
Generate descriptions of scenes from video files.

It generates a thumbnail from each scene of the video, generates a description of the thumbnail content, and outputs to a .csv file.

It currently only uses DeepDanbooru, so only works for anime content. I am hoping to also add support for CLIP interrogator.

## Requirements
`pip install -r requirements.txt`

## Usage
`python scenelabel.py input -k`

```
positional arguments:
  input              a video file or a folder containing video files

options:
  -h, --help         show this help message and exit
  -k, --keep-thumbs  keep generated thumbnails in a folder named after each video file
  ```

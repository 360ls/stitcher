## Realtime 360 Stitcher

## Pre-requisites
- Python 2.7
- OpenCV 2.4
- At least 2 cameras

Install dependencies:
```bash
pip install -r requirements.txt
```

Generate the setup profile:

```bash
python configure.py
``` 

## Stitching Video from Cameras

```bash
python run.py
```
This will bring up two streams coming from the cameras and the combined stream.
To stop the program, make sure one of the stream windows is selected
and press `q`.

## Stitching Local Images
Make sure that the images are in the directory specified in the `source_dir` 
field in `profile.yml`. Then run the following command:

```bash
python run.py -l
```

The resulting stitched image will be stored in the directory specified in the
`dest_dir` field in `profile.yml`.

## Stitching from Local Videos
Make sure that the video paths are specified in the `left-video` and `right-video` fields in `profile.yml`. Then run the following command:

```bash
python run.py -v
```

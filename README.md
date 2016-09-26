## Realtime 360 Stitcher

## Pre-requisites
- Python 2.7
- OpenCV 2.4
- 2+ USB Cameras

Install dependencies:
```bash
pip install -r requirements.txt
```

## Setup
Generate the setup profile:

```bash
python configure.py
``` 

Make sure images are in the `data/sources` directory and the videos are in the `data/videos` directory

## Running

```bash
python run.py
```

This will start the CLI with the following options.

1. Stitching Videos from Cameras
2. Stitching Local Images
3. Stitching from Local Videos

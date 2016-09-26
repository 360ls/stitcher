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

## Running
Make sure that the configuration script has been run.

```bash
python run.py
```

This will start the CLI with the following options.
1. Stitching Videos from Cameras
2. Stitching Local Images
3. Stitching from Local Videos

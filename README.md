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

```bash
python run.py
```
This will bring up two streams coming from the cameras and the combined stream.
To stop the program, make sure one of the stream windows is selected
and press `q`.

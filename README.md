# stitch-flex
Demonstrates flexible stitching for an incoming array of cameras.
[![Build Status](https://travis-ci.org/360ls/stitch-flex.svg?branch=master)](https://travis-ci.org/360ls/stitch-flex)

## Production

### To install the package:

```bash
$ make install
```

This will install package dependencies via npm (node.js) and pip (python), including the yarn package manager dependency.

### Then, to run the app, either:

```bash
$ make run
```
to simply run the app

OR

```bash
$ make
```

to clean the package, do a fresh (but not brand new) install of dependencies, and then run the app.

### To run the cli:
```bash
$ make cli
```

## Demoing

### To set up the camera streams
```bash
$ make camera-setup
```

### To demonstrate threading through taking snapshots
```bash
$ make snap
```

## Development

### To lint the application:

```bash
$ make lint-py
```

### To run tests against the application:

```bash
make test
```

You can also install packages in a text editor like Sublime Text 3 to show linting in real-time. This can be done for both eslint (JS) and pylint (Python)

## Package Structure
```bash
stitch-flex
    .gitignore
    .travis.yml
    conftest.py
    LICENSE
    Makefile
    package.json
    README.md
    app/
        __init__.py
        __init__.pyc
        cli.py
        electronapp.py
        stitcher/
            __init__.py
            stitch.py
            __pycache__/
            core/
                __init__.py
                feedhandler.py
                stitcher.py
            correction/
                __init__.py corrector.py
            flex/
                __init__.py
                detector.py
                flexor.py
        storage/
   
            uncorrected.mp4
            uncorrected.png
            uncorrected_checker.jpg
            calibration_inputs/
            flex/
            stitch_tester/
            syncedvideos/
       
                cam1/
                    unused/
                cam2/
                    unused/
                cam3/
                cam4/
                    unused/
        test/
            nocv/
                __init__.py
                test_inputscanner.py
                __pycache__/
            opencv/
                __init__.py
                test_feed.py
                __pycache__/
        util/
            __init__.py
            __init__.pyc
            calibrate.py
            capture.py
            feed.py
            fpschecker.py
            inputscanner.py
            listfiles.py
            textformatter.py
            validatefeeds.py
    config/
        .pylintrc
        requirements.txt
    out/
        captured_frames/
        captured_videos/
    output/
```

## Future Target Functionality
1. The ability to add different car configurations for adaptive stitching

2. Ability to add and remove cameras to and from stitch on the go

3. Add and remove a camera seamlessly when cameras are in a row

4. Be able to determine camera order via homography

5. Addition of better frame error handling

6. Limit keypoint identification to a specific side of the image to limit the computation time and complexity of homography calculation.

7. Resize frames during stitch to get rid of extra flange warping.

8. The ability to determine configuration based on available cameras and homographies.

9. Ability to compute and cache all homographies at the beginning of setup for adaptive stitching. 

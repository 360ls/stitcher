# 360ls-stitcher
Realtime Panoramic 360 stitcher for a camera array.

[![Build Status](https://travis-ci.org/360ls/stitcher.svg?branch=master)](https://travis-ci.org/360ls/stitcher)

## Overview
This repository holds functionality for stitching up to four cameras in a camera array with overlapping fields of view. The implementation requires installation of OpenCV 2.4 or 3 which can be done using the [provision repository](https://github.com/360ls/provision) housed in the 360ls group.

## Production

### Installing dependencies

```bash
$ make install
```

### Running the application

```bash
$ make run
```

### Running the CLI
```bash
$ make cli
```

## Development

### Running utility functions

```bash
$ make utils
```

### Linting

```bash
$ make lint
```


## Existing Functionality
This stitching implementation leverages the SURF keypoint extraction algorithm, along with FLANN keypoint matching, to gather matches, compute a homography, and stitch images via warping based on that homography.

The implementation works like this:

1. Camera feeds are read by the system.

2. Frames are undistorted (based on pre-determined distortion coefficients). We used GoPro cameras for our particular implementation.

3. Frames are then resized and stitched.

4. After stitching, frames are written to video writer and streamed via RTMP

5. RTMP is consumed by Wowza or other service and used to send footage to client applications.


## Future Target Functionality

1. Ability to add and remove cameras to and from stitch on the go

2. Be able to determine camera order via homography

3. Addition of better frame error handling

4. Limiting keypoint identification to a specific side of the image to decrease computation time and complexity of homography calculation.

5. The ability to determine configuration based on available cameras and homographies.


## Note About Future Direction
Optimized for performance via extensive performance profiling, the stitching is currently bottlenecked by the performance of methods from the OpenCV library. To improve upon stitching in the future, time would need to be spent developing clever ways to get around this bottleneck. That said, with proper computing power and an array of appropriate cameras, this stitching algorithm is already robust and vetted.

Because of the reliance on OpenCV's structure for performance, stitching could likely be optimized if ported over to C++ and improved even further if OpenCV was pulled out of the pipeline entirely. 

Alternative methods of rendering a panorama image have been explored, including mapping equirect images to a cylinder map and piping that cylinder map into an OpenGL renderer. This would likely increase performance a significant amount, but would also require creation of a player that can respond to user movement by sending information back to the OpenGL rendering process. This could create some logistical hurdles that would need to be sorted out, but is not out of the question. Future development may explore this methodology.

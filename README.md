# 360ls-stitcher
Realtime Panoramic 360 stitcher for a 4 camera array.

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

### To run the cli:
```bash
$ make cli
```

## Demoing

### To set up the camera streams
```bash
$ make camera-setup
```

## Development

### Linting

```bash
$ make lint
```

### Running utility functions

```bash
$ make app
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

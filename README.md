## Realtime 360 Stitcher
[![Build Status](https://travis-ci.org/dongy7/360ls-stitcher.svg?branch=master)](https://travis-ci.org/dongy7/360ls-stitcher)

## Pre-requisites
- Python 2.7
- OpenCV 2.4
- 2+ USB Cameras

Install dependencies:

```bash
make install
```

## Setup
Generate the setup profile:

```bash
make configure
``` 

Make sure images are in the `data/sources` directory and the videos are in the `data/videos` directory

## Running

```bash
make run
```

This will start the CLI with the following options.

1. Stitching Videos from Cameras
2. Stitching from Local Videos
3. Test camera stream
4. Reconfigure profile

## Streaming
Make sure that the port number is configured in `profile.yml`.

Run the following command to start the client program that waits
for the frames over the socket in the background.

```bash
make client
```

Then start the CLI and choose the streaming option.

## Generate Documentation
The documentation is generated in a directory called
`360ls-stitcher-docs` in the parent directory of the project.


```bash
make html
```

The generated documentation should be in the `360ls-stitcher-docs/html` directory.

## Linting
The linter configuration can be founder under `config/pylintrc`.

```bash
make lint
```

## Testing

```bash
make test
```

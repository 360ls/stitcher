## Realtime 360 Stitcher

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
2. Stitching Local Images
3. Stitching from Local Videos

## Streaming
Make sure that the port number is configured in `profile.yml`.

Run the following command to start the client program that waits
for the frames over the socket in the background.

```bash
make client
```

Then start the CLI and choose the streaming option.

## Generate Documentation

```bash
make html
```
The generated documentation should be in the `docs/build` directory.

## Linting

```bash
make lint
```

## Testing

```bash
make test
```

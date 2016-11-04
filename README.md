## Realtime 360 Stitcher
[![Build Status](https://travis-ci.org/360ls/360ls-stitcher.svg?branch=master)](https://travis-ci.org/360ls/360ls-stitcher)

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

## Setting up the Documentation Repository
Go to the parent directory of the project and 
create a directory called `360ls-stitcher-docs` and clone
the main repo to a directory called `html`:

```bash
mkdir 360ls-stitcher-docs
cd 360ls-stitcher-docs
git clone https://github.com/dongy7/360ls-stitcher.git html
```

Go to the `html` directory and create a local branch
called `gh-pages` tracking the remote `gh-pages` branch:

```bash
cd html
git checkout -b gh-pages origin/gh-pages
```


## Generating Documentation
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
The following command will run the test suite defined under the `test` directory.

```bash
make test
```

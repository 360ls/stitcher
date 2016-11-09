# stitch-flex
Demonstrates flexible stitching for an incoming array of cameras.
[![Build Status](https://travis-ci.org/360ls/stitch-flex.svg?branch=master)](https://travis-ci.org/360ls/stitch-flex)

## Production

### To install the package:

```bash
make clean-install
```

This will install package dependencies via npm (node.js) and pip (python), including the yarn package manager dependency.

### Then, to run the app, either:

```bash
make run
```
to simply run the app

OR

```bash
make
```

to clean the package, do a fresh (but not brand new) install of dependencies, and then run the app.

### To run the cli:
```bash
make cli
```

## Demoing

### To set up the camera streams
```bash
make camera-setup
```

### To demonstrate threading through taking snapshots
```bash
make snap
```

## Development

### To lint the application:

For JS files:
```bash
eslint nameoffile.js
```

For Python files;
```bash
make lint-py
```

### To run tests against the application:

```bash
make test
```

You can also install packages in a text editor like Sublime Text 3 to show linting in real-time. This can be done for both eslint (JS) and pylint (Python)

## Package Structure
```bash
stitch-flex/
    .eslintrc.json
    .gitignore
    .travis.yml
    LICENSE
    main.js
    Makefile
    package.json
    README.md
    yarn.lock
    app/
        __init__.py
        cli.py
        electronapp.py
        snapper/
            __init__.py
            snapstreams.py
            streamsnapper.py
        stitcher/
            __init__.py
            stitch.py
            core/
                stitcher.py
            correction/
            flex/
                __init__.py
        storage/
        templates/
            cli.html
            index.html
        test/
            __init__.py
            test_feed.py
            test_inputscanner.py
        util/
            __init__.py
            feed.py
            inputscanner.py
            listfiles.py
            textformatter.py
            validatefeeds.py
    config/
        .pylintrc
        requirements.txt
    out/
```
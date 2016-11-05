# stitch-flex
Demonstrates flexible stitching for an incoming array of cameras.

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

to clean the package, do a fresh install of dependencies, and then run the app.

## Development

### To test the application:

```bash
make test
```

### To lint the application:
```bash
eslint nameoffile.js
```

## Package Structure
```bash
stitch-flex/
    .eslintrc.json
    .gitignore
    LICENSE
    main.js
    Makefile
    package.json
    README.md
    yarn.lock
    app/
        __init__.py
        app.py
        snapstreams.py
        streamsnapper.py
        output/
        util/
            listfiles.py
    config/
        requirements.txt
```
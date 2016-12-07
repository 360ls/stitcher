PACKAGE_DIR = app
CONFIGURATION_DIR = config
SNAPPER_DIR = $(PACKAGE_DIR).snapper
UTILITY_DIR = $(PACKAGE_DIR).util
STITCHER_DIR = $(PACKAGE_DIR).stitcher
FLEX_DIR = $(PACKAGE_DIR).stitcher.flex
TEST_DIR = $(PACKAGE_DIR)/test

PY = python
OPTS = -m

RUN_PACKAGE = $(PY) $(OPTS)

all: clean install run

.PHONY: all

install:
	pip install -r requirements.txt

configure:
	$(RUN_PACKAGE) $(UTILITY_DIR).$@

stitch:
	$(RUN_PACKAGE) $(STITCHER_DIR).$@

run: stitch

cli:
	$(RUN_PACKAGE) $(PACKAGE_DIR).$@ -n

clean:
	find . -name '*.pyc' -delete ;

lint:
	pylint app --rcfile=config/.pylintrc

test:
	pytest

test-travis:
	pytest $(TEST_DIR)/nocv

tree:
	$(RUN_PACKAGE) $(UTILITY_DIR).listfiles

utils:
	bash cli.sh

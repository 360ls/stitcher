# Directory Variables for Relative Paths
PACKAGE_DIR=app
CONFIGURATION_DIR=config
SNAPPER_DIR=app.snapper
UTILITY_DIR=app.util
STITCHER_DIR=app.stitcher
TEST_DIR=app/test

# Ensures clean and run are not interpreted as files
all: clean install run
.PHONY: all 

clean-install:
	rm -rf node_modules ; pip install -r $(CONFIGURATION_DIR)/requirements.txt ; npm install ;
		npm install -g eslint yarn electron-prebuilt

install:
	pip install -r $(CONFIGURATION_DIR)/requirements.txt ; yarn install

run:
	electron . ; python -m $(PACKAGE_DIR).cli -n

cli:
	python -m $(PACKAGE_DIR).cli -n

clean:
	find . -name '*.pyc' -delete ;

lint-py:
	pylint app --rcfile=config/.pylintrc

test:
	pytest

test-travis:
	pytest $(TEST_DIR)/nocv

push:
	git push origin; git push 360;

### =============  Utilities  ============= ###

single-corrected:
	python -m $(STITCHER_DIR).stitch

single-corrected-better:
	python -m $(STITCHER_DIR).stitch2

flex-naive:
	python -m $(UTILITY_DIR).threadedflex

camera-setup:
	python -m $(UTILITY_DIR).validatefeeds

capture-frame:
	python -m $(UTILITY_DIR).capture

capture-video:
	python -m $(UTILITY_DIR).capture --type=video

snap:
	python -m $(SNAPPER_DIR).snapstreams --output out

tree:
	python -m $(UTILITY_DIR).listfiles

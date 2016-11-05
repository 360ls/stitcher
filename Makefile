# Directory Variables for Relative Paths
PACKAGE_DIR=.
CONFIGURATION_DIR=config

# Ensures clean and run are not interpreted as files
all: clean install run
.PHONY: all 

clean-install:
	rm -rf node_modules ; pip install -r $(CONFIGURATION_DIR)/requirements.txt ; npm install ;
		npm install -g eslint yarn electron-prebuilt 

install:
	pip install -r $(CONFIGURATION_DIR)/requirements.txt ; yarn install

run:
	electron .

clean:
	find . -name '*.pyc' -delete ; rm node_

test:
	pytest

### =============  Utilities  ============= ###

tree:
	python app/util/listfiles.py

snap:
	python app/snapstreams.py --output output



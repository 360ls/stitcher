# Directory Variables for Relative Paths
PACKAGE_DIR=.
CONFIGURATION_DIR=config

# Ensures clean and run are not interpreted as files
all: clean install run
.PHONY: all 

install:
	pip install -r $(CONFIGURATION_DIR)/requirements.txt ; npm install

run:
	electron .

clean:
	find . -name '*.pyc' -delete


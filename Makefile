PACKAGE_DIR=stitcher
all: run

install:
	pip install -r requirements.txt
	

configure:
	python $(PACKAGE_DIR)/configure.py

run:
	python $(PACKAGE_DIR)/run.py

client:
	python $(PACKAGE_DIR)/client.py &
